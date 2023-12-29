"""
    Conducting EDA:
    - Correlation Analysis: Looking at the correlation of numerical variables in the dataset and interpreting the numbers.
"""
import pandas as pd  # type: ignore
import streamlit as st
import seaborn as sns  # type: ignore
import matplotlib.pyplot as plt

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


st.title("Correlations: NetFlix Rotten Tomatoes Data 🍅")

# Load the csv file
df = pd.read_csv(r"..\data-visualization-eda\netflix-rotten-tomatoes-metacritic-imdb.csv")

# Pearson Correlation Heatmap
st.header("Pearson Correlation Heatmap")
plt.clf()
corr = df.corr(numeric_only=True)
cmap = sns.diverging_palette(220, 10, as_cmap=True)
hm = sns.heatmap(corr, cmap=cmap, annot=True, fmt=".2f")
st.pyplot(hm.figure)
