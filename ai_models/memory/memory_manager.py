from ai_models.common.memory import ChatMemory

class MemoryManager:
  

    def __init__(self, history_limit: int = 10):
        self.history_limit = history_limit
        self.chat=ChatMemory()

    def get_summary(self, user_profile: str, session_id: str) -> str:
        history = self.chat.get_history(session_id=session_id, limit=self.history_limit)

        if not history:
            return ""

        formatted = [f"{msg['role'].capitalize()} : {msg['content']}" for msg in history]
        return "\n".join(formatted)
