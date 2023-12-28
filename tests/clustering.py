import pandas as pd
from AI_masters_germany import utils, clustering, plotting

if __name__ == '__main__':
    df = pd.read_csv('../dataset.csv')
    df = utils.database_preprocessing(df=df, remove_stopwords=True)
    clustering_result = clustering.cluster_courses(
        df=df
    )
    plotting.plot_clusters(clustering_result)
