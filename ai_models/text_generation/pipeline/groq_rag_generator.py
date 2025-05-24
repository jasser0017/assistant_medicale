
from groq import Groq
from text_generation.pipeline.prompt_chain import PromptChain
from common.memory import ChatMemory

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
models = {
    "intent": "qwen-qwq-32b",
    "clarify": "deepseek-r1-distill-llama-70b",
    "generate": "meta-llama/llama-4-maverick-17b-128e-instruct"
}

USER_PROFILE = "Patient"

client = Groq(api_key=API_KEY)
memory_manager = ChatMemory()

pipeline = PromptChain(
    client=client,
    model_name=models,
    memory_manager=memory_manager,
    user_profile=USER_PROFILE
)
def process_medical_request(user_input: str) -> str:
    return pipeline.run(user_input)


