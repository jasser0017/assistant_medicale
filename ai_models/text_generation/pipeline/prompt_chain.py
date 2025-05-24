from .intent_classifier import IntentClassifier
from .clarification import Clarifier
from .final_generator import FinalGenerator
from ..retrievers.rag_retriever import RAGRetriever
from groq import Groq

models = {
    "intent": "qwen-qwq-32b",
    "clarify": "deepseek-r1-distill-llama-70b",
    "generate": "meta-llama/llama-4-maverick-17b-128e-instruct"
}

class PromptChain:
    def __init__(self,models: dict , memory_manager,client):
        self.client =client
        
        self.memory_manager = memory_manager
        self.intentor   = IntentClassifier(client, models["intent"])
        self.clarifier  = Clarifier(client, models["clarify"])
        self.final_gen  = FinalGenerator(client, models["generate"])
        self.rag        = RAGRetriever()


    def run(self, user_input: str,session_id: str,user_profile: str) -> str:
        original_input = user_input
        intent = self.intentor.classify(original_input)
        clarification = self.clarifier.check_ambiguity(original_input, intent)
        
        
        if clarification:
            print(f"[🔁 Clarification requise] → {clarification}")
            return clarification

        #final_intent = self.intentor.classify(original_input)
        rag_snippets = []
        special_instruction = None

        if intent in { "question médicale – éducation","question médicale – prévention","question médicale – diagnostic"}and clarification is None:
            rag_snippets = self.rag.retrieve_snippets(user_input)
        elif intent == "urgence médicale":
            special_instruction = (
                "Tu es un assistant chargé de gérer des situations à potentiel critique."
                "Si l’entrée de l’utilisateur indique un risque sérieux ou une urgence médicale, tu dois immédiatement recommander de consulter un professionnel de santé humain."

                "❌ Ne propose jamais d’auto-diagnostic."
                "❌ Ne suggère aucun traitement ou conduite à suivre."
                "✅ Ta seule réponse doit être une recommandation claire et ferme de consulter un médecin ou d’appeler les urgences."
            )
        elif intent  == "prise de rendez-vous":
            special_instruction=(
                "Tu es un assistant virtuel sans accès aux outils de planification ou aux agendas."

                "✅ Ta réponse doit :"        

                "Informer poliment l’utilisateur que tu ne peux pas fixer de rendez-vous,"

                "Lui suggérer de contacter un assistant humain ou le service concerné pour finaliser la prise de rendez-vous."

                "❌ Ne tente jamais de simuler une prise de rendez-vous."
                "❌ Ne pose pas de questions sur les disponibilités ou préférences horaires."
            )
        elif intent == "discussion générale":
            special_instruction =(
                "Tu es un assistant médical doté d'une posture empathique et bienveillante."

                "✅ Adopte un ton amical, détendu et accessible."
                "✅ Engage la conversation avec naturel, sans forcer."
                "✅ Si l’occasion se présente, oriente doucement la discussion vers des sujets de santé ou de bien-être, sans brusquer l’utilisateur."

                "❌ Ne force jamais le sujet médical si ce n’est pas approprié."
                "❌ Ne donne pas de diagnostic ni de conseils médicaux sans contexte clair."
            )
        
        elif intent =="autre":
            special_instruction=(
                "Tu es un assistant spécialisé dans les sujets de santé."
                "Si la requête n'entre pas clairement dans ton domaine de compétence :"

                "✅ Invite poliment l’utilisateur à reformuler sa question ou à proposer un sujet de santé plus précis."
                "✅ Garde un ton respectueux et encourageant, sans jugement."

                "❌ Ne tente pas de répondre à une question hors domaine."
                "❌ Ne fournis pas d’informations spéculatives ou générales en dehors du champ médical."

            )

        
        memory_text = self.memory_manager.get_summary(user_profile, session_id=session_id)

        print(f"[INTENTION] => {intent}")
        print(f"[CLARIFICATION] => {clarification}")
        print(f"[RAG] => {'activé' if rag_snippets else 'non activé'}")
        print(f"[INSTRUCTION] => {special_instruction}")
        final_response = self.final_gen.generate(
            question=user_input,
            intent=user_input,
            clarification=None,
            rag_snippets=rag_snippets,
            memory=memory_text,
            user_profile=user_profile,
            instruction=special_instruction
        )
        return final_response










        



