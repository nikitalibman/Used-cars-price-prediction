import re
import json
from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, VARCHAR, Integer, Date
from decline_cookies import get_url


def get_home_url(url: str) -> str:
    """Load the home autoscout page and click on the button 'Results'."""

    chrome_driver, current_url = get_url(url)
    # Wait for the 'results' button to be clickable
    results_button = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'search-mask-search-cta')))
    results_button.click()

    wait = WebDriverWait(chrome_driver, 10)
    wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'ListItem_title_bold__iQJRq')))

    current_url = chrome_driver.current_url

    return current_url, chrome_driver


def total_pages(soup: BeautifulSoup) -> int:
    """Get the number of total pages from the main page."""

    try:
        indicator = soup.find(
            'li', class_='pagination-item--disabled pagination-item--page-indicator')
        pages = int(indicator.text.split('/')[-1].strip())
        return pages
    except:
        print('Page indicator not found.')


def pages_urls(autoscout_url) -> list:
    """Get a list of all URLs from every main page."""

    url, _ = get_home_url(autoscout_url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    all_pages = []
    try:
        for i in range(1, total_pages(soup) + 1):
            url_part = url.split('?')
            page_url = url_part[0] + \
                f'?atype=C&desc=0&page={i}&search_id=m76u8v3lpc&sort=standard&source=listpage_pagination&ustate=N%2CU'
            all_pages.append(page_url)
        return all_pages
    except:
        print('No pages were found.')


def get_main_htmls(autoscout_url) -> list:
    """Create a list of html codes as soup elements about all main pages."""

    all_pages = pages_urls(autoscout_url)
    soups_list = []
    if all_pages is not None:
        for k in all_pages:
            try:
                soups_list.append(BeautifulSoup(requests.get(k).text, 'lxml'))
            except:
                continue
    return soups_list


def parce_car_info(soups_list: list, tag: str, attr: str, df: list) -> list:
    """This function scraps over the website in order to extract specific information about each car (characteristics, prices etc)"""

    for element in soups_list:
        try:
            info = element.find_all(tag, attrs={'class': attr})
        except:
            continue
        for i in info:
            df.append(i.get_text())
    return df


def create_car_dataframes(soups_list: list) -> tuple[list, list, list, list]:
    """Create blank lists and populate them with cars' info"""

    cars = []
    characteristics = []
    prices = []
    locations = []
    cars = parce_car_info(soups_list, 'span',
                          'ListItem_title_bold__iQJRq', cars)
    characteristics = parce_car_info(
        soups_list, 'div', 'VehicleDetailTable_container__XhfV1', characteristics)
    prices = parce_car_info(
        soups_list, 'p', 'Price_price__APlgs PriceAndSeals_current_price__ykUpx', prices)
    locations = parce_car_info(
        soups_list, 'span', 'SellerInfo_address__leRMu', locations)
    return cars, characteristics, prices, locations


def format_cars_info(characteristics: list, prices: list, locations: list) -> tuple[list, list, list]:
    """Format cars' info about characteristics, prices, locations"""

    fuel_types = ['Gasoline', 'Diesel', 'Ethanol', 'Electric', 'Hydrogen', 'LPG', 'CNG', 'Electric/Gasoline',
                  'Others', 'Electric/Diesel']
    fuel_pattern = '|'.join(fuel_types)
    gear = ['Automatic', 'Manual', 'Semi-automatic']
    gear_pattern = '|'.join(gear)
    # here we extract specific patterns of each car characteristics. The initial text that was extracted from web
    # scraping contains too much unrelated data
    for i in range(len(characteristics)):
        patterns = [r'\d{1,3}(?:,\d{3})*\s?km', f'({gear_pattern})', r'\d{1,2}/\d{4}', f'({fuel_pattern})',
                    r'(\d{1,3}(?:,\d{3})*) hp']
        characteristics[i] = [re.search(pattern, characteristics[i]).group(0).replace(',', '').replace(' km', '')
                              .replace(' hp', '').strip() if re.search(pattern, characteristics[i])
                              else None for pattern in patterns]
    # here we extract integer from price text
    for i in range(len(prices)):
        prices[i] = int(re.sub(r'\D', '', prices[i]))

    # here we extract only country abbreviation
    for i in range(len(locations)):
        try:
            locations[i] = locations[i].split('• ')[1].split('-')[0]
        except:
            locations[i] = locations[i].split('-')[0]

    return characteristics, prices, locations


def get_cars_info_lists(autoscout_url: str) -> tuple[list, list, list]:
    soups_list = get_main_htmls(autoscout_url)
    cars, characteristics, prices, locations = create_car_dataframes(
        soups_list)
    format_cars_info(characteristics, prices, locations)
    return cars, characteristics, prices, locations


def change_space_to_dash(makes_list: list) -> dict:
    """Create a blank list where we store all makes' names which contain space, for example 'Aston Martin'."""

    space_names = []
    for make in makes_list:
        if ' ' in make:
            space_names.append(make)

    # Here we create a dictionary where to each make with a space in the name is assigned the same make name but with a dash
    mapping_dict = {}
    for make_with_space in space_names:
        make_with_dash = make_with_space.replace(" ", "-")
        mapping_dict[make_with_space] = make_with_dash

    return mapping_dict


def replace_make_name(mapping_dict: dict, cars: str):
    """This function performs replacement of cars' makes with spaces into dashes '-'."""

    for make_with_space, make_with_dash in mapping_dict.items():
        if make_with_space in cars:
            cars = cars.replace(make_with_space, make_with_dash)
    return cars


def to_pandas(cars: list, characteristics: list, prices: list, locations: list) -> pd.DataFrame:
    """This function collects all previously formed lists and form 1 united dataframe in pandas."""

    # Here we transform our lists into pandas Series
    cars = pd.DataFrame(cars, columns=['make', 'model'])
    characteristics = pd.Series(characteristics)
    prices = pd.Series(prices, name='price')
    locations = pd.Series(locations, name='location')
    # Create a DataFrame from the Series, which splits the lists into columns
    df = pd.DataFrame(characteristics.tolist(), columns=[
                      'mileage', 'transmission', 'registration', 'fuel', 'power'])
    merged_df = pd.concat([cars, df], axis=1)
    merged_df2 = pd.concat([merged_df, locations], axis=1)
    main_pages_info = pd.concat([merged_df2, prices], axis=1)
    return main_pages_info


def get_clean_dataframe(autoscout_url: str) -> to_pandas:
    """Get a clean pandas dataframe."""
    # Read makes from CSV file
    with open("src/makes_list.csv", "r") as f:
        makes_list = [line.strip() for line in f if line.strip()]
    mapping_dict = change_space_to_dash(makes_list)
    cars, characteristics, prices, locations = get_cars_info_lists(
        autoscout_url)
    # Apply replacements to cars list
    cars = [replace_make_name(mapping_dict, car) for car in cars]
    # here we devide each string element of a list into 2 parts: car's make and car's model
    for car in range(len(cars)):
        cars[car] = cars[car].split(' ', 1)
    return to_pandas(cars, characteristics, prices, locations)


def load_to_postgres(autoscout_url: str, param='append') -> None:
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
    # Load the dataframe
    df = get_clean_dataframe(autoscout_url)
    # Set proper data types
    df['make'] = df['make'].astype(str)
    df['model'] = df['model'].astype(str)
    df['mileage'] = pd.to_numeric(
        df['mileage'], errors='coerce').astype('Int64')
    df['transmission'] = df['transmission'].astype(str)
    df['registration'] = pd.to_datetime(
        '01/' + df['registration'], format='%d/%m/%Y', errors='coerce').dt.date
    df['fuel'] = df['fuel'].astype(str)
    df['power'] = pd.to_numeric(df['power'], errors='coerce').astype('Int64')
    df['location'] = df['location'].astype(str)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').astype('Int64')

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
    df.to_sql(table_name, engine, schema='autoscout',
              if_exists=param, index=False, dtype=dtype)
    print(f'Table {table_name} was updated.')


if __name__ == '__main__':
    print('Script execution is started.')
    start = datetime.now()
    autoscout_url = 'https://www.autoscout24.com/'
    load_to_postgres(autoscout_url)
    end = datetime.now()
    print('Total time :', end - start)
