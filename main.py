#************************************************************************
# Authors:
# Date:
#************************************************************************
import json
from typing import Any

import pandas as pd
import requests

restcountries_url = "https://restcountries.com/v3.1/all"


def get_data(url: str) -> json:
    # Send a GET request to the specified URL
    request = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if request.status_code == 200:
        # Parse the response content as JSON
        response = request.json()
        # Return the parsed JSON data
        return response
    else:
        # If the request was not successful, return an error message
        return 'Error fetching data'


def transform_data(data: Any) -> pd.DataFrame:
    # Extract relevant fields from each dictionary in the list
    countries = {
        'country_name': [info['name'].get('common') for info in data],
        'independence': [info.get('independent') for info in data],
        'un_members': [info.get('unMember') for info in data],
        'startOfWeek': [info.get('startOfWeek') for info in data],
        'official_country_name': [info['name'].get('official') for info in data],
        'common_native_names': [info['name'].get('nativeName', {}).get('eng', {}).get('common') for info in data],
        
        # Handle currency details
        'currency_code': [list(info.get('currencies', {}).keys())[0] if info.get('currencies') else None for info in data],
        'currency_name': [list(info.get('currencies', {}).values())[0].get('name') if info.get('currencies') else None for info in data],
        'currency_symbol': [list(info.get('currencies', {}).values())[0].get('symbol') if info.get('currencies') else None for info in data],
        
        # get country information
        'country_code': [info.get('cca3') for info in data],
        'capital': [info.get('capital', [None])[0] for info in data],
        'region': [info.get('region') for info in data],
        'sub_region': [info.get('subregion') for info in data],
        
        # Join languages into a single string
        'languages': [', '.join(info.get('languages', {}).values()) for info in data],
        
        # Get land area and population
        'area': [info.get('area') for info in data],
        'population': [info.get('population') for info in data],
        
        'continents': [info.get('continents', [None])[0] for info in data],   # Extract continent
        
        # Handle latlng safely
        'longitude': [info.get('latlng', [None, None])[1] for info in data],
        'latitude': [info.get('latlng', [None, None])[0] for info in data]
    }

    # Convert dictionary to DataFrame
    df_data = pd.DataFrame(countries)
    
    return df_data

def create_db_table(cur):
    cur.execute("""
        DROP TABLE IF EXISTS world_countries;
        
        CREATE TABLE IF NOT EXISTS world_countries (
            country_code VARCHAR(255) PRIMARY KEY,
            country_name VARCHAR(255),
            independence BOOLEAN,
            un_members BOOLEAN,
            start_of_week TEXT,
            official_country_name VARCHAR(255),
            common_native_name VARCHAR(255),
            currency_code VARCHAR(10),
            currency_name VARCHAR(255),
            currency_symbol VARCHAR(10),
            capital VARCHAR(255),
            region VARCHAR(255),
            sub_region VARCHAR(255),
            languages TEXT,
            area FLOAT,
            population INT,
            continents VARCHAR(255)
        )
    """)

