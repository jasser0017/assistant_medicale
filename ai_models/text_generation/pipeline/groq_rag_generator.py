'''''
import os
from dotenv import load_dotenv

from ai_models.common.intent_detector import detect_health_intent
from ai_models.common.memory import ChatMemory
from ai_models.utils.specialty_detection import detect_specialty
from ai_models.text_generation.generators.text_generator import GroqTextGenerator
from ai_models.text_generation.retrievers.rag_retriever import RAGRetriever
from deep_translator import GoogleTranslator
from langdetect import detect

load_dotenv()






class GroqRAGPipeline:
    def __init__(self):
        self.generator = GroqTextGenerator()
        self.retriever = RAGRetriever()
    

    def detect_language(self,text:str)->str:
        try:
            return detect(text)
        except:
            return "en"
    
    def translate_if_needed(self,text:str,target_lang:str="en")->str:
        src_lang=self.detect_language(text)
        if src_lang == target_lang:
            return text
        return GoogleTranslator(source=src_lang, target=target_lang).translate(text)

    def generate_adaptive_answer(self, question: str, session_id: str, profil: str,  top_k: int = 3, max_tokens: int = 500) -> str:
        intent=detect_health_intent(question)
        lang = self.detect_language(question)
        try:
            history = ChatMemory.get_history(session_id, limit=10)
        except Exception:
            history= []

        history_ctx = ""
        for turn in history:
            speaker = (
                ("Patient" if profil == "patient" else "Médecin")
                if turn["role"] == "user" else
                "Assistant"
            )
            history_ctx += f"{speaker}: {turn['content']}\n"
        
        if intent =="small_talk":
            prompt = f"""
Tu es un assistant médical sympathique et accessible.

=== Historique de la discussion ===
{history_ctx}

➡️ Message actuel :
{question}

Réponds de manière naturelle et humaine.
"""
            raw = self.generator.generate(prompt, max_tokens=max_tokens)
            answer= self.translate_if_needed(raw, lang)
            
        
        elif intent == "diagnostic":
            
            answer=self.generate_with_rag(question, session_id, profil, history_ctx, top_k, max_tokens)
        
        elif intent in {"education", "prevention"}:
            
                answer = self.generate_with_rag(question, session_id, profil, history_ctx, top_k, max_tokens)
          
        
        elif intent == "psychologie":
            prompt = f"""
Tu es un assistant bienveillant qui aide les patients à gérer le stress, l’anxiété ou les émotions. Tu écoutes sans juger et proposes des solutions douces.

=== Historique de la discussion ===
{history_ctx}

➡️ Problème évoqué :
{question}

Réponds avec empathie et encouragement.
"""
            raw = self.generator.generate(prompt, max_tokens=max_tokens)
            answer= self.translate_if_needed(raw, lang)

        elif intent == "orientation":
            prompt = f"""
Tu aides les utilisateurs à comprendre vers qui se tourner (médecin, spécialiste, centre de soins) et comment organiser leur parcours de soins.

=== Historique de la discussion ===
{history_ctx}

➡️ Besoin exprimé :
{question}

Réponds avec précision et clarté.
"""         
            raw = self.generator.generate(prompt, max_tokens=max_tokens)
            answer= self.translate_if_needed(raw, lang)
        elif intent == "suivi":
            prompt = f"""
Tu es un assistant personnel médical. Tu encourages l’utilisateur à suivre ses objectifs santé (traitement, activité, alimentation…) et tu rappelles les bonnes pratiques.

=== Historique de la discussion ===
{history_ctx}

➡️ Question / retour :
{question}

Sois positif, motivant et précis.
"""         
            raw = self.generator.generate(prompt, max_tokens=max_tokens)
            answer= self.translate_if_needed(raw, lang)
        else:
            prompt = f"""
Tu es un assistant médical polyvalent. Tu aides selon le contexte ci-dessous.

=== Historique ===
{history_ctx}

➡️ Question :
{question}

Sois clair, utile et professionnel.
"""
        raw = self.generator.generate(prompt, max_tokens=max_tokens)
        
        answer= self.translate_if_needed(raw, lang)

            

        ChatMemory.add_message(session_id, "user", question)
        ChatMemory.add_message(session_id, "assistant", answer)

        return answer

       
    def generate_with_rag(self, question, session_id, profil, history_ctx, top_k, max_tokens):
        lang = self.detect_language(question)
        question_en = self.translate_if_needed(question, "en")
        speciality = detect_specialty(question_en)
        self.retriever.index_articles_from_list(question_en, rebuild=False)
        docs = self.retriever.query(question_en, top_k=top_k)
        context = "\n\n".join(d for d, _ in docs)

        if profil == "medecin":
            style = "Formule ta réponse comme à un médecin : vocabulaire technique, concis, avec références."
        else:
            style = "Formule ta réponse comme à un patient : clair, simple, sans jargon."

        prompt = f"""
Tu es un assistant médical expert en {speciality}.

=== Historique ===
{history_ctx}

  === Sources ===
{context}

{style}

➡️ Question :
{question_en}
Réponds précisément.
"""
        answer = self.generator.generate(prompt, max_tokens=max_tokens)
        return self.translate_if_needed(answer, lang)
    


   

   


    

# Test CLI
if __name__ == "__main__":
    pipeline = GroqRAGPipeline()
    #answer_patient = pipeline.generate_answer("Comment prévenir le cancer du sein ?", profil="patient")
    #answer_medecin = pipeline.generate_answer(" Est-ce que la vaccination contre la grippe est vraiment efficace chaque année ?", profil="patient")
    #answer_patient10=pipeline.generate_answer("Quelles sont les recommandations pour une grossesse saine ?", profil="patient")
    #answer_patient11=pipeline.generate_adaptive_answer("comment utiliser le pansement", profil="patient")
    answer = pipeline.generate_adaptive_answer(
    "merci beaucoup que dieu vous protége   ",
    session_id="test-456",
    profil="medecin",
    intent="small_talk"
)

    print("\n🧠 Réponse générée pour patient :\n")
    #print(answer_patient)
    #print("\n🧠 Réponse générée pour patient :\n")
    #print(answer_medecin)
    #print("\n🧠 Réponse générée pour patient :\n")
    #print(answer_patient10)
    #print("\n🧠 Réponse générée pour patient :\n")
    #print(answer_patient11)
    print("\n🧠 Réponse générée pour medecin :\n")
    print(answer)


'''''

