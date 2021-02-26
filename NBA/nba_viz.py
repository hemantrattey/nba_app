import streamlit as st 
import pandas as pd 
import numpy as np 
import base64

st.title('NBA Player Stats')
st.markdown(""" 
This app scrapes the [basketball-reference](https://www.basketball-reference.com/) website and gives you the stats of players. 

The main libraries needed are ***pandas*** and ***base64*** (for encoding csv file)""")

st.sidebar.header('Select Input')
year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2022))))

#Now time for web scraping. All the data will be downloaded on real time and nothing will be stored on the server.


@st.cache
def load_data(year):
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html'
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis = 1)
    return playerstats

playerstats = load_data(year)

# Select Team
sorted_unique_teams = sorted(playerstats['Tm'].unique())
team = st.sidebar.multiselect('Team', sorted_unique_teams, sorted_unique_teams)

# Select Position
unique_pos = list(playerstats['Pos'].unique())
position = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering Data

df_selected_team = playerstats[(playerstats['Tm'].isin(team) & (playerstats['Pos'].isin(position)))]
st.write('Data shape : ' + str(df_selected_team.shape))
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html = True)