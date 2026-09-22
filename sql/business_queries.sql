-- Business queries — every query uses only columns verified to exist.
-- Run: sqlite3 data/outputs/airline_cx.db < sql/business_queries.sql

-- Q1. Negative-review rate by airline (min 500 reviews), worst first
SELECT airline_name, COUNT(*) AS n,
       ROUND(100.0*SUM(CASE WHEN recommended='no' THEN 1 ELSE 0 END)/COUNT(*),1) AS neg_pct,
       ROUND(AVG(overall_score),2) AS avg_score
FROM reviews GROUP BY airline_name HAVING COUNT(*)>=500
ORDER BY neg_pct DESC LIMIT 15;

-- Q2. Recommendation rate, top airlines by volume
SELECT airline_name, COUNT(*) AS n,
       ROUND(100.0*SUM(CASE WHEN recommended='yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS reco_pct
FROM reviews GROUP BY airline_name ORDER BY n DESC LIMIT 15;

-- Q3. Sentiment-proxy mix by airline (top 10 by volume)
SELECT airline_name,
       ROUND(100.0*SUM(sentiment_proxy='negative')/COUNT(*),1) AS neg_pct,
       ROUND(100.0*SUM(sentiment_proxy='neutral')/COUNT(*),1) AS neu_pct,
       ROUND(100.0*SUM(sentiment_proxy='positive')/COUNT(*),1) AS pos_pct
FROM predictions GROUP BY airline_name ORDER BY COUNT(*) DESC LIMIT 10;

-- Q4. Mean service ratings across all reviews (NULL = not rated, excluded)
SELECT ROUND(AVG(seat_comfort_rating),2) AS seat, ROUND(AVG(service_rating),2) AS service,
       ROUND(AVG(food_rating),2) AS food, ROUND(AVG(value_rating),2) AS value,
       ROUND(AVG(ground_service_rating),2) AS ground, ROUND(AVG(entertainment_rating),2) AS entertain,
       ROUND(AVG(wifi_rating),2) AS wifi FROM reviews;

-- Q5. CX risk-band distribution overall and for bottom-5 airlines by reco rate
SELECT risk_band, COUNT(*) AS n, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM predictions),1) AS pct
FROM predictions GROUP BY risk_band ORDER BY n DESC;
SELECT airline_name, ROUND(100.0*SUM(risk_band='high')/COUNT(*),1) AS high_risk_pct, COUNT(*) AS n
FROM predictions GROUP BY airline_name HAVING COUNT(*)>=500 ORDER BY high_risk_pct DESC LIMIT 5;

-- Q6. Yearly trend: volume, mean score, recommendation rate
SELECT date_flown_year AS yr, COUNT(*) AS n, ROUND(AVG(overall_score),2) AS avg_score,
       ROUND(100.0*SUM(CASE WHEN recommended='yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS reco_pct
FROM reviews WHERE date_flown_year IS NOT NULL GROUP BY yr ORDER BY yr;

-- Q7. Segment analysis: recommendation rate by cabin and travel type
SELECT cabin_type, COUNT(*) AS n,
       ROUND(100.0*SUM(CASE WHEN recommended='yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS reco_pct
FROM reviews GROUP BY cabin_type ORDER BY reco_pct;
SELECT travel_type, COUNT(*) AS n,
       ROUND(100.0*SUM(CASE WHEN recommended='yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS reco_pct
FROM reviews GROUP BY travel_type ORDER BY reco_pct;

-- Q8. Model check: predicted vs actual recommendation agreement
SELECT recommended AS actual, pred_recommended AS predicted, COUNT(*) AS n
FROM predictions GROUP BY actual, predicted ORDER BY actual, predicted;
