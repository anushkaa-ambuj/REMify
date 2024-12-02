import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Load data
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to process sleep stages from the ML model's predictions
def calculate_sleep_metrics(data):
    sleep_stages = data['Sleep Stage'].value_counts()
    total_sleep = data.shape[0] * 30  # assuming data collected every 30 seconds
    rem_duration = sleep_stages.get('REM', 0) * 30
    deep_duration = sleep_stages.get('Deep', 0) * 30
    light_duration = sleep_stages.get('Light', 0) * 30
    return total_sleep, rem_duration, deep_duration, light_duration

# App layout
st.title("REMify: Sleep Stage Monitoring Dashboard")

# 1. File upload
uploaded_file = st.file_uploader("Upload your sleep data CSV", type=["csv"])

if uploaded_file is not None:
    data = load_data(uploaded_file)
    
    # 2. Display basic data summary
    st.subheader("Data Preview")
    st.write(data.head())

    # 3. Show metrics
    st.subheader("Sleep Metrics Summary")
    total_sleep, rem_duration, deep_duration, light_duration = calculate_sleep_metrics(data)
    st.write(f"**Total Sleep Duration:** {total_sleep / 3600:.2f} hours")
    st.write(f"**REM Sleep Duration:** {rem_duration / 3600:.2f} hours")
    st.write(f"**Deep Sleep Duration:** {deep_duration / 3600:.2f} hours")
    st.write(f"**Light Sleep Duration:** {light_duration / 3600:.2f} hours")

    # 4. Plot Sleep Stages Over Time
    st.subheader("Sleep Stages Over Time")
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='Timestamp', y='Sleep Stage', data=data)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # 5. Heart Rate and Motion Trends
    st.subheader("Heart Rate and Motion Trends")

    # Heart rate (RED and IR from MAX30102)
    fig, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Timestamp', y='RED', data=data, label='Heart Rate (RED)', ax=ax1)
    sns.lineplot(x='Timestamp', y='IR', data=data, label='Heart Rate (IR)', ax=ax1)
    ax1.set_ylabel("Heart Rate")
    ax1.set_xlabel("Time")
    ax1.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Accelerometer and Gyroscope Data (MPU6050)
    fig, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 10))
    sns.lineplot(x='Timestamp', y='Ax', data=data, label='Acc X', ax=ax2)
    sns.lineplot(x='Timestamp', y='Ay', data=data, label='Acc Y', ax=ax2)
    sns.lineplot(x='Timestamp', y='Az', data=data, label='Acc Z', ax=ax2)
    ax2.set_ylabel("Accelerometer")
    ax2.legend()

    sns.lineplot(x='Timestamp', y='Gx', data=data, label='Gyro X', ax=ax3)
    sns.lineplot(x='Timestamp', y='Gy', data=data, label='Gyro Y', ax=ax3)
    sns.lineplot(x='Timestamp', y='Gz', data=data, label='Gyro Z', ax=ax3)
    ax3.set_ylabel("Gyroscope")
    ax3.set_xlabel("Time")
    ax3.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
