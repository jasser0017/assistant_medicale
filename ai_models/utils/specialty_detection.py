from ai_models.constants import SPECIALTY_MESH
import re

KEYWORDS = {
    "cardiology": [
        r"cardio", r"heart", r"myocard", r"hypertension", r"arrhythm", r"angina", r"vascular",
        r"tachycardia", r"bradycardia", r"stroke", r"coronary"
    ],
    "dermatology": [
        r"skin", r"derm", r"psoriasis", r"eczema", r"rash", r"acne", r"melanoma",
        r"vitiligo", r"urticaria", r"dermatitis"
    ],
    "neurology": [
        r"neuro", r"brain", r"stroke", r"parkinson", r"epilepsy", r"seizure", r"multiple sclerosis",
        r"migraine", r"headache", r"alzheimer", r"neurodegenerative"
    ],
    "endocrinology": [
        r"diabet", r"thyroid", r"endocrine", r"insulin", r"hypoglycemia", r"hyperthyroidism",
        r"hypothyroidism", r"cushing", r"addison", r"obesity", r"dyslipid"
    ],
    "oncology": [
        r"cancer", r"tumor", r"neoplasm", r"carcinoma", r"sarcoma", r"chemotherapy", r"metastasis",
        r"radiotherapy", r"oncology"
    ],
    "gastroenterology": [
        r"stomach", r"liver", r"intestin", r"colon", r"hepat", r"gastr", r"ibs", r"crohn",
        r"ulcer", r"gastroesophageal", r"reflux", r"cirrhosis", r"hepatitis"
    ],
    "pulmonology": [
        r"lung", r"respir", r"asthma", r"bronch", r"copd", r"pneumonia", r"tuberculosis",
        r"pulmonary embolism"
    ],
    "nephrology": [
        r"kidney", r"renal", r"nephr", r"urine", r"dialysis", r"glomerulonephritis", r"nephrotic",
        r"pyelonephritis", r"polycystic"
    ],
    "hematology": [
        r"blood", r"anemia", r"leukemia", r"lymphoma", r"clot", r"hemoglobin", r"thrombosis",
        r"coagulation", r"myeloma"
    ],
    "infectious_disease": [
        r"virus", r"bacteria", r"infection", r"hiv", r"covid", r"flu", r"tuberculosis",
        r"malaria", r"sepsis", r"meningitis"
    ],
    "rheumatology": [
        r"arthritis", r"rheumat", r"lupus", r"joint pain", r"autoimmune", r"spondyloarthritis",
        r"osteoporosis", r"vasculitis", r"fibromyalgia"
    ],
    "psychiatry": [
        r"depression", r"anxiety", r"mental", r"bipolar", r"schizophrenia", r"ptsd",
        r"ocd", r"eating disorder", r"autism", r"adhd"
    ],
    "pediatrics": [
        r"child", r"infant", r"baby", r"pediatric", r"newborn", r"neonatal"
    ],
    "geriatrics": [
        r"elderly", r"aging", r"geriatric", r"senior", r"aged"
    ],
    "obstetrics_gynecology": [
        r"pregnan", r"obstetric", r"gynecolog", r"menstruation", r"fertility", r"uterus",
        r"labor", r"delivery", r"postpartum"
    ],
    "urology": [
        r"urinary", r"bladder", r"prostate", r"urolog", r"erectile", r"incontinence"
    ],
    "orthopedics": [
        r"bone", r"fracture", r"orthopedic", r"joint", r"spine", r"scoliosis",
        r"osteoporosis"
    ],
    "ophthalmology": [
        r"eye", r"vision", r"retina", r"glaucoma", r"cataract", r"ocular"
    ],
    "otolaryngology": [
        r"ear", r"nose", r"throat", r"sinus", r"hearing", r"larynx", r"otolaryngology"
    ],
    "allergy_immunology": [
        r"allerg", r"asthma", r"immune", r"hypersensitivity", r"autoimmune"
    ],
    "anesthesiology": [
        r"anesth", r"sedation", r"pain management", r"analgesia"
    ],
    "emergency_medicine": [
        r"emergency", r"trauma", r"urgent", r"accident", r"resuscitation"
    ],
    "rehabilitation": [
        r"rehab", r"physiotherapy", r"recovery", r"functional", r"rehabilitation"
    ],
    "radiology": [
        r"scan", r"mri", r"ct", r"radiograph", r"imaging", r"ultrasound"
    ],
    "nuclear_medicine": [
        r"nuclear", r"radiotracer", r"pet scan", r"scintigraphy"
    ],
    "occupational_medicine": [
        r"occupational", r"workplace", r"job-related", r"work injury"
    ],
    "legal_medicine": [
        r"forensic", r"autopsy", r"legal", r"toxicology", r"medicolegal"
    ],
    "family_medicine": [
        r"family doctor", r"primary care", r"general practitioner", r"gp", r"family practice"
    ],
}


def detect_specialty(question: str) -> str | None:
    q = question.lower()
    for spec, patterns in KEYWORDS.items():
        if any(re.search(p, q) for p in patterns):
            return spec
    return "general"  