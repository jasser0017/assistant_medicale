from ai_models.common.detection_name import extract_name_with_llm


def find_latest_user_name(history: list) -> str:
    for msg in reversed(history):
        if msg["role"] == "user":
            name = extract_name_with_llm(msg["content"])
            if name:
                return name
    return ""
