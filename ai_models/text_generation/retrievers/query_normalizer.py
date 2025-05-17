'''
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk, re, unicodedata

# (Re)vérification douce
for res in ["punkt", "stopwords", "wordnet"]:
    try:
        nltk.data.find(f"tokenizers/{res}" if res == "punkt" else f"corpora/{res}")
    except LookupError:
        nltk.download(res)

def normalize_query(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    filtered = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(filtered)
'''
import os
from groq import Groq
from dotenv import load_dotenv
import requests
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Normalizer:
    def __init__(self, model="mistral-saba-24b"):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model
        self.api_key =os.getenv("GROQ_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    def normalize_query(self,text: str) -> str:
        prompt = f"""
Tu es un assistant médical intelligent.

Ta tâche est de transformer une requête utilisateur en une suite courte de mots-clés médicaux utilisables dans une base PubMed.

❌ Ne fais pas de phrase.
❌ Ne reformule pas, ne résume pas.
✅ Garde uniquement les termes de recherche concrets (ex : symptômes, causes, maladies, organes, traitements).

Requête : "{text}"
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Tu es un assistant de normalisation de requêtes médicales."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Groq API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"].strip()




if __name__ == "__main__":
    normalize=Normalizer()
    text = "I want to know the possible complications of obesity?"
    print(normalize.normalize_query(text))
    
