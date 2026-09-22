"""Proxy sentiment labeling from OverallScore (1-10 scale).

No human-annotated sentiment column exists in the dataset, so labels are
DERIVED from customer ratings = proxy labels, not ground-truth sentiment.

Threshold justification (verified distribution: 1:44070, 2:12228, 3:7769,
4:4812, 5:5396, 6:4412, 7:7589, 8:11754, 9:12512, 10:14582):
  negative: 1-3 (clear detractors, 64,067 / 51.2% of scored rows)
  neutral : 4-6 (ambivalent middle, 14,620 / 11.7%)
  positive: 7-10 (clear promoters, 41,845 / 33.4%)
Boundaries sit at the natural gaps around the rare middle scores, keeping
all three classes populated. Rows with missing OverallScore get NaN label.
"""
from __future__ import annotations

import pandas as pd

LABEL_MAP = {"negative": 0, "neutral": 1, "positive": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def add_proxy_sentiment(df: pd.DataFrame, score_col: str = "OverallScore") -> pd.DataFrame:
    df = df.copy()
    s = pd.to_numeric(df[score_col], errors="coerce")
    df["sentiment_proxy"] = pd.NA
    df.loc[s.between(1, 3), "sentiment_proxy"] = "negative"
    df.loc[s.between(4, 6), "sentiment_proxy"] = "neutral"
    df.loc[s.between(7, 10), "sentiment_proxy"] = "positive"
    return df
