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
            "Tu es un assistant médical multilingue spécialisé dans la correction de texte.\n"
            "Corrige la requête suivante en respectant strictement ces consignes :\n"
            "- Corrige toutes les fautes d’orthographe, de grammaire et de formulation.\n"
                f"Phrase : {requete}\nCorrection :"
            )
        elif langue == "en":
            return (
                "You are a multilingual medical assistant specialized in text correction.\n"
                "Correct the following query while strictly following these rules:\n"
                "- Fix all spelling, grammar, and phrasing mistakes.\n"
                f"Sentence: {requete}\nCorrected:"
            )
        else:
            return (
                "The following sentence may be in any language."
                "You are a multilingual medical assistant specialized in text correction.\n"
                "Correct the following query while strictly following these rules:\n"
                "- Fix all spelling, grammar, and phrasing mistakes.\n"
                "without translating the sentence or altering its medical meaning.\n\n"
                f"Text:\n{requete}\n\nCorrected:"
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

  
    requete = "The doctor have wrote a perscription for the women who had feaver?"  
    try:
        correction = corrector.corriger_requete(requete)
        print("🧾 Requête originale :", requete)
        print("✅ Correction proposée :", correction)
    except Exception as e:
        print("❌ Erreur lors de la correction :", str(e))


