from process import processdata
import pandas as pd
from matplotlib import pyplot as plt

# files = ['ontime_2010_final.csv', 'ontime_2011_final.csv']
files = ['ontime_2010_final.csv', 'ontime_2011_final.csv', 'ontime_2012_final.csv',
          'ontime_2013_final.csv', 'ontime_2014_final.csv', 'ontime_2015_final.csv']

delay_percentage_by_month = pd.DataFrame()

for file in files:
    print(file)
    df = processdata(file)

    ########### Yearly line chart of delay percentage by months #########
    grouped_total = df[['id','month']].groupby('month').count()
    grouped_delay = df[df.arr_del15 == 1][['arr_del15', 'month']].groupby('month').count()
    print("Total flights", grouped_total)
    print("Delay flights", grouped_delay)

    delay_percentage_by_month[file[7:11]] = grouped_delay.arr_del15/grouped_total.id

    # release memory space
    del df

delay_percentage_by_month.plot(kind='line')
