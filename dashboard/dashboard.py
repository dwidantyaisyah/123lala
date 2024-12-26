import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_data = pd.read_csv('day.csv')
hour_data = pd.read_csv('hour.csv')

# Dashboard title
st.title("Bike Sharing Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose Dataset", ["Day Data", "Hour Data"])

# Function to display dataset
def display_dataset(data):
    st.subheader("Dataset Preview")
    st.write(data.head())

    st.subheader("Summary Statistics")
    st.write(data.describe())

    st.subheader("Missing Values")
    st.write(data.isnull().sum())

# Function for univariate analysis
def univariate_analysis(data):
    st.subheader("Univariate Analysis")
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        st.write(f"Distribution of {col}")
        fig, ax = plt.subplots()
        sns.histplot(data[col], kde=True, bins=30, ax=ax)
        st.pyplot(fig)

# Function for bivariate analysis
def bivariate_analysis(data):
    st.subheader("Bivariate Analysis")
    st.write("Correlation Heatmap")
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(data[numerical_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Function for categorical analysis
def categorical_analysis(data):
    st.subheader("Categorical Analysis")
    categorical_cols = data.select_dtypes(include=['object', 'category', 'int64']).columns
    for col in categorical_cols:
        if data[col].nunique() < 10:  # Filter for small number of unique values
            st.write(f"Countplot for {col}")
            fig, ax = plt.subplots()
            sns.countplot(x=data[col], ax=ax)
            st.pyplot(fig)

# Main logic for navigation
if options == "Day Data":
    st.header("Day Data Analysis")
    display_dataset(day_data)
    univariate_analysis(day_data)
    bivariate_analysis(day_data)
    categorical_analysis(day_data)

elif options == "Hour Data":
    st.header("Hour Data Analysis")
    display_dataset(hour_data)
    univariate_analysis(hour_data)
    bivariate_analysis(hour_data)
    categorical_analysis(hour_data)
