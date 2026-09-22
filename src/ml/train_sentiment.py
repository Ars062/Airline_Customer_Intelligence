"""Phase 4b(i) — text-only 3-class proxy-sentiment classifier.

Labels are DERIVED from OverallScore (1-3 neg / 4-6 neu / 7-10 pos) => proxy
labels, not human annotation. Inputs are REVIEW TEXT ONLY: the source rating
(OverallScore) and all service ratings are excluded to avoid leakage.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from src.nlp.features import make_tfidf
from src.nlp.labels import INV_LABEL_MAP, LABEL_MAP, add_proxy_sentiment

BASE = Path(__file__).resolve().parents[2]
CLEAN_PATH = BASE / "data" / "processed" / "airline_reviews_clean.csv"
MODEL_PATH = BASE / "models" / "sentiment_model.joblib"
METRICS_PATH = BASE / "models" / "sentiment_metrics.json"


def main() -> None:
    df = add_proxy_sentiment(pd.read_csv(CLEAN_PATH, low_memory=False))
    df = df[df["sentiment_proxy"].notna()].copy()
    df["Review"] = df["Review"].fillna("")
    print("label balance:", df["sentiment_proxy"].value_counts().to_dict())
    y = df["sentiment_proxy"].map(LABEL_MAP).astype(int)
    X = df["Review"]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42)
    clf = make_pipeline(make_tfidf(), LogisticRegression(max_iter=1000))
    clf.fit(X_tr, y_tr)
    pred = clf.predict(X_te)
    macro_f1 = float(f1_score(y_te, pred, average="macro"))
    report = classification_report(y_te, pred, target_names=["negative", "neutral", "positive"])
    print(report)
    print("macro-F1:", round(macro_f1, 4))
    print("confusion:\n", confusion_matrix(y_te, pred))
    joblib.dump({"model": clf, "label_map": INV_LABEL_MAP}, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps({
        "macro_f1": round(macro_f1, 4),
        "classification_report": report,
        "confusion_matrix": confusion_matrix(y_te, pred).tolist(),
        "inputs": ["Review text only"],
        "leakage_excluded": ["OverallScore", "all 7 service ratings", "Recommended", "Title"],
        "disclaimer": "Labels derived from ratings = proxy labels, not human-annotated sentiment.",
    }, indent=2))
    print(f"saved -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
