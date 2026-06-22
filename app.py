import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Gold Dashboard", layout="wide")

st.title("🌍 Country Economic Dashboard (2010 vs 2015)")
st.write("Live data from Snowflake GOLD layer")

# -----------------------------
# SNOWFLAKE CONNECTION
# -----------------------------
connection_parameters = {
    "account": "RMBNDYR-MI13930",
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "FINAL_PROJECT",
    "schema": "GOLD"
}

try:
    session = Session.builder.configs(connection_parameters).create()
    st.success("Connected successfully")
except Exception as e:
    st.exception(e)
    st.stop()

# -----------------------------
# LOAD DATA (AUTO REFRESH)
# -----------------------------
df = session.sql("SELECT * FROM GOLD_COUNTRY_COMPARISON").to_pandas()

# -----------------------------
# FILTERS (OPTIONAL)
# -----------------------------
countries = df["COUNTRY_NAME"].unique()

selected = st.multiselect(
    "Select Countries",
    countries,
    default=list(countries)
)

filtered_df = df[df["COUNTRY_NAME"].isin(selected)]

# -----------------------------
# CHART 1 - GDP (HORIZONTAL STYLE)
# -----------------------------
st.subheader("📊 GDP Per Capita (2010 vs 2015)")

gdp_df = filtered_df.set_index("COUNTRY_NAME")[["GDP_2010", "GDP_2015"]]

# Convert wide format → long format (better for grouped bars)
gdp_long = gdp_df.reset_index().melt(
    id_vars="COUNTRY_NAME",
    var_name="Year",
    value_name="GDP"
)

import altair as alt

chart = alt.Chart(gdp_long).mark_bar().encode(
    x=alt.X("COUNTRY_NAME:N", title="Country"),
    xOffset="Year:N",   # 👈 THIS creates side-by-side bars
    y=alt.Y("GDP:Q", title="GDP Per Capita"),
    color="Year:N"
).properties(
    width=600
)

st.altair_chart(chart, use_container_width=True)
# -----------------------------
# CHART 2 - POPULATION (VERTICAL)
# -----------------------------
st.subheader("👥 Population (2010 vs 2015)")

pop_df = filtered_df.set_index("COUNTRY_NAME")[["POPULATION_2010", "POPULATION_2015"]]

st.bar_chart(pop_df)

# -----------------------------
# DATA VIEW
# -----------------------------
st.subheader("📄 Data Table")
st.dataframe(filtered_df)
