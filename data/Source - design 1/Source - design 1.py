import pandas as pd
import altair as alt

# load data from local computer
airport_data = 'Airports (2).csv'

# load data into dataframe
airport_df = pd.read_csv(airport_data)

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

# filter the data by year and group by country and year
group_airport_df = european_airport_df[european_airport_df['Year'].isin(range(2016, 2021))].groupby(
    by=['Country', 'Year'])['Passengers'].sum().reset_index()

# sum the passengers for each year
group_airport_year_df = group_airport_df.groupby(by=['Year'])['Passengers'].sum().reset_index()

# merge the year totals back to the original data frame
group_airport_df = group_airport_df.merge(group_airport_year_df, on='Year', suffixes=('', '_year'))

# calculate the percentage of passengers for each country per year
group_airport_df['Percentage'] = group_airport_df['Passengers'] / group_airport_df['Passengers_year']

# convert the resulting Series to a DataFrame and rename the column
group_airport_df = group_airport_df.rename(columns={'Passengers': 'Total Passengers'})

# create the interactive visualization using the pie chart
select_year = alt.selection_single(
    name='year', fields=['Year'], init={'Year': 2016},
    bind=alt.binding_select(options=list(range(2016, 2021)), name="Select Year")
)

# create a pie chart using Altair
def chart(select_year):
    chart = alt.Chart(group_airport_df).mark_arc(innerRadius=60, outerRadius=120, filled=True).encode(
        theta=alt.Theta(field='Percentage', type='quantitative', title='Percentage', stack=True),
        color=alt.Color(field="Country", type="nominal", title='Country'),
        tooltip=['Country', 'Total Passengers'],
    ).add_selection(
        select_year
    ).transform_filter(
        select_year
    ).transform_filter(
        alt.FieldOneOfPredicate(field='Year', oneOf=[2016, 2017, 2018, 2019, 2020])
    ).add_selection(select_year).transform_filter(select_year).properties(
        title={
            "text": "  Number of Airport Passengers in 2016-2020",
            "fontSize": 18,
            "fontWeight": "bold",
            "anchor": "middle"
        }
    )

    # add the total number of passengers to the chart
    subtitle = alt.Chart(
        pd.DataFrame({'text': [f"All Passengers:{group_airport_year_df['Passengers'][0]}"]})).mark_text(
        size=10, align='center', font='Courier', fontWeight='lighter'
    ).encode(
        text=alt.Text('text:N')
    ).properties(
        width=180,
        height=300
    ).transform_calculate(
        angle='0'
    )

    # create a text chart with percentage values
    text_chart = \
        alt.Chart(group_airport_df).mark_text(radius=140, font='Courier New', fontSize=16, fontWeight='bold',
                                              align='center').encode(
            text=alt.Text("Percentage:Q", format=".1%"),
            theta=alt.Theta('Percentage:Q', stack=True),
            color=alt.Color(field="Country", type="nominal", title='Country'),
        ).transform_filter(
            select_year
        )

    return chart + text_chart + subtitle


alt.hconcat(
    chart(alt.selection_single()).properties(title='Single (Click)'),
    chart(alt.selection_multi()).properties(title='Multi (Shift-Click)'),
    chart(alt.selection_interval()).properties(title='Interval (Drag)')
)

# display the chart
pie_chart = chart(select_year)
pie_chart.configure_view(strokeWidth=0).configure_title(anchor='middle').show()
