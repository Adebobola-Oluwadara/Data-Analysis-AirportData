from pathlib import Path
import pandas as pd
import altair as alt
import math

airport_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airports.dat.txt')
airline_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airlines.dat.txt')
route_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/routes.dat.txt')

# load data into dataframe`````
airline_df = pd.read_csv(airline_data, header=None, names=['airlineId', 'name',
                                                           'alias', 'IATA', 'ICAO',
                                                           'callsign', 'country_airline', 'active'])
airport_df = pd.read_csv(airport_data, header=None, names=['airportId', 'airportName', 'city',
                                                           'country_airport', 'IATA', 'ICAO',
                                                           'lat', 'long', 'alt',
                                                           'timezone', 'dst', 'tbase',
                                                           'type', 'source'])
route_df = pd.read_csv(route_data, header=None, names=['airlineCode', 'airlineId',
                                                       'sourcePort', 'sourcePortId',
                                                       'destPort', 'destPortId',
                                                       'codeShare', 'stops', 'equip'])

# panda settings to display all columns in console
pd.set_option('display.expand_frame_repr', False)

# disable the default 5000 rows limit
alt.data_transformers.disable_max_rows()

# Merge the data on 'sourcePort'
merged_df = pd.merge(route_df, airport_df[['IATA', 'country_airport']], left_on='sourcePort', right_on='IATA',
                     how='inner')
# merged_df = pd.merge(merged_df, airline_df[['ICAO', 'country_airline']], left_on='airlineCode', right_on='ICAO',
# how='inner')

# Calculate the count of flights between each country pair
flight_counts = merged_df.groupby(['country_airport', 'country_airline']).size().reset_index(name='count')

# Create a heatmap
heatmap = alt.Chart(flight_counts).mark_rect().encode(
    x=alt.X('country_airport:N', sort=alt.Sort(field='count', order='descending')),
    y=alt.Y('country_airline:N', sort=alt.Sort(field='count', order='descending')),
    color=alt.Color('count:Q', scale=alt.Scale(scheme='greens')),
    tooltip=['country_airport', 'country_airline', 'count']
).properties(
    width=700,
    height=500
)

# heatmap.show()
