
```bash
== Headers ==
     1  1   Trip ID
     2  2   Taxi ID
     3  3   Trip Start Timestamp
     4  4   Trip End Timestamp
     5  5   Trip Seconds
     6  6   Trip Miles
     7  7   Pickup Census Tract
     8  8   Dropoff Census Tract
     9  9   Pickup Community Area
    10  10  Dropoff Community Area
    11  11  Fare
    12  12  Tips
    13  13  Tolls
    14  14  Extras
    15  15  Trip Total
    16  16  Payment Type
    17  17  Company
    18  18  Pickup Centroid Latitude
    19  19  Pickup Centroid Longitude
    20  20  Pickup Centroid Location
    21  21  Dropoff Centroid Latitude
    22  22  Dropoff Centroid Longitude
    23  23  Dropoff Centroid  Location

== Row count ==
15406960

== Preview (first 10 rows) ==
Trip ID                                   Taxi ID                                                                                                                           Trip Start Timestamp    Trip End Timestamp      Trip Seconds  Trip Miles  Pickup Census Tract  Dropoff Census Tract  Pickup Community Area  Dropoff Community Area  Fare    Tips    Tolls  Extras  Trip Total  Payment Type  Company                            Pickup Centroid Latitude  Pickup Centroid Longitude  Pickup Centroid Location              Dropoff Centroid Latitude  Dropoff Centroid Longitude  Dropoff Centroid  Location
09eed8a4728538948d277396a42aafe6b036d538  35057a271731c5b976bda25efe85aa0c1901d0a5fc9ba2b7068508375a4c43033b282303a439c95d4ef479c592268f31ac7eb0b3db8f3998aaa79e82458a1d71  05/01/2026 12:00:00 AM  05/01/2026 12:30:00 AM  1.457         18,96                                                  76                     32                      $46,25  $12,69  $0,00  $4,00   $63,44      Credit Card   Chicago Independents               41,980264315              -87,913624596              POINT (-87.913624596 41.9802643146)   41,878865584               -87,625192142               POINT (-87.6251921424 41.8788655841)
08ef88dc90712c9d7cfcb5d1edac9d6fb070d9db  38f6145c9a2b848dc1baa16fd91087e606b12bcb8757a9eb003dfab2c031fcaeb931c1ae6b486fab5f1c21037f33a187d1cb97080f4334a63f7ce0713d0f47b4  05/01/2026 12:00:00 AM  05/01/2026 12:15:00 AM  1.260         4,7                                                    8                      23                      $16,00  $0,00   $0,00  $0,00   $16,00      Cash          Transit Administrative Center Inc  41,899602111              -87,633308037              POINT (-87.6333080367 41.899602111)   41,900069603               -87,720918238               POINT (-87.7209182385 41.9000696026)
14272d1dedb28d0954d3fff687788f379e0eabf7  2bb3cec6c1f7c3ea064aff56988b02be67da8f90a02af8ffe64d88b042564125da6abbcd3448bd6f7bc0836827aa8c40007fb6a72e8acd3122983486e6c26222  05/01/2026 12:00:00 AM  05/01/2026 12:15:00 AM  1.632         18,59                                                  76                     8                       $46,25  $10,15  $0,00  $4,00   $60,90      Credit Card   Sun Taxi                           41,980264315              -87,913624596              POINT (-87.913624596 41.9802643146)   41,899602111               -87,633308037               POINT (-87.6333080367 41.899602111)
7d5a2364bd929c1e5c07bf9e8ae6f60fc99fbcf7  02ef8f01232b1b1828f4e5e1b8e8a85cd71b67c449afafbd2dd7ab726b2bb72795fcd00a9bb2477dfa6f8a325bbfde41ae888127ecd354096a1117f5e6fd9e0d  05/01/2026 12:00:00 AM  05/01/2026 12:30:00 AM  1.967         16,39                                                  7                      71                      $42,75  $8,65   $0,00  $0,00   $51,40      Prcard        City Service                       41,922686284              -87,649488729              POINT (-87.6494887289 41.9226862843)  41,744205146               -87,656305986               POINT (-87.6563059862 41.7442051463)
863b9b2b00af33990eb59400b6db1ac586d58a16  f9bc93a0ba6b1f18c9709a96c99bb9c5a99054b1711f80ddfe986a0f78a02470f146c48fd7d66bf74fe374f53d032676cb2fb7871afce4314dfdac97d4f22d32  05/01/2026 12:00:00 AM  05/01/2026 12:00:00 AM  648           3,55                                                   76                                             $12,00  $0,00   $0,00  $4,00   $16,50      Credit Card   City Service                       41,980264315              -87,913624596              POINT (-87.913624596 41.9802643146)                                                          
954c3b4006793e96c39ea56df7db1cf4283aede9  b5ad9d970e0745256fbb7517babae43abcb43115d076dfcf4f08b427f18135fe75de72c1e3ebba579bc0a464055ca9ae6869f49fab8cc793a829e5c9f11cdf0b  05/01/2026 12:00:00 AM  05/01/2026 12:30:00 AM  1.980         13,9                                                   56                     8                       $37,50  $0,00   $0,00  $4,00   $41,50      Cash          Transit Administrative Center Inc  41,79259236               -87,769615453              POINT (-87.7696154528 41.7925923603)  41,899602111               -87,633308037               POINT (-87.6333080367 41.899602111)
d06eddc331367e8282eb138f0a0157730f3a0470  f1ed053acb7ee562f935ec0660878752bf1e1de1aa458b7bbaf9fafe036c83bcb2b21c12864ffe6af9e5e0184cbf3f04b784cf4895bf999e701877809ac0fceb  05/01/2026 12:00:00 AM  05/01/2026 12:15:00 AM  1.161         11,41                                                  76                     14                      $29,25  $0,00   $0,00  $0,00   $29,25      Cash          Chicago Independents               41,980264315              -87,913624596              POINT (-87.913624596 41.9802643146)   41,968069                  -87,721559063               POINT (-87.7215590627 41.968069)
9360cffa2936c678348fa228fc5ba0570767b25b  48c0b5669ed50a0dcd8bf0e69fd99bb2669cb027ec06c0b76f9781a5497dcb8cb04b1d3106e61447749bfbb5b6547bc82fc3e94ce2ea87b154d3f53ad364be98  05/01/2026 12:00:00 AM  05/01/2026 12:00:00 AM  698           3,82                                                   28                     8                       $25,00  $5,10   $0,00  $0,00   $30,60      Credit Card   Flash Cab                          41,874005383              -87,66351755               POINT (-87.6635175498 41.874005383)   41,899602111               -87,633308037               POINT (-87.6333080367 41.899602111)
7f9a8b3ce1e8c341fb313510bb5940201efd7e8b  a0144e27e6b11720292c08c38cc696f14e6254bbbad9719b78f017a6b01f99447cb485124377fdcc851e412403e14575490b637104cf6f1bf65858571a8e1e9f  05/01/2026 12:00:00 AM  05/01/2026 12:15:00 AM  1.320         10,8                                                   56                     28                      $28,50  $0,00   $0,00  $4,00   $32,50      Cash          Transit Administrative Center Inc  41,79259236               -87,769615453              POINT (-87.7696154528 41.7925923603)  41,874005383               -87,66351755                POINT (-87.6635175498 41.874005383)
497b50a57cb828b7d2b8f4cff0e09394fdb539ec  b972ec70e50b0f04e4fa382c61337d527d0cdfcf2c3007f28776933fe723960f4f35af95829923b98de387e054b62c6e7b1d233e0783c19d80e4226f45581494  05/01/2026 12:00:00 AM  05/01/2026 12:00:00 AM  600           1,7                                                    28                     8                       $8,75   $2,00   $0,00  $0,00   $10,75      Credit Card   Transit Administrative Center Inc  41,874005383              -87,66351755               POINT (-87.6635175498 41.874005383)   41,899602111               -87,633308037               POINT (-87.6333080367 41.899602111)
```

