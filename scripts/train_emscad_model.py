#!/usr/bin/env python3
"""Train scikit-learn classifier on EMSCAD fake job postings dataset."""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def _build_text(df: pd.DataFrame) -> pd.Series:
    cols = [c for c in ["title", "company_profile", "description", "requirements", "benefits"] if c in df.columns]
    if not cols:
        raise ValueError("Dataset missing expected EMSCAD text columns.")
    return df[cols].fillna("").agg(" ".join, axis=1)


def train(dataset_path: Path, output_model_path: Path) -> None:
    df = pd.read_csv(dataset_path)
    if "fraudulent" not in df.columns:
        raise ValueError("Dataset must include 'fraudulent' target column.")

    X = _build_text(df)
    y = df["fraudulent"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds, digits=4))

    output_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "source_dataset": str(dataset_path)}, output_model_path)
    print(f"Saved model to: {output_model_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train fake job classifier from EMSCAD CSV.")
    parser.add_argument("--dataset", required=True, help="Path to EMSCAD CSV from Kaggle.")
    parser.add_argument("--out", default="models/fake_job_classifier.joblib", help="Output model path.")
    args = parser.parse_args()
    train(Path(args.dataset), Path(args.out))


if __name__ == "__main__":
    main()
