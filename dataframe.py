import pandas as pd


def df_construct (marks_menu, cars, characteristics, prices, locations):
    # here we create a blank list where we store all marks names which contain space, for example 'Aston Martin'
    space_names = []
    for mark in marks_menu:
        if ' ' in mark:
            space_names.append(mark)

    # Here we create a dictionary where to each mark with a space in the name is assigned the same mark name but with a dash
    mapping_dict = {}
    for mark_with_space in space_names:
        mark_with_dash = mark_with_space.replace(" ", "-")
        mapping_dict[mark_with_space] = mark_with_dash

    # This function performs replacement of cars' marks with spaces into dashes '-'
    def replace_mark_name(name):
        for mark_with_space, mark_with_dash in mapping_dict.items():
            if mark_with_space in name:
                name = name.replace(mark_with_space, mark_with_dash)
        return name

    # Apply replacements to cars list
    cars = [replace_mark_name(item) for item in cars]

    # here we devide each string element of a list into 2 parts: car's mark and car's model
    for car in range(len(cars)):
        cars[car] = cars[car].split(' ', 1)

    # This function collects all previously formed lists and form 1 united dataframe in pandas
    def to_pandas():
        # Here we transform our lists into pandas Series
        c = pd.DataFrame(cars, columns=['mark', 'model'])
        ch = pd.Series(characteristics)
        p = pd.Series(prices, name='price')
        l = pd.Series(locations, name='location')
        # Create a DataFrame from the Series, which splits the lists into columns
        df = pd.DataFrame(ch.tolist(), columns=['mileage', 'transmission', 'registration', 'fuel', 'power'])
        merged_df = pd.concat([c, df], axis=1)
        merged_df2 = pd.concat([merged_df, l], axis=1)
        main_pages_info = pd.concat([merged_df2, p], axis=1)
        return main_pages_info

    return to_pandas()


if __name__ == '__main__':
    pass
