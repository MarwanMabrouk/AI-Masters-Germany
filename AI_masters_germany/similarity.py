from sentence_transformers import SentenceTransformer, util
import torch

def encode_text(df,
                feature='Course Name',
                sentence_transformer_model='distiluse-base-multilingual-cased-v1'):
    
    corpus=df[feature]
    embedder=SentenceTransformer(sentence_transformer_model)
    corpus_embeddings=embedder.encode(corpus,convert_to_tensor=True)
    return corpus_embeddings


def text_similarity(df,
                    corpus_embeddings,
                    queries,
                    top_k=5,
                    sentence_transformer_model='distiluse-base-multilingual-cased-v1'):
    
    embedder=SentenceTransformer(sentence_transformer_model)
    results={}
    
    for query in queries:
        query_embedding=embedder.encode(query,convert_to_tensor=True)
        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        results[query]=top_results
    
    return results