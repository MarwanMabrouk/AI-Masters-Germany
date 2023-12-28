import pandas as pd
from AI_masters_germany import clustering, plotting

if __name__ == '__main__':
    df = pd.read_csv('../dataset.csv')
    clustering_result = clustering.cluster_courses(
        df=df
    )
