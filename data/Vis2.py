import altair as alt
from pathlib import Path
import pandas as pd
from vega_datasets import data


# load data from local computer
airport_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airports.dat.txt')
airline_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airlines.dat.txt')
route_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/routes.dat.txt')


# load data into dataframe`````
airline_df = pd.read_csv(airline_data, header=None, names=['airlineId', 'name',
                                                           'alias', 'IATA', 'ICAO',
                                                           'callsign', 'country_airline', 'active'])
airport_df = pd.read_csv(airport_data, header=None, names=['airportId', 'airportName', 'city',
                                                           'country_airport', 'IATA', 'ICAO',
                                                           'lat', 'long', 'altitude',
                                                           'timezone', 'dst', 'tbase',
                                                           'type', 'source'])
airport_df['altitude'] = pd.to_numeric(airport_df['altitude'], errors='coerce')
route_df = pd.read_csv(route_data, header=None, names=['airlineCode', 'airlineId',
                                                       'sourcePort', 'sourcePortId',
                                                       'destPort', 'destPortId',
                                                       'codeShare', 'stops', 'equip'])

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
                            left_on='sourcePortId', right_on='airportId', how='inner')

# states = alt.topo_feature(countries, 'countries')
source = alt.topo_feature(data.world_110m.url, 'countries')

# Define a color scale based on altitude
color_scale = alt.Scale(
    domain=(0, merged_merged_df['altitude'].max()),
)

background = alt.Chart(source).mark_geoshape(
    color=alt.Color('altitude:Q', scale=color_scale),
    fill=alt.Color('country_airport:N', scale=alt.Scale(scheme='reds')),
    stroke='white',
).project('naturalEarth1').properties(
    width=1100,
    height=700,
    title='DISTRIBUTION OF AIRPORTS IN THE WORLD'
).properties(width=500, height=300)

points = alt.Chart(merged_merged_df).mark_circle().encode(
    longitude='long:Q',
    latitude='lat:Q',
    size=alt.value(10),
    tooltip=['airportName', 'city', 'country_airport'],
    color=alt.Color('altitude:Q', scale=color_scale, legend=None)
)

chart = background + points
chart.show()





