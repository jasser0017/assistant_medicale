import numpy as np
from ai_models.text_generation.embedders.nomic_embedder import NomicEmbedder
def select_best_mesh(query: str, mesh_terms: list[str]) -> str:
    embedder = NomicEmbedder()
    query_vec = np.array(embedder.embed([query])[0]).reshape(1, -1)
    mesh_vecs = np.array(embedder.embed(mesh_terms))

    similarities = (query_vec @ mesh_vecs.T)[0]  # produit scalaire car vecteurs unitaires (approx cosinus)
    best_idx = int(np.argmax(similarities))
    return mesh_terms[best_idx]