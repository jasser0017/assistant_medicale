from groq import Groq
from dotenv import load_dotenv
import os

from ai_models.utils.methodes import clean_response


load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
class IntentClassifier:
    def __init__(self, api_key=API_KEY, model="qwen-qwq-32b"):
        if not api_key:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = Groq(api_key=api_key)
        self.model = model
        
        self.labels = [
            "question médicale – éducation",
            "question médicale – prévention",
            "question médicale – diagnostic",
            "urgence médicale",
            "prise de rendez-vous",
            "discussion générale",
            "autre"
        ]

    def classify(self, user_input: str) -> str:
        prompt = (
            f"Analyse la requête suivante et classe-la dans UNE SEULE des catégories suivantes :\n"
            f"{', '.join(self.labels)}.\n"
            "Réponds uniquement par le nom de la catégorie, sans explication, "
            "et dans la même langue que la requête de l'utilisateur."
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant médical multilingue. "
                    "Tu comprends automatiquement la langue utilisée, et tu réponds dans la même langue."
                )
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nRequête utilisateur : « {user_input} »"
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500
        )

        return clean_response(response.choices[0].message.content.strip())
if __name__ == "__main__":
    intent=IntentClassifier()

    #print("\n",  intent.classify("hello my name is jasser allela and i use Clear for men"))
    #print("\n",  intent.classify("Fuck off"))
    #print("\n",  intent.classify("quelles sont les symptomes de diabetes ???"))
    #print("\n",  intent.classify("مرحباً، اسمي جاسر أليل وأستخدم Clear للرجال"))
    #print("\n",  intent.classify("你好，我叫 Jasser Allele，我用的是 Clear 男士护理产品"))

    print("\n",  intent.classify("je veux savoir des informations a propos le cancer de sein "))
    print("\n",  intent.classify("on peut parler de football"))
