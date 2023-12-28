from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pandas as pd
from sklearn.metrics import silhouette_score


def cluster_courses(df,
                    feature_columns=('Course Name', 'Course Description', 'Goals'),
                    sentence_transformer_model='distiluse-base-multilingual-cased-v1',
                    reduction_method='tsne',
                    n_clusters='auto',
                    k_ranges=np.linspace(2, 401, 400)):
    """
    Cluster courses based on specified feature columns.

    :param df: Pandas DataFrame containing the database.
    :param feature_columns: DataFrame columns you want to use for clustering (e.g. 'Course Name', 'Goals').
    :param sentence_transformer_model: Which sBert model you want to use for the embedding calculation.
    :param reduction_method: Method to use in order to reduce dimensionality of the embeddings (can be 'tsne' or 'pca').
    :param n_clusters: Number of clusters for the K-Means clustering algorithm.
                       If set to 'auto', try to find the optimal amount of clusters bases on silhouette scores.
                       This is recommended if you don't need the result fast, since finding the amount
                       of clusters is computationally expensive.
    :param k_ranges: Different k_means k values that are going to be tested in order to find the optimal k.
                     Is only used when n_clusters is set to True!
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

    if n_clusters != 'auto':
        k_means = KMeans(n_clusters=n_clusters, n_init='auto')
        clusters = k_means.fit_predict(X)
    else:
        print('Start searching the optimal amount of clusters...')
        best_k = None
        best_score = float('-inf')

        for k in k_ranges:
            k = int(k)  # floats (like produced by np.linspace) cause python exceptions
            k_means = KMeans(n_clusters=k, n_init='auto')
            clusters = k_means.fit_predict(X)
            score = silhouette_score(X, clusters)
            print(f'k: {k} -> silhouette score: {score}')
            if score > best_score:
                best_k = k
                best_score = score

        # Search finished. We now have the estimated the optimal amount of clusters
        print(f'The optimal amount of clusters seems to be {best_k}.')
        # Now cluster again, but this time with the estimated optimal k.
        k_means = KMeans(n_clusters=best_k, n_init='auto')
        clusters = k_means.fit_predict(X)

    result = pd.DataFrame(X, columns=['Component_1', 'Component_2'])
    result['Cluster'] = clusters
    result['Course Name'] = df['Course Name']

    return result
