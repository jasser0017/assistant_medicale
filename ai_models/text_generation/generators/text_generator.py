import os
from dotenv import load_dotenv
from groq import Groq



load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

class GroqTextGenerator:
    def __init__(self, api_key=API_KEY, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        if not api_key:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = Groq(api_key=api_key)
        self.model = model
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        
    
           
        system_instruction = (
        "You are a **multilingual medical assistant**. "
        "First, identify the language of the user message and respond in that same language. "
        "Ensure that all units of measure and drug names are localized appropriately. "
        "Provide clear, precise, professional medical information without requiring any external language‐detection service."
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
    prompt_fr = " quelle est le Efferalgan."
    print("FR >>", generator.generate(prompt_fr))

    # Test avec une question en anglais
    prompt_en = "¿Cuáles son los síntomas más comunes de la hipertensión arterial??"
    #print("\nEN >>", generator.generate(prompt_en))

    prompt_allmend="Was ist Gesichtslähmung?"
    #print("\nALL>>",generator.generate(prompt_allmend))

    prompt_arabe="ما هو شلل الوجه"
    #print("\nArabe>>",generator.generate(prompt_arabe))

    prompt_chinois="什么是面瘫"
    #print("\nchinois", generator.generate(prompt_chinois))



