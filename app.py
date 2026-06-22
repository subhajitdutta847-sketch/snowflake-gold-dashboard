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
import streamlit as st
import altair as alt

st.subheader("📊 GDP Per Capita (2010 vs 2015)")

gdp_df = filtered_df.set_index("COUNTRY_NAME")[["GDP_2010", "GDP_2015"]]

# Convert to long format (required for grouped bars)
gdp_long = gdp_df.reset_index().melt(
    id_vars="COUNTRY_NAME",
    var_name="Year",
    value_name="GDP"
)

base = alt.Chart(gdp_long)

bar = base.mark_bar().encode(
    x=alt.X("COUNTRY_NAME:N", title="Country"),
    xOffset="Year:N",   # grouped bars
    y=alt.Y("GDP:Q", title="GDP Per Capita"),
    color="Year:N"
)

# 🔥 Add text labels on top of bars
text = base.mark_text(
    dy=-5,
    color="black"
).encode(
    x=alt.X("COUNTRY_NAME:N"),
    xOffset="Year:N",
    y=alt.Y("GDP:Q"),
    text=alt.Text("GDP:Q", format=".0f")
)

chart = (bar + text).properties(width=700)

st.altair_chart(chart, use_container_width=True)
# -----------------------------
# CHART 2 - POPULATION (VERTICAL)
# -----------------------------
import streamlit as st
import altair as alt

st.subheader("👥 Population (2010 vs 2015)")

pop_df = filtered_df.set_index("COUNTRY_NAME")[["POPULATION_2010", "POPULATION_2015"]]

# Convert wide → long format
pop_long = pop_df.reset_index().melt(
    id_vars="COUNTRY_NAME",
    var_name="Year",
    value_name="Population"
)

base = alt.Chart(pop_long)

# Bars (grouped side-by-side)
bar = base.mark_bar().encode(
    x=alt.X("COUNTRY_NAME:N", title="Country"),
    xOffset="Year:N",
    y=alt.Y("Population:Q", title="Population"),
    color="Year:N"
)

# 🔥 Value labels on bars
text = base.mark_text(
    dy=-5,
    color="black"
).encode(
    x=alt.X("COUNTRY_NAME:N"),
    xOffset="Year:N",
    y=alt.Y("Population:Q"),
    text=alt.Text("Population:Q", format=",.0f")
)

chart = (bar + text).properties(width=700)

st.altair_chart(chart, use_container_width=True)
# -----------------------------
# DATA VIEW
# -----------------------------
st.subheader("📄 Data Table")
st.dataframe(filtered_df)
