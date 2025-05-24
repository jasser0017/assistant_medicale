import os
from typing import Tuple, List, Dict
import uuid
from ai_models.utils.preprocessor import Preprocessor
from dotenv import load_dotenv
from groq import Groq
from ai_models.memory.memory_manager import MemoryManager
from ai_models.common.memory import ChatMemory
from ai_models.text_generation.pipeline.prompt_chain import PromptChain

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)
preprocessor = Preprocessor(client)
memory = MemoryManager()
models = {
    "intent": "qwen-qwq-32b",
    "clarify": "deepseek-r1-distill-llama-70b",
    "generate": "meta-llama/llama-4-maverick-17b-128e-instruct"
}

# On initialise le pipeline sans forcer le profil
pipeline_base = PromptChain(client=client, models=models,memory_manager=memory)
    


def chat_medical_text(question: str, profil: str, session_id: str = None) -> Tuple[str, str, List[Dict[str, str]]]:
    if session_id is None:
        session_id = str(uuid.uuid4())

     

    question=preprocessor.normalize_question(question)
    answer = pipeline_base.run(user_input=question, session_id=session_id,user_profile=profil.capitalize())

    
    ChatMemory.add_message(session_id, role="user", content=question)
    ChatMemory.add_message(session_id, role="assistant", content=answer)

    history = ChatMemory.get_history(session_id=session_id)

    return session_id, answer, history
