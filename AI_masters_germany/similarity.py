from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

def encode_text(df,
                embedder,
                features='Course Name',
                ):
    """Generates embeddings for course names, description and goals in the database

    Args:
        df (Pandas Dataframe): Database of courses loaded as pandas dataframe
        embedder (Sentence Transformer): Defines embedding model used to encode corpus
        features (str, optional): set the attribute to be included in the embedding, can also include description 
                                  and goals. Defaults to 'Course Name'.

    Returns:
        Sentence Embeddings: encoded text as sentence embeddings
    """    
   
    corpus=np.array(df[list(features)].astype(str).agg(' '.join, axis=1))
    corpus_embeddings=embedder.encode(corpus,convert_to_tensor=True)
    return corpus_embeddings


def text_similarity(query,
                    embedder,
                    corpus_embeddings,
                    top_k=5,
                    ):
    """Extracts highest similar courses to user input

    Args:
        query (Str): Query inserted by user
        embedder (Sentence Transformer): Defines embedding model used to encode query
        corpus_embeddings (sentence embeddings): generated embeddings for entire corpus
        top_k (int, optional): Top k results returned by retriever. Defaults to 5.

    Returns:
        List: List of tuples with most similar courses and their similarity score to query
    """    
        
    results={}
    query_embedding=embedder.encode(query,convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    results=top_results
    
    return results

