import pandas as pd
from AI_masters_germany import utils, clustering
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')
class AIM:
    """Class that handles course clustering features
    """    
    def __init__(self, collection_object):
        self.__collection_object = collection_object
        self.__database = pd.DataFrame(list(collection_object.find()))
        self.__preprocessed_database = utils.database_preprocessing(self.__database)
        self.__activated_clustering = False
        self.__course_clusters = None

    def get_database(self, unprocessed=False):
        if unprocessed:
            return self.__database
        else:
            return self.__preprocessed_database


    def cluster_courses(self, n_clusters='auto', k_ranges=np.linspace(80, 121, 40)):
        """handles cluster_courses function

        Args:
            n_clusters (str, optional): 
            Number of clusters for the K-Means clustering algorithm. Defaults to 'auto'.
            If set to 'auto', try to find the optimal amount of clusters bases on silhouette scores.
                       This is recommended if you don't need the result fast, since finding the amount
                       of clusters is computationally expensive.
            k_ranges (_type_, optional): Different k_means k values that are going to be tested in order to find the optimal k.
                                         Defaults to np.linspace(80, 121, 40).

        Returns:
            pandas Dataframe: 'Component_1', 'Component_2', 'Cluster Name', 'Course Name',
                                                    'Course Name','Degree Name','Uni Name'
        """        
        self.__activated_clustering = True

        self.__course_clusters = clustering.cluster_courses(
            df=self.__preprocessed_database,
            n_clusters=n_clusters,
            k_ranges=k_ranges
        )

        return self.__course_clusters

    def get_clustered_courses(self):
        if not self.__activated_clustering:
            raise ValueError('You need to start clustering before trying to get the clustering results!')
        else:
            while self.__course_clusters is None:
                print('Waiting for the clustering to finish...')
                time.sleep(2)
            return self.__course_clusters
