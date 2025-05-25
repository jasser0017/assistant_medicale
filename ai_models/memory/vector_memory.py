from ai_models.memory.semantic_summarizer import SemanticSummarizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from collections import deque



class VectorMemory:
    def __init__(self, maxlen=20,summarizer: SemanticSummarizer | None = None):
        self.maxlen = maxlen
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.reset()
        self.summarizer = summarizer  

    def reset(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.vectors = []
        self.history = deque(maxlen=self.maxlen)
        self.current_session_id = None  

    def start_session(self, session_id: str):
        if self.current_session_id != session_id:
            self.reset()
            self.current_session_id = session_id

    def add(self, user_msg: str, bot_msg: str):
        if self.summarizer:
            user_msg = self.summarizer.summarize_to_50_tokens("utilisateur", user_msg)
            bot_msg = self.summarizer.summarize_to_50_tokens("assistant", bot_msg)

        text = f"Utilisateur : {user_msg}\nAssistant : {bot_msg}"
        self.history.append(text)
        embedding = self.model.encode([text])[0].astype("float32")
        self.vectors.append(embedding)
        self.index.add(np.array([embedding]))

    def retrieve(self, current_input: str, top_k=3) -> list[str]:
        if not self.vectors:
            return []
        query_embedding = self.model.encode([current_input])[0].astype("float32").reshape(1, -1)
        _, indices = self.index.search(query_embedding, top_k)
        return [self.history[i] for i in indices[0] if i < len(self.history)]
