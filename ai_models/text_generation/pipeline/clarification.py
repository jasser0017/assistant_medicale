from dotenv import load_dotenv
from groq import Groq
import re
import os

from ai_models.utils.methodes import clean_response

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

class Clarifier:
    def __init__(self, api_key=API_KEY, model="deepseek-r1-distill-llama-70b"):
        if not api_key:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = Groq(api_key=api_key)
        self.model = model
    def check_ambiguity(self, user_input: str, intent: str) -> str | None:
        prompt = (
            f"L’intention de l’utilisateur est : « {intent} ».\n"
            f"Voici sa question : « {user_input} »\n\n"
            "Cette question est-elle incomplète, imprécise ou ambiguë ? "
            "Si oui, propose UNE SEULE question de clarification à poser à l'utilisateur. "
            "Sinon, réponds uniquement : « OK »."
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant médical spécialisé dans la reformulation et la précision. "
                    "Tu détectes automatiquement les questions floues ou imprécises."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=700
        )

        result =  clean_response(response.choices[0].message.content.strip())
        if result.lower() in {"ok", "ok.", "non", "aucune clarification", "pas besoin"}:
            return None
        return result
if __name__ == "__main__":
    clarif=Clarifier()
    print("\n", clarif.check_ambiguity("je veux parler a props le cancer de sein","question médicale – diagnostic"))