import os
from dotenv import load_dotenv

from ai_models.common.intent_detector import detect_health_intent
from ai_models.common.memory import ChatMemory
from ai_models.utils.find_name import find_latest_user_name
from ai_models.utils.specialty_detection import detect_specialty
from ai_models.text_generation.generators.text_generator import GroqTextGenerator
from ai_models.text_generation.retrievers.rag_retriever import RAGRetriever
from deep_translator import GoogleTranslator
from langdetect import detect

load_dotenv()

class GroqRAGPipeline:
    def __init__(self):
        self.generator = GroqTextGenerator()
        self.retriever = RAGRetriever()

    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return "en"

    def translate_if_needed(self, text: str, target_lang: str = "en") -> str:
        src_lang = self.detect_language(text)
        if src_lang == target_lang:
            return text
        return GoogleTranslator(source=src_lang, target=target_lang).translate(text)

    def generate_adaptive_answer(
    self,
    question: str,
    session_id: str,
    profil: str,
    top_k: int = 3,
    max_tokens: int = 200
) -> str:
    # 1) Intent et langue
        intent = detect_health_intent(question)
        lang = self.detect_language(question)

    # 2) Historique
        try:
            history = ChatMemory.get_history(session_id, limit=10)
        except:
            history = []
        history_ctx = ""
        for turn in history:
            speaker = "Patient" if turn["role"] == "user" else "Assistant"
            history_ctx += f"{speaker}: {turn['content']}\n"
        
        stored_name = find_latest_user_name(history)
        name_intro = f"\nTu t’adresses à un patient nommé {stored_name}." if stored_name else ""



    # 3) Style selon intent
        style_map = {
        "small_talk":  "Sois naturel, chaleureux et courtois.",
        "diagnostic":  "Analyse les symptômes avec prudence et propose des conseils sans prescrire.",
        "education":   "Explique clairement les termes médicaux sans jargon.",
        "prevention":  "Donne des conseils simples pour rester en bonne santé.",
        "psychologie": "Répond avec empathie et encouragement.",
        "orientation": "Oriente vers les bons professionnels et démarches.",
        "suivi":       "Encourage et rappelle les bonnes pratiques."
    }
        style = style_map.get(intent, "Sois utile, professionnel et bienveillant,IMPORTANT : Réponds **toujours** en **{lang}**, la langue de l’utilisateur.{name_intro}")

    # 4) Contexte RAG si nécessaire
        rag_block = ""
        if intent in ("diagnostic", "education", "prevention"):
            question_en = self.translate_if_needed(question, "en")
            self.retriever.index_articles_from_list(question_en, rebuild=False)
            docs = self.retriever.query(question_en, top_k=top_k)
            excerpts = "\n\n---\n".join(doc for doc, _ in docs)
            rag_block = f"\n\n📚 Extraits scientifiques :\n{excerpts}"

    # 5) Construction du prompt
        prompt = f"""
IMPORTANT : Réponds **toujours** en **{lang}**, la langue de l’utilisateur.

Tu es un assistant médical expert, profil : **{profil}**, intent : **{intent}**.{name_intro}

{style}

=== Historique de la conversation ===
{history_ctx}

➡️ Message actuel :
{question}{rag_block}

Réponds de façon complète et adaptée.
""".strip()

    # 6) Génération et formatage
        raw = self.generator.generate(prompt, max_tokens=max_tokens)
        answer = raw.strip()

    # 7) Sauvegarde en mémoire
        ChatMemory.add_message(session_id, "user", question)
        ChatMemory.add_message(session_id, "assistant", answer)

        return answer