```bash
== Writing selected stats using xsv ==
field,type,sum,min,max,min_length,max_length,mean,stddev
Trip ID,Unicode,,0000006aa752d456d05c6eeb43b057adb1ffa540,ffffffdda8f2f9f98cf474cce05b7e5e34dc25e4,40,40,,
Taxi ID,Unicode,,000daaa11a2d961100513e232a1ce05391c5d797d2dc5687dedf8d061758071464a4712b6b7e1cb5bfa8a7d046a32efdea99d40582007dfa455182ed7ec426d7,ffda53354c610fd3af1aee46d723028a49014e35f7280ca3d812716eb3cf1f0a763556368e4139b7183ee1fb36e26104de62bb86601f2fa16e3d96167e25b84e,2,128,,
Trip Start Timestamp,Unicode,,01/01/2024 01:00:00 AM,12/31/2025 12:45:00 PM,22,22,,
Trip End Timestamp,Unicode,,01/01/2024 01:00:00 AM,12/31/2025 12:45:00 PM,0,22,,
Trip Seconds,Float,4172346801.2140765,0,999,0,6,270.86083488429114,318.6319652924088
Trip Miles,Unicode,,0,"99,99",0,8,,
Pickup Census Tract,Integer,116829599168192611,17031010100,17031980100,0,11,17031489801.72849,371718.99655845115
Dropoff Census Tract,Integer,113349213281733674,17031010100,17031980100,0,11,17031405209.87828,339250.90881308017
Pickup Community Area,Integer,523022263,1,77,0,2,34.919962779448646,25.99993002970627
Dropoff Community Area,Integer,360616122,1,77,0,2,25.68413698676304,20.300408115456825
Fare,Unicode,,"$0,00","$999,99",0,9,,
Tips,Unicode,,"$0,00","$99,99",0,7,,
Tolls,Unicode,,"$0,00","$99,99",0,9,,
Extras,Unicode,,"$0,00","$99,99",0,9,,
Trip Total,Unicode,,"$0,00","$999,99",0,9,,
Payment Type,Unicode,,Cash,Unknown,4,11,,
Company,Unicode,,2733 - 74600 Benny Jona,Wolley Taxi,7,36,,
Pickup Centroid Latitude,Unicode,,"41,650221676","42,021223593",0,12,,
Pickup Centroid Longitude,Unicode,,"-87,530712484","-87,913624596",0,13,,
Pickup Centroid Location,Unicode,,POINT (-87.5307124836 41.7030053028),POINT (-87.913624596 41.9802643146),0,36,,
Dropoff Centroid Latitude,Unicode,,"41,650221676","42,021223593",0,12,,
Dropoff Centroid Longitude,Unicode,,"-87,534902901","-87,913624596",0,13,,
Dropoff Centroid  Location,Unicode,,POINT (-87.5349029012 41.707311449),POINT (-87.913624596 41.9802643146),0,36,,

```

