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

# Function to plot a bar chart
def plot_bar_chart(column_name, score_column, top_n=10):
    plt.figure(figsize=(10, 6))

    if column_name in ["Director", "Writer"]:
        top_values = df[column_name].value_counts().head(top_n).index
        filtered_df = df[df[column_name].isin(top_values)]
        sns.barplot(data=filtered_df, x=column_name, y=score_column, ci=None)
    else:
        sns.barplot(data=df, x=column_name, y=score_column, ci=None)

    plt.title(f"Average {score_column} by {column_name}")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel(column_name)
    plt.ylabel(f"Average {score_column}")
    plt.tight_layout()


st.title("Exploratory Data Analysis: NetFlix Rotten Tomatoes Data 🍅")

# Load the csv file
df = pd.read_csv(r"netflix-rotten-tomatoes-metacritic-imdb.csv")

# Extract unique genres
unique_genres = set(
    genre for genres in df["Genre"].str.split(", ").dropna() for genre in genres
)

# Create one-hot encoded columns for genres
for genre in unique_genres:
    df[f"Genre-{genre}"] = df["Genre"].dropna().str.contains(genre).astype(bool)

tab1, tab2 = st.tabs(["Introduction", "Final Dashboard"])

with tab1:
    """Given the Netflix Rotten Tomatoes dataset, this app shows an automatic Exploratory Data Analysis, covering:
- an initial analysis (columns number, columns title, columns data type, rows number, duplicated data, missing/null data)
- data histograms to numerical variables
- distribution of categorical variables
- bivariate analysis: blind correlation of all numerical variables
- Pearson correlation to the most relevant numerical values: scores, awards and votes
    """

with tab2:
    st.title("Totals")

    # Pie charts
    col1, col2, col3 = st.columns(3)  # [1,3] allows to uneven the column width
    cols = [col1, col2, col3]

    for i, col in enumerate(["Series or Movie", "Runtime", "View Rating"]):
        top_n = 8
        labels = list(df[col].value_counts().index)[:top_n]
        sizes = list(df[col].value_counts())[:top_n]

        with cols[i]:
            # Plot "Series or Movie" pie chart
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, startangle=90)
            ax.pie([100], radius=0.3, colors=["white"], startangle=90)
            ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

            st.pyplot(fig)

    sizes = []
    for genre in unique_genres:
        sizes.append(sum(df[f"Genre-{genre}"].dropna()))
    labels = list(unique_genres)
    df_aux = pd.DataFrame([sizes, labels]).T
    df_aux.columns = ["Count", "Genre"]  # type: ignore
    df_aux.sort_values("Count", ascending=False, inplace=True)

    # "Genre" bar chart
    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_aux, x="Count", y="Genre", ax=ax)

    st.pyplot(fig2)

    # Bar charts for scores
    st.title("Scores")

    # Lists: columns to consider and scores
    cols = ["Series or Movie", "Genre", "View Rating", "Runtime", "Director", "Writer"]  # type: ignore
    scores = [
        "Hidden Gem Score",
        "IMDb Score",
        "Rotten Tomatoes Score",
        "Metacritic Score",
    ]

    # Display settings
    num_rows = 2
    num_cols = 3
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 10))
    axs = axs.ravel()

    # Display score select control
    selected_score = st.selectbox("Select one score metric:", scores, index=2)

    # Loop through the columns and create bar charts for each score
    for i, column in enumerate(cols):
        if column in ["Director", "Writer"]:
            top_n = 10
            df_aux1 = df.groupby(column)[selected_score].agg(["count", "mean"])  # type: ignore
            df_aux1.sort_values(by="count", ascending=False, inplace=True)
            value_counts = df_aux1[:top_n]
            sns.barplot(
                data=value_counts,
                x=value_counts.index,
                y=value_counts["mean"],
                ax=axs[i],
            )
            axs[i].set_title(f"Top {top_n} {column}")
            axs[i].set_xticklabels(value_counts.index, rotation=45, ha="right")
        elif column == "Genre":
            sizes = []
            for genre in unique_genres:
                sizes.append(df[df[f"Genre-{genre}"] == True][selected_score].mean())  # type: ignore
            labels = list(unique_genres)
            sns.barplot(x=labels, y=sizes, ax=axs[i])
            axs[i].set_title(f"{column} vs {selected_score}")
        else:
            sns.barplot(data=df, x=column, y=selected_score, ax=axs[i])
            axs[i].set_title(f"{column} vs {selected_score}")
            axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=90, ha="right")

        axs[i].set_ylabel(selected_score)
        axs[i].set_xlabel(column)
        axs[i].tick_params(axis="x", labelrotation=90)

    # Adjust layout and display
    plt.tight_layout()
    st.pyplot(fig)
