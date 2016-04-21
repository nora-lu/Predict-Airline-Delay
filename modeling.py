import pandas as pd
from sklearn import linear_model, cross_validation, metrics, svm
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

base_path = '/work/project2/'
files = ['joined_weather_2010.csv', 'joined_weather_2011.csv', 'joined_weather_2012.csv',
		 'joined_weather_2013.csv', 'joined_weather_2014.csv', 'joined_weather_2015.csv']
#files = ['joined_weather_2010.csv']
df = pd.DataFrame()
for file in files:
	df_ontime = pd.read_csv(base_path+file, sep=',', encoding='utf-8', nrows=500)
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

len = len(df)
train_len = round(len * 0.8)

cols = ['month', 'unique_carrier', 'taxi_out', 'taxi_in', 'holidays', 'dep_temp_f', 'dep_wind_speed_mph',
			'dep_precipitation_in', 'dep_conditions', 'arr_temp_f', 'arr_wind_speed_mph', 'arr_precipitation_in',
			'arr_conditions', 'distance_group', 'day_of_week', 'crs_dep_hour']
categ = [cols.index(x) for x in ('crs_dep_hour', 'month',  'distance_group', 'holidays', 'dep_conditions', 'arr_conditions',
	                                 'unique_carrier', 'day_of_week')]
enc = OneHotEncoder(categorical_features = categ)

def buildModel(df):
	train_y = df['arr_del15'][:train_len]
	train_x = df[cols][:train_len]

	# transform categorical features
	train_x['unique_carrier'] = pd.factorize(train_x['unique_carrier'])[0]
	train_x['dep_conditions'] = pd.factorize(train_x['dep_conditions'])[0]
	train_x['arr_conditions'] = pd.factorize(train_x['arr_conditions'])[0]
	
	pd.set_option('display.max_rows', 500)
	print(train_x)

	# train_x['origin'] = pd.factorize(train_x['origin'])[0]
	#	train_x['dest'] = pd.factorize(train_x['dest'])[0]
	# print(train_x)
	train_x = enc.fit_transform(train_x)
	print(train_x.shape)

	# Create Random Forest classifier with 50 trees
	clf_rf = RandomForestClassifier(n_estimators=50, n_jobs=-1)
	clf_rf.fit(train_x.toarray(), train_y)

	del train_x, train_y
	print("Model built")
	return clf_rf

rf = buildModel(df)
test_x = df[cols][train_len:]
test_x['unique_carrier'] = pd.factorize(test_x['unique_carrier'])[0]
test_x['dep_conditions'] = pd.factorize(test_x['dep_conditions'])[0]
test_x['arr_conditions'] = pd.factorize(test_x['arr_conditions'])[0]
test_x = enc.transform(test_x)
print(test_x.shape)

test_y = df['arr_del15'][train_len:]

del df

# Evaluate on test set
pr = rf.predict(test_x.toarray())

# print results
cm = confusion_matrix(test_y, pr)
print("Confusion matrix")
print(pd.DataFrame(cm))
report_svm = precision_recall_fscore_support(list(test_y), list(pr), average='binary')
print(report_svm)
print("\nprecision = %0.2f, recall = %0.2f, F1 = %0.2f, accuracy = %0.2f\n" % \
        (report_svm[0], report_svm[1], report_svm[2], accuracy_score(list(test_y), list(pr))))

# train_x = transformed[:train_len]
# test_x = transformed[train_len:]
#
# # Create logistic regression model with L2 regularization
# clf_lr = linear_model.LogisticRegression(penalty='l2', class_weight='balanced')
# clf_lr.fit(train_x, train_y)
#
# # Predict output labels on test set
# pr = clf_lr.predict(test_x)
#
# # display evaluation metrics
# cm = confusion_matrix(test_y, pr)
# print("Confusion matrix")
# print(pd.DataFrame(cm))
# report_lr = precision_recall_fscore_support(list(test_y), list(pr), average='binary')
# print("\nprecision = %0.2f, recall = %0.2f, F1 = %0.2f, accuracy = %0.2f\n" % \
#         (report_lr[0], report_lr[1], report_lr[2], accuracy_score(list(test_y), list(pr))))
