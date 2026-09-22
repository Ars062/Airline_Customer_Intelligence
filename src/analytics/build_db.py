"""Build SQLite analytical DB + run business queries (verified output).

Reads : data/processed/airline_reviews_clean.csv, data/outputs/review_predictions.csv
        sql/schema.sql, sql/business_queries.sql
Writes: data/outputs/airline_cx.db (git-ignored), reports/sql_results.md
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2]
DB_PATH = BASE / "data" / "outputs" / "airline_cx.db"
REPORT_PATH = BASE / "reports" / "sql_results.md"

REVIEW_COLS = {
    "unique_id": "unique_id", "AirlineName": "airline_name", "CabinType": "cabin_type",
    "TravelType": "travel_type", "TripVerified": "trip_verified", "OriginCountry": "origin_country",
    "Route": "route", "Aircraft": "aircraft", "DateFlown": "date_flown",
    "date_flown_year": "date_flown_year", "date_flown_month": "date_flown_month",
    "DatePub": "date_pub", "OverallScore": "overall_score", "Recommended": "recommended",
    "SeatComfortRating": "seat_comfort_rating", "ServiceRating": "service_rating",
    "FoodRating": "food_rating", "ValueRating": "value_rating",
    "GroundServiceRating": "ground_service_rating", "EntertainmentRating": "entertainment_rating",
    "WifiRating": "wifi_rating", "Title": "review_title", "Review": "review_text",
    "review_char_len": "review_char_len", "review_word_count": "review_word_count",
    "is_empty_review": "is_empty_review",
}
PRED_COLS = {
    "unique_id": "unique_id", "AirlineName": "airline_name", "CabinType": "cabin_type",
    "TravelType": "travel_type", "Recommended": "recommended", "OverallScore": "overall_score",
    "sentiment_proxy": "sentiment_proxy", "pred_recommended": "pred_recommended",
    "p_recommend": "p_recommend", "pred_sentiment": "pred_sentiment",
    "cx_risk": "cx_risk", "risk_band": "risk_band", "date_flown_year": "date_flown_year",
}


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.executescript((BASE / "sql" / "schema.sql").read_text(encoding="utf-8"))
    clean = pd.read_csv(BASE / "data" / "processed" / "airline_reviews_clean.csv", low_memory=False)
    preds = pd.read_csv(BASE / "data" / "outputs" / "review_predictions.csv", low_memory=False)
    clean.rename(columns=REVIEW_COLS)[list(REVIEW_COLS.values())].to_sql(
        "reviews", con, if_exists="append", index=False)
    preds.rename(columns=PRED_COLS)[list(PRED_COLS.values())].to_sql(
        "predictions", con, if_exists="append", index=False)
    con.commit()
    n_rev = con.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
    n_pred = con.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    print(f"db rows: reviews={n_rev} predictions={n_pred} -> {DB_PATH}")

    script = (BASE / "sql" / "business_queries.sql").read_text(encoding="utf-8")
    statements = [s.strip() for s in script.split(";") if s.strip() and not s.strip().startswith("-- Run")]
    out = ["# SQL Results (VERIFIED run against SQLite)", ""]
    for i, stmt in enumerate(statements, 1):
        clean_stmt = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--"))
        if not clean_stmt.strip():
            continue
        df = pd.read_sql_query(clean_stmt, con)
        out += [f"## Q{i}", f"```\n{df.to_string(index=False)}\n```", ""]
        print(f"--- Q{i} ---\n{df.to_string(index=False)}\n")
    con.close()
    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"report -> {REPORT_PATH}")


if __name__ == "__main__":
    main()
