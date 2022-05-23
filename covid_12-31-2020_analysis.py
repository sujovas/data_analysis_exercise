import pandas as pd
import plotly.express as px
import plotly.io as pio

# it is possible to easily change .csv date from github database to view results for different time
covid_data = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/12-31-2020.csv')

# numbers of confirmed, deaths, recovered and active cases
covid_data['Active'] = covid_data['Confirmed'] - covid_data['Deaths'] - covid_data['Recovered']
cases = covid_data.groupby('Country_Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
print('')
print(cases)

# latest number of deaths and recovered people
data = covid_data.groupby(['Country_Region', 'Province_State'])['Confirmed', 'Deaths', 'Recovered'].max()
pd.set_option('display.max_rows', None)
print('')
print(data)

# data for Chinese provinces
c_data = covid_data[covid_data['Country_Region'] == 'China']
c_data = c_data[['Province_State', 'Confirmed', 'Deaths', 'Recovered']]
c_result = c_data.sort_values(by='Confirmed', ascending=False)
c_result = c_result.reset_index(drop=True)
print('')
print('Chinese province data')
print(c_result)

# death cases
data = covid_data.groupby('Country_Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
d_result = data[data['Deaths'] > 0][['Country_Region', 'Deaths']]
print('')
print(d_result)

# countries with no cases
data = covid_data.groupby('Country_Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
no_c_result = data[data['Confirmed'] == 0]['Country_Region']
print('')
print('Countries with no cases')
print(no_c_result)

# all cases died
data = covid_data.groupby('Country_Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
result = data[data['Confirmed'] == data['Deaths']]
result = result[['Country_Region', 'Confirmed', 'Deaths']]
result = result.sort_values('Confirmed', ascending=False)
result = result[result['Confirmed'] > 0]
result = result.reset_index(drop=True)
print('')
print('Countries where all cases died')
print(result)

# all cases recovered
data = covid_data.groupby('Country_Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
result = data[data['Confirmed'] == data['Recovered']]
result = result[['Country_Region', 'Confirmed', 'Recovered']]
result = result.sort_values('Confirmed', ascending=False)
result = result[result['Confirmed'] > 0]
result = result.reset_index(drop=True)
print('')
print('Countries where all cases recovered')
print(result)

# top 10 countries
result = covid_data.groupby('Country_Region')['Last_Update', 'Confirmed', 'Deaths', 'Recovered'].max().sort_values(
    by='Confirmed', ascending=False)[:10]
pd.set_option('display.max_column', None)
print('')
print('Top 10 countries in confirmed cases')
print(result)


#province wise death cases in India plot
in_data = covid_data[covid_data['Country_Region'] == 'India'].drop(['Country_Region', 'Lat', 'Long_'], axis=1)
in_data = in_data[in_data.sum(axis=1) > 0]
in_data = in_data.groupby(['Province_State'])['Deaths'].sum().reset_index()
in_data_death = in_data[in_data['Deaths'] > 0]
state_fig = px.bar(in_data_death, x='Province_State', y='Deaths',
                   title='State wise deaths reported of COVID-19 in India in 2020', text='Deaths')
state_fig.show()


#active cases in USA plot
covid_data['Active'] = covid_data['Confirmed'] - covid_data['Deaths'] - covid_data['Recovered']
us_data = covid_data[covid_data['Country_Region'] == 'US'].drop(['Country_Region', 'Lat', 'Long_'], axis=1)
us_data = us_data[us_data.sum(axis=1) > 0]

us_data = us_data.groupby(['Province_State'])['Active'].sum().reset_index()
us_data_death = us_data[us_data['Active'] > 0]
state_fig = px.bar(us_data_death, x='Province_State', y='Active', title='State wise recovery cases of COVID-19 in USA',
                   text='Active')
state_fig.show()

#combined data for Japan plot
covid_data['Active'] = covid_data['Confirmed'] - covid_data['Deaths'] - covid_data['Recovered']
combine_jap_data = covid_data[covid_data['Country_Region']=='Japan'].drop(['Country_Region','Lat', 'Long_'], axis=1)
combine_jap_data = combine_jap_data[combine_jap_data.sum(axis = 1) > 0]
combine_jap_data = combine_jap_data.groupby(['Province_State'])['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
combine_jap_data = pd.melt(combine_jap_data, id_vars='Province_State', value_vars=['Confirmed', 'Deaths', 'Recovered', 'Active'], value_name='Count', var_name='Case')
fig = px.bar(combine_jap_data, x='Province_State', y='Count', text='Count', barmode='group', color='Case', title='Japan province wise combine number of confirmed, deaths, recovered, active COVID-19 cases')
fig.show()

