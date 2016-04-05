from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from process import processdata
import pandas as pd
import os



os.chdir('/Users/shushenglu/codes/Predict_Airline_Delay/')

top_50_airports = ['ATL', 'LAX', 'ORD', 'DFW', 'JFK', 'DEN', 'SFO', 'CLT', 'LAS', 'PHX', 'IAH', 'MIA', 'SEA',
                   'EWR', 'MCO', 'MSP', 'DTW', 'BOS', 'PHL', 'LGA', 'FLL', 'BWI', 'IAD', 'MDW', 'SLC', 'DCA',
                   'HNL', 'SAN', 'TPA', 'PDX', 'STL', 'HOU', 'BNA', 'AUS', 'OAK', 'MCI', 'MSY', 'RDU', 'SJC',
                   'SNA', 'DAL', 'SMF', 'SJU', 'SAT', 'RSW', 'PIT', 'CLE', 'IND', 'MKE', 'CMH']

locations = pd.read_csv('other_files/airports.dat.txt', header=None, names=['id', 'name', 'city', 'country',
                                                                            'airport_id', 'icao', 'lat', 'lot',
                                                                            'altitude', 'timezone', 'dst', 'tz'])

locations = locations[locations['airport_id'].isin(top_50_airports)]

files = ['ontime_2010_final.csv', 'ontime_2011_final.csv', 'ontime_2012_final.csv',
         'ontime_2013_final.csv', 'ontime_2014_final.csv', 'ontime_2015_final.csv']

for file in files:
    print(file)
    df = processdata(file)
    ########### Total and Delay by Origin Airport #########
    grouped_total = df[['id', 'origin']].groupby('origin').count()
    grouped_total.reset_index(level=0, inplace=True)
    grouped_total = grouped_total[grouped_total['origin'].isin(top_50_airports)]
    grouped_total.columns = ['airport_id', 'total' + file[7:11]]

    grouped_delay = df[df.arr_del15 == 1][['id', 'origin']].groupby('origin').count()
    grouped_delay.reset_index(level=0, inplace=True)
    grouped_delay = grouped_delay[grouped_delay['origin'].isin(top_50_airports)]
    grouped_delay.columns = ['airport_id', 'delay' + file[7:11]]

    locations = locations.merge(grouped_total, on='airport_id').merge(grouped_delay, on='airport_id')
    # release memory spacel
    del df

print(locations)
locations['total'] = locations['total2010'] + locations['total2011'] + locations['total2012'] + locations['total2013'] + \
                     locations['total2014'] + locations['total2015']

locations['delay'] = locations['delay2010'] + locations['delay2011'] + locations['delay2012'] + locations['delay2013'] + \
                     locations['delay2014'] + locations['delay2015']

locations['delay_ratio'] = locations['delay'] / locations['total']

### read airport delay ratio csv file
locations = pd.read_csv('/Users/shushenglu/GitHub/Predict-Airline-Delay/statistics-results/airport_delay_ratio.csv')

### Map Visualization
fig = plt.figure()
fig.set_size_inches(6, 6)

m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
            projection='lcc', lat_1=33, lat_2=45, lon_0=-95)

m.drawcoastlines()
m.drawstates()
m.drawcountries()

# total_by_carrier = pd.DataFrame()
# delay_by_carrier = pd.DataFrame()

loc = locations[['delay_ratio', 'lot', 'lat', 'airport_id']]
lons = loc['lot'].tolist()
lats = loc['lat'].tolist()
ratios = loc['delay_ratio'].tolist()
labels = loc['airport_id'].tolist()


def get_marker_color(ratio):
    if ratio < 0.3:
        return ('go')
    elif ratio < 0.624:
        return ('yo')
    else:
        return ('ro')


ratio_min = min(ratios)
ratio_max = max(ratios)
ratios = [(x - ratio_min) / (ratio_max - ratio_min) for x in ratios]
min_marker_size = 20
for lon, lat, ratio in zip(lons, lats, ratios):
    x, y = m(lon, lat)
    msize = (ratio - 0.1) * min_marker_size
    mcolor = get_marker_color(ratio)
    m.plot(x, y, mcolor, alpha=0.7, markersize=msize)

### Add labels of 10 most delayed
x, y = m(lons, lats)
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt + 10000, ypt + 5000, label)
