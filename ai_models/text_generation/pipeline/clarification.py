from ai_models.utils.methodes import clean_response
from groq import Groq

class Clarifier:
    def __init__(self, client, model="deepseek-r1-distill-llama-70b"):
        self.client = client
        self.model = model

    def check_ambiguity(self, user_input: str, intent: str) -> str | None:
        prompt = (
            f"L’intention de l’utilisateur est : « {intent} ».\n"
            f"Voici sa question : « {user_input} »\n\n"
            "Ta tâche est d’analyser la question de l’utilisateur.\n"
"Si elle est claire et ne nécessite pas de précision, réponds uniquement : « OK ».\n"
"Si elle est floue, incomplète ou ambiguë, propose UNE SEULE question de clarification, directe, sans aucune phrase d’introduction.\n"
"❌ Ne commence pas par « la question est imprécise » ou « pour clarifier ».\n"
"✅ Vas droit au but avec une seule reformulation utile."

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

        result = clean_response(response.choices[0].message.content.strip())
        if result.lower() in {"ok", "ok.", "non", "aucune clarification", "pas besoin"}:
            return None
        return result
'''
if __name__ == "__main__":
    from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client=Groq(api_key=API_KEY)
clarif=Clarifier(client=client, model="deepseek-r1-distill-llama-70b")
print("\n", clarif.check_ambiguity("j’ai très mal à la poitrine, ça me fait peur","urgence médicale"))

'''