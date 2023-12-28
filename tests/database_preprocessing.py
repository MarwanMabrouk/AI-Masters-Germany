import pandas as pd
from AI_masters_germany import utils

if __name__ == '__main__':
    df = pd.read_csv('../dataset.csv')
    print(df.head())
    df = utils.database_preprocessing(df)
    print(df.head())

