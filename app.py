import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

# Cache the result of the function
@st.cache(allow_output_mutation=True)
def terrorist_attack_fatalities(country_name):
    supported_countries = ['afghanistan', 'bangladesh', 'bhutan', 'pakistan', 'india', 'nepal', 'maldives', 'srilanka']

    if country_name.lower() not in supported_countries:
        return "We don't have data for this country."

    # URL of the webpage to scrape
    url = 'https://www.satp.org/datasheet-terrorist-attack/fatalities/' + country_name

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class name "grid"
        table = soup.find('table', class_='grid')

        if table:
            # Initialize lists to store data
            data = []

            # Find all rows in the table
            rows = table.find_all('tr')

            # Iterate through rows and extract data
            for row in rows:
                # Find all cells in the row
                cells = row.find_all('td')

                # Extract and store cell content
                row_data = [cell.get_text(strip=True) for cell in cells]
                data.append(row_data)

            # Convert the data into a pandas DataFrame
            columns = ['Year', 'Incidents of Killing', 'Civilians', 'Security Forces', 'Terrorists/Insurgents/Extremists', 'Not Specified', 'Total']
            df = pd.DataFrame(data, columns=columns)

            # Remove the first and last rows (often headers and totals)
            df = df[1:-1]

            # Update the year in the second row to 2000
            df.loc[1, 'Year'] = '2000'

            return df
        else:
            return "Table not found with the specified class name."
    else:
        return "Failed to retrieve the webpage."

def main():
    st.set_page_config(layout="wide")
    
    st.markdown(
        """
        <style>
        .container1 {
            width: 100%;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            }

        .container2 {
            width: 100%;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.header("Yearly Fatalities")
        options = ['india', 'afghanistan', 'bangladesh', 'bhutan', 'pakistan', 'nepal', 'maldives', 'srilanka']
        selected_option = st.selectbox("Select Country:", options)

    with st.container():
        result = terrorist_attack_fatalities(selected_option)
        
        # Display a subset of the data (e.g., first 50 rows)
        st.table(result)
        st.plotly_chart(result.plot(x='Year', y='Civilians', kind='line'))



    # with st.container():
    #     st.markdown("Made By Ashish Mehta")

    # df1 = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
    
    # # Create a Folium map and add markers or other elements as needed
    # m = folium.Map(location=[37.76, -122.4], zoom_start=10)
    # folium_static(m)
    
    

if __name__ == "__main__":
    main()

    
