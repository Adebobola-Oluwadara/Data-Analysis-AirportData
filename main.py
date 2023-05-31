from pathlib import Path
import pandas as pd
import altair as alt

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

# Drop duplicates before merging on the country column
# airport_df = airport_df.drop_duplicates(subset=['country'])
# airline_df = airline_df.drop_duplicates(subset=['country'])
airline_df['airlineId'] = airline_df['airlineId'].astype(str)
airport_df['airportId'] = airport_df['airportId'].astype(str)

# merged three data together.
merged_df = pd.merge(airline_df, route_df, on='airlineId', how='inner')
merged_merged_df = pd.merge(merged_df, airport_df,
                            left_on='destPortId', right_on='airportId', how='inner')
grouped_df = merged_merged_df.groupby('destPort')
print(merged_merged_df)

states = alt.topo_feature(country_airport, 'countries')
source = alt.topo_feature(data.world_110m.url, 'countries')
background = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white',
    color='blue'
).project('mercator').properties(
    width=500,
    height=300,
    title='POPULAR AIRPORTS DESTINATION IN THE WORLD BASED ON PASSENGER\'S RECORDS '
        
)

# points = alt.Chart(merged_merged_df).mark_circle().encode(
#     longitude='long:Q',
#     latitude='lat:Q',
#     size=alt.value(10),
#     tooltip=['city', 'airportName']
# )
#
# chart = background + points
# chart.configure_view(
#     fill='red'
# )
#
# chart.show()


# der = alt.Chart(countries).mark_geoshape(
#     fill='lightgray',
#     stroke='white'
# ).project(
#     "equirectangular"
# ).properties(
#     width=500,
#     height=300
# )
# der.show()
# merged_df = airport_df.merge(airline_df, on='ICAO', how='inner')
# merged_df = merged_df[merged_df['country'].isin(aad)]
# print(merged_df)

# chart = alt.Chart(merged_df).mark_circle(size=100).encode(
#     latitude='lat:Q',
#     longitude='lon:Q',
#     color='country:N',
#     shape='airline:N'
# ).properties(
#     width=600,
#     height=400
# ).project(
#     type='mercator'
# )
#
# # Add city label
# text = chart.mark_text(dx=10, dy=-10).encode(
#     text='city:N',
#     latitude='lat:Q',
#     longitude='lon:Q'
# )
#
# # combine the chart and text layer
# chart = chart + text
#
# chart.show()
