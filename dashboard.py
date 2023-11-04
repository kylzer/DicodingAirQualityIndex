# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load CSV
all_df = pd.read_csv('main_data.csv', index_col=0)

# Seaborn Themes
sns.set(style='white')

# Time
min_date = pd.to_datetime(pd.to_datetime(all_df["date"].min()).strftime("%Y-%m-%d"))
max_date = pd.to_datetime(pd.to_datetime(all_df["date"].max()).strftime("%Y-%m-%d"))

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Dataset by Date
main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

# Header
st.header('Beijing Air Quality Condition')
st.subheader("Best & Worst Carbon Monoxide by Station")

# Carbon Monoxide by Station
station_list = main_df['station'].unique().tolist()
temp_dict = {}
for station in station_list:
    temp_station = main_df[(main_df["station"] == station)]
    temp_dict[station] = temp_station['CO'].mean()

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

tempHighest = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)[:6])
tempLowest = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=False)[:6])


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(55, 15))

plt.subplot(1,2,1)
sns.barplot(x=tempHighest.values(), y=tempHighest.keys(), orient='h', palette=colors, hue=tempHighest.keys())
ax[0].set_xlabel("Carbon Monoxide Value", fontsize=30)
ax[0].set_title("Highest Carbon Monoxide Station", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

plt.subplot(1,2,2)
sns.barplot(x=tempLowest.values(), y=tempLowest.keys(), orient='h', palette=colors, hue=tempLowest.keys())
ax[1].set_xlabel("Carbon Monoxide Value", fontsize=30)
ax[1].set_title("Lowest Carbon Monoxide Station", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Correlation Every Columns/Attribute
st.subheader("Correlation Every Attribute/Features")

fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(main_df.corr(numeric_only='True'), annot=True, fmt=".1f")
st.pyplot(fig)

# Comparison PM2.5 and PM10 Over Year
if((int(end_date.strftime("%Y")) - int(start_date.strftime("%Y"))) != 0):
    st.subheader("Comparison PM2.5 and PM10 Over Year")

    fig, ax = plt.subplots(figsize=(15, 10))

    plt.plot(main_df['PM2.5'].groupby(pd.to_datetime(main_df['date']).dt.year).mean(), label='PM2.5') 
    plt.plot(main_df['PM10'].groupby(pd.to_datetime(main_df['date']).dt.year).mean(), label='PM10') 

    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.xticks(pd.to_datetime(main_df['date']).dt.year.unique().tolist(), rotation=25)
    st.pyplot(fig)
else:
    st.subheader("Comparison PM2.5 and PM10 Over Year (Only Show if Year Range Not Zero)")

# AQI Status Count
st.subheader("AQI Status Count")

tempGroup = main_df.groupby(['AQI', 'station'], as_index = False)['AQI'].value_counts()
tempList = tempGroup['AQI'].unique().tolist()

fig, ax = plt.subplots(3, 2, figsize=(40, 40))
for i, p in enumerate(tempList):
    plt.subplot(3, 2, i+1)
    plt.title(p, loc="center", fontsize=30)
    tempDF = tempGroup[tempGroup['AQI'] == p]
    sns.barplot(tempDF, x="station", y="count", order=tempDF.sort_values('count').station, palette = sns.color_palette("mako", 12))
    plt.xlabel('Station', fontsize=26)
    plt.ylabel('Counts', fontsize=26)
    plt.xticks(rotation=26, fontsize=26)
    plt.yticks(fontsize=26)

fig.tight_layout(h_pad=5, w_pad=5)
st.pyplot(fig)