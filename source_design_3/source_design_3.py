from pathlib import Path
import altair as alt
import pandas as pd
from vega_datasets import data

# load data from local computer
airport_data = Path('../airports.dat.txt')
country_data = Path('world_country_and_usa_states_latitude_and_longitude_values.csv')

# load data into dataframe
airport_df = pd.read_csv(airport_data, header=None, names=['airportId', 'n_ame', 'city',
                                                           'country', 'IATA', 'ICAO',
                                                           'lat', 'long', 'alt',
                                                           'timezone', 'dst', 'tbase',
                                                           'type', 'source'])
country_df = pd.read_csv(country_data, header=None, names=['country_code', 'latitude',
                                                           'longitude', 'country',
                                                           'usa_state_code', 'usa_state_latitude',
                                                           'usa_state_longitude', 'usa_state'])

# panda settings to display all columns in console
pd.set_option('display.expand_frame_repr', False)

# merge country and airport
merged_data = pd.merge(airport_df, country_df, left_on='country', right_on='country', how='inner')

# grouping the data by 'country' and counting their airports
extractedData = merged_data.groupby(by=['country', 'country_code', 'latitude', 'longitude']).count()['airportId'].reset_index()

# rename 'airportId' as 'airport count'
extractedData.rename(columns={'airportId': "airport count"}, inplace=True)

extractedData = extractedData.sort_values(by='airport count')

# Load the world map
source = alt.topo_feature(data.world_110m.url, 'countries')

# create the chart using extractedData
chart = alt.Chart(extractedData)

# add the geoshape layer for Europe
background = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator')

# add the circle layer for airports
circles = chart.mark_circle().encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    size=alt.Size('airport count:Q', title='Airport Count'),
    tooltip=['country', 'airport count']
)

# combine the layers and set chart properties
proportional_symbol_map = (background + circles).properties(
    title='TOTAL NUMBER OF AIRPORTS IN THE WORLD',
    width=800,
    height=600
)

# display the chart
proportional_symbol_map.show()


