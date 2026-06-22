# 🚀 Snowflake Gold Dashboard (Streamlit App)

A modern **data analytics dashboard built with Streamlit and Snowflake**, designed to query, transform, and visualize country-level data from a Gold-layer table.

---

## 📌 Project Overview

This project is an end-to-end data application that connects to **Snowflake**, reads processed data from a Gold layer table, and displays insights in an interactive **Streamlit dashboard**.

It demonstrates:
- Cloud data warehouse integration (Snowflake)
- SQL-based analytics
- Python data processing
- Interactive web app development using Streamlit

---

## 🏗️ Architecture

Snowflake (Gold Layer Table)
↓
Snowpark / Snowflake Connector
↓
Python Backend (Pandas)
↓
Streamlit UI Dashboard 

## 📊 Features

- 🔗 Secure connection to Snowflake using credentials
- 📥 Fetch data from `GOLD.GOLD_COUNTRY_COMPARISON` table
- 🔍 Filter data by country or other attributes
- 📊 Interactive visualizations (tables, charts)
- ⚡ Real-time data refresh on rerun
- 🧩 Modular Python code structure

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Snowflake Snowpark / Connector**
- **Pandas**
- **SQL (Snowflake)**

---

## 📁 Project Structure
snowflake-gold-dashboard/
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── .streamlit/
│ └── secrets.toml # Snowflake credentials (NOT pushed to GitHub)
├── README.md # Project documentation


---

## ⚙️ Setup Instructions

### Clone the repository
```bash
git clone https://github.com/your-username/snowflake-gold-dashboard.git
cd snowflake-gold-dashboard
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
.streamlit/secrets.toml

Add
[snowflake]
account = "YOUR_ACCOUNT"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
role = "YOUR_ROLE"
warehouse = "YOUR_WAREHOUSE"
database = "YOUR_DATABASE"
schema = "YOUR_SCHEMA"

