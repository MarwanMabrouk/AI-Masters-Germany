import pandas as pd
from AI_masters_germany import utils

if __name__ == '__main__':
    df = pd.read_csv('../dataset.csv')
    #print(df.head())
    print(df.iloc[15]['Course Description'])
    df = utils.database_preprocessing(df, remove_stopwords=True)
    #print(df.head())
    print(df.iloc[15]['Course Description'])
