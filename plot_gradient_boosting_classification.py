import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import ensemble

###############################################################################
# Load data
base_path = '/work/project2/'
files = ['joined_weather_2010.csv', 'joined_weather_2011.csv', 'joined_weather_2012.csv',
		 'joined_weather_2013.csv', 'joined_weather_2014.csv', 'joined_weather_2015.csv']

df = pd.DataFrame()
for file in files:
	df_ontime = pd.read_csv(base_path+file, sep=',', encoding='utf-8')
	df_ontime['crs_dep_hour'] = df_ontime['dep_time_blk'].map(lambda x: str(x)[:2])
	df_ontime = df_ontime[df_ontime.crs_dep_hour != 'na']
	df_ontime['crs_dep_hour'] = df_ontime['crs_dep_hour'].astype('int')
	df_ontime['taxi_out'] = df_ontime['taxi_out'].astype('int')
	df_ontime['holidays'] = df_ontime['holidays'].astype('int')

	df_ontime = df_ontime[pd.notnull(df_ontime.dep_temp_f) & pd.notnull(df_ontime.arr_temp_f)]

	df_ontime['dep_temp_f'] = df_ontime['dep_temp_f'].astype('int')
	df_ontime['dep_wind_speed_mph'] = df_ontime['dep_wind_speed_mph'].astype('int')
	df_ontime['dep_precipitation_in'] = df_ontime['dep_precipitation_in'].astype('int')
	df_ontime['arr_temp_f'] = df_ontime['arr_temp_f'].astype('int')
	df_ontime['arr_wind_speed_mph'] = df_ontime['arr_wind_speed_mph'].astype('int')
	df_ontime['arr_precipitation_in'] = df_ontime['arr_precipitation_in'].astype('int')
	df_ontime['arr_del15'] = df_ontime['arr_del15'].astype('int')
	df = df.append(df_ontime)
	del df_ontime

df.drop(df.columns[[0,1,3,5,6,7,8,9,10,11,12,13,17,18,20,21,22,23,24,27,32]], axis=1, inplace=True)
print(df.info())

cols = ['month', 'unique_carrier', 'taxi_out', 'taxi_in', 'holidays', 'dep_temp_f', 'dep_wind_speed_mph',
			'dep_precipitation_in', 'dep_conditions', 'arr_temp_f', 'arr_wind_speed_mph', 'arr_precipitation_in',
			'arr_conditions', 'distance_group', 'day_of_week', 'crs_dep_hour']

X = df[cols]
y = df['arr_del15']
offset = int(X.shape[0] * 0.8)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

X_train.loc[:, 'unique_carrier'] = pd.factorize(X_train['unique_carrier'])[0]
X_test.loc[:, 'unique_carrier'] = pd.factorize(X_test['unique_carrier'])[0]

X_train.loc[:, 'dep_conditions'] = pd.factorize(X_train['dep_conditions'])[0]
X_test.loc[:, 'dep_conditions'] = pd.factorize(X_test['dep_conditions'])[0]

X_train.loc[:, 'arr_conditions'] = pd.factorize(X_train['arr_conditions'])[0]
X_test.loc[:, 'arr_conditions'] = pd.factorize(X_test['arr_conditions'])[0]
###############################################################################
# Fit classification model
params = {'n_estimators': 100, 'max_depth': 1, 'min_samples_split': 2,
          'learning_rate': 0.1, 'loss': 'deviance'}
clf = ensemble.GradientBoostingClassifier(**params)

clf.fit(X_train, y_train)
print("Model built")
score = clf.score(X_test, y_test)
print(score)

###############################################################################
# Plot training deviance

# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

# for i, y_pred in enumerate(clf.staged_predict(X_test)):
#     test_score[i] = clf.loss_(y_test, y_pred)
#
# print(test_score)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

###############################################################################
# Plot feature importance
feature_importance = clf.feature_importances_
print(feature_importance)
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
print(sorted_idx)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos, (np.array(cols))[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.savefig('importance.png')