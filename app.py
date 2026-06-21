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
    "account": "MU09414",
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "FINAL_PROJECT",
    "schema": "GOLD"
}

session = Session.builder.configs(connection_parameters).create()

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

st.bar_chart(gdp_df)

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
