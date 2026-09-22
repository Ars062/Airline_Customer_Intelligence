"""Text preprocessing — preserves linguistic signal, no stopword massacre."""
from __future__ import annotations

import re

import pandas as pd

URL_RE = re.compile(r"https?://\S+|www\.\S+")
WS_RE = re.compile(r"\s+")


def clean_text(s: str) -> str:
    """Lowercase, strip URLs, keep letters/numbers/punctuation spacing sane.

    Deliberately keeps stopwords and negation words (not/no/never) because
    they carry sentiment signal. Drops nothing except URLs/whitespace noise.
    """
    if pd.isna(s):
        return ""
    s = str(s).lower()
    s = URL_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip()
    return s
