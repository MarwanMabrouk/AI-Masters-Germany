import pandas as pd
from AI_masters_germany import utils, clustering
import numpy as np
import time


class AIM:
    def __init__(self, collection_object):
        self.__collection_object = collection_object
        self.__database = pd.DataFrame(list(collection_object.find()))
        self.__database = utils.database_preprocessing(self.__database)
        self.__activated_clustering = False
        self.__course_clusters = None

    def get_database(self):
        return self.__database


    def cluster_courses(self, n_clusters='auto', k_ranges=np.linspace(80, 121, 40)):
        self.__activated_clustering = True

        self.__course_clusters = clustering.cluster_courses(
            df=self.__database,
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
