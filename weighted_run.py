"""Run the declared second improvement: class-weighted fine-tuning."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    set_seed,
)

LABELS = ["scene_identification", "production_detail", "plot_interpretation", "fact_context"]
BASE_MODEL = "distilbert-base-uncased"
EPOCHS = 5
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
MAX_LENGTH = 128
SEEDS = [42, 7, 2024]


def split_dataset(df, seed):
    def stratify(frame):
        return frame["label"] if frame["label"].value_counts().min() >= 2 else None

    rest, test = train_test_split(
        df, test_size=0.15, random_state=seed, stratify=stratify(df)
    )
    train, val = train_test_split(
        rest,
        test_size=0.15 / 0.85,
        random_state=seed,
        stratify=stratify(rest),
    )
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)


def to_dataset(frame, tokenizer):
    labels = frame["label"].map({label: i for i, label in enumerate(LABELS)})
    dataset = Dataset.from_dict({"text": frame["text"].tolist(), "labels": labels.tolist()})
    return dataset.map(
        lambda batch: tokenizer(
            batch["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH
        ),
        batched=True,
    )


class WeightedTrainer(Trainer):
    def __init__(self, class_weights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        loss = torch.nn.functional.cross_entropy(
            outputs.logits, labels, weight=self.class_weights.to(outputs.logits.device)
        )
        return (loss, outputs) if return_outputs else loss


def evaluate(trainer, tokenizer, test, seed):
    predictions = trainer.predict(to_dataset(test, tokenizer))
    predicted = np.argmax(predictions.predictions, axis=-1)
    gold = test["label"].map({label: i for i, label in enumerate(LABELS)}).to_numpy()
    confidence = torch.softmax(torch.tensor(predictions.predictions), dim=1).max(dim=1).values.numpy()
    correct = predicted == gold
    order = np.argsort(confidence)
    thirds = len(gold) // 3
    low, high = order[:thirds], order[-thirds:]
    precision, recall, f1, support = precision_recall_fscore_support(
        gold, predicted, labels=range(len(LABELS)), zero_division=0
    )
    confusion = {
        label: {
            other: int(((gold == i) & (predicted == j)).sum())
            for j, other in enumerate(LABELS)
        }
        for i, label in enumerate(LABELS)
    }
    return {
        "seed": seed,
        "n_test": len(gold),
        "accuracy": float(accuracy_score(gold, predicted)),
        "f1_macro": float(f1_score(gold, predicted, average="macro", zero_division=0)),
        "per_label": {
            label: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i, label in enumerate(LABELS)
        },
        "confusion": confusion,
        "confidence": {
            "mean_when_right": float(confidence[correct].mean()),
            "mean_when_wrong": float(confidence[~correct].mean()),
            "accuracy_most_confident_third": float(correct[high].mean()),
            "accuracy_least_confident_third": float(correct[low].mean()),
            "n_per_third": thirds,
        },
        "class_weights": {
            label: float(len(train) / (len(LABELS) * (train["label"] == label).sum()))
            for label in LABELS
        },
    }


results = []
df = pd.read_csv("labels.csv")
for seed in SEEDS:
    set_seed(seed)
    train, val, test = split_dataset(df, seed)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=len(LABELS),
        id2label=dict(enumerate(LABELS)),
        label2id={label: i for i, label in enumerate(LABELS)},
    )
    counts = torch.tensor([(train["label"] == label).sum() for label in LABELS], dtype=torch.float)
    weights = len(train) / (len(LABELS) * counts)
    args = TrainingArguments(
        output_dir="./takemeter_weighted_out",
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        eval_strategy="epoch",
        save_strategy="no",
        report_to="none",
        disable_tqdm=False,
        seed=seed,
    )
    trainer = WeightedTrainer(
        class_weights=weights,
        model=model,
        args=args,
        train_dataset=to_dataset(train, tokenizer),
        eval_dataset=to_dataset(val, tokenizer),
    )
    trainer.train()
    results.append(evaluate(trainer, tokenizer, test, seed))

Path("results_three_seeds_weighted.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
