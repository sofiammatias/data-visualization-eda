"""
    Conducting EDA:
    - Univariate Analysis: Analyze continuous and categorical variables, one variable at a time.
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


st.title("Univariate Analysis: NetFlix Rotten Tomatoes Data 🍅")

# Load the csv file
df = pd.read_csv(r"..\\netflix-rotten-tomatoes-metacritic-imdb.csv")


# Extract unique genres
unique_genres = set(
    genre for genres in df["Genre"].str.split(", ").dropna() for genre in genres
)

# Create one-hot encoded columns for genres
for genre in unique_genres:
    df[f"Genre-{genre}"] = df["Genre"].dropna().str.contains(genre).astype(bool)

# Univariate Analysis: Numerical
st.header("Numerical Variables")
num_cols = df.select_dtypes(include=["float64"]).columns
if len(num_cols) == 1:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x=num_cols, ax=ax)
    ax.set_title(num_cols)
    # ax.set_ylabel("Count")
    st.pyplot(fig)
elif len(num_cols) == 2:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x=num_cols[0], ax=ax1)
    ax1.set_title(num_cols[0])
    # ax1.set_ylabel("Count")
    sns.histplot(data=df, x=num_cols[1], ax=ax2)
    ax2.set_title(num_cols[1])
    # ax2.set_ylabel("Count")
    st.columns([ax1, ax2])
elif len(num_cols) > 2:
    num_rows = (len(num_cols) - 1) // 3 + 1
    fig, axs = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))
    axs = axs.ravel()
    for i, col in enumerate(num_cols):
        sns.histplot(data=df, x=col, ax=axs[i])
        axs[i].set_title(col)
    fig.tight_layout()
    st.pyplot(fig)

# Univariate Analysis: Categorical
st.header("Categorical Variables")
# cat_cols = df.select_dtypes(include=["object"]).columns
cat_cols = ["Series or Movie", "Runtime", "View Rating", "Genre"]
if len(cat_cols) == 1:
    fig, ax = plt.subplots(figsize=(10, 5))
    create_countplot(df, cat_cols[0], ax)
    st.pyplot(fig)
elif len(cat_cols) == 2:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    create_countplot(df, cat_cols[0], ax1)
    create_countplot(df, cat_cols[1], ax2)
    st.columns([ax1, ax2])
elif len(cat_cols) > 2:
    num_rows = (len(cat_cols) - 1) // 2 + 1
    fig, axs = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
    axs = axs.ravel()
    for i, col in enumerate(cat_cols):
        unique_vals = df[col].unique()
        if col == "Genre":
            sizes = []
            for genre in unique_genres:
                sizes.append(sum(df[f"Genre-{genre}"].dropna()))
            labels = list(unique_genres)
            sns.barplot(x=labels, y=sizes, ax=axs[i])
        else:
            sns.countplot(data=df, x=col, ax=axs[i])
        axs[i].set_xlabel(col)
        axs[i].set_ylabel("Count")
        axs[i].tick_params(axis="x", labelrotation=90, labelsize=8)
    fig.tight_layout()
    st.pyplot(fig)

# Outliers
# Separate columns with outliers
out_cols = []
for col in num_cols:
    if abs(df[col].skew()) > 1.5:  # Check if the variable is highly skewed
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if not outliers.empty:
            out_cols.append(col)

st.header("Outliers")
num_rows = (len(out_cols) - 1) // 3 + 1
fig, axs = plt.subplots(num_rows, 4, figsize=(15, 5 * num_rows))
axs = axs.ravel()

for i, col in enumerate(out_cols):
    sns.boxplot(data=df[col], ax=axs[i])
    axs[i].set_title(f"{col}")
    axs[i].set_xlabel("")
    axs[i].set_ylabel(col)
    axs[i].grid(True)

    if i == len(out_cols) - 1:
        break
if len(out_cols) % 2 != 0:
    fig.delaxes(axs[-1])
fig.tight_layout()
st.pyplot(fig)
