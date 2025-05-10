import re
from ai_models.text_generation.retrievers.medical_query_corrector import QueryCorrector
from ai_models.text_generation.retrievers.query_normalizer import normalize_query
from ai_models.utils.methodes import translate_if_needed
from ai_models.utils.specialty_detection import detect_specialty
from ai_models.constants import SPECIALTY_MESH
from ai_models.utils.mesh_selector import select_best_mesh


corrector = QueryCorrector()

def clean_query(text: str,log: bool = False) -> str:
    """
    Nettoie la requête en supprimant les ponctuations non alphanumériques 
    (hors tiret et espace) et en retirant les espaces inutiles.
    """
    try:
        corrected = corrector.corriger_requete(text)
    except Exception as e:
        print(f"⚠️ Correction échouée, utilisation brute : {e}")
        corrected = text
    
    if log:

        translated = translate_if_needed(corrected)
        normalized = normalize_query(translated)
        print(f"📌 Originale    : {text}")
        print(f"🩺 Corrigée     : {corrected}")
        print(f"🌍 Traduite     : {translated}")
        print(f"🧹 Normalisée   : {normalized}")
        print("-" * 60)
    return normalized

def build_enriched_query(question: str,) -> str:
    
    question_clean = clean_query(question,log=True)
    
    

  
    specialty = detect_specialty(question_clean)
    mesh_terms = SPECIALTY_MESH.get(specialty, [])

    
    if not mesh_terms:
        print(f"⚠️ Aucun terme MeSH pour la spécialité détectée : {specialty}")
        return question_clean

   
    best_mesh = select_best_mesh(question_clean, mesh_terms)

    
    enriched_query = f'({question_clean}) AND ("{best_mesh}"[Mesh])'

    print(f"🔍 Requête enrichie : {enriched_query}")
    return enriched_query
