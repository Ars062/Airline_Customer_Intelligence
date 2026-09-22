"""Customer Experience Risk Score + full-dataset predictions.

Customer Experience Risk Score is a PORTFOLIO-PROJECT analytical indicator,
not an airline metric. Formula (transparent, 0-1):

  cx_risk = 0.40 * P(not recommended | model)
          + 0.25 * (OverallScore <= 3)
          + 0.20 * (fraction of rated service dims scored 1-2)
          + 0.15 * (Recommended == 'no')

Bands: low <0.33, medium 0.33-0.66, high >=0.66.
Writes data/outputs/review_predictions.csv (one row per review).
"""
from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from src.nlp.labels import INV_LABEL_MAP, add_proxy_sentiment

BASE = Path(__file__).resolve().parents[2]
CLEAN_PATH = BASE / "data" / "processed" / "airline_reviews_clean.csv"
OUT_PATH = BASE / "data" / "outputs" / "review_predictions.csv"

SERVICE_COLS = ["SeatComfortRating", "ServiceRating", "FoodRating", "ValueRating",
                "GroundServiceRating", "EntertainmentRating", "WifiRating"]


def main() -> None:
    rec = joblib.load(BASE / "models" / "recommended_model.joblib")
    sent = joblib.load(BASE / "models" / "sentiment_model.joblib")
    df = add_proxy_sentiment(pd.read_csv(CLEAN_PATH, low_memory=False))
    df["Review"] = df["Review"].fillna("")
    top_airlines = set(df["AirlineName"].value_counts().head(30).index)
    df["airline_group"] = df["AirlineName"].where(df["AirlineName"].isin(top_airlines), "Other")
    X = df[["Review"] + SERVICE_COLS + ["review_char_len", "review_word_count",
                                        "airline_group", "CabinType", "TravelType", "TripVerified"]]
    p_yes = rec["model"].predict_proba(X)[:, 1]
    df["pred_recommended"] = pd.Series(p_yes >= 0.5).map({True: "yes", False: "no"}).values
    df["p_recommend"] = p_yes.round(4)
    df["pred_sentiment"] = pd.Series(sent["model"].predict(df["Review"])).map(INV_LABEL_MAP).values

    low = (pd.to_numeric(df["OverallScore"], errors="coerce") <= 3).fillna(False).astype(float)
    rated = df[SERVICE_COLS].notna()
    bad = df[SERVICE_COLS].apply(lambda c: pd.to_numeric(c, errors="coerce").isin([1, 2])).where(rated, False)
    bad_frac = (bad.sum(axis=1) / rated.sum(axis=1).clip(lower=1)).fillna(0)
    reco_no = (df["Recommended"] == "no").astype(float)
    df["cx_risk"] = (0.40 * (1 - p_yes) + 0.25 * low + 0.20 * bad_frac + 0.15 * reco_no).round(4)
    df["risk_band"] = pd.cut(df["cx_risk"], [-0.01, 0.33, 0.66, 1.01], labels=["low", "medium", "high"])

    print("risk bands:", df["risk_band"].value_counts(dropna=False).to_dict())
    print("mean risk:", round(float(df["cx_risk"].mean()), 4))
    out = df[["unique_id", "AirlineName", "CabinType", "TravelType", "Recommended",
              "OverallScore", "sentiment_proxy", "pred_recommended", "p_recommend",
              "pred_sentiment", "cx_risk", "risk_band", "date_flown_year"]]
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print(f"wrote {OUT_PATH} {out.shape}")


if __name__ == "__main__":
    main()
