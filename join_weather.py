import os
import pandas as pd
import numpy as np

# os.chdir('/work/project2/')

airport_info = pd.read_csv('airports.dat', header=None, names=['id', 'name', 'city', 'country',
                                                                            'iata', 'icao', 'lat', 'lot',
                                                                            'altitude', 'timezone', 'dst', 'tz'])

airport_info = airport_info[['city','iata']]
airport_info = airport_info.set_index('iata')
airport_info.index.name = None

ontime = pd.read_csv('joined_holiday_2015.csv')

ontime = ontime.join(airport_info, on=['origin'])
###Uncomment to check how many cities have different names
#ontime.loc[ontime['origin_city_name'] != ontime['city']].groupby('city').count()
ontime['origin_city_name'] = ontime['city']
ontime = ontime.drop('city', 1)

ontime = ontime.join(airport_info, on=['dest'])
ontime['dest_city_name'] = ontime['city']
ontime = ontime.drop('city', 1)

weather = pd.read_csv('weather-by-year/weather_2015.csv')
weather = weather.rename(columns = {' wind_speed_mph':'wind_speed_mph','city':'original_city'})

weather = weather[['original_city','state','zip','airport_code','temperature_f','wind_speed_mph','precipitation_in','events','date','time_blk']]

airport_info = pd.read_csv('airports.dat', header=None, names=['id', 'name', 'city', 'country',
                                                                            'iata', 'icao', 'lat', 'lot',
                                                                            'altitude', 'timezone', 'dst', 'tz'])

airport_info = airport_info[['city','icao']]
airport_info = airport_info.set_index('icao')
airport_info.index.name = None

weather = weather.join(airport_info, on=['airport_code'])
weather = weather.drop('original_city', 1)

weather.precipitation_in.fillna(0,inplace=True)
weather.events.fillna("Good", inplace=True)
weather.wind_speed_mph.fillna(0,inplace=True)
weather.wind_speed_mph.replace(to_replace='Calm',value = 0,inplace=True)
weather['wind_speed_mph'] = pd.to_numeric(weather['wind_speed_mph'])
weather.drop_duplicates(['date','city', 'state', 'airport_code', 'time_blk'],keep= 'last', inplace=True)

ontime = pd.merge(ontime,weather, how = 'left',left_on=['origin_city_name','fl_date','dep_time_blk','origin_state_abr'],
                  right_on=['city','date','time_blk','state'])
ontime = ontime.drop(['city','date','time_blk','state','zip'],axis =1)

ontime.rename(columns= {'temperature_f':'dep_temp_f',
                        'wind_speed_mph':'dep_wind_speed_mph',
                        'precipitation_in':'dep_precipitation_in',
                        'events':'dep_conditions'},inplace=True)

ontime = pd.merge(ontime,weather, how = 'left',left_on=['dest_city_name','fl_date','arr_time_blk','dest_state_abr'],
                  right_on=['city','date','time_blk','state'])
ontime.drop(['city','date','time_blk','state','zip'],axis = 1, inplace= True)

ontime.rename(columns= {'temperature_f':'arr_temp_f',
                        'wind_speed_mph':'arr_wind_speed_mph',
                        'precipitation_in':'arr_precipitation_in',
                        'events':'arr_conditions'},inplace=True)

ontime = ontime[(pd.notnull(ontime.airport_code_x)) & (pd.notnull(ontime.airport_code_y))]

ontime.to_csv('joined_weather_2015.csv', index=False)
