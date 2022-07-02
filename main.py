import streamlit as st
import pandas as pd
import plotly.express as px

temp_val = 0
def dailyCaseClac(x):
    global temp_val
    currentVal = x - temp_val
    temp_val = x
    return int(currentVal)

covid = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
df = pd.read_csv(covid)
melt_df = df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])
melt_df.rename(columns={'variable':'Date','value':'Total_cases'},inplace=True)

#death ='https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
#recover ='https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'



country_list = list(melt_df['Country/Region'].unique())
state_list = list(melt_df['Province/State'].unique())

page_value  = st.sidebar.radio('Select Page', ['Basic Info','Last 5 Days','New Cases','Total Cases','Recoveries','Deaths'])


st.title('COVID-19')

if page_value == 'Basic Info':

    st.header('COVID-19 (Coronavirus disease)')
    st.write(''' **Coronavirus disease (COVID-19)** is an infectious disease caused by the **SARS-CoV-2 virus**.
Most people who fall sick with COVID-19 will experience mild to moderate symptoms and recover without 
special treatment.However,some will become seriously ill and require medical attention.''')
    
    st.subheader('HOW IT SPREADS')
    st.write(
    ''' The virus can spread from an infected person’s mouth or nose in small liquid particles when they cough, sneeze, speak, sing or breathe.
    These particles range from larger respiratory droplets to smaller aerosols.
    You can be infected by breathing in the virus if you are near someone who has COVID-19, or by touching a contaminated surface and then your eyes, nose or mouth.
    The virus spreads more easily indoors and in crowded settings.'''
)
    st.markdown('**Most common symptoms:** Fever,Cough,Tiredness,Loss of Taste or Smell')

if page_value=='Last 5 Days':
    selectedcountry  = st.sidebar.selectbox('Select Country', country_list)
    selectedstate  = st.sidebar.selectbox('Select State', state_list)
    st.header('Country wise Last 5 days')
    a=df.iloc[:,:2]
    b=df.iloc[:,-5:]
    c=pd.concat([a,b],1)
    d=c[(c['Country/Region']==selectedcountry) | (c['Province/State']==selectedstate)]

    st.table(d)

if page_value == 'New Cases':
    
    selectedcountry  = st.sidebar.selectbox('Select Country', country_list)
    t=st.sidebar.number_input('Pick Last Days',7,900,step=7)
    rec_df=melt_df[melt_df['Country/Region'] == selectedcountry].tail(t)
    rec_df['New_Cases'] = melt_df[melt_df['Country/Region'] == selectedcountry]['Total_cases'].apply(lambda x: int(dailyCaseClac(x)))
    rec_df.drop(['Lat','Long'],1,inplace=True)
    st.header('New Cases')
    fig=px.line(rec_df,x='Date',y='New_Cases')
    st.dataframe(rec_df)
    st.plotly_chart(fig)

if page_value=='Total Cases':
    selectedcountry  = st.sidebar.selectbox('Select Country', country_list)
    rec_df=melt_df[melt_df['Country/Region'] == selectedcountry]
    rec_df['New_Cases'] = melt_df[melt_df['Country/Region'] == selectedcountry]['Total_cases'].apply(lambda x: int(dailyCaseClac(x)))
    rec_df.drop(['Lat','Long'],1,inplace=True)
    st.header('Total Cases')
    fig=px.line(rec_df,x='Date',y='New_Cases')
    st.header('Total Cases')
    st.plotly_chart(fig)


    

    


    
    
    


