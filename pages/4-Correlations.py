"""
    Conducting EDA:
    - Initial Data Exploration: Read in data, take a glimpse at a few rows, calculate some summary statistics.
    - Univariate Analysis: Analyze continuous and categorical variables, one variable at a time.
    - Bivariate Analysis: Looking at the relationship between two variables at a time.
    - Identify and Handling Duplicate and Missing Data: Find and remove duplicate rows, and replace missing values with their mean and mode.
    - Correlation Analysis: Looking at the correlation of numerical variables in the dataset and interpreting the numbers.


"""
import pandas as pd  # type: ignore
import streamlit as st
import numpy as np
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import io

# Configurations
#st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout="wide", page_title="NetFlix Rotten Tomatoes Data - EDA", page_icon = "🍅")
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

# Load the csv file
df = pd.read_csv(
    r"C:\Users\xufia\OneDrive\Documentos\Programação - Cursos\Projetos\data-visualization-eda\data-visualization-eda\netflix-rotten-tomatoes-metacritic-imdb.csv"
)

# Pearson Correlation Heatmap
st.header("Pearson Correlation Heatmap")
corr = df.corr()
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, square=True, annot=True, fmt=".2f")
st.pyplot()
