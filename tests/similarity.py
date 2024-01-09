import pandas as pd
from AI_masters_germany import utils,similarity
import numpy as np


if __name__ == '__main__':
    df = pd.read_csv('../dataset.csv')
    df = utils.database_preprocessing(df=df, remove_stopwords=True)
    #corpus=list(df['Course Name'])
    df['Course Name']=df['Course Name']+'.'
    corpus=np.array(df[list(('Course Name','Course Description','Goals'))].astype(str).agg(' '.join, axis=1))
    corpus_embeddings=similarity.encode_text(df=df,sentence_transformer_model='msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned')
    queries=['Natural Language Processing','High Performance Computing','Data Analytics','Learning Analytics',
             'Computer Vision','AI Ethics','Linear Algebra','Discrete Mathematics','Data Science','Masters Thesis','Algorithms','Modern optimization techniques','Information Mining','Machine Learning','Deep Learning','Neuroinformaatik','Computational Linguistics']
    similarity_results=similarity.text_similarity(df=df,corpus_embeddings=corpus_embeddings,queries=queries,sentence_transformer_model='msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned')

    for query in queries:
        top_results=similarity_results[query]
        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")
        for score,idx in zip(top_results[0],top_results[1]):
            print(corpus[idx].split('.')[0], "(Score: {:.4f})".format(score))
