import altair as alt
import pandas as pd
from vega_datasets import data

# load data from local computer
airport_data = 'airports.dat.txt'
airline_data = 'airlines.dat.txt'
route_data = 'routes.dat.txt'

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

# use the world map
countries = alt.topo_feature(data.world_110m.url, 'countries')

# panda settings to display all columns in console
pd.set_option('display.expand_frame_repr', False)

# disable the default 5000 rows limit
alt.data_transformers.disable_max_rows()

# convert airportId from int to string.
airline_df['airlineId'] = airline_df['airlineId'].astype(str)
airport_df['airportId'] = airport_df['airportId'].astype(str)

# merged three data together.
merged_df = pd.merge(airline_df, route_df, on='airlineId', how='inner')
merged_merged_df = pd.merge(merged_df, airport_df,
                            left_on='destPortId', right_on='airportId', how='inner')

# use data on map
source = alt.topo_feature(data.world_110m.url, 'countries')
background = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white',
    color='blue'
).project('mercator').properties(
    width=1500,
    height=700,
    title='DISTRIBUTION OF DESTINATION AIRPORTS IN THE WORLD'
)

points = alt.Chart(merged_merged_df).mark_circle().encode(
    longitude='long:Q',
    latitude='lat:Q',
    size=alt.value(10),
    tooltip=['airportName', 'city', 'country_airport']
)

# show the map
chart = background + points
chart.show()
