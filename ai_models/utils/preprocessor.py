from groq import Groq
import requests


class Preprocessor:
    def __init__(self,client,model="mistral-saba-24b") :
        self.client= client
        self.model=model
    
    def normalize_question(self, user_input:str)->str:
        
        prompt=("You are an assistant specialized in rewriting vague, poorly written, or informal user input intended for medical purposes."

"Your task is to rephrase the original input so it becomes clear, direct, and grammatically correct, while preserving 100% of its original meaning. Do not add, remove, or interpret anything."

"🌍 Language instructions:"

"✅ Detect and keep the original language of the user’s input."

"❌ Do not translate the text or switch languages."

"❌ Never answer or complete the request."

"✅ Only rewrite the input to make its intention medically interpretable and linguistically clear."

f"Original input: {user_input}")
        messages = [
            {"role": "system", "content": "Tu es un assistant de reformulation médicale."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
    '''
if __name__ == "__main__":
    from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client=Groq(api_key=API_KEY)
preprocessor=Preprocessor( client=client,model="mistral-saba-24b")

print(preprocessor.normalize_question(" "))
'''