import streamlit as st
import pandas as pd

st.title("Walmart Sales Analysis")

df = pd.read_csv("Walmart_Sales.csv")
#converte date column to datetime format
df["Date"]= pd.to_datetime(df["Date"], format="%d-%m-%Y")
#Add additional date columns for easier analysis
df['Year']=df['Date'].dt.year
df['Month']=df['Date'].dt.month
df['Quarter']=df['Date'].dt.quarter
st.write("Dataset loaded successfully")
st.write("Shape:", df.shape)
st.write("Columns:", df.columns.tolist())

st.dataframe(df.head())

st.subheader("Question 1: How many unique stores are there in the dataset?")
unique_stores = df["Store"].nunique()
st.write(f"There are {unique_stores} unique stores in the dataset.")

st.subheader("Question 2: What is the date range covered bt the dataset?")
data_range_start = df["Date"].min()
data_range_end =df["Date"].max() 
st.write(f"The dataset covers from {data_range_start.date()} to {data_range_end.date()}")

st.subheader("Question 3. Which store had the highest total weekly sales across the entire period?")
store_total_sales = df.groupby('Store')['Weekly_Sales'].sum()
max_sales_store = store_total_sales.idxmax()
max_sales_store = store_total_sales.max()
st.write(f"Store {max_sales_store} had the highest total weekly sales of ${max_sales_store:,.2f}")
st.bar_chart(store_total_sales)

st.subheader("Question 4: Average Weekly Sales for Holiday vs Non-Holiday Weeks")
holiday_sales = df.groupby("Holiday_Flag")["Weekly_Sales"].mean()
result = pd.DataFrame({
    "Holiday Status":["Non-Holiday","Holiday"],
    "Average Weekly Sales":[holiday_sales[0],holiday_sales[1]]
})
st.dataframe(result) 

st.subheader("Question 5: Which store had the highest average weekly sales?")
avg_sales = df.groupby("Store")["Weekly_Sales"].mean()
best_store = avg_sales.idxmax()
best_sales = avg_sales.max()
st.write(f"Store **{best_store}** had the highest average weekly sales of **${best_sales:,.2f}**.")
st.bar_chart(avg_sales)

st.subheader("Question 6: Correlation between Temperature and Weekly Sales for each Store")
correlations = {}
for store in df["Store"].unique():
    store_data = df[df["Store"] == store]
    correlations[store] = store_data["Temperature"].corr(store_data["Weekly_Sales"])
corr_df = pd.DataFrame(
    correlations.items(),
    columns=["Store","Correlation"]
)
st.dataframe(corr_df.sort_values("Correlation", ascending=False))

st.subheader("Question 7: Month with highest average sales for each store")
store_month_sales = df.groupby(['Store', 'Month'])['Weekly_Sales'].mean().reset_index()
idx = store_month_sales.groupby('Store')['Weekly_Sales'].idxmax()
best_months = store_month_sales.loc[idx]
st.dataframe(best_months[['Store', 'Month', 'Weekly_Sales']])

st.subheader("Question 8: Average Fuel_Price during holiday vs non-holiday weeks")
fuel_by_holiday = df.groupby('Holiday_Flag')['Fuel_Price'].mean()
st.write(f"Answer: Average fuel price for non-holiday weeks: ${fuel_by_holiday[0]:.3f}")
st.write(f"Average fuel price for holiday weeks: ${fuel_by_holiday[1]:.3f}")

st.subheader("Question 9: Store with highest average unemployment rate")
store_unemployment = df.groupby('Store')['Unemployment'].mean()
max_unemp_store = store_unemployment.idxmax()
max_unemp_value = store_unemployment.max()
st.write(f"Answer: Store {max_unemp_store} has the highest average unemployment rate of {max_unemp_value:.3f}%")

st.subheader("Question 10: Week with maximum Weekly_Sales for each store")
idx_max_sales = df.groupby('Store')['Weekly_Sales'].idxmax()
max_sales_weeks = df.loc[idx_max_sales, ['Store', 'Date', 'Weekly_Sales']]
st.dataframe(max_sales_weeks.sort_values('Store'))

st.subheader("Question 11: Total sales for each year")
yearly_sales = df.groupby('Year')['Weekly_Sales'].sum()
for year, sales in yearly_sales.items():
    st.write(f"{year}: ${sales:,.2f}")
    
st.subheader("Question 12: Quarter with highest average sales for each store")
store_quarter_sales = df.groupby(['Store', 'Quarter'])['Weekly_Sales'].mean().reset_index()
idx_q = store_quarter_sales.groupby('Store')['Weekly_Sales'].idxmax()
best_quarters = store_quarter_sales.loc[idx_q]
st.dataframe(best_quarters[['Store', 'Quarter', 'Weekly_Sales']])    

