import os
from dotenv import load_dotenv
from groq import Groq
from langdetect import detect  


load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

class GroqTextGenerator:
    def __init__(self, api_key=API_KEY, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        if not api_key:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 1120) -> str:
        """
        Génère un texte médical en respectant la langue du prompt.
        
        Args:
            prompt (str): La question ou sujet à traiter.
            max_tokens (int): Longueur maximale du texte généré.
        
        Returns:
            str: Le texte généré par le modèle.
        """
        
        lang = detect(prompt)

        if lang == "fr":
            system_instruction = (
                "Tu es un assistant médical expert. "
                "Tu réponds exclusivement en français, avec rigueur et clarté. "
                "Tes réponses sont adaptées à un public médical ou de patients selon la question."
            )
        elif lang == "en":
            system_instruction = (
                "You are a medical assistant. "
                "Always respond in English, clearly and professionally. "
                "Your answers should be tailored to the user's level (expert or patient)."
            )
        else:
           
            system_instruction = (
                "You are a helpful medical assistant. "
                "Always respond in the same language as the user prompt."
            )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

# Test rapide
if __name__ == "__main__":
    generator = GroqTextGenerator()

    # Test avec une question en français
    prompt_fr = " quelle est la paralysie faciale."
    print("FR >>", generator.generate(prompt_fr))

    # Test avec une question en anglais
    prompt_en = "¿Cuáles son los síntomas más comunes de la hipertensión arterial??"
    print("\nEN >>", generator.generate(prompt_en))
