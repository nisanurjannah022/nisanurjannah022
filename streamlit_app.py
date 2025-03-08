import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile

# Mengatur halaman Streamlit
st.set_page_config(page_title='Bike Sharing Analysis', layout='wide')

# Data Wrangling
with zipfile.ZipFile('/mnt/data/Bike-sharing-dataset.zip', 'r') as z:
    z.extractall('/mnt/data/')

df = pd.read_csv('/mnt/data/hour.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

# Judul Dashboard
st.title('📊 Bike Sharing Analysis')
st.write('Analisis pengaruh musim dan suhu terhadap jumlah peminjaman sepeda.')

# Filter Interaktif
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_map)

selected_season = st.selectbox('Pilih Musim:', df['season_label'].unique())
filtered_df = df[df['season_label'] == selected_season]

min_temp, max_temp = st.slider('Pilih Rentang Suhu:', float(df['temp'].min()), float(df['temp'].max()), (float(df['temp'].min()), float(df['temp'].max())))
filtered_df = filtered_df[(filtered_df['temp'] >= min_temp) & (filtered_df['temp'] <= max_temp)]

# Visualisasi 1: Jumlah Peminjaman Berdasarkan Musim
st.subheader('Jumlah Peminjaman Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x='season_label', y='cnt', data=df, ci=None, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Musim')
st.pyplot(fig)

# Visualisasi 2: Hubungan Suhu dan Peminjaman
st.subheader('Hubungan antara Suhu dan Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(10,5))
sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=ax)
ax.set_xlabel('Suhu')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_title('Hubungan antara Suhu dan Jumlah Peminjaman')
st.pyplot(fig)

# Insight
st.write('## 🔍 Insight:')
st.write(f'- Jumlah peminjaman sepeda tertinggi terjadi di musim **{selected_season}**.')
st.write('- Peminjaman sepeda meningkat saat suhu lebih tinggi, tetapi ada titik tertentu di mana jumlah peminjaman mulai menurun meski suhu tinggi.')

# Conclusion
st.write('## ✅ Conclusion:')
st.write('- **Musim panas memiliki jumlah peminjaman tertinggi.**')
st.write('- **Ada hubungan positif antara suhu dan jumlah peminjaman, tetapi hanya sampai batas tertentu.**')
