from ai_models.text_generation.pipeline.groq_rag_generator import GroqRAGPipeline
from typing import Tuple, List, Dict
import uuid
from ai_models.common.memory import ChatMemory
pipeline = GroqRAGPipeline()

def chat_medical_text(question: str, profil: str,session_id: str = None)->Tuple[str, str, List[Dict[str, str]]]:
    if session_id is None:
        session_id = str(uuid.uuid4())
    answer = pipeline.generate_adaptive_answer(question=question,session_id=session_id, profil=profil)
    history = ChatMemory.get_history(session_id)
    #if "\n\n📚 Sources utilisées" in output:
        #answer, citation_block = output.split("\n\n📚 Sources utilisées", 1)
        #citations = citation_block.strip().split("\n")
        #citations = [c.strip("- ") for c in citations if c.strip()]
    #else:
        #answer = output
        #citations = []

    return session_id, answer,history
