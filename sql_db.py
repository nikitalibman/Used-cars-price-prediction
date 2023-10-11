from sqlalchemy import create_engine
import json


def connect (df, param):
    # Load database configuration from a JSON file in order to avoid hardcoding sensible information
    with open('postgres_configs.json') as config_file:
        config = json.load(config_file)
    # configurations to connect to a SQL database
    db_user = config['postgres']['user']
    db_password = config['postgres']['pwd']
    db_host = config['postgres']['host']
    db_port = config['postgres']['port']
    db_name = config['postgres']['db']
    # Connection string
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)
    df.to_sql('cars', engine, if_exists=param, schema='autoscout')

if __name__ == '__main__':
    pass
    #param takes 'replace' or 'append'
