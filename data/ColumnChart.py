from pathlib import Path
import altair as alt
import pandas as pd

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

# panda settings to display all columns in console
pd.set_option('display.expand_frame_repr', False)

# grouping the data by 'country' and counting their airports
extractedData = airport_df.groupby(by=['country']).count()['airportId'].reset_index()

# rename 'airportId' as 'airport count'
extractedData.rename(columns={'airportId': "airport count"}, inplace=True)

# extracting data for only countries in Europe
extractedData = (extractedData[extractedData['country'].isin(countries_in_europe)])

extractedData = extractedData.sort_values(by='airport count')

# plot 'column chart' in ascending order
chart = alt.Chart(extractedData).mark_bar().encode(
    y=alt.Y('country:N', sort=alt.EncodingSortField(field='airport count', op='sum', order='ascending')),
    x=alt.X('airport count:Q'),
).properties(
    width=500,
    height=650,
    title='TOTAL NUMBER OF AIRPORTS IN EUROPEAN COUNTRIES'
)

# Add text labels to each bar
text = chart.mark_text(
    align='center',
    dx=15
).encode(
    text='airport count'
)

# chart display in browser
chart_with_text = chart + text
chart_with_text.show()