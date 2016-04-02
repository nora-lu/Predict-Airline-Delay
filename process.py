import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
import matplotlib.pyplot as plt

base_file_path = 'D:\CS586\Project2\Predict_airline_delay_modeling_data'
# files = ['ontime_2010_final.csv']
files = ['ontime_2010_final.csv', 'ontime_2011_final.csv', 'ontime_2012_final.csv',
         'ontime_2013_final.csv', 'ontime_2014_final.csv', 'ontime_2015_final.csv']
delay_keys = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']

delay_per_year = []

for file in files:
    csv_file = base_file_path + '\\' + file
    df = pd.read_csv(csv_file, sep=',', dtype={'crs_elapsed_time ': np.str},
                     encoding='utf-8')
    df.rename(columns=lambda  x: x.strip(), inplace=True)
    print("Length of raw dataset", file, " is ", len(df));

    # Remove records where delay information is missing
    df = df[df.arr_del15 != 'null']
    df.arr_del15 = df.arr_del15.astype('float')

    print("After removing missing records, length is", len(df))

    for key in delay_keys:
        df[key] = df[key].astype(str)
        df[key] = df[key].replace('null', '0')
        df[key] = df[key].astype(float)

    total = len(df)
    delay = 0
    for value in df['arr_del15']:
        if value == 1:
            delay = delay + 1

    print("Total flights =", total)
    print("Delay flights =", delay)
    print("Percentage of delay flights is", delay/total)
    print()
    del df


# sub_df = df[['cancelled', 'diverted']]
#     sub_df = sub_df.as_matrix()
#     print(sub_df.shape)
#
#     sel = VarianceThreshold(threshold=.8*(1-.8))
#     sel.fit_transform(sub_df)
