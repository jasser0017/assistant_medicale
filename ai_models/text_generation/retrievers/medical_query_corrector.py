import requests
import os
from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

class QueryCorrector:
    def __init__(self):
        self.api_key = os.getenv("COHERE")
        self.api_url = "https://api.cohere.ai/v1/generate"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _build_prompt(self, requete: str) -> str:
        """
        Construit dynamiquement un prompt en fonction de la langue détectée.
        """
        try:
            langue = detect(requete)
        except:
            langue = "unknown"

        if langue == "fr":
            return (
                "Tu es un assistant médical multilingue spécialisé dans la correction linguistique stricte."

                "Corrige la phrase suivante en respectant exclusivement les règles suivantes :"

                "✅ Corrige les fautes d’orthographe, de grammaire et de conjugaison."

                "❌ N’ajoute aucun mot."

                "❌ Ne supprime aucun mot."

                "❌ Ne reformule pas le style ni la structure de la phrase."

                f"Phrase à corriger : {requete}"
            )
        elif langue == "en":
            return (
               " You are a multilingual medical assistant specialized in strict linguistic correction."

                "Your task is to correct the following sentence while following these exact rules:"

                "✅ Fix all spelling, grammar, and verb conjugation errors."

                "❌ Do not add any words."

                "❌ Do not remove any words."

                "❌ Do not change the structure or phrasing."

                f"Sentence: {requete}"

            )
        else:
            return (
               "You are a multilingual medical assistant specialized in strict linguistic correction."

                "Your task is to correct the text below without translating it or altering its medical meaning, and while following these exact rules:"

                "✅ Correct all spelling, grammar, and verb conjugation errors."

                "❌ Do not translate the sentence."

                "❌ Do not add, remove, or replace any words unless required for grammar correction."

                "❌ Do not change the structure or phrasing beyond necessary grammatical fixes."

                "✅ Preserve the original wording and medical intent as much as possible."

                f"Text:{requete}"
            )

    def corriger_requete(self, requete: str) -> str:
        prompt = self._build_prompt(requete)

        data = {
            "model": "command-r-plus",
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.2
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json()["generations"][0]["text"].strip()
        else:
            raise Exception(f"Erreur API Cohere : {response.status_code} - {response.text}")


if __name__ == "__main__":
    corrector = QueryCorrector()

  
    requete = " Les symptômes du diabète de type 1"  
    try:
        correction = corrector.corriger_requete(requete)
        print("🧾 Requête originale :", requete)
        print("✅ Correction proposée :", correction)
    except Exception as e:
        print("❌ Erreur lors de la correction :", str(e))


