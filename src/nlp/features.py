"""Shared feature builders: TF-IDF (uni+bigrams) + review-length features."""
from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.nlp.preprocess import clean_text

TEXT_COL = "clean_review"
LEN_COLS = ["review_char_len", "review_word_count"]


def make_tfidf() -> TfidfVectorizer:
    return TfidfVectorizer(
        preprocessor=clean_text,
        ngram_range=(1, 2),
        max_features=20000,
        min_df=5,
        sublinear_tf=True,
    )


def numeric_pipe():
    return Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])


def cat_pipe():
    return Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