st.subheader("Question 13: Average CPI for weeks with above-median sales")
median_sales = df['Weekly_Sales'].median()
above_median = df[df['Weekly_Sales'] > median_sales]
below_median = df[df['Weekly_Sales'] <= median_sales]
avg_cpi_above = above_median['CPI'].mean()
avg_cpi_below = below_median['CPI'].mean()
st.write(f"Answer: Average CPI for weeks with sales above median: {avg_cpi_above:.3f}")
st.write(f"Average CPI for weeks with sales below median: {avg_cpi_below:.3f}")

st.subheader("Question 14: Store with most consistent sales (lowest standard deviation)")
store_std = df.groupby('Store')['Weekly_Sales'].std()
min_std_store = store_std.idxmin()
min_std_value = store_std.min()
max_std_store = store_std.idxmax()
max_std_value = store_std.max()
st.write(f"Answer: Store {min_std_store} has the most consistent sales with std deviation of ${min_std_value:,.2f}")
st.write(f"Store {max_std_store} has the least consistent sales with std deviation of ${max_std_value:,.2f}")

st.subheader("Question 15: Percentage change in average weekly sales from 2010 to 2012 for each store")
store_year_avg = df.groupby(['Store', 'Year'])['Weekly_Sales'].mean().unstack()
if 2010 in store_year_avg.columns and 2012 in store_year_avg.columns:

    pct_change = ((store_year_avg[2012] - store_year_avg[2010]) / store_year_avg[2010] * 100).dropna()

    st.write("Percentage change from 2010 to 2012:")

    for store, change in pct_change.items():
        st.write(f"Store {store}: {change:.2f}%")

else:
    st.write("Note: Not all stores have data for both 2010 and 2012")
    

st.subheader("Question 16: Top 5 weeks with highest Weekly_Sales")
top_5_weeks = df.nlargest(5, 'Weekly_Sales')[['Store', 'Date', 'Weekly_Sales']].reset_index(drop=True)
st.dataframe(top_5_weeks) 

st.subheader("Question 17: Average Temperature during top 10% sales weeks")
sales_90th_percentile = df['Weekly_Sales'].quantile(0.90)
top_10_sales = df[df['Weekly_Sales'] >= sales_90th_percentile]
avg_temp_top10 = top_10_sales['Temperature'].mean()
avg_temp_all = df['Temperature'].mean()
st.write(f"Answer: Average temperature during top 10% sales weeks: {avg_temp_top10:.2f}°F")
st.write(f"Overall average temperature: {avg_temp_all:.2f}°F")   

st.subheader("Question 18: Average Weekly_Sales for weeks with Unemployment > 8% for each store")
high_unemp_data = df[df['Unemployment'] > 8]
if not high_unemp_data.empty:

    store_high_unemp_avg = high_unemp_data.groupby('Store')['Weekly_Sales'].mean()

    st.write("Average sales during high unemployment (>8%):")

    for store, sales in store_high_unemp_avg.items():
        st.write(f"Store {store}: ${sales:,.2f}")

else:
    st.write("No weeks with unemployment above 8% found.")
    
st.subheader("Question 19: Date when Fuel_Price reached maximum for each store")
idx_max_fuel = df.groupby('Store')['Fuel_Price'].idxmax()
max_fuel_dates = df.loc[idx_max_fuel, ['Store', 'Date', 'Fuel_Price']]
st.dataframe(max_fuel_dates.sort_values('Store'))

st.subheader("Question 20: Store with strongest positive correlation between CPI and Weekly_Sales")
cpi_correlations = {}
for store in df['Store'].unique():

    store_data = df[df['Store'] == store]

    corr = store_data['CPI'].corr(store_data['Weekly_Sales'])

    cpi_correlations[store] = corr

max_corr_store = max(cpi_correlations.items(), key=lambda x: x[1])

min_corr_store = min(cpi_correlations.items(), key=lambda x: x[1])

st.write(f"Answer: Store {max_corr_store[0]} has the strongest positive correlation: {max_corr_store[1]:.4f}")
st.write(f"Store {min_corr_store[0]} has the strongest negative correlation: {min_corr_store[1]:.4f}")    


st.subheader("Bonus: Summary Statistics")

st.write("=" * 50)
st.write("SUMMARY STATISTICS")
st.write("=" * 50)

st.write(f"Total number of records: {len(df)}")

st.write(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

st.write(f"Total sales across all stores: ${df['Weekly_Sales'].sum():,.2f}")

st.write(f"Average weekly sales: ${df['Weekly_Sales'].mean():,.2f}")

st.write(f"Number of holiday weeks: {df['Holiday_Flag'].sum()}")

st.write(f"Number of non-holiday weeks: {len(df) - df['Holiday_Flag'].sum()}")