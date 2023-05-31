import pandas as pd
import altair as alt
from pathlib import Path

# load data from local computer
airport_data = Path('/Users/oluwadara/PycharmProjects/scientificProject/data/Airports (1).csv')

# load data into dataframe
airport_df = pd.read_csv(airport_data, header=None,
                         names=['Rank', 'Airport', 'Location', 'Country', 'Code', 'Passengers', 'Year'])

# list of European countries
european_countries = ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina',
                      'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland',
                      'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo',
                      'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
                      'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal',
                      'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
                      'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City']

# filter the data by the list of European countries
european_airport_df = airport_df[airport_df['Country'].isin(european_countries)]

# filter the data by year and group by country
group_airport_df = european_airport_df[european_airport_df['Year'] == 2019].groupby(by=['Country']).sum(numeric_only=True)['Passengers']

# sum the passengers for each year
group_airport_year_df = group_airport_df.groupby(by=['Year'])['Passengers'].sum().reset_index()


# convert the resulting Series to a DataFrame and rename the column
group_airport_df = group_airport_df.to_frame().rename(columns={'Passengers': 'Total Passengers'})

# calculate the percentage of passengers for each country
group_airport_df = group_airport_df.reset_index()
group_airport_df['Percentage'] = group_airport_df['Total Passengers'] / group_airport_df['Total Passengers'].sum()


# create a pie chart using Altair
chart = alt.Chart(group_airport_df).mark_arc(innerRadius=60, outerRadius=120).encode(
    theta=alt.Theta(field='Percentage', type='quantitative', title='Percentage', stack=True),
    color=alt.Color(field="Country", type="nominal", title='Country'),
    tooltip=['Country', 'Total Passengers']
).properties(
    title={
      "text": ['Percentage of Passengers by Country in 2019'],
      "subtitle": ["Source: Kaggle"],
      "fontSize": 16,
      "fontWeight": "normal",
      "anchor": "middle"
    }
)

subtitle = alt.Chart(pd.DataFrame({'text': [f'Test {group_airport_year_df[0]}']})).mark_text(
    size=16, align='center', font='Courier New', fontWeight='lighter'
).encode(
    text=alt.Text('text:N')
).properties(
    width=300,
    height=300
).transform_calculate(
    angle='0'
)

text = chart.mark_text(radius=140, font='Courier New', fontSize=16, fontWeight='bold', align='center').encode(
    text=alt.Text("Percentage:Q", format=".1%"),
    theta=alt.Theta('Percentage:Q', stack=True)
)

(chart + text + subtitle).configure_view(strokeWidth=0).configure_title(anchor='middle').show()