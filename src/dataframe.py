"""
This module creates a pandas dataframe from all the acquired information about the cars.
"""


import pandas as pd
import makes
import parsing

def change_space_to_dash(makes_list):
    """Create a blank list where we store all makes' names which contain space, for example 'Aston Martin'"""
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


def replace_make_name(mapping_dict, cars):
    """This function performs replacement of cars' makes with spaces into dashes '-'."""
    for make_with_space, make_with_dash in mapping_dict.items():
        if make_with_space in cars:
            cars = cars.replace(make_with_space, make_with_dash)
    return cars


def to_pandas(cars, characteristics, prices, locations):
    """This function collects all previously formed lists and form 1 united dataframe in pandas."""
    # Here we transform our lists into pandas Series
    cars = pd.DataFrame(cars, columns=['make', 'model'])
    characteristics = pd.Series(characteristics)
    prices = pd.Series(prices, name='price')
    locations = pd.Series(locations, name='location')
    # Create a DataFrame from the Series, which splits the lists into columns
    df = pd.DataFrame(characteristics.tolist(), columns=['mileage', 'transmission', 'registration', 'fuel', 'power'])
    merged_df = pd.concat([cars, df], axis=1)
    merged_df2 = pd.concat([merged_df, locations], axis=1)
    main_pages_info = pd.concat([merged_df2, prices], axis=1)
    return main_pages_info

def main(url):
    # Read makes from CSV file
    with open("src/makes_list.csv", "r") as f:
        makes_list = [line.strip() for line in f if line.strip()]
    mapping_dict = change_space_to_dash(makes_list)
    cars, characteristics, prices, locations = parsing.main(url)
    # Apply replacements to cars list
    cars = [replace_make_name(mapping_dict, car) for car in cars]
    # here we devide each string element of a list into 2 parts: car's make and car's model
    for car in range(len(cars)):
        cars[car] = cars[car].split(' ', 1)
    return to_pandas(cars, characteristics, prices, locations)
    

if __name__ == '__main__':
    url = 'https://www.autoscout24.com/'
    print(main(url))
