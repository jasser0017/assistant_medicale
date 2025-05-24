from groq import Groq


from ai_models.utils.methodes import clean_response


class IntentClassifier:
    def __init__(self, client, model="qwen-qwq-32b"):
        self.client = client
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

'''
if __name__ == "__main__":
    from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client=Groq(api_key=API_KEY)
preprocessor=IntentClassifier( client=client,model="mistral-saba-24b")

print(preprocessor.classify("j’ai très mal à la poitrine, ça me fait peur"))

'''
