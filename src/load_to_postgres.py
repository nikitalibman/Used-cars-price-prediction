"""
This module connects to a Postgres database. With a help of a sqlalchemy engine a formed dataframe is uploaded to
the SQL database. An argument param takes either 'replace' or 'append' values.
"""

from sqlalchemy import create_engine, VARCHAR, Integer, Date
import json
from datetime import datetime
import dataframe
import pandas as pd


def load_to_postgres(df, param='append'):
    """Load database configuration from a JSON file in order to avoid hard-coding sensible information."""
    with open('postgres_configs.json') as config_file:
        config = json.load(config_file)
    # Configurations to connect to a SQL database
    db_user = config['postgres']['user']
    db_password = config['postgres']['pwd']
    db_host = config['postgres']['host']
    db_port = config['postgres']['port']
    db_name = config['postgres']['db']
    # Connection string
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)
    # Get the current date in 'yy_dd_mm' format
    current_date = datetime.now().strftime('%y_%m_%d')
    # Add the current date to the table name
    table_name = f'cars_{current_date}'
    # Set proper data types
    df['make'] = df['make'].astype(str)
    df['model'] = df['model'].astype(str)
    df['mileage'] = df['mileage'].astype(int)
    df['transmission'] = df['transmission'].astype(str)
    df['registration'] = pd.to_datetime('01/' + df['registration'], format='%d/%m/%Y', errors='coerce').dt.date
    df['fuel'] = df['fuel'].astype(str)
    df['power'] = df['power'].astype(int)
    df['location'] = df['location'].astype(str)
    df['price'] = df['price'].astype(int)

    # SQLAlchemy dtype mapping
    dtype = {
        'make': VARCHAR(100),
        'model': VARCHAR(100),
        'mileage': Integer,
        'transmission': VARCHAR(50),
        'registration': Date,
        'fuel': VARCHAR(50),
        'power': Integer,
        'location': VARCHAR(50),
        'price': Integer
    }
    # Upload dataframe to a corresponding table with a current date
    df.to_sql(table_name, engine, schema='autoscout', if_exists=param, index=False, dtype=dtype)
    print(f'Table {table_name} was updated.')


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/'
    df = dataframe.main(url)
    # param = 'replace'
    load_to_postgres(df)
