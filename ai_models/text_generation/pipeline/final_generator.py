import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
class FinalGenerator:
    def __init__(self, api_key=API_KEY, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        if not api_key:
            raise ValueError("La clé API Groq n'est pas définie. Vérifie ton fichier .env.")
        self.client = Groq(api_key=api_key)
        self.model = model
    def generate(self,question: str,intent: str,clarification: str | None ,rag_snippets: list[str],memory: dict,user_profile: str) -> str:
        """
        Génère la réponse finale du chatbot.

        :param question: question utilisateur (clarifiée si applicable)
        :param intent: intention détectée
        :param clarification: texte de clarification (si présent)
        :param rag_snippets: extraits RAG optionnels
        :param memory: dictionnaire d'informations médicales connues
        :param user_profile: ex. "Patient" ou "Médecin"
        :return: réponse générée
        """

        
        system_prompt = (
            "Tu es un assistant médical intelligent multilingue. "
            "Tu fournis des réponses claires, rigoureuses et adaptées au profil : "
            f"{user_profile.lower()}.\n"
            "Réponds toujours dans la langue utilisée par l'utilisateur.\n"
            "Si la question relève d’un domaine critique (urgence, cancer...), reste neutre et suggère de consulter un professionnel."
        )

        context_parts = [f"🧠 Intention détectée : {intent}"]
        if clarification:
            context_parts.append(f"❓ Clarification : {clarification}")
        if memory:
            memory_str = "\n".join(f"{k}: {v}" for k, v in memory.items())
            context_parts.append(f"📂 Dossier connu :\n{memory_str}")
        if rag_snippets:
            context_parts.append("📚 Informations scientifiques :\n" + "\n---\n".join(rag_snippets))

        context_parts.append(f"📝 Question : {question}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n\n".join(context_parts)}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    generator=FinalGenerator()
    print(generator.generate())