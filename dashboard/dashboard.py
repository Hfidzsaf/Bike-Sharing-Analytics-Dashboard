import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman dashboard
st.set_page_config(page_title="Bike Sharing Dashboard 🚲", layout="wide")

sns.set_theme(style='whitegrid')

# 1. Menyiapkan Helper Functions
def create_monthly_rent_df(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })
    monthly_rent_df.index = monthly_rent_df.index.strftime('%B %Y')
    monthly_rent_df = monthly_rent_df.reset_index()
    return monthly_rent_df

def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby(by="hr").cnt.mean().reset_index()
    return hourly_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by="weathersit").cnt.mean().reset_index()
    return weather_rent_df

# 2. Load Data
day_df = pd.read_csv("dashboard/main_data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df = pd.read_csv("data/hour.csv")

# 3. Sidebar (Tanpa Logo)
with st.sidebar:
    st.title("Filters 🛠️")
    
    # Filter Rentang Waktu
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter Cuaca (Multiselect)
    weather_options = day_df['weathersit'].unique()
    selected_weather = st.multiselect(
        'Select Weather Condition',
        options=weather_options,
        default=weather_options
    )

# Filter Dataframe utama
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date)) &
                 (day_df["weathersit"].isin(selected_weather))]

# 4. Judul Dashboard
st.title('🚲 Bike Sharing Analytics Dashboard')
st.markdown("Exploring trends and patterns in bike rental data.")

# 5. Menampilkan Metrics Utama
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    avg_rentals = round(main_df.cnt.mean(), 1)
    st.metric("Avg Rentals per Day", value=avg_rentals)

with col3:
    max_rentals = main_df.cnt.max()
    st.metric("Peak Day Records", value=f"{max_rentals:,}")
st.divider()

# 6. Visualisasi 1: Tren Bulanan
st.subheader('📈 Monthly Rentals Performance')
monthly_df = create_monthly_rent_df(main_df)
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(
    data=monthly_df, 
    x="dteday", 
    y="cnt", 
    marker='o', 
    linewidth=3, 
    color="#007BFF", 
    ax=ax
)
plt.xticks(rotation=45)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# 7. Visualisasi 2 & 3: Jam Puncak & Kondisi Cuaca
col_left, col_right = st.columns(2)

with col_left:
    st.subheader('🕒 Peak Hours')
    hourly_df = create_hourly_rent_df(hour_df)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="hr", 
        y="cnt", 
        data=hourly_df, 
        palette="Blues_r", 
        ax=ax
    )
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Avg Rentals")
    st.pyplot(fig)

with col_right:
    st.subheader('☁️ Impact of Weather')
    weather_df = create_weather_rent_df(main_df)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="weathersit", 
        y="cnt", 
        data=weather_df, 
        palette="coolwarm", 
        ax=ax
    )
    ax.set_xlabel("Weather Type")
    ax.set_ylabel("Avg Rentals")
    st.pyplot(fig)

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center;">
        <p>Copyright © 2026 - Hafidz Surya Afifi</p>
    </div>
    """, 
    unsafe_allow_html=True
)