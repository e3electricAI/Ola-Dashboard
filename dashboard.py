import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data from the CSV file (replace with the actual path to your CSV)
data = pd.read_csv('ola_dealers_with_showroom_count.csv')

# Clean the data: Convert showroom count to numeric, handle errors
data['Number of Showrooms'] = pd.to_numeric(data['Number of Showrooms'], errors='coerce')

# Basic analysis
state_count = data['State'].value_counts()
city_count = data.groupby('City').size()
avg_showrooms_per_city = data.groupby('City')['Number of Showrooms'].mean()

# Streamlit Page Layout
st.title("Ola Dealer Showroom Dashboard")

st.write("""
This dashboard visualizes the distribution of Ola dealers and their showrooms across various states and cities in India.
""")

# Display the dealer count per state
st.header("Number of Dealers per State")
state_fig = px.bar(state_count, x=state_count.index, y=state_count.values,
                   labels={'x': 'State', 'y': 'Number of Dealers'},
                   title="Number of Dealers per State")
st.plotly_chart(state_fig)

# Display the showroom count per city
st.header("Number of Showrooms per City (Tabular Format)")

# Prepare the table of dealer counts per city
city_showroom_data = city_count.reset_index(name='Number of Dealers')
city_showroom_data.columns = ['City', 'Number of Dealers']

# Display the city-wise dealer count in a table
st.write(city_showroom_data)

# Show average showrooms per city
st.header("Average Showrooms per City")
avg_showrooms_fig = px.bar(avg_showrooms_per_city, x=avg_showrooms_per_city.index, y=avg_showrooms_per_city.values,
                            labels={'x': 'City', 'y': 'Average Number of Showrooms'},
                            title="Average Number of Showrooms per City")
st.plotly_chart(avg_showrooms_fig)

# Show Summary Insights
st.header("Summary Insights")
st.write(f"- **Total number of dealers**: {data.shape[0]}")
st.write(f"- **Total number of states represented**: {len(state_count)}")
st.write(f"- **Total number of cities represented**: {len(city_count)}")
st.write(f"- **Average number of showrooms per city**: {avg_showrooms_per_city.mean():.2f}")

# Optional: Display data table if needed
st.subheader("Raw Data")
st.write(data)