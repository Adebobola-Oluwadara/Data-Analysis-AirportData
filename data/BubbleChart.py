import altair as alt
import pandas as pd
from pathlib import Path

# load data from local computer
airport_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/airports.dat.txt')

# array of countries in Europe
countries_in_europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
                       "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
                       "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein",
                       "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands",
                       "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia",
                       "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City"
                       ]

# load data into dataframe
airport_df = pd.read_csv(airport_data, header=None, names=['airportId', 'n_ame', 'city',
                                                           'country', 'IATA', 'ICAO',
                                                           'lat', 'long', 'alt',
                                                           'timezone', 'dst', 'tbase',
                                                           'type', 'source'])

# grouping the data by 'country' and counting their airports
extractedData = airport_df.groupby(by=['country']).count()['airportId'].reset_index()

# rename 'airportId' as 'airport count'
extractedData.rename(columns={'airportId': "airport count"}, inplace=True)

# extracting data for only countries in Europe
extractedData = extractedData[extractedData['country'].isin(countries_in_europe)]

# define the bubble chart
chart = alt.Chart(extractedData).mark_circle().encode(
    x=alt.X('country:N'),
    y=alt.Y('airport count:Q', scale=alt.Scale(type='log')),
    size=alt.Size('airport count:Q'),
    color=alt.Color('country:N')
).properties(
    width=500,
    height=500,
    title='Total Number of Airports in European Countries'
)

# display the chart
chart.show()
