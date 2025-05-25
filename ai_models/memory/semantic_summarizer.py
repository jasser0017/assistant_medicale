from groq import Groq
from transformers import AutoTokenizer

class SemanticSummarizer:
    def __init__(self, client: Groq, model="mistral-saba-24b"):
        self.client = client
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def summarize_to_50_tokens(self, role: str, message: str) -> str:
        if len(self.tokenizer.encode(message)) <= 20:
            return message


        prompt = (
            f"Tu es un assistant intelligent.\n"
            f"Ta tâche est de résumer un message {role} en 50 tokens maximum, "
            f"tout en conservant son sens principal et le contexte implicite.\n\n"
            f"Message original :\n{message}\n\n"
            f"Résumé :"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en résumé multilingue."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20
        )

        return response.choices[0].message.content.strip()



'''
if __name__ == "__main__":
    from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client=Groq(api_key=API_KEY)
preprocessor=SemanticSummarizer( client=client,model="mistral-saba-24b")

print(preprocessor.summarize_to_50_tokens(" Depuis plusieurs années, les scientifiques alertent sur les conséquences du réchauffement climatique. La fonte des glaciers, la montée du niveau des océans et les événements météorologiques extrêmes sont autant de signes de l'impact des activités humaines sur l’environnement. De nombreux gouvernements ont mis en place des politiques pour réduire les émissions de gaz à effet de serre, comme la promotion des énergies renouvelables ou le développement des transports propres. Cependant, les efforts restent insuffisants face à l'urgence climatique, et une action collective plus ambitieuse est nécessaire pour limiter les dégâts irréversibles."))

'''