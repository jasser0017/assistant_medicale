from Bio import Entrez
from tqdm import tqdm
import json
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()
Entrez.email = os.getenv("Email")  # Obligatoire pour accéder à l’API PubMed


def search_pubmed(enriched_query: str, max_results: int = 50):
    handle = Entrez.esearch(db="pubmed", term=enriched_query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_details(pubmed_ids):
    ids_str = ",".join(pubmed_ids)
    handle = Entrez.efetch(db="pubmed", id=ids_str, rettype="abstract", retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records["PubmedArticle"]


def save_articles(records, output_file=None, query_slug=None):
    if output_file is None:
        if query_slug is None:
            raise ValueError("query_slug doit être fourni si output_file est None")
        output_file = f"data/pubmed_articles_{query_slug}.json"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data = []

    for article in tqdm(records, desc="Sauvegarde des articles"):
        try:
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
            pmid = article["MedlineCitation"]["PMID"]
            data.append({
                "pmid": str(pmid),
                "title": title,
                "abstract": abstract
            })
        except Exception:
            continue

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(data)} articles enregistrés dans {output_file}")


def download_pubmed(enriched_query, max_results=50):
    print(f"🔍 Recherche d'articles PubMed pour : {enriched_query}")
    ids = search_pubmed(enriched_query, max_results=max_results)
    print(f"✅ {len(ids)} articles trouvés.")
    records = fetch_details(ids)
    slug = hashlib.md5(enriched_query.encode()).hexdigest()
    save_articles(records, query_slug=slug)



# Test rapide
if __name__ == "__main__":
    download_pubmed(enriched_query="What are the most common symptoms of arterial hypertension", max_results=30)


#1)Etape 1


#tqdm: nous permet de suivre la progression de la boucle 

#: nous permet de gerer les donnes biologiques 

#BiO.Entrez est utilser pour intergir avec l'API de PubMed permet de chercher,récuperer les details d'articles

#os: nous permet de gerer les fichiers et les repertoires(creation si il est necessaire)

#2)Etape 2
#Entrez.email="mon email" pour que je peux acceder a PubMed

#3)Etape 3

#on tape une prompt qui doit une chaine avec le parametre quary:str, on va chercher dans PubMed que ce on
#est en train de chercher par la consulation de tout  le PubMed(par Entrez.read(variable(qui represente que
#ce on est en train de chercher cela signifie representer la prompt)) puis on retourne 50 identenfiants des
#articles trouves 

#4)Etape 4 

#apres on prendre ces ids on va la transfermer dans une liste separez par une virgule, puis on va faire  a travers
#PubMed un resume a travers les identifiants de ces article et  l on va stocker sous forme xml

#5) etape 5

#ici on va enrigister les resumes dans un fichier json qui va etre dans data/pubmed_articles.json
#dans la condition ou il n existe pas on va la creer. sionn ov va parcourir  tous les xml afin d extraire
#le titre et le resume puis on l ajoute dans le fichier json


#6) etape 6:

#represente le pipline compleet de tout ce on a fait 