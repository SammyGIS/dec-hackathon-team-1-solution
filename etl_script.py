#************************************************************************
# Authors:
# Date:
#************************************************************************
import json
import os
from typing import Any

import pandas as pd
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
DEFAULTDB = os.getenv("DEFAULTDB")
PASSWORD=os.getenv("PASSWORD")

print(DBNAME)
restcountries_url = "https://restcountries.com/v3.1/all"

def get_data(url: str) -> json:
    request = requests.get(url)
    if request.status_code == 200:
        print("data fectched successfully")
        return request.json()
    else:
        return 'Error fetching data'

def transform_data(data: Any) -> pd.DataFrame:
    try:
        countries = {
            'country_name': [info['name'].get('common') for info in data],
            'independence': [info.get('independent') for info in data],
            'un_members': [info.get('unMember') for info in data],
            'start_of_week': [info.get('startOfWeek') for info in data],
            'official_country_name': [info['name'].get('official') for info in data],
            'common_native_names': [info['name'].get('nativeName', {}).get('eng', {}).get('common') for info in data],
            
            'currency_code': [list(info.get('currencies', {}).keys())[0] if info.get('currencies') and len(info.get('currencies')) > 0 else None for info in data],
            'currency_name': [list(info.get('currencies', {}).values())[0].get('name') if info.get('currencies') and len(info.get('currencies')) > 0 else None for info in data],
            'currency_symbol': [list(info.get('currencies', {}).values())[0].get('symbol') if info.get('currencies') and len(info.get('currencies')) > 0 else None for info in data],
            
            'country_code': [info.get('cca3') for info in data],
            'capital': [info.get('capital', [None])[0] for info in data],
            'region': [info.get('region') for info in data],
            'sub_region': [info.get('subregion') for info in data],
            
            'languages': [', '.join(info.get('languages', {}).values()) for info in data],
            
            'area': [info.get('area') for info in data],
            'population': [info.get('population') for info in data],
            
            'continents': [info.get('continents', [None])[0] if info.get('continents') and len(info.get('continents')) > 0 else None for info in data],
            
            'longitude': [info.get('latlng', [None, None])[1] for info in data],
            'latitude': [info.get('latlng', [None, None])[0] for info in data]
        }

        df_data = pd.DataFrame(countries)
        print('data transformed successfully')
        return df_data
    except Exception as e:
        print('An error ocuured:',{e})


def create_db(host,default_db,user,password,port,dbname):
    # Connect to the default 'postgres' database to create a new one
    conn = psycopg2.connect(
        f"host={host} dbname={default_db} user={user} password={password} port={port}")
    conn.autocommit = True  # Ensure we are not in a transaction block
    try:
        cur = conn.cursor()
        # Check if the database already exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        if cur.fetchone() is None:
            cur.execute(f"CREATE DATABASE {dbname}")
            print(f"Database '{dbname}' created successfully.")
        else:
            print(f"Database '{dbname}' already exists.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()  # Close the connection to the default database

def create_table(cur):
    try:
        cur.execute("""
            DROP TABLE IF EXISTS world_countries;
            CREATE TABLE world_countries (
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
                continents VARCHAR(255),
                latitude FLOAT,
                longitude FLOAT
            )
        """)
        print("Table created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")

def insert_data_to_db(df: pd.DataFrame, cur, conn):
    try:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO world_countries (
                    country_code,
                    country_name,
                    independence,
                    un_members,
                    start_of_week,
                    official_country_name,
                    common_native_name,
                    currency_code,
                    currency_name,
                    currency_symbol,
                    capital,
                    region,
                    sub_region,
                    languages,
                    area,
                    population,
                    continents,
                    latitude,
                    longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['country_code'],
                row['country_name'],
                row['independence'],
                row['un_members'],
                row['start_of_week'],
                row['official_country_name'],
                row['common_native_names'],
                row['currency_code'],
                row['currency_name'],
                row['currency_symbol'],
                row['capital'],
                row['region'],
                row['sub_region'],
                row['languages'],
                row['area'],
                row['population'],
                row['continents'],
                row['latitude'],
                row['longitude']
            ))

        conn.commit()

        print("Data inserted successfully.")

    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

def main():
    data = get_data(url=restcountries_url)

    if data != 'Error fetching data':
        create_db(host=HOST,default_db=DEFAULTDB,
                  user=USER,password=PASSWORD,port=PORT,dbname=DBNAME)
        conn = psycopg2.connect(f"host={HOST} dbname={DBNAME} user={USER} password={PASSWORD} port={PORT}")
        cur = conn.cursor()
        transformed_data = transform_data(data)
        print(f'data has {transformed_data.shape[0]} rows and {transformed_data.shape[1]} columns')
        create_table(cur)
        insert_data_to_db(transformed_data, cur, conn)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
