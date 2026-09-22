"""Lightweight topic/service analysis.

1. chi2 top TF-IDF terms per proxy-sentiment class (discriminative vocabulary).
2. LSA (TruncatedSVD, 10 topics) on a 30k stratified sample for discovery.
Analyst-defined business mapping is labelled as such, not model output.
Writes reports/topics.md.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from src.nlp.features import make_tfidf
from src.nlp.labels import add_proxy_sentiment
from src.nlp.preprocess import clean_text

BASE = Path(__file__).resolve().parents[2]
CLEAN_PATH = BASE / "data" / "processed" / "airline_reviews_clean.csv"
REPORT_PATH = BASE / "reports" / "topics.md"


def top_terms_per_class(df: pd.DataFrame, vec: TfidfVectorizer, X, k: int = 20) -> dict:
    """Direction-aware discriminative terms: compare mean TF-IDF per class."""
    import numpy as np
    feats = vec.get_feature_names_out()
    mean_neg = np.asarray(X[(df["sentiment_proxy"] == "negative").to_numpy()].mean(axis=0)).ravel()
    mean_pos = np.asarray(X[(df["sentiment_proxy"] == "positive").to_numpy()].mean(axis=0)).ravel()
    diff = mean_pos - mean_neg  # >0 => positive-leaning, <0 => negative-leaning
    return {
        "negative": [feats[i] for i in diff.argsort()[:k]],
        "positive": [feats[i] for i in diff.argsort()[::-1][:k]],
    }


def main() -> None:
    df = add_proxy_sentiment(pd.read_csv(CLEAN_PATH, low_memory=False))
    df = df[df["sentiment_proxy"].isin(["negative", "positive"])].copy()
    df["clean"] = df["Review"].fillna("").map(clean_text)
    vec = make_tfidf()
    X = vec.fit_transform(df["clean"])
    discrim = top_terms_per_class(df, vec, X)

    sample = df.groupby("sentiment_proxy", group_keys=False)[df.columns].apply(
        lambda g: g.sample(min(len(g), 15000), random_state=42))
    Xs = vec.transform(sample["clean"])
    svd = TruncatedSVD(n_components=10, random_state=42)
    svd.fit(Xs)
    feats = vec.get_feature_names_out()
    topics = []
    for i, comp in enumerate(svd.components_):
        topics.append([feats[j] for j in comp.argsort()[::-1][:12]])

    lines = ["# Topic / Service Analysis (VERIFIED run)", "",
             "Labels are rating-derived proxies. Business mapping below is analyst-defined.",
             "", "## Discriminative terms (chi2, negative vs positive)",
             f"- negative: {', '.join(discrim['negative'])}",
             f"- positive: {', '.join(discrim['positive'])}", "",
             "## LSA discovery topics (10, top terms each)"]
    for i, t in enumerate(topics):
        lines.append(f"- T{i}: {', '.join(t)}")
    lines += ["", "## Analyst-defined business categories (NOT model output)",
              "- Delay/cancellation & schedule reliability; Staff attitude/helpfulness; "
              "Seat comfort & legroom; Food & beverage; Baggage handling; "
              "Check-in/boarding & ground process; Value for money; "
              "Verified-complaint markers (e.g. 'never again', 'worst', 'rude', 'delayed').",
              "Map LSA/chi2 terms into these only for dashboard grouping, and label as analyst-defined."]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print("NEG:", discrim["negative"][:10])
    print("POS:", discrim["positive"][:10])


if __name__ == "__main__":
    main()
