# InsightAI — Business Analytics Copilot

## Project Overview
InsightAI is a Python-based business analytics application that helps users upload datasets, inspect data quality, explore business insights, and visualize data through interactive charts.

## Features
- Upload CSV and Excel datasets
- View dataset rows and columns
- Check missing values and duplicate rows
- Generate automatic business insights
- Explore interactive charts
- Download data quality reports
- Download numeric summaries and processed data

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly
- NumPy
- Scikit-learn
- Excel and CSV

## Dataset
The project was tested with an e-commerce dataset containing 397,563 rows and 9 columns.

## Key Insights
- Total recorded sales: 8,132,583.30
- Unique invoices: 18,532
- Unique customers: 4,338
- Total quantity: 5,166,857
- Missing values: 0
- Duplicate rows detected: 27

*Sales figures are calculated from the dataset's Sales column.*

## How to Run
1. Install Python.
2. Install the required packages:
   `pip install streamlit pandas numpy plotly openpyxl scikit-learn`
3. Open the project folder in the terminal.
4. Run:
   `python -m streamlit run app.py`

## Author
AI & Machine Learning Student | Aspiring Data Analyst

## Project Goal
To make business data analysis easier through automated insights, data-quality checks, and interactive visualizations.
## Dashboard Screenshot
![InsightAI Dashboard](InsightAI_Dashboard.png)
