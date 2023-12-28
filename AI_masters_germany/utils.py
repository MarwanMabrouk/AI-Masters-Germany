import pandas as pd


def database_preprocessing(df):
    """
    Database preprocessing function.

    :param df: A pandas dataframe (e.g., result of pandas.read_csv method).
    :return: A preprocessed pandas dataframe.
    """
    # Remove most special characters
    df = df.replace(to_replace=r'[^A-Za-z0-9äÄöÖüÜ.,-: ]', value='', regex=True)

    # 'Mandatory?' is boolean, but database contains different ways of specifying yes/no (e.g., 'PP' and 'WP')
    # Let's fix that!
    df['Mandatory?'] = df['Mandatory?'].fillna('y')  # Default for N.A. values is that the course is mandatory
    # It's important to first fill up the N.A. values and then apply conversion to string + lowering!
    df['Mandatory?'] = df['Mandatory?'].apply(lambda x: str(x).lower())  # Make whole df lowercase (except column names)
    df['Mandatory?'] = df['Mandatory?'].replace('pp', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('yes', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('obligatory', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('wp', 'n')
    df['Mandatory?'] = df['Mandatory?'].replace('elective', 'n')
    df['Mandatory?'] = df['Mandatory?'].replace('no', 'n')
    # todo: fix dataset TU Chemnitz entries
    df['Mandatory?'] = df['Mandatory?'].apply(lambda x: 'n' if x not in ['y', 'n'] else x)
    return df
