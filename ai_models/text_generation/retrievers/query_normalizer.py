from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk, re, unicodedata

# (Re)vérification douce
for res in ["punkt", "stopwords", "wordnet"]:
    try:
        nltk.data.find(f"tokenizers/{res}" if res == "punkt" else f"corpora/{res}")
    except LookupError:
        nltk.download(res)

def normalize_query(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    filtered = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(filtered)

if __name__ == "__main__":
    print(normalize_query("What is breast cancer?"))
    print(normalize_query("what the  breast cancer is "))
