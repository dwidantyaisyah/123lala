import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper functions
def create_daily_rides_df(df):
    daily_rides_df = df.resample(rule='D', on='dteday').agg({
        "instant": "count",
        "cnt": "sum"
    })
    daily_rides_df = daily_rides_df.reset_index()
    daily_rides_df.rename(columns={
        "instant": "ride_count",
        "cnt": "total_rides"
    }, inplace=True)
    
    return daily_rides_df

def create_weather_df(df):
    weather_df = df.groupby("weathersit").cnt.sum().reset_index()
    weather_df.rename(columns={"cnt": "total_rides"}, inplace=True)
    
    return weather_df

# Load data
bike_df = pd.read_csv('day.csv')

# Convert date column to datetime
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Sidebar filter
min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                      (bike_df["dteday"] <= str(end_date))]

# Dataframes for visualization
daily_rides_df = create_daily_rides_df(filtered_df)
weather_df = create_weather_df(filtered_df)

# Dashboard content
st.header('Bike Sharing Dashboard 🚴‍♂️')
st.subheader('Daily Rides Overview')

col1, col2 = st.columns(2)

with col1:
    total_rides = daily_rides_df.total_rides.sum()
    st.metric("Total Rides", value=total_rides)

with col2:
    total_days = daily_rides_df.ride_count.sum()
    st.metric("Total Days Recorded", value=total_days)

# Plot daily rides
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rides_df["dteday"],
    daily_rides_df["total_rides"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.set_title("Daily Rides", fontsize=20)
st.pyplot(fig)

# Weather impact on rides
st.subheader("Weather Impact on Rides")

fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(
    x="weathersit", 
    y="total_rides", 
    data=weather_df,
    palette="Blues_d", 
    ax=ax
)
ax.set_title("Total Rides by Weather Condition", fontsize=20)
ax.set_xlabel("Weather Situation", fontsize=15)
ax.set_ylabel("Total Rides", fontsize=15)
st.pyplot(fig)

st.caption('Copyright © Bike Sharing Analysis 2023')
