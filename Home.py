import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# -------------------------------------------------------------------
# Page Config
# -------------------------------------------------------------------
st.set_page_config(page_title="Global Cybersecurity Threats (2015-2024)", layout="wide")

st.title("🔐 Global Cybersecurity Threat Analysis")
st.markdown("""
This app performs an exploratory data analysis (EDA) on a real-world cybersecurity dataset.
It explores cyber attack trends and patterns across countries, industries, financial losses,
attack sources, vulnerabilities, and defense mechanisms.
""")

# -------------------------------------------------------------------
# Load Dataset
# -------------------------------------------------------------------
st.sidebar.header("📂 Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Global_Cybersecurity_Threats.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload the 'Global_Cybersecurity_Threats.csv' file to continue.")
    st.stop()

# -------------------------------------------------------------------
# Data Preview
# -------------------------------------------------------------------
st.header("1. Dataset Preview")
st.dataframe(df)

col1, col2 = st.columns(2)
with col1:
    st.subheader("First 45 Rows")
    st.dataframe(df.head(45))
with col2:
    st.subheader("Last 50 Rows")
    st.dataframe(df.tail(50))

# -------------------------------------------------------------------
# Data Exploration
# -------------------------------------------------------------------
st.header("2. Data Exploration")

with st.expander("Dataset Info"):
    buffer = []
    df.info(buf=None)  # info() prints to stdout, so we build our own summary
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum().values,
        "Dtype": df.dtypes.values
    })
    st.dataframe(info_df)

with st.expander("Statistical Summary (describe)"):
    st.dataframe(df.describe(include="all"))

with st.expander("Missing Values Check"):
    st.write("Number of missing values per column:")
    st.dataframe(df.isnull().sum())
    if df.isnull().sum().sum() == 0:
        st.success("No missing values found in the dataset.")
    else:
        st.error("Missing values detected in the dataset.")

# -------------------------------------------------------------------
# Unique Values
# -------------------------------------------------------------------
st.header("3. Unique Values in Key Columns")

unique_cols = [
    "Country", "Year", "Attack Type", "Target Industry",
    "Financial Loss (in Million $)", "Number of Affected Users",
    "Attack Source", "Security Vulnerability Type",
    "Defense Mechanism Used", "Incident Resolution Time (in Hours)"
]

selected_col = st.selectbox("Select a column to view unique values", unique_cols)
if selected_col in df.columns:
    st.write(df[selected_col].unique())
else:
    st.info(f"Column '{selected_col}' not found in the uploaded dataset.")

# -------------------------------------------------------------------
# EDA Visualizations
# -------------------------------------------------------------------
st.header("4. Exploratory Data Analysis (EDA)")

# --- Line Chart: Country vs Year ---
st.subheader("📈 Country vs Year")
if "Country" in df.columns and "Year" in df.columns:
    fig1 = px.line(df, x="Country", y="Year", color="Country",
                    title="Country and Year")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Shows cyber attack records across different countries and years. "
               "Each colored line represents a country, helping compare attack "
               "distribution among countries.")

# --- Box Chart: Attack Type vs Country ---
st.subheader("📦 Attack Type vs Country")
if "Attack Type" in df.columns and "Country" in df.columns:
    fig2 = px.box(df, x="Attack Type", y="Country", color="Attack Type",
                   title="Cyber Attack According to Country")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Compares attack types across different countries, "
               "highlighting variation and unusual observations.")

# --- Pie Chart: Target Industry ---
st.subheader("🥧 Industries Targeted by Hackers")
if "Target Industry" in df.columns:
    count = df["Target Industry"].value_counts().reset_index()
    count.columns = ["Target Industry", "count"]
    fig3 = px.pie(count, names="Target Industry", values="count",
                   title="Industries Targeted by Hackers")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Shows the percentage of attacks on each industry. "
               "Larger slices indicate industries targeted more frequently.")

# --- Bar Chart: Target Industry vs Financial Loss ---
st.subheader("💰 Financial Loss by Industry")
if "Target Industry" in df.columns and "Financial Loss (in Million $)" in df.columns:
    fig4 = px.bar(df, x="Target Industry", y="Financial Loss (in Million $)",
                   color="Target Industry", title="Financial Loss Over Industries")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Compares financial losses among industries. "
               "Taller bars indicate higher financial losses.")

# --- Box Chart: Attack Source vs Affected Users ---
st.subheader("👥 Attack Source vs Affected Users")
if "Attack Source" in df.columns and "Number of Affected Users" in df.columns:
    sample_df = df.head(2000)
    fig5 = px.box(sample_df, x="Attack Source", y="Number of Affected Users",
                   color="Attack Source", title="Attack Source over No. of Affected Users")
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("Shows the relationship between attack source and number of "
               "affected users, useful for understanding user impact by source.")

# --- Violin Chart: Security Vulnerability vs Defense Mechanism ---
st.subheader("🎻 Defense Mechanism vs Security Vulnerability")
if "Defense Mechanism Used" in df.columns and "Security Vulnerability Type" in df.columns:
    fig6 = px.violin(df, y="Defense Mechanism Used", x="Security Vulnerability Type",
                       color="Security Vulnerability Type",
                       title="Defense Mechanism Used over Security Vulnerability")
    st.plotly_chart(fig6, use_container_width=True)
    st.caption("Shows how different defense mechanisms are associated with "
               "different types of security vulnerabilities.")

# --- Seaborn Line Plot: Incident Resolution Time ---
st.subheader("⏱️ Incident Resolution Time by Vulnerability Type")
if "Incident Resolution Time (in Hours)" in df.columns and "Security Vulnerability Type" in df.columns:
    fig7, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, y="Incident Resolution Time (in Hours)",
                 x="Security Vulnerability Type", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig7)
    st.caption("Shows how long it takes to resolve incidents for different "
               "vulnerability types. Higher points indicate longer resolution times.")

# -------------------------------------------------------------------
# Conclusion
# -------------------------------------------------------------------
st.header("5. Overall Project Conclusion")
st.markdown("""
This project analyzes a global cybersecurity threats dataset to understand cyber attack
patterns across different countries and industries. It examines attack types, financial
losses, affected users, attack sources, security vulnerabilities, defense mechanisms, and
incident resolution times. Using statistical analysis and visualizations such as line charts,
box plots, pie charts, bar charts, and violin plots, the project identifies the most targeted
industries, the attacks causing the highest financial losses, common vulnerabilities, and the
effectiveness of security responses. Overall, the analysis provides valuable insights that can
help organizations strengthen cybersecurity strategies and improve incident response.
""")

