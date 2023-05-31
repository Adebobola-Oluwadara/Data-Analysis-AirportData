from pathlib import Path
import altair as alt
import pandas as pd
from vega_datasets import data

# Since these data are each more than 5,000 rows we'll import from the URLs
airport_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airports.dat.txt')
route_data = 'https://bit.ly/3m5olIF'
airline_data = 'https://bit.ly/3SqbvAu'

# load data into dataframe
airport_df = pd.read_csv(airport_data, header=None, names=['airportId', 'n_ame', 'city',
                                                           'country', 'IATA', 'ICAO',
                                                           'lat', 'long', 'alt',
                                                           'timezone', 'dst', 'tbase',
                                                           'type', 'source'])
route_df = pd.read_csv(route_data, header=None, names=['airlineCode', 'airlineId',
                                                       'sourcePort', 'sourcePortId',
                                                       'destPort', 'destPortId',
                                                       'codeShare', 'stops', 'equip'])
airline_df = pd.read_csv(airline_data, header=None, names=['airlineId', 'name',
                                                           'alias', 'IATA', 'ICAO',
                                                           'callsign', 'country_airline', 'active'])

# convert airportId from int to string.
airline_df['airlineId'] = airline_df['airlineId'].astype(str)
airport_df['airportId'] = airport_df['airportId'].astype(str)

# merged three data together.
merged_df = pd.merge(airline_df, route_df, on='airlineId', how='inner')
merged_merged_df = pd.merge(merged_df, airport_df,
                            left_on='sourcePortId', right_on='airportId', how='inner')

# grouping the data by 'country' and counting their airports
extractedData = merged_merged_df.groupby(by=['country', 'lat', 'long']).count()['airportId'].reset_index()

# rename 'airportId' as 'airport count'
extractedData.rename(columns={'airportId': "airport count"}, inplace=True)

extractedData = extractedData.sort_values(by='airport count')

# Load the world map
source = alt.topo_feature(data.world_110m.url, 'countries')

# Create mouseover selection
select_city = alt.selection_single(
    on="mouseover", nearest=True, fields=["sourcePort"], empty="none"
)

background = alt.Chart(source).mark_geoshape(
    fill="lightgray",
    stroke="white"
).properties(
    width=750,
    height=500
).project("naturalEarth1")

connections = alt.Chart(merged_merged_df).mark_rule(opacity=0.35).encode(
    latitude="lat:Q",
    longitude="long:Q",
    latitude2="lat2:Q",
    longitude2="lon2:Q"
).transform_lookup(
    lookup="sourcePort",
    from_=route_df
).transform_lookup(
    lookup="destPort",
    from_=route_df,
    as_=["country", "lat2", "lon2"]
).transform_filter(
    select_city
)

points = alt.Chart(merged_merged_df).mark_circle().encode(
    latitude="lat:Q",
    longitude="long:Q",
    size=alt.Size("routes:Q", scale=alt.Scale(range=[0, 1000]), legend=None),
    order=alt.Order("routes:Q", sort="descending"),
    tooltip=['country', 'airport count']
).transform_aggregate(
    routes="count()",
    groupby=[""]
).transform_lookup(
    lookup="origin",
    from_=lookup_data
).transform_filter(
    (alt.datum.state != "PR") & (alt.datum.state != "VI")
).add_params(
    select_city
)

(background + connections + points).configure_view(stroke=None)