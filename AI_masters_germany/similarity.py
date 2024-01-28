from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

def encode_text(df,
                features='Course Name',
                sentence_transformer_model='distiluse-base-multilingual-cased-v1'):
   
    corpus=np.array(df[list(features)].astype(str).agg(' '.join, axis=1))
    embedder=SentenceTransformer(sentence_transformer_model)
    corpus_embeddings=embedder.encode(corpus,convert_to_tensor=True)
    return corpus_embeddings


def text_similarity(df,
                    query,
                    top_k=5,
                    sentence_transformer_model='distiluse-base-multilingual-cased-v1'):
    
    embedder=SentenceTransformer(sentence_transformer_model)
    results={}
    corpus_embeddings=encode_text(df,features=['Course Name','Course Description','Goals'],sentence_transformer_model=sentence_transformer_model)
    query_embedding=embedder.encode(query,convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    results=top_results
    
    return results

