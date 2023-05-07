"""
    Conducting EDA:
    - Initial Data Exploration: Read in data, take a glimpse at a few rows, calculate some summary statistics.
    - Univariate Analysis: Analyze continuous and categorical variables, one variable at a time.
    - Bivariate Analysis: Looking at the relationship between two variables at a time.
    - Identify and Handling Duplicate and Missing Data: Find and remove duplicate rows, and replace missing values with their mean and mode.
    - Correlation Analysis: Looking at the correlation of numerical variables in the dataset and interpreting the numbers.


"""
import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache_resource
@st.cache_data

# Define function to create a countplot
def create_countplot(df, col, ax):
    """Function to create a countplot"""
    sns.countplot(data=df, x=col, ax=ax)
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.set_xticklabels([])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best')

# Define function to create a boxplot
def create_boxplot(df, col, ax):
    """Function to create a boxplot"""
    sns.boxplot(data=df, y=col, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel(col)

st.title ("Exploratory Data Analysis: NetFlix Rotten Tomatoes Data")

# Load the csv file
df = pd.read_csv (r'C:\Users\xufia\OneDrive\Documentos\Programação - Cursos\Projetos\data-visualization-eda\data-visualization-eda\netflix-rotten-tomatoes-metacritic-imdb.csv')

# use tabs for different analysis
tab1, tab2, tab3, tab4 = st.tabs(["Initial Analysis", 
                                  "Univariate Analysis", 
                                  "Bivariate Analysis",
                                  "Correlations"])

with tab1:
    # Seeing dataframe
    st.header ('Data Table')
    st.dataframe (df)

    # Dataframe info: columns info
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()#.split('\n')
    st.header ('Columns Info')
    st.text(s)

    #Duplicates
    st.header ('Other Info')
    if int(df.duplicated().sum()) == 0:
        st.write ('There are no duplicated rows.')
    
    if int(df.isna().any().sum()) == 0:
        st.write ('There are no missing values.')
    else:
        st.write (f"There are {df.isna().any().sum()} missing values.")

with tab2:
    # Univariate Analysis: Numerical
    st.header("Numerical Variables")
    num_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if len(num_cols) == 1:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(data=df, x=num_cols, ax=ax)
        ax.set_title(num_cols)
        #ax.set_ylabel("Count")
        st.pyplot(fig)
    elif len(num_cols) == 2:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.histplot(data=df, x=num_cols[0], ax=ax1)
        ax1.set_title(num_cols[0])
        #ax1.set_ylabel("Count")
        sns.histplot(data=df, x=num_cols[1], ax=ax2)
        ax2.set_title(num_cols[1])
        #ax2.set_ylabel("Count")
        st.columns([ax1, ax2])
    elif len(num_cols) > 2:
        num_rows = (len(num_cols) - 1) // 3 + 1
        fig, axs = plt.subplots(num_rows, 3, figsize=(15, 5*num_rows))
        axs = axs.ravel()
        for i, col in enumerate(num_cols):
            sns.histplot(data=df, x=col, ax=axs[i])
            axs[i].set_title(col)
        fig.tight_layout()
        st.pyplot(fig)
    
    # Univariate Analysis: Categorical
    st.header("Categorical Variables")
    cat_cols = df.select_dtypes(include=["object"]).columns
    cat_cols = ['Series or Movie', 'Runtime', 'View Rating']
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
        num_rows = (len(cat_cols) - 1) // 3 + 1
        fig, axs = plt.subplots(num_rows, 3, figsize=(15, 5*num_rows))
        axs = axs.ravel()
        for i, col in enumerate(cat_cols):
            sns.countplot(data=df, x=col, ax=axs[i])
            axs[i].set_xlabel(col)
            axs[i].set_ylabel("Count")
            axs[i].tick_params(axis='x', labelrotation=45, labelsize=8)
            axs[i].set_xticklabels([])
            handles, labels = axs[i].get_legend_handles_labels()
            axs[i].legend(handles, labels, loc='best')
        fig.tight_layout()
        st.pyplot(fig)

    # Outliers
    # Separate columns with outliers
    out_cols = []
    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if not outliers.empty:
            out_cols.append(col)

    st.header("Outliers")
    num_rows = (len(out_cols) - 1) // 2 + 1
    fig, axs = plt.subplots(num_rows, 2, figsize=(10, 5*num_rows))
    axs = axs.ravel()

    for i, col in enumerate(num_cols):
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


with tab3:
    # Bivariate Analysis
    st.header("Bivariate Analysis")
    sns.pairplot(df)
    st.pyplot()

with tab4:
    # Pearson Correlation Heatmap
    st.header("Pearson Correlation Heatmap")
    corr = df.drop("Country name", axis=1).corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, square=True, annot=True, fmt=".2f")
    st.pyplot()
