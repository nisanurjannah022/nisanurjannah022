import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    all_data = pd.read_csv("main_data.csv", parse_dates=["dteday"])
    return all_data

# Load dataset
all_data = load_data()

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", value=all_data["dteday"].min())
end_date = st.sidebar.date_input("End Date", value=all_data["dteday"].max())

# Filter berdasarkan tanggal
try:
    filtered_data = all_data[(all_data["dteday"] >= pd.to_datetime(start_date)) & (all_data["dteday"] <= pd.to_datetime(end_date))]
except Exception as e:
    st.warning("Tanggal tidak valid, menampilkan semua data.")
    filtered_data = all_data

# Pengaruh Musim terhadap Peminjaman Sepeda
season_rentals = filtered_data.groupby("season")["cnt_day"].mean()
max_index = season_rentals.idxmax()
colors = ["#b6bdd8"] * len(season_rentals)
colors[max_index - 1] = "#565a6b"

st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(["Spring", "Summer", "Fall", "Winter"], season_rentals, color=colors)
ax.set_xlabel("Season")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda")
st.pyplot(fig)

# Tren Peminjaman Sepeda Berdasarkan Bulan
monthly_rentals = filtered_data.groupby("mnth")["cnt_day"].sum().reset_index()

st.subheader("Tren Peminjaman Sepeda Berdasarkan Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="mnth", y="cnt_day", data=monthly_rentals, marker="o", color="#1f77b4", linewidth=2, ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Tren Peminjaman Sepeda Berdasarkan Bulan", fontsize=14)
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)