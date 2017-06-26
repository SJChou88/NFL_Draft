# NFL_Draft

This project attempts to predict the first round draft using publicly available data and machine learning while ignoring specific team needs.  

## Data

Data is sourced from http://www.pro-football-reference.com and http://collegepollarchive.com using scrapy. Combine drill performance, college football statistics, and college team rankings were merged together for each player when available. Some data was not available, so medians by position were used and then percentiles by positions were used for modeling.

## Modeling

Multiple regressions were tested, but the last techniques used were xgboost with gridsearch for parameters, followed by logistic regression to remove a number of variables ( as many interactions terms were present ), and then another xgboost regression.

## Results

The model was successful at predicting about 30% of first round draft picks. It had difficulty predicting on positions with very little college statistics ( offensive line ) and certain position where physical attributes are over valued on the top end ( 40 times for WR and CB ).
