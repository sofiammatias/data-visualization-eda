"""
    Conducting EDA:
    - Bivariate Analysis: Looking at the relationship between two variables at a time.

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
    layout="wide", page_title="NetFlix Rotten Tomatoes Data - EDA", page_icon="🍅"
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


st.title("Bivariate Analysis: NetFlix Rotten Tomatoes Data 🍅")

# Load the dataframe
df = st.session_state.df

# Bivariate Analysis
st.header("Potential Correlations Between 2 Variables")
sns.pairplot(df)
st.pyplot()
