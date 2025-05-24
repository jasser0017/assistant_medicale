import re
from ai_models.text_generation.retrievers.medical_query_corrector import QueryCorrector
from ai_models.text_generation.retrievers.query_normalizer import Normalizer
from ai_models.utils.methodes import translate_if_needed
from ai_models.utils.specialty_detection import detect_specialty
from ai_models.constants import SPECIALTY_MESH
from ai_models.utils.mesh_selector import select_best_mesh
from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))




corrector = QueryCorrector()
normalize=Normalizer(client)

def clean_query(text: str,log=False) -> str:
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
        print("🧾 🔍 TRAITEMENT DE LA REQUÊTE UTILISATEUR")
        print(f"📌 Originale    : {text}")
        print(f"🩺 Corrigée     : {corrected}")
        print(f"🌍 Traduite     : {translated}")
        print(f"🧹 Normalisée   : {normalized}")
        print("-" * 60)
    
    

    translated = translate_if_needed(corrected)
    normalized =normalize.normalize_query(translated)

    return normalized

def build_enriched_query(question: str,) -> str:
    
    question_clean = clean_query(question,log=False)
    
    

  
    specialty = detect_specialty(question_clean)
    mesh_terms = SPECIALTY_MESH.get(specialty, [])

    
    if not mesh_terms:
        print(f"⚠️ Aucun terme MeSH pour la spécialité détectée : {specialty}")
        return question_clean

   
    best_mesh = select_best_mesh(question_clean, mesh_terms)

    
    enriched_query = f'({question_clean}) AND ("{best_mesh}"[Mesh])'

    print(f"🔍 Requête enrichie : {enriched_query}")
    return enriched_query

if __name__ == "__main__":
    print(build_enriched_query("wath is the breast cancer"))
