import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

base_file_path = '/Users/qian/Downloads/Predict_airline_delay_modeling_data/'
delay_keys = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']

def processdata(file):
    csv_file = base_file_path + file
    df = pd.read_csv(csv_file, sep=',', dtype={'crs_elapsed_time ': np.str},
                     encoding='utf-8')
    df.rename(columns=lambda  x: x.strip(), inplace=True)
    # print("Length of raw dataset", file, " is ", len(df));

    # Remove records where delay information is missing
    df = df[df.arr_del15 != 'null']
    df.arr_del15 = df.arr_del15.astype('float')
    # print("After removing missing records, length is", len(df))

    for key in delay_keys:
        df[key] = df[key].astype(str)
        df[key] = df[key].replace('null', '0')
        df[key] = df[key].astype(float)

    # total = len(df)
    # delay = 0
    # for value in df['arr_del15']:
    #     if value == 1:
    #         delay = delay + 1
    #
    # print("Total flights =", total)
    # print("Delay flights =", delay)
    # print("Percentage of delay flights is", delay/total)
    # print()
    return df[['id', 'year', 'month', 'day_of_month', 'fl_date', 'unique_carrier', 'tail_num', 'fl_num',
               'origin_airport_id', 'dest_airport_id', 'crs_dep_time', 'taxi_out', 'taxi_in', 'arr_del15',
               'arr_delay_group', 'air_time', 'distance_group', 'carrier_delay', 'weather_delay',
               'nas_delay', 'security_delay', 'late_aircraft_delay']]



# sub_df = df[['cancelled', 'diverted']]
#     sub_df = sub_df.as_matrix()
#     print(sub_df.shape)
#
#     sel = VarianceThreshold(threshold=.8*(1-.8))
#     sel.fit_transform(sub_df)
