

import os
import requests
from dotenv import load_dotenv

load_dotenv()
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")

class NomicEmbedder:
    def __init__(self):
        if not NOMIC_API_KEY:
            raise ValueError("❌ Clé API Nomic manquante dans le .env")

        self.api_key = NOMIC_API_KEY
        self.endpoint = "https://api-atlas.nomic.ai/v1/embedding/text"

    def embed(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
    "model": "nomic-embed-text-v1",
    "texts": texts
}


        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Erreur API Nomic: {response.status_code} - {response.text}")

        return response.json()["embeddings"]
    

    #tout d'abord on verifieer si L'API key est definie ou non , 
    #si non un messge d'erreur va appartre sinon on commence 
    #a construire la classe NomicEmbeder et on stocke au sein
    #de lui lURL et l API key, puis on defini la methode embed
    #qui prend en parametre une liste de texte et nous rendre 
    #vecteur numerique(embedding), cette methode contient 2 dictionnaire
    #headers qui contient 2 attribut Autorization qui nous permet de l acces
    #content-text qui donne une idee au fonction que le retour doit en json
    #et l autre dictionnaire est payload contient 2 attribut de meme qui
    #represente le model et le type d'entree 
