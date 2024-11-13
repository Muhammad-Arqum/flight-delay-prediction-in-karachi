# Run command
# python -m streamlit run frontend.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Load both datasets
df_emirates = pd.read_csv('emirates_flight_delay_karachi.csv')
df_pia = pd.read_csv('pia_flight_delay_karachi.csv')

# Set up Streamlit app
st.set_page_config(page_title="Flight Delay Prediction - Karachi", layout="wide")

# Title of the app
st.title("Flight Delay Prediction in Karachi (2022-2023)")

# Sidebar options for user-friendly navigation
st.sidebar.header("Filter Options")

# Airline selection dropdown
airline = st.sidebar.selectbox("Select Airline", options=["Emirates", "PIA"])

# Year selection dropdown
year = st.sidebar.selectbox("Select Year", options=[2022, 2023])

# Load the appropriate dataset based on the user's airline selection
if airline == "Emirates":
    filtered_df = df_emirates[df_emirates['Date'].str.contains(str(year))]
else:
    filtered_df = df_pia[df_pia['Date'].str.contains(str(year))]

# Graph 1: Delay Distribution
st.subheader(f"{airline} Flight Delay Distribution in {year}")
delay_fig = px.histogram(
    filtered_df, 
    x='Delay (Minutes)', 
    nbins=30, 
    title=f"Distribution of Flight Delays ({airline})",
    labels={'Delay (Minutes)': 'Delay Duration (Minutes)'},
    color_discrete_sequence=['#FFAE42'] if airline == "Emirates" else ['#1f77b4']
)
st.plotly_chart(delay_fig, use_container_width=True)

# Graph 2: Delay Reasons
st.subheader(f"Reasons for {airline} Flight Delays in {year}")
delay_reason_fig = px.pie(
    filtered_df[filtered_df['Reason for Delay'] != 'None'], 
    names='Reason for Delay', 
    title=f"Reasons for Delays ({airline})",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(delay_reason_fig, use_container_width=True)

# Additional user interaction: Display raw data if user selects it
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader(f"{airline} Flight Delay Data")
    st.dataframe(filtered_df)

# New section for Past Delay Analysis
st.sidebar.header("Past Delay Analysis Options")
if st.sidebar.checkbox("Show Past Delay Analysis"):
    st.subheader(f"Past Delay Analysis for {airline} (2022-2023)")
    
    # Load the combined past experience dataset
    df_past_analysis = pd.concat([df_emirates, df_pia])

    # Create a pivot table or similar analysis
    analysis = df_past_analysis.groupby(['Reason for Delay']).agg(
        Average_Delay=('Delay (Minutes)', 'mean'),
        Total_Flights=('Flight Number', 'count')
    ).reset_index()

    # Display analysis
    st.dataframe(analysis)

    # Predict future delays (simple average prediction based on past data)
    st.subheader("Future Delay Predictions (Estimated Average)")
    future_predictions = analysis[['Reason for Delay', 'Average_Delay']]
    future_predictions['Future Prediction'] = future_predictions['Average_Delay']  # Basic prediction based on average
    st.dataframe(future_predictions)

# New section: Future Delay Prediction with Additional Features
st.sidebar.header("Future Delay Analysis with Additional Features")

if st.sidebar.checkbox("Show Future Delay Analysis"):
    st.subheader("Enhanced Future Delay Analysis")

    # Trend Analysis Line Chart
    st.subheader(f"{airline} Monthly Delay Trend Analysis in {year}")
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_trend = filtered_df.groupby('Month').agg(Average_Delay=('Delay (Minutes)', 'mean')).reset_index()
    trend_fig = px.line(
        monthly_trend, 
        x='Month', 
        y='Average_Delay', 
        title=f"{airline} Monthly Delay Trend in {year}",
        labels={'Average_Delay': 'Average Delay (Minutes)', 'Month': 'Month'},
        color_discrete_sequence=['#FF6347']
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    # Moving Average Prediction
    st.subheader(f"{airline} Moving Average Delay Prediction in {year}")
    filtered_df['3-Month Moving Average'] = filtered_df['Delay (Minutes)'].rolling(window=3).mean()
    moving_avg_fig = px.line(
        filtered_df, 
        x='Date', 
        y='3-Month Moving Average', 
        title=f"{airline} 3-Month Moving Average Delay Prediction",
        labels={'3-Month Moving Average': '3-Month Average Delay (Minutes)', 'Date': 'Date'},
        color_discrete_sequence=['#4682B4']
    )
    st.plotly_chart(moving_avg_fig, use_container_width=True)

    # Future Prediction Simulation
    st.subheader(f"Simulated Future Delay Prediction for {airline}")
    future_dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
    future_delays = np.random.normal(loc=filtered_df['Delay (Minutes)'].mean(), scale=10, size=12)
    future_data = pd.DataFrame({'Date': future_dates, 'Predicted Delay': future_delays})
    
    prediction_fig = px.line(
        future_data, 
        x='Date', 
        y='Predicted Delay', 
        title="Future Delay Prediction Simulation (2024)",
        labels={'Predicted Delay': 'Predicted Delay (Minutes)', 'Date': 'Month'},
        color_discrete_sequence=['#FFA500']
    )
    st.plotly_chart(prediction_fig, use_container_width=True)

# Footer
st.sidebar.text("Powered by Streamlit & Plotly")