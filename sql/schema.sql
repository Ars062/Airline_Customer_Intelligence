-- Schema for the Airline Customer Experience analytical database (SQLite).
-- Built by src/analytics/build_db.py from data/processed/airline_reviews_clean.csv
-- and data/outputs/review_predictions.csv. No server required.
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS predictions;

CREATE TABLE reviews (
    unique_id TEXT PRIMARY KEY,
    airline_name TEXT NOT NULL,
    cabin_type TEXT,
    travel_type TEXT,
    trip_verified TEXT,
    origin_country TEXT,
    route TEXT,
    aircraft TEXT,
    date_flown TEXT,
    date_flown_year INTEGER,
    date_flown_month INTEGER,
    date_pub TEXT,
    overall_score REAL,
    recommended TEXT NOT NULL,
    seat_comfort_rating REAL,
    service_rating REAL,
    food_rating REAL,
    value_rating REAL,
    ground_service_rating REAL,
    entertainment_rating REAL,
    wifi_rating REAL,
    review_title TEXT,
    review_text TEXT,
    review_char_len INTEGER,
    review_word_count INTEGER,
    is_empty_review INTEGER
);

CREATE TABLE predictions (
    unique_id TEXT PRIMARY KEY,
    airline_name TEXT NOT NULL,
    cabin_type TEXT,
    travel_type TEXT,
    recommended TEXT NOT NULL,
    overall_score REAL,
    sentiment_proxy TEXT,
    pred_recommended TEXT NOT NULL,
    p_recommend REAL,
    pred_sentiment TEXT,
    cx_risk REAL,
    risk_band TEXT,
    date_flown_year INTEGER,
    FOREIGN KEY (unique_id) REFERENCES reviews(unique_id)
);

CREATE INDEX idx_rev_airline ON reviews(airline_name);
CREATE INDEX idx_rev_reco ON reviews(recommended);
CREATE INDEX idx_rev_year ON reviews(date_flown_year);
CREATE INDEX idx_pred_airline ON predictions(airline_name);
CREATE INDEX idx_pred_band ON predictions(risk_band);
CREATE INDEX idx_pred_sent ON predictions(sentiment_proxy);
