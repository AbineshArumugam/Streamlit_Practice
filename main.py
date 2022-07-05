#Importing Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#Importing Datasets 
cases='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
cases_df=pd.read_csv(cases)
deaths_df=pd.read_csv(deaths)

#Un-pivoting the datasets
melt_cases_df = cases_df.melt(id_vars=['Country/Region','Province/State','Lat','Long'],var_name='Date',value_name='Cases')
melt_deaths_df=deaths_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name='Date',value_name='Deaths')
melt_cases_df['Date'] = pd.to_datetime(melt_cases_df['Date'])
melt_deaths_df['Date'] = pd.to_datetime(melt_deaths_df['Date'])

# Creating Sidebar
page=st.sidebar.radio('Select Page',['Info','Cases','Deaths'])
last_date=melt_cases_df['Date'].max()
selected_country  = st.sidebar.selectbox('Select Country', list(list(melt_cases_df['Country/Region'].unique())))
st.sidebar.write('Last Updated date:',last_date )

#Page Title
st.title('COVID-19 Dashboard')

#Info Page
if page == 'Info':

    st.header('COVID-19 (Coronavirus disease)')
    st.write(''' **Coronavirus disease (COVID-19)** is an infectious disease caused by the **SARS-CoV-2 virus**.
Most people who fall sick with COVID-19 will experience mild to moderate symptoms and recover without 
special treatment.However,some will become seriously ill and require medical attention.''')
    
    st.subheader('HOW IT SPREADS')
    st.write(
    ''' The virus can spread from an infected person’s mouth or nose in small liquid particles when they cough, sneeze, speak, sing or breathe.
    These particles range from larger respiratory droplets to smaller aerosols.
    You can be infected by breathing in the virus if you are near someone who has COVID-19, or by touching a contaminated surface and then your eyes, nose or mouth.
    The virus spreads more easily indoors and in crowded settings.''')
    st.markdown('**Most common symptoms:** Fever,Cough,Tiredness,Loss of Taste or Smell')

#Cases Page

if page=='Cases':
    st.header('Total Cases')
    st.markdown(int(melt_cases_df[melt_cases_df['Country/Region']==selected_country]['Cases'].max()))

    #New DataFrame with New cases
    new_cases_df=melt_cases_df[melt_cases_df['Country/Region']==selected_country]
    new_cases_df['New Cases']=new_cases_df['Cases'].diff()
    st.write('New Cases on:',last_date)
    st.markdown(int(new_cases_df['New Cases'].tail(1)))

    #Ploting line plot based on new cases
    cases_fig= px.line(new_cases_df,x ='Date',y = 'New Cases')
    cases_fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    st.plotly_chart(cases_fig)

#Deaths Page

if page=='Deaths':
    st.header('Total Deaths')
    st.markdown(int( melt_deaths_df[melt_deaths_df['Country/Region']==selected_country]['Deaths'].max()))

    #New DataFrame with New deaths
    new_deaths_df=melt_deaths_df[melt_deaths_df['Country/Region']==selected_country]
    new_deaths_df['New Deaths']=new_deaths_df['Deaths'].diff()
    st.write('New Deaths on:',last_date)
    st.markdown(int(new_deaths_df['New Deaths'].tail(1)))

    #Ploting line plot based on new cases
    deaths_fig= px.line(new_deaths_df,x ='Date',y = 'New Deaths')
    deaths_fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    st.plotly_chart(deaths_fig)