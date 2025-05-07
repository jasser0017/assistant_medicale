from ai_models.text_generation.generators.text_generator import GroqTextGenerator


classifier = GroqTextGenerator(model="meta-llama/llama-4-maverick-17b-128e-instruct")

CATEGORIES = [
    "small_talk",
    "diagnostic",
    "education",
    "prevention",
    "psychologie",
    "orientation",
    "suivi"
]

def detect_health_intent(text: str) -> str:
    prompt = f"""
Tu es un classificateur d'intention pour un assistant de santé.
Voici les catégories possibles :
- small_talk : salutation, remerciement, formule de politesse
- diagnostic : symptômes, maladies, traitements, examens médicaux
- education : comprendre des termes médicaux (ex : c'est quoi...)
- prevention : conseils pour rester en bonne santé (sport, alimentation, hygiène)
- psychologie : stress, anxiété, soutien émotionnel
- orientation : trouver un médecin, consulter, parcours de soin
- suivi : encouragement, objectifs santé, rappels

Classifie le texte suivant dans UNE seule de ces catégories :
{text}

Réponds uniquement par le label exact (ex : diagnostic).
"""

    try:
        out = classifier.generate(prompt, max_tokens=10).strip().lower().rstrip(".")
        if out in CATEGORIES:
            return out
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")
    return "education"
