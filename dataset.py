import pandas as pd
import numpy as np

# Emirates Dataset
np.random.seed(42)
num_flights = 1000
flight_numbers = [f"EK{np.random.randint(500, 8000)}" for _ in range(num_flights)]
dates = pd.date_range(start="2022-01-01", end="2023-12-31", periods=num_flights)
delays = np.random.normal(loc=15, scale=30, size=num_flights).clip(min=0).round().astype(int)
reasons = ['Weather', 'Mechanical Issue', 'Crew', 'Traffic Control', 'None']
delay_reasons = np.random.choice(reasons, size=num_flights, p=[0.3, 0.2, 0.1, 0.1, 0.3])

# Create DataFrame for Emirates
df_emirates = pd.DataFrame({
    'Flight Number': flight_numbers,
    'Date': dates,
    'Delay (Minutes)': delays,
    'Reason for Delay': delay_reasons
})

# Convert 'Date' to datetime format and handle any invalid entries
df_emirates['Date'] = pd.to_datetime(df_emirates['Date'], errors='coerce')

# Save Emirates dataset to CSV
df_emirates.to_csv('emirates_flight_delay_karachi.csv', index=False)

# PIA Dataset
flight_numbers = [f"PK{np.random.randint(100, 1000)}" for _ in range(num_flights)]
dates = pd.date_range(start="2022-01-01", end="2023-12-31", periods=num_flights)
delays = np.random.normal(loc=20, scale=35, size=num_flights).clip(min=0).round().astype(int)
delay_reasons = np.random.choice(reasons, size=num_flights, p=[0.35, 0.25, 0.1, 0.1, 0.2])

# Create DataFrame for PIA
df_pia = pd.DataFrame({
    'Flight Number': flight_numbers,
    'Date': dates,
    'Delay (Minutes)': delays,
    'Reason for Delay': delay_reasons
})

# Convert 'Date' to datetime format and handle any invalid entries
df_pia['Date'] = pd.to_datetime(df_pia['Date'], errors='coerce')

# Save PIA dataset to CSV
df_pia.to_csv('pia_flight_delay_karachi.csv', index=False)
