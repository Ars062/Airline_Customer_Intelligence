# EDA Summary (VERIFIED run on cleaned data)

Figures in `reports/figures/`. Each answers the business question in its title.

## rating_dist
`{1.0: 44070, 2.0: 12228, 3.0: 7769, 4.0: 4812, 5.0: 5396, 6.0: 4412, 7.0: 7589, 8.0: 11754, 9.0: 12512, 10.0: 14582, nan: 4331}`

## reco_by_airline
`{'Frontier Airlines': 8.4, 'Spirit Airlines': 14.0, 'American Airlines': 14.4, 'Allegiant Air': 17.8, 'United Airlines': 19.0, 'Air Canada': 29.2, 'Delta Air Lines': 32.4, 'Ryanair': 39.1, 'Turkish Airlines': 39.2, 'British Airways': 41.4, 'Emirates': 50.0, 'Lufthansa': 55.3, 'Qantas Airways': 57.1, 'Qatar Airways': 76.2, 'China Southern Airlines': 87.1}`

## rating_by_airline
`{'Frontier Airlines': 1.85, 'Spirit Airlines': 2.26, 'American Airlines': 2.44, 'Allegiant Air': 2.71, 'United Airlines': 2.83, 'Air Canada': 3.71, 'Delta Air Lines': 3.96, 'Turkish Airlines': 4.42, 'Ryanair': 4.43, 'British Airways': 4.81, 'Emirates': 5.41, 'Lufthansa': 5.49, 'Qantas Airways': 5.75, 'Qatar Airways': 7.39, 'China Southern Airlines': 7.88}`

## service_means
`means={'WifiRating': 1.99, 'GroundServiceRating': 2.44, 'EntertainmentRating': 2.68, 'ValueRating': 2.69, 'FoodRating': 2.76, 'SeatComfortRating': 2.78, 'ServiceRating': 3.03} coverage%={'SeatComfortRating': 88.9, 'ServiceRating': 88.8, 'FoodRating': 71.9, 'ValueRating': 98.2, 'GroundServiceRating': 67.8, 'EntertainmentRating': 58.2, 'WifiRating': 22.8}`

## trend
`months=111 vol_range=(1,1556) score_range=(1.66,10.00)`

## segments
`{'CabinType': {'Economy Class': 36.5, 'Premium Economy': 43.3, 'First Class': 55.3, 'Business Class': 62.9}, 'TravelType': {'Family Leisure': 29.2, 'Couple Leisure': 30.7, 'Business': 34.1, 'Solo Leisure': 40.0}}`

## reviewlen
`median_len={'no': 666.0, 'yes': 516.0}`

Business interpretation (finding → implication) is developed in `reports/PROJECT_REPORT.md` (Phase 10); wording stays associational, not causal.
