"""
    Conducting EDA:
    - Initial Data Exploration: Read in data, take a glimpse at a few rows, calculate some summary statistics.
"""

import pandas as pd  # type: ignore
import streamlit as st
import numpy as np
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import io

# Configurations
# st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(
    layout="wide",
    page_title="NetFlix Rotten Tomatoes Data - Initial Analysis",
    page_icon="📋",
)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


@st.cache_resource
@st.cache_data

# Define function to create a countplot
def create_countplot(df, col, ax):
    """Function to create a countplot"""
    sns.countplot(data=df, x=col, ax=ax)
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.set_xticklabels([])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="best")


# Define function to create a boxplot
def create_boxplot(df, col, ax):
    """Function to create a boxplot"""
    sns.boxplot(data=df, y=col, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel(col)


st.title("Initial Analysis: NetFlix Rotten Tomatoes Data 🍅")


# Load the csv file
df = pd.read_csv(
    r"C:\Users\xufia\OneDrive\Documentos\Programação - Cursos\Projetos\data-visualization-eda\data-visualization-eda\netflix-rotten-tomatoes-metacritic-imdb.csv"
)

# Seeing dataframe
st.header("Data Table")
st.dataframe(df)

# Dataframe info: columns info
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()  # .split('\n')
st.header("Columns Info")
st.text(s)

st.header("Other Info")
# Duplicates
if int(df.duplicated().sum()) == 0:
    st.write("There are no duplicated rows.")

# Null values
if int(df.isna().any().sum()) == 0:
    st.write("There are no missing values.")
else:
    st.write(f"There are {df.isna().any().sum()} variables with missing values.")
    st.write(f"Average for {df.columns[13]} is {df[df.columns[13]].mean()}")
