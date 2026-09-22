"""EDA — Airline Customer Experience platform.

Reads : data/processed/airline_reviews_clean.csv
Writes: reports/figures/*.png + reports/eda.md

Every chart answers a business question (see titles + eda.md).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
CLEAN_PATH = BASE / "data" / "processed" / "airline_reviews_clean.csv"
FIG_DIR = BASE / "reports" / "figures"
REPORT_PATH = BASE / "reports" / "eda.md"

SERVICE_COLS = ["SeatComfortRating", "ServiceRating", "FoodRating", "ValueRating",
                "GroundServiceRating", "EntertainmentRating", "WifiRating"]
TOP_N = 15
plt.rcParams.update({"figure.dpi": 120, "axes.grid": True, "grid.alpha": 0.3})


def load() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_PATH, low_memory=False)
    df["date_flown"] = pd.to_datetime(df["date_flown"], errors="coerce")
    return df


def fig_rating_dist(df: pd.DataFrame) -> str:
    vc = df["OverallScore"].value_counts(dropna=False).sort_index()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    vc.dropna().plot(kind="bar", ax=ax, color="#1f77b4")
    ax.set_title("Q: How satisfied are customers overall? — OverallScore is polarized (1-star dominates)")
    ax.set_xlabel("OverallScore (1-10)"); ax.set_ylabel("Reviews")
    fig.tight_layout(); p = FIG_DIR / "fig_rating_dist.png"; fig.savefig(p); plt.close(fig)
    return f"{vc.to_dict()}"


def fig_reco_by_airline(df: pd.DataFrame) -> str:
    top = df["AirlineName"].value_counts().head(TOP_N).index
    rate = df[df["AirlineName"].isin(top)].groupby("AirlineName")["Recommended"].apply(lambda s: (s == "yes").mean() * 100)
    rate = rate.sort_values()
    fig, ax = plt.subplots(figsize=(8, 5.5))
    rate.plot(kind="barh", ax=ax, color="#2ca02c")
    ax.set_title("Q: Which major airlines earn recommendations? — Recommendation % (top 15 by volume)")
    ax.set_xlabel("% recommended"); fig.tight_layout()
    p = FIG_DIR / "fig_reco_by_airline.png"; fig.savefig(p); plt.close(fig)
    return rate.round(1).to_dict().__str__()


def fig_rating_by_airline(df: pd.DataFrame) -> str:
    top = df["AirlineName"].value_counts().head(TOP_N).index
    avg = df[df["AirlineName"].isin(top)].groupby("AirlineName")["OverallScore"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5.5))
    avg.plot(kind="barh", ax=ax, color="#ff7f0e")
    ax.set_title("Q: Where is average satisfaction highest/lowest? — Mean OverallScore (top 15 by volume)")
    ax.set_xlabel("Mean OverallScore"); fig.tight_layout()
    p = FIG_DIR / "fig_rating_by_airline.png"; fig.savefig(p); plt.close(fig)
    return avg.round(2).to_dict().__str__()


def fig_service_means(df: pd.DataFrame) -> str:
    means = df[SERVICE_COLS].mean().sort_values()
    cov = df[SERVICE_COLS].notna().mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    means.plot(kind="barh", ax=ax, color="#9467bd")
    ax.set_title("Q: Which service dimensions score worst? — Mean rating 1-5 (NaN = not rated, excluded)")
    ax.set_xlabel("Mean rating"); fig.tight_layout()
    p = FIG_DIR / "fig_service_means.png"; fig.savefig(p); plt.close(fig)
    return f"means={means.round(2).to_dict()} coverage%={cov.round(1).to_dict()}"


def fig_trend(df: pd.DataFrame) -> str:
    t = df.dropna(subset=["date_flown"]).copy()
    t["ym"] = t["date_flown"].dt.to_period("M").dt.to_timestamp()
    g = t.groupby("ym").agg(n=("OverallScore", "size"), mean_score=("OverallScore", "mean"),
                            reco_rate=("Recommended", lambda s: (s == "yes").mean() * 100))
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    ax1.plot(g.index, g["n"], color="#1f77b4", label="Review volume")
    ax1.set_ylabel("Reviews per month", color="#1f77b4")
    ax2 = ax1.twinx()
    ax2.plot(g.index, g["mean_score"], color="#d62728", label="Mean OverallScore")
    ax2.set_ylabel("Mean OverallScore", color="#d62728")
    ax1.set_title("Q: Is experience improving or deteriorating? — Volume vs mean score over DateFlown")
    fig.tight_layout(); p = FIG_DIR / "fig_trend.png"; fig.savefig(p); plt.close(fig)
    return f"months={len(g)} vol_range=({int(g['n'].min())},{int(g['n'].max())}) score_range=({g['mean_score'].min():.2f},{g['mean_score'].max():.2f})"


def fig_segments(df: pd.DataFrame) -> str:
    out = {}
    for col in ["CabinType", "TravelType"]:
        rate = df.groupby(col)["Recommended"].apply(lambda s: (s == "yes").mean() * 100).sort_values()
        out[col] = rate.round(1).to_dict()
        fig, ax = plt.subplots(figsize=(7, 4))
        rate.plot(kind="barh", ax=ax, color="#17becf")
        ax.set_title(f"Q: Who recommends least? — Recommendation % by {col}")
        ax.set_xlabel("% recommended"); fig.tight_layout()
        p = FIG_DIR / f"fig_seg_{col.lower()}.png"; fig.savefig(p); plt.close(fig)
    return out.__str__()


def fig_reviewlen(df: pd.DataFrame) -> str:
    g = df.groupby("Recommended")["review_char_len"].median().to_dict()
    fig, ax = plt.subplots(figsize=(7, 4))
    df.boxplot(column="review_char_len", by="Recommended", ax=ax, showfliers=False)
    ax.set_title("Q: Do unhappy customers write more? — Review length by recommendation")
    ax.set_ylabel("Characters (outliers hidden)"); fig.suptitle("")
    fig.tight_layout(); p = FIG_DIR / "fig_reviewlen_by_reco.png"; fig.savefig(p); plt.close(fig)
    return f"median_len={g}"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load()
    print(f"EDA input: {df.shape}")
    results = {
        "rating_dist": fig_rating_dist(df),
        "reco_by_airline": fig_reco_by_airline(df),
        "rating_by_airline": fig_rating_by_airline(df),
        "service_means": fig_service_means(df),
        "trend": fig_trend(df),
        "segments": fig_segments(df),
        "reviewlen": fig_reviewlen(df),
    }
    REPORT_PATH.write_text(
        "# EDA Summary (VERIFIED run on cleaned data)\n\n"
        "Figures in `reports/figures/`. Each answers the business question in its title.\n\n"
        + "\n".join(f"## {k}\n`{v}`\n" for k, v in results.items())
        + "\nBusiness interpretation (finding → implication) is developed in "
          "`reports/PROJECT_REPORT.md` (Phase 10); wording stays associational, not causal.\n",
        encoding="utf-8",
    )
    print(f"figures -> {FIG_DIR} | report -> {REPORT_PATH}")
    for k, v in results.items():
        print(f"[{k}] {v[:400]}")


if __name__ == "__main__":
    main()
