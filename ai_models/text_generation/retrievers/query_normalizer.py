
from groq import Groq

import requests



class Normalizer:
    def __init__(self,client, model="mistral-saba-24b"):
        self.model = model
        self.client=client
    def normalize_query(self,text: str) -> str:
        prompt = f"""
Tu es un assistant médical intelligent.

Ta tâche est de transformer une requête utilisateur en une suite courte de mots-clés médicaux utilisables dans une base PubMed.

❌ Ne fais pas de phrase.
❌ Ne reformule pas, ne résume pas.
✅ Garde uniquement les termes de recherche concrets (ex : symptômes, causes, maladies, organes, traitements).

Requête : "{text}"
"""
        messages = [
            {"role": "system", "content": "Tu es un assistant de normalisation de requêtes médicales."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()




'''
if __name__ == "__main__":
    normalize=Normalizer()
    text = "I want to know the possible complications of obesity?"
    print(normalize.normalize_query(text))
   ''' 
