from ai_models.text_generation.generators.text_generator import GroqTextGenerator


def extract_name_with_llm(text: str) -> str | None:
    prompt = f"""
You are a name extraction assistant.
From the following message, extract the user's first name only regardless of the language used, if they give it:
Message: "{text}"
First name (only):"""
    result = GroqTextGenerator().generate(prompt, max_tokens=10)
    name = result.strip().split()[0]
    if name and len(name) < 25:
        return name.capitalize()
    return None