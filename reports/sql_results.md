# SQL Results (VERIFIED run against SQLite)

## Q1
```
     airline_name    n  neg_pct  avg_score
Frontier Airlines 3136     91.6       1.85
  Spirit Airlines 4829     86.0       2.26
American Airlines 5509     85.6       2.44
    Allegiant Air 1893     82.2       2.71
 Air Canada rouge 1207     81.7       3.00
   Flair Airlines  818     81.2       2.66
  United Airlines 4506     81.0       2.83
      VietJet Air  544     79.6       2.65
 Sunwing Airlines  715     77.8       3.28
 Vueling Airlines 1172     77.4       3.08
          WOW air  579     77.4       3.00
            Swoop  707     76.8       3.02
  Jetblue Airways 1475     75.2       3.47
         Wizz Air 1265     74.7       3.20
 WestJet Airlines  942     73.8       3.55
```

## Q2
```
           airline_name    n  reco_pct
      American Airlines 5509      14.4
        Spirit Airlines 4829      14.0
        United Airlines 4506      19.0
        British Airways 3541      41.4
      Frontier Airlines 3136       8.4
        Delta Air Lines 2770      32.4
       Turkish Airlines 2298      39.2
               Emirates 2254      50.0
              Lufthansa 2203      55.3
          Qatar Airways 2196      76.2
                Ryanair 2157      39.1
             Air Canada 2146      29.2
China Southern Airlines 1970      87.1
          Allegiant Air 1893      17.8
         Qantas Airways 1775      57.1
```

## Q3
```
     airline_name  neg_pct  neu_pct  pos_pct
American Airlines     81.6      5.7     12.6
  Spirit Airlines     84.3      2.1     13.1
  United Airlines     75.9      7.1     17.0
  British Airways     44.6     18.7     36.6
Frontier Airlines     85.0      2.3      7.3
  Delta Air Lines     59.6      8.6     29.0
 Turkish Airlines     52.3     12.9     34.3
         Emirates     36.5     20.7     42.7
        Lufthansa     36.9     14.7     48.3
    Qatar Airways     13.8     16.3     69.9
```

## Q4
```
 seat  service  food  value  ground  entertain  wifi
 2.78     3.03  2.76   2.69    2.44       2.68  1.99
```

## Q5
```
risk_band     n  pct
     high 67874 52.4
      low 51253 39.6
   medium 10328  8.0
```

## Q6
```
     airline_name  high_risk_pct    n
Frontier Airlines           89.8 3136
  Spirit Airlines           85.3 4829
American Airlines           82.5 5509
   Flair Airlines           80.2  818
    Allegiant Air           77.2 1893
```

## Q7
```
  yr     n  avg_score  reco_pct
2012     1       7.00     100.0
2013     2      10.00     100.0
2014   150       5.83      58.7
2015  9796       5.25      50.9
2016 11898       5.31      51.8
2017 11764       4.70      43.3
2018 14231       3.89      33.0
2019 15366       3.60      29.2
2020  5554       3.20      24.5
2021  6352       2.71      17.9
2022 12213       2.75      18.5
2023  3666       3.23      24.1
```

## Q8
```
     cabin_type      n  reco_pct
           None   3018      18.9
  Economy Class 102735      36.5
Premium Economy   4816      43.3
    First Class   2412      55.3
 Business Class  16474      62.9
```

## Q9
```
   travel_type     n  reco_pct
Family Leisure 19900      29.2
Couple Leisure 23845      30.7
      Business 14155      34.1
  Solo Leisure 33246      40.0
          None 38309      53.8
```

## Q10
```
actual predicted     n
    no        no 75160
    no       yes  2437
   yes        no  2541
   yes       yes 49317
```
