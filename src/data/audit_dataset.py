"""Dataset audit for Airline Customer Experience & Service Intelligence Platform.

Reads the immutable raw CSV at data/AirlineReviews.csv and writes:
  - data/outputs/dataset_audit.json  (machine-readable)
  - data/outputs/dataset_audit.csv   (per-column missing-value table)
  - reports/dataset_audit.md         (human-readable, regenerated here)

Raw data is never modified.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

RAW_PATH = Path(__file__).resolve().parents[2] / "data" / "AirlineReviews.csv"
OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "data" / "outputs"
REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"

DATELIKE_RE = re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|19\d\d|20\d\d)\b", re.I)


def audit(df: pd.DataFrame) -> dict:
    n_rows, n_cols = df.shape
    missing = df.isna().sum()
    missing_pct = (missing / max(n_rows, 1) * 100).round(2)
    review_col = "Review" if "Review" in df.columns else None
    text_stats = {}
    if review_col:
        lens = df[review_col].fillna("").astype(str).str.len()
        text_stats = {
            "n_empty": int((lens == 0).sum()),
            "n_short_lt20": int((lens < 20).sum()),
            "n_long_gt3000": int((lens > 3000).sum()),
            "mean_len": round(float(lens.mean()), 2),
            "median_len": float(lens.median()),
            "p90_len": float(lens.quantile(0.90)),
            "p99_len": float(lens.quantile(0.99)),
            "max_len": int(lens.max()),
        }
    # Heuristic date-likeness: sample non-null strings matching month/year tokens
    datelike = {}
    for c in df.columns:
        if df[c].dtype == object:
            sample = df[c].dropna().astype(str).head(200)
            hits = sum(bool(DATELIKE_RE.search(s)) for s in sample)
            datelike[c] = {"sample_hits_frac": round(hits / max(len(sample), 1), 3)}
    return {
        "shape": {"n_rows": int(n_rows), "n_cols": int(n_cols)},
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing": {c: int(v) for c, v in missing.items()},
        "missing_pct": {c: float(v) for c, v in missing_pct.items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "nunique": {c: int(v) for c, v in df.nunique(dropna=False).items()},
        "numeric_describe": df.select_dtypes(include="number").describe().round(4).to_dict(),
        "text_stats_Review": text_stats,
        "datelike_heuristic": datelike,
        "overall_score_value_counts": (
            df["OverallScore"].value_counts(dropna=False).sort_index().to_dict()
            if "OverallScore" in df.columns else {}
        ),
        "recommended_value_counts": (
            df["Recommended"].value_counts(dropna=False).to_dict()
            if "Recommended" in df.columns else {}
        ),
    }


def main() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_PATH, low_memory=False)
    report = audit(df)
    (OUTPUTS_DIR / "dataset_audit.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "n_missing": [int(report["missing"][c]) for c in df.columns],
        "missing_pct": [float(report["missing_pct"][c]) for c in df.columns],
        "n_unique_incl_na": [int(report["nunique"][c]) for c in df.columns],
    }).to_csv(OUTPUTS_DIR / "dataset_audit.csv", index=False)
    print(f"rows={report['shape']['n_rows']} cols={report['shape']['n_cols']} "
          f"dupes={report['duplicate_rows']}")
    print(f"wrote {OUTPUTS_DIR / 'dataset_audit.json'}")
    print(f"wrote {OUTPUTS_DIR / 'dataset_audit.csv'}")


if __name__ == "__main__":
    main()
