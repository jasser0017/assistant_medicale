import json
import os
from ai_models.text_generation.retrievers.medical_query_corrector import QueryCorrector
from ai_models.text_generation.retrievers.query_normalizer import Normalizer
import numpy as np
from dotenv import load_dotenv
import faiss
from rank_bm25 import BM25Okapi
from ai_models.text_generation.embedders.nomic_embedder import NomicEmbedder
from ai_models.text_generation.retrievers.pumbed_downloader import download_pubmed
from ai_models.utils.methodes import detect_language, translate_if_needed
from ai_models.utils.query_enricher import build_enriched_query
import joblib
from typing import List, Dict
import hashlib


EMBED_CACHE_DIR = "data/.embed_cache"
ARTICLE_CACHE_DIR = "data/article_cache"
INDEX_DIR = "data/index_cache"
os.makedirs(ARTICLE_CACHE_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
embed_cache = joblib.Memory(location=EMBED_CACHE_DIR, verbose=0)

class RAGRetriever:
    def __init__(self):
        self.embedder = NomicEmbedder()
        self.corrector = QueryCorrector()
        self.normalize=Normalizer()
        self.texts: List[str] = []
        self.metadatas: List[Dict] = []
        self._embed = embed_cache.cache(self.embedder.embed)
        self._article_cache: Dict[str, List[Dict]] = {}
        self.index = None
        self.cache_index_path = None  

    def _slug(self, text: str, log: bool= False) -> str:
        try:
            corrected = self.corrector.corriger_requete(text)
        except Exception as e:
            print(f"⚠️ Correction impossible, utilisation brute : {e}")
            corrected = text
        translated = translate_if_needed(corrected)
       
        normalized =self.normalize.normalize_query(translated)
        if log:
            print("🧾 🔍 TRAITEMENT DE LA REQUÊTE UTILISATEUR")
            print(f"📌 Originale    : {text}")
            print(f"🩺 Corrigée     : {corrected}")
            print(f"🌍 Traduite     : {translated}")
            print(f"🧹 Normalisée   : {normalized}")
            print("-" * 60)       
        return hashlib.md5(normalized.encode()).hexdigest()

    def _cache_path_for_query(self, query: str) -> str:
        slug = self._slug(query)
        return os.path.join(ARTICLE_CACHE_DIR, f"{slug}.json")

    def _faiss_index_path_for_query(self, query: str) -> str:
        slug = self._slug(query)
        return os.path.join(INDEX_DIR, f"faiss_index_{slug}.bin")

    def _load_articles_from_disk(self, query: str) -> List[Dict]:
        fpath = self._cache_path_for_query(query)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_articles_to_disk(self, query: str, articles: List[Dict]):
        fpath = self._cache_path_for_query(query)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

    def collect_articles(self, query: str, max_docs: int = 50, force_refresh: bool = False) -> List[Dict]:
        if not force_refresh and query in self._article_cache:
            return self._article_cache[query]

        if not force_refresh:
            disk_cached = self._load_articles_from_disk(query)
            if disk_cached:
                self._article_cache[query] = disk_cached
                print(f"✅ Chargé {len(disk_cached)} articles en cache.")
                return disk_cached

        print(f"\n🔍 Récupération multi-sources avec enrichissement UMLS pour : {query}")
        try:
            enriched_query = build_enriched_query(query)
            download_pubmed(enriched_query, max_results=max_docs)
            slug = hashlib.md5(enriched_query.encode()).hexdigest()
            pubmed_path = os.path.join("data", f"pubmed_articles_{slug}.json")
        except Exception as e:
            print(f"Error fetching articles: {e}")
            return []

        all_articles = []
        if os.path.exists(pubmed_path):
            with open(pubmed_path, "r", encoding="utf-8") as f:
                pubmed_articles = json.load(f)
                for art in pubmed_articles:
                    if art.get("title") and art.get("abstract"):
                        all_articles.append({
                        "title": art["title"],
                        "abstract": art["abstract"],
                        "pmid": art.get("pmid")
        })


        print(f"📚 Articles totaux collectés : {len(all_articles)}")

        abstracts = [a['abstract'].split() for a in all_articles if isinstance(a.get("abstract"), str)]
        if not abstracts:
            print("⚠️ Aucun article n'a été trouvé ou indexé. BM25 désactivé.")
            self._article_cache[query] = []
            self._save_articles_to_disk(query, [])
            return []

        bm25 = BM25Okapi(abstracts)
        bm25_scores = bm25.get_scores(enriched_query.split())
        scored = list(zip(bm25_scores, all_articles))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [art for _, art in scored[:max_docs]]

        print(f"✅ Top {len(selected)} articles sélectionnés par BM25.")

        self._article_cache[query] = selected
        self._save_articles_to_disk(query, selected)
        return selected

    def index_articles_from_list(self, query: str, rebuild: bool = False):
        self.cache_index_path = self._faiss_index_path_for_query(query)
        meta_path = self.cache_index_path + ".meta"

        if not rebuild and os.path.exists(self.cache_index_path) and os.path.exists(meta_path):
            print("ℹ️  Index déjà présent – chargement.")
            self.load_index()
            return

        articles = self.collect_articles(query, max_docs=50)
        texts, metadatas = [], []
        for article in articles:
            text = article["title"] + "\n\n" + article["abstract"]
            texts.append(text)
            metadatas.append({
                "pmid": article["pmid"],
                "title": article["title"]
            })

        embeddings = self._embed(texts)
        embeddings_np = np.array(embeddings).astype("float32")

        if embeddings_np.size == 0:
            print("⚠️ Embeddings vides — indexation interrompue.")
            return  False

        self.index = faiss.IndexFlatL2(embeddings_np.shape[1])
        self.index.add(embeddings_np)

        self.texts = texts
        self.metadatas = metadatas

        print("✅ Indexation terminée avec FAISS.")
        faiss.write_index(self.index, self.cache_index_path)
        with open(meta_path, "wb") as f:
            joblib.dump((self.texts, self.metadatas), f)
        print(f"💾 FAISS index enregistré à {self.cache_index_path}")
        return True

    def load_index(self):
        if not os.path.exists(self.cache_index_path):
            raise FileNotFoundError(f"❌ Aucun index trouvé à {self.cache_index_path}.")
        meta_path = self.cache_index_path + ".meta"
        self.index = faiss.read_index(self.cache_index_path)
        with open(meta_path, "rb") as f:
            self.texts, self.metadatas = joblib.load(f)
        print(f"✅ Index chargé ({len(self.texts)} passages).")

    def query(self, question: str, top_k: int = 5):
        if self.index is None:
            self.load_index()
        query_embedding = self._embed([question])[0]
        query_vec = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            doc = self.texts[idx]
            meta = self.metadatas[idx]
            results.append((doc, meta))
        return results
    def retrieve_snippets(self, query: str, top_k: int = 5) -> list[str]:

        print(f"📥 Récupération de snippets pour : {query}")
        self._slug(query, log=True)
        self.index_articles_from_list(query)
        

        try:
            results = self.query(query, top_k=top_k)
        except FileNotFoundError as e:
            print(f"❌ Erreur : {e}")
            return []
        if not results:
            print("❌ Aucun document trouvé pour cette requête.")
            return []
        snippets = []

        for doc, meta in results:
            snippet = f"{meta['title']}\n\n{doc}"
            snippets.append(snippet)

        return snippets



if __name__ == "__main__":
    rag = RAGRetriever()
    query = "quelles sont les symptomes de diabetes ?"
    print(rag.retrieve_snippets("oui,j'ai mal a la ventre hier"))

