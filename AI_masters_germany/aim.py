import pandas as pd
from AI_masters_germany import utils, clustering
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')


class AIM:
    """
    Class that offers interface to course clustering related operations.

    Used as a generalizing method to load database, get preprocessed database
    and more (e.g., start course clustering).

    Was implemented to easily introduce course clustering in threads,
    in order to avoid letting the user wait minutes for the course clustering to finish
    before visiting the website.
    """    
    def __init__(self, collection_object):
        self.__collection_object = collection_object
        self.__database = pd.DataFrame(list(collection_object.find()))  # Fetch everything from the database and convert to pandas DataFrame
        self.__preprocessed_database = utils.database_preprocessing(self.__database)  # Preprocesses the whole (DataFrame) dataset
        self.__activated_clustering = False
        self.__course_clusters = None

    def get_database(self, unprocessed=False):
        """Depending on the parameter unprocessed, return either the preprocessed or unprocessed database"""
        if unprocessed:
            return self.__database
        else:
            return self.__preprocessed_database

    def cluster_courses(self, n_clusters='auto', k_ranges=np.linspace(80, 121, 40)):
        """
        Do course clustering

        Will be started in a thread in app.py in order to avoid letting the user wait minutes for the course clustering
        to finish before being able to visit the website.

        :param n_clusters: Number of clusters for the K-Means clustering algorithm. Defaults to 'auto'.
                           If set to 'auto', try to find the optimal amount of clusters bases on silhouette
                           scores. This is recommended if you don't need the result fast, since finding the
                           amount of clusters is computationally expensive.
        :param k_ranges: Different k_means k values that are going to be tested in order to find the optimal k.
                         Defaults to np.linspace(80, 121, 40).

        :return: pandas Dataframe with 'Component_1', 'Component_2', 'Cluster Name', 'Course Name', 'Course Name',
                 'Degree Name','Uni Name'
        """        
        self.__activated_clustering = True

        self.__course_clusters = clustering.cluster_courses(
            df=self.__preprocessed_database,
            n_clusters=n_clusters,
            k_ranges=k_ranges
        )

        return self.__course_clusters

    def get_clustered_courses(self):
        """
        Wait until course clustering finishes and then return the clustered courses. If course clustering
        wasn't started yet, raise Exception.

        :return: Clustered courses
        """
        if not self.__activated_clustering:
            raise ValueError('You need to start clustering before trying to get the clustering results!')
        else:
            while self.__course_clusters is None:
                print('Waiting for the clustering to finish...')
                time.sleep(2)
            return self.__course_clusters
