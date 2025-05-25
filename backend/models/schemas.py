from pydantic import BaseModel
from typing import List,Optional,Dict

class ChatRequest(BaseModel):
    question: str
    profil: str
    session_id:Optional[str]=None

class ChatResponse(BaseModel):
    session_id:str
    answer: str
    
    
