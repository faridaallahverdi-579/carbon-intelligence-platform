import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Carbon Intelligence Platform", layout="wide")

st.title("🌍 Carbon Intelligence Platform")

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("owid-co2-data.csv")

df = df[["country","year","co2","iso_code"]].dropna()

# yalnız real ölkələr
df = df[df["iso_code"].str.len() == 3]

# =====================
# ANALYTICS
# =====================
st.header("📊 Global CO2 Analysis")

latest_year = df["year"].max()
latest_data = df[df["year"] == latest_year]

st.write(f"Latest data year: {latest_year}")

top = latest_data.sort_values("co2", ascending=False).head(10)

st.subheader("Top Emitters")
st.bar_chart(top.set_index("country")["co2"])

# =====================
# 🌍 MAP
# =====================
st.subheader("🌍 World Map")

fig = px.choropleth(
    latest_data,
    locations="iso_code",
    color="co2",
    hover_name="country",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig)

# =====================
# 📊 COUNTRY COMPARISON
# =====================
st.subheader("📊 Country Comparison")

countries = st.multiselect(
    "Select countries",
    df["country"].unique(),
    default=["Azerbaijan","Turkey"]
)

compare_df = df[df["country"].isin(countries)]

fig2 = px.line(compare_df, x="year", y="co2", color="country")
st.plotly_chart(fig2)

# =====================
# 🧮 SMART CALCULATOR
# =====================
st.header("🧮 Smart Carbon Calculator")

car_km = st.slider("🚗 Weekly car usage (km)", 0, 500)
flights = st.number_input("✈️ Flights per year", 0, 50)
electricity = st.slider("⚡ Monthly electricity (kWh)", 0, 1000)

coffee = st.slider("☕ Coffee per day", 0, 10)
elevator = st.slider("🛗 Elevator uses per day", 0, 50)
shower = st.slider("🚿 Shower minutes per day", 0, 60)

if st.button("Calculate"):

    carbon = (
        car_km * 0.12 +
        flights * 90 +
        electricity * 0.4 +
        coffee * 0.1 * 365 +
        elevator * 0.05 * 365 +
        shower * 0.2 * 365
    )

    st.success(f"🌍 Your annual carbon footprint: {carbon:.2f} kg CO₂")

    # RANGE
    if carbon < 2000:
        st.success("🟢 Normal level")
    elif carbon < 5000:
        st.warning("🟡 Moderate")
    else:
        st.error("🔴 High footprint")

    # 🌱 TREES
    trees = carbon / 22
    st.write(f"🌱 Trees needed to offset: {trees:.0f}")

    # 💰 COST
    cost = (carbon / 1000) * 50
    st.write(f"💰 Carbon cost: ${cost:.2f}")

    # 🎯 GOAL
    monthly = carbon / 12
    goal = st.slider("Monthly limit", 0, 500, 200)

    st.write(f"Monthly footprint: {monthly:.2f}")

    if monthly < goal:
        st.success("✅ Within goal")
    else:
        st.error("❌ Above goal")

    # 💡 INSIGHTS
    st.subheader("💡 Tips")

    if coffee > 3:
        st.write("☕ Reduce coffee consumption")

    if elevator > 10:
        st.write("🛗 Use stairs more")

    if shower > 20:
        st.write("🚿 Shorter showers recommended")

    if car_km > 200:
        st.write("🚗 Reduce car usage")