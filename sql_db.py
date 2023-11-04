"""
This module connects to a Postgres database. With a help of a sqlalchemy engine a formed dataframe is uploaded to
the SQL database. An argument param takes either 'replace' or 'append' values.
"""

from sqlalchemy import create_engine
import json
from datetime import datetime


def connect (df, param):
    # Load database configuration from a JSON file in order to avoid hardcoding sensible information
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
    # Get the current date in 'dd.mm' format
    current_date = datetime.now().strftime('%d.%m')
    # Add the current date to the table name
    table_name = f'cars_{current_date}'
    # Upload dataframe to a corresponding table with a current date
    df.to_sql(table_name, engine, if_exists=param, index=False, schema='autoscout')

if __name__ == '__main__':
    pass
