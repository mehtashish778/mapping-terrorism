import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np






def terrorist_attack_fatalities(country_name):
    supported_countries = ['afghanistan', 'bangladesh', 'bhutan', 'pakistan', 'india', 'nepal', 'maldives','srilanka']

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
    
    
    st. set_page_config(layout="wide")
    
    # Add custom CSS styling to control container dimensions
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

    # Create a container for the dropdown
    with st.container():
        st.header("Yearly Fatalities")
        options =['india','afghanistan', 'bangladesh', 'bhutan', 'pakistan',  'nepal', 'maldives','srilanka']
        selected_option = st.selectbox("Select Country:", options)

    # Create a container for the output
    with st.container():
        result = terrorist_attack_fatalities(selected_option)
        
        st.table(result)
        # st.write(result,unsafe_allow_html=True, className="full-width")
        
        
    with st.container():
        st.markdown("Made By Ashish Mehta")
        
    df1 = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])

<<<<<<< HEAD
    # st.map(df1)
    st.area_chart(result)

=======
    # st.map(df1)
>>>>>>> 986154b89f4689d6cb2e59dc2c236d9b7759a2da
    
    

if __name__ == "__main__":
    main()
