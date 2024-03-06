from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np


def encode_text(df, embedder, features='Course Name'):
    """
    Generate embeddings based on course feature(s).

    :param df: Database loaded as pandas dataframe.
    :param embedder: Defines embedding model used to encode corpus.
    :param features: Define attribute(s) to be included in the embedding.
                     Defaults to 'Course Name', but could also include course descriptions and goals.

    :return: Encoded text as sentence embeddings.
    """
    # First we are going to extract the feature-columns and join them by whitespaces
    corpus = np.array(df[list(features)].astype(str).agg(' '.join, axis=1))
    # Apply sentence transformer on our data
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    return corpus_embeddings


def text_similarity(query, embedder, corpus_embeddings, top_k=5):
    """
    Extracts most similar courses to user input.

    :param query: Query inserted by user.
    :param embedder: Defines embedding model used to encode query.
    :param corpus_embeddings: Generated embeddings for entire corpus.
    :param top_k: Chose how many top results to return. Defaults to 5 (for top 5 most similar courses).

    :return: List of tuples with most similar courses and their similarity score to query.
    """    
        
    results={}
    query_embedding=embedder.encode(query,convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    results=top_results
    
    return results

