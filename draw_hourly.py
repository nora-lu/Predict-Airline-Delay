from process import processdata
import pandas as pd
from matplotlib import pyplot as plt

files = ['ontime_2010_final.csv', 'ontime_2011_final.csv', 'ontime_2012_final.csv',
          'ontime_2013_final.csv', 'ontime_2014_final.csv', 'ontime_2015_final.csv']

delay_percentage_by_hour = pd.DataFrame()


for file in files:
    print(file)
    df = processdata(file)

    ########### Yearly line chart of delay percentage by hours #########
    df['hour'] = df['dep_time_blk'].map(lambda x: str(x)[:2])
    grouped_total = df[['id','hour']].groupby('hour').count()
    grouped_delay = df[df.arr_del15 == 1][['arr_del15', 'hour']].groupby('hour').count()
    print("Total flights", grouped_total)
    print("Delay flights", grouped_delay)

    delay_percentage_by_hour[file[7:11]] = grouped_delay.arr_del15/grouped_total.id

    # release memory space
    del df

delay_percentage_by_hour.plot(kind='line')
plt.show()
