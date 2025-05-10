import re
from ai_models.text_generation.retrievers.query_normalizer import normalize_query
from ai_models.utils.methodes import translate_if_needed
from ai_models.utils.specialty_detection import detect_specialty
from ai_models.constants import SPECIALTY_MESH
from ai_models.utils.mesh_selector import select_best_mesh

def clean_query(text: str) -> str:
    """
    Nettoie la requête en supprimant les ponctuations non alphanumériques 
    (hors tiret et espace) et en retirant les espaces inutiles.
    """
    translated = translate_if_needed(text)
    normalized = normalize_query(translated)
    return normalized

def build_enriched_query(question: str) -> str:
    # Nettoyage de la question
    question_clean = clean_query(question)
    print("\n req" ,question_clean )

    # Détection de la spécialité médicale
    specialty = detect_specialty(question_clean)
    mesh_terms = SPECIALTY_MESH.get(specialty, [])

    # Si aucun terme MeSH défini pour cette spécialité
    if not mesh_terms:
        print(f"⚠️ Aucun terme MeSH pour la spécialité détectée : {specialty}")
        return question_clean

    # Sélection du meilleur terme MeSH
    best_mesh = select_best_mesh(question_clean, mesh_terms)

    # Construction de la requête enrichie
    enriched_query = f'({question_clean}) AND ("{best_mesh}"[Mesh])'

    print(f"🔍 Requête enrichie : {enriched_query}")
    return enriched_query
