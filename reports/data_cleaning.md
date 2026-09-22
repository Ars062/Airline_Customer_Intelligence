# Data Cleaning Report (VERIFIED run)

Raw: `AirlineReviews.csv` (129455 rows, untouched). Clean: `data/processed/airline_reviews_clean.csv` (129455 rows x 29 cols).

## Transformations
Input: AirlineReviews.csv — 129455 rows x 22 cols.
Duplicate rows: 0 — none removed.
- `Aircraft`: whitespace strip turned 1 whitespace-only values into missing.
- All text columns: leading/trailing whitespace stripped, internal runs collapsed to one space.
- `EntertainmentRating`: 54120 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `FoodRating`: 36314 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `GroundServiceRating`: 41649 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `SeatComfortRating`: 14362 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `ServiceRating`: 14480 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `ValueRating`: 2382 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- `WifiRating`: 99978 zeros recoded to NaN (0 = not rated, verified dominant e.g. Wifi 77%); 0 out-of-range values coerced to NaN.
- JUSTIFICATION: audit showed 0 is the modal value in low-usage services (Wifi/Entertainment); treating it as a score would corrupt means and model inputs.
- `OverallScore`: coerced to numeric; 0 out-of-range values set to NaN (missing stays 4331, no imputation — target-adjacent).
- `Recommended`: lowercased/stripped; unexpected values: none.
- `TripVerified`: normalized to {Trip Verified, Not Verified, NaN} via substring match (fixes `NotVerified`, duplicated labels, and one route-sentence data-entry error containing 'Not Verified', mapped to Not Verified with route fragment discarded).
  before={nan: 69947, 'Trip Verified': 45440, 'Not Verified': 14056, 'NotVerified': 9, 'Trip Verified,Trip Verified': 1, 'Not Verified,Not Verified': 1, 'Chicago to Colorado Springs. Not Verified': 1} after={<NA>: 69947, 'Trip Verified': 45441, 'Not Verified': 14067}
- `DateFlown` ('November 2019' style) parsed to `date_flown` (month start); parsed 90993/129455, rest NaN (no imputation).
- `DatePub` (ordinal suffixes 11th/25th/31st stripped) parsed to `date_pub`; parsed 129455/129455.
- Reviews: 824 empty flagged via `is_empty_review` (kept — ratings still valid); added `review_char_len`, `review_word_count`. No text altered.

## Columns added
- `date_flown`, `date_flown_year`, `date_flown_month`, `date_pub`, `review_char_len`, `review_word_count`, `is_empty_review`

## Missing-value policy
- No imputation of ratings, dates, or categories. Zeros in 0–5 service scales recoded to NaN (not-rated). Whitespace-only strings → NaN.
