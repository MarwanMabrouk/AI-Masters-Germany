from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

def encode_text(df,
                embedder,
                features='Course Name',
                ):
   
    corpus=np.array(df[list(features)].astype(str).agg(' '.join, axis=1))
    corpus_embeddings=embedder.encode(corpus,convert_to_tensor=True)
    return corpus_embeddings


def text_similarity(df,
                    query,
                    embedder,
                    corpus_embeddings,
                    top_k=5,
                    ):
    
        
    results={}
    query_embedding=embedder.encode(query,convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    results=top_results
    
    return results

