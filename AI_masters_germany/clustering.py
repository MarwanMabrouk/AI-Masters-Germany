from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pandas as pd


def cluster_courses(df,
                    feature_columns=('Course Name', 'Course Description', 'Goals'),
                    sentence_transformer_model='distiluse-base-multilingual-cased-v1',
                    reduction_method='tsne',
                    n_clusters=48):
    """
    Cluster courses based on specified feature columns.

    :param df: Pandas DataFrame containing the database.
    :param feature_columns: DataFrame columns you want to use for clustering (e.g. 'Course Name', 'Goals').
    :param sentence_transformer_model: Which sBert model you want to use for the embedding calculation.
    :param reduction_method: Method to use in order to reduce dimensionality of the embeddings (can be 'tsne' or 'pca').
    :param n_clusters: Number of clusters for the K-Means clustering algorithm.
    :return: A pandas Dataframe with the columns: 'Component_1', 'Component_2', 'Cluster', 'Course Name'
    """

    if reduction_method.lower() not in ['tsne', 'pca']:
        raise ValueError('The only valid dimensionality reduction methods are "pca" and "tsne"!')

    model = SentenceTransformer(sentence_transformer_model)
    # Concat value of all the feature columns together
    # If the course name is used as a feature, make a sentence out of the name.
    if 'Course Name' in feature_columns:
        df['Course Name'] = df['Course Name'] + '.'
    model_input = np.array(df[list(feature_columns)].astype(str).agg(' '.join, axis=1))
    embeddings = model.encode(model_input)

    if reduction_method.lower() == 'tsne':
        X = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(embeddings)
    else:
        X = PCA(n_components=2).fit_transform(embeddings)

    k_means = KMeans(n_clusters=n_clusters, n_init='auto', random_state=0)
    clusters = k_means.fit_predict(X)

    result = pd.DataFrame(X, columns=['Component_1', 'Component_2'])
    result['Cluster'] = clusters
    result['Course Name'] = df['Course Name']

    return result
