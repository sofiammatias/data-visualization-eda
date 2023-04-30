import pandas as pd
import streamlit as st

st.title ("Exploratory Data Analysis: World Happiness Data")
#df = pd.read_excel (r'C:\Users\xufia\OneDrive\Ambiente de Trabalho\DataForFigure2_1WHR2021C2.xls')
df = pd.read_excel (r'C:\Users\xufia\OneDrive\Documentos\Programação - Cursos\Projetos\data-visualization-eda\data-visualization-eda\DataForFigure2_1WHR2021C2.xls')
st.dataframe (df)