Filter out not needed columns using xsv and write to interim folder for further processing.
Removing columns: Trip ID, Taxi ID, Pickup Centroid Location, Dropoff Centroid Location
Trip ID and Taxi ID are identifiers, and the POINT (...) location columns are redundant because you already have lat/lon. This leads to a reduction of the dataset to 2.88 GB.

```bash
xsv select "Trip Start Timestamp,Trip End Timestamp,Trip Seconds,Trip Miles,Pickup Census Tract,Dropoff Census Tract,Pickup Community Area,Dropoff Community Area,Fare,Tips,Tolls,Extras,Trip Total,Payment Type,Company,Pickup Centroid Latitude,Pickup Centroid Longitude,Dropoff Centroid Latitude,Dropoff Centroid Longitude" \
'data/Taxi_Trips_(2024-)_20260514.csv' \
> data/interim/taxi_selected.csv
```

The timestamp min/max from xsv stats is unreliable because Trip Start Timestamp is treated as Unicode, so min/max are lexicographic strings, not real dates.

```bash
xsv select "Trip Start Timestamp" data/interim/taxi_selected.csv \
| tail -n +2 \
| cut -d "/" -f3 \
| cut -d " " -f1 \
| sort \
| uniq -c
```

````
6480350 2024
6825838 2025
2100772 2026

|      Year |           Rows |
| --------: | -------------: |
|      2024 |      6,480,350 |
|      2025 |      6,825,838 |
|      2026 |      2,100,772 |
| **Total** | **15,406,960** |
````

Keep trips with valid pickup time and pickup coordinates.

```bash
xsv search -s "Trip Start Timestamp" ".+" data/interim/taxi_selected.csv \
| xsv search -s "Pickup Centroid Latitude" ".+" \
| xsv search -s "Pickup Centroid Longitude" ".+" \
> data/interim/taxi_all_years_xsv_cleaned.csv

14985606
-rw-r--r--@ 1 moritz  staff   2.8G May 21 23:31 data/interim/taxi_all_years_xsv_cleaned.csv

xsv search -s "Trip Start Timestamp" "/2024 " data/interim/taxi_selected.csv \
| xsv search -s "Pickup Centroid Latitude" ".+" \
| xsv search -s "Pickup Centroid Longitude" ".+" \
> data/interim/taxi_2024_xsv_cleaned.csv

6300899
-rw-r--r--@ 1 moritz  staff   1.2G May 21 23:31 data/interim/taxi_2024_xsv_cleaned.csv

xsv search -s "Trip Start Timestamp" "/2025 " data/interim/taxi_selected.csv \
| xsv search -s "Pickup Centroid Latitude" ".+" \
| xsv search -s "Pickup Centroid Longitude" ".+" \
> data/interim/taxi_2025_xsv_cleaned.csv

6642470
-rw-r--r--@ 1 moritz  staff   1.3G May 21 23:31 data/interim/taxi_2025_xsv_cleaned.csv

xsv search -s "Trip Start Timestamp" "/2026 " data/interim/taxi_selected.csv \
| xsv search -s "Pickup Centroid Latitude" ".+" \
| xsv search -s "Pickup Centroid Longitude" ".+" \
> data/interim/taxi_2026_xsv_cleaned.csv

2042237
-rw-r--r--@ 1 moritz  staff   395M May 21 23:31 data/interim/taxi_2026_xsv_cleaned.csv
```

````
| Dataset   |       Rows |   Size |
| --------- | ---------: | -----: |
| all years | 14,985,606 | 2.8 GB |
| 2024      |  6,300,899 | 1.2 GB |
| 2025      |  6,642,470 | 1.3 GB |
| 2026      |  2,042,237 | 395 MB |
```