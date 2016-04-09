import pandas as pd
from sklearn import linear_model, cross_validation, metrics, svm
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# read file
df = pd.read_csv('D:\CS586\Project2'+'\\'+'test.csv', sep=',', encoding='utf-8')
df['crs_dep_hour'] = df['dep_time_blk'].map(lambda x: str(x)[:2]).astype('int')
df['taxi_out'] = df['taxi_out'].astype('int')
df['taxi_in'] = df['taxi_in'].astype('int')
print(df.info())

len = len(df)
print(len)
train_len = round(len * 0.8)
print(train_len)

cols = ['month', 'origin_airport_id', 'dest_airport_id',
               'taxi_out', 'taxi_in', 'distance_group', 'day_of_week', 'crs_dep_hour']
train_y = df['arr_del15'][:train_len].as_matrix()
train_x = df[cols][:train_len].as_matrix()

test_y = df['arr_del15'][train_len:].as_matrix()
test_x = df[cols][train_len:].as_matrix()

# Create logistic regression model with L2 regularization
clf_lr = linear_model.LogisticRegression(penalty='l2', class_weight='balanced')
clf_lr.fit(train_x, train_y)

# Predict output labels on test set
pr = clf_lr.predict(test_x)

# display evaluation metrics
cm = confusion_matrix(test_y, pr)
print("Confusion matrix")
print(pd.DataFrame(cm))
report_lr = precision_recall_fscore_support(list(test_y), list(pr), average='binary')
print("\nprecision = %0.2f, recall = %0.2f, F1 = %0.2f, accuracy = %0.2f\n" % \
        (report_lr[0], report_lr[1], report_lr[2], accuracy_score(list(test_y), list(pr))))

del df