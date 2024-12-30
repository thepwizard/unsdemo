import streamlit as st
import pymongo
import pandas as pd
import time

# MongoDB Configuration
MONGO_URI = "mongodb://admin:password@mongodb:27017"
DB_NAME = "unified_namespace"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# Streamlit UI
st.set_page_config(page_title="Unified Namespace Dashboard", layout="wide")
st.title("Unified Namespace Dashboard")
st.write("Real-time insights powered by Unified Namespace (UNS) to enable better decision-making across the organization.")

# Commentary Section
st.subheader("Unified Namespace Commentary")
st.write("""
The Unified Namespace (UNS) integrates real-time data across the organization, providing a single source of truth for decision-making. 
- **Machine Uptime**: Tracks operational efficiency to reduce downtime and optimize production.
- **Breakdown Events**: Identifies critical issues affecting output and allows for proactive maintenance.
- **Inventory Management**: Ensures raw materials are sufficiently stocked to avoid production delays.
- **Order Status**: Provides visibility into production flow and order completion rates.
- **Sensor Data**: Monitors environmental conditions (temperature, pressure) to ensure process stability.

By leveraging UNS, organizations can eliminate data silos, enabling faster response times, improved productivity, and reduced costs.
""")

# Function to Fetch Data from MongoDB
def get_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    if data:
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df
    return pd.DataFrame()

# Layout with Columns
col1, col2 = st.columns(2)

# KPI: Machine Uptime
with col1:
    st.subheader("Key Performance Indicators (KPIs)")
    machine_status_data = get_data("machine_status")
    if not machine_status_data.empty and "status" in machine_status_data.columns:
        total_machines = len(machine_status_data)
        operational_count = machine_status_data[machine_status_data["status"] == "running"].shape[0]
        uptime_percentage = (operational_count / total_machines * 100) if total_machines > 0 else 0
        st.metric("Machine Uptime (%)", f"{uptime_percentage:.2f}%")
    else:
        st.metric("Machine Uptime (%)", "No Data")

    # KPI: Breakdown Events
    breakdown_count = machine_status_data[machine_status_data["status"] == "breakdown"].shape[0] if not machine_status_data.empty else 0
    st.metric("Breakdown Events", breakdown_count)

    # KPI: Orders Pending
    orders_data = get_data("orders")
    pending_orders = orders_data[orders_data["status"] == "pending"].shape[0] if not orders_data.empty else 0
    st.metric("Pending Orders", pending_orders)

# KPI: Real-Time Inventory
with col2:
    inventory_data = get_data("raw_materials")
    if not inventory_data.empty:
        total_inventory = inventory_data["quantity"].sum()
        st.metric("Total Inventory (kg)", total_inventory)
    else:
        st.metric("Total Inventory (kg)", "No Data")

# Row for Graph Visualizations
st.subheader("Real-Time Data Trends")

# Temperature and Pressure Graphs
col3, col4 = st.columns(2)

with col3:
    st.write("**Temperature Trends**")
    temperature_data = get_data("temperature")
    if not temperature_data.empty:
        st.line_chart(temperature_data.set_index("timestamp")["value"], use_container_width=True)
    else:
        st.write("No temperature data available.")

with col4:
    st.write("**Pressure Trends**")
    pressure_data = get_data("pressure")
    if not pressure_data.empty:
        st.line_chart(pressure_data.set_index("timestamp")["value"], use_container_width=True)
    else:
        st.write("No pressure data available.")

# Inventory and Orders Graphs
col5, col6 = st.columns(2)

with col5:
    st.write("**Inventory Levels Over Time**")
    if not inventory_data.empty:
        st.bar_chart(inventory_data.set_index("timestamp")["quantity"], use_container_width=True)
    else:
        st.write("No inventory data available.")

with col6:
    st.write("**Order Status Distribution**")
    if not orders_data.empty:
        order_status_counts = orders_data["status"].value_counts()
        st.bar_chart(order_status_counts, use_container_width=True)
    else:
        st.write("No order data available.")

# Additional Detailed Tables

# Create Columns for Displaying Tables Side by Side
col7, col8 = st.columns(2)

# Machine Status Table
with col7:
    st.subheader("Machine Status Table")
    if not machine_status_data.empty:
        st.dataframe(machine_status_data[['timestamp', 'machine_id', 'status']].sort_values(by="timestamp", ascending=False))
    else:
        st.write("No machine status data available.")

# Orders Table
with col8:
    st.subheader("Orders Table")
    if not orders_data.empty:
        st.dataframe(orders_data[['timestamp', 'order_id', 'product', 'quantity', 'status']].sort_values(by="timestamp", ascending=False))
    else:
        st.write("No order data available.")

# Create New Row for Inventory Levels Table and Sensor Data Tables
col9, col10 = st.columns(2)

# Inventory Levels Table
with col9:
    st.subheader("Inventory Levels Table")
    if not inventory_data.empty:
        st.dataframe(inventory_data[['timestamp', 'material_id', 'quantity']].sort_values(by="timestamp", ascending=False))
    else:
        st.write("No inventory data available.")

# Temperature Data Table
with col10:
    st.subheader("Temperature Data Table")
    if not temperature_data.empty:
        st.dataframe(temperature_data[['timestamp', 'sensor_id', 'value']].sort_values(by="timestamp", ascending=False))
    else:
        st.write("No temperature data available.")

# Create Another Row for Pressure Data Table
col11, col12 = st.columns(2)

# Pressure Data Table
with col11:
    st.subheader("Pressure Data Table")
    if not pressure_data.empty:
        st.dataframe(pressure_data[['timestamp', 'sensor_id', 'value']].sort_values(by="timestamp", ascending=False))
    else:
        st.write("No pressure data available.")
