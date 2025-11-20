from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

classifier = pipeline("image-classification", model="google/mobilenet_v2_1.0_224")

IMAGE_KEYWORDS = {
    "plastique": [
        "plastic", "bottle", "water bottle", "packet", "bag",
        "cover", "wrapper", "container", "jug", "polyethylene"
    ],
    "verre": [
        "glass", "wine bottle", "beer bottle", "jar", "vial",
        "goblet", "flask", "cup"
    ],
    "papier": [
        "paper", "newspaper", "cardboard", "carton", "tissue",
        "book", "magazine", "packet", "envelope"
    ],
    "métal": [
        "metal", "tin", "can", "aluminum", "steel", "iron",
        "screw", "bolt", "tool", "pan", "pot"
    ],
  "organique": [
    "fruit", "banana", "apple", "vegetable", "food",
    "bread", "meat", "organic", "plant", "leaf",
    "compost", "soil", "earth", "mulch", "scraps",
    "peel", "peels", "waste", "food waste",
    "leftovers", "biodegradable"
]

}


def map_image_label_to_category(label: str):
    label = label.lower()

    for category, keywords in IMAGE_KEYWORDS.items():
        for kw in keywords:
            if kw in label:
                return category

    return "autre"


def predict_image(img):
    result = classifier(img)[0]['label']
    return map_image_label_to_category(result)


from sentence_transformers import SentenceTransformer, util

# Charger modèle NLP puissant et léger
text_model = SentenceTransformer("all-MiniLM-L6-v2")
print(">>> NLP model OK: using sentence-transformers")


# ----------- NIVEAU 1 : Catégorie principale -----------
# ----------- NIVEAU 1 : Catégorie principale (descriptions longues pour une meilleure sémantique) -----------

# --- NIVEAU 1 EN VERSION ULTRA STABLE AVEC EXEMPLES MULTIPLES ---

CATEGORIES = [
    # PLASTIQUE
    "plastique: bouteille plastique, bouteille en plastique, bouteille d'eau en plastique, bouteille soda plastique, sac plastique, film plastique, emballage chips, gobelet plastique, pot yaourt plastique, pot plastique, emballage alimentaire plastique, tupperware, plastique mou, sachet plastique ; pas métal, pas verre, pas papier, pas organique, pas canette, pas conserve",

    # METAL
    "métal: canette, canette coca, canette soda, aluminium, boite de conserve, conserve métal, conserve en aluminium, opercule métal, couvercle métal, conserve poisson, conserve tomate, capsule métal, canette bière, lame métal, fer, acier, acier recyclable, objet métallique ; pas plastique, pas verre, pas papier, pas organique, pas électronique",

    # PAPIER
    "papier: feuille papier, journal, carton, boite en carton, carton amazon, serviette papier, essuie-tout, magazine, livre en papier, document papier, papier mouillé, emballage carton ; pas métal, pas verre, pas plastique, pas organique",

    # VERRE
    "verre: bouteille en verre, bocal en verre, pot en verre, flacon verre, bouteille vin, bouteille bière, pot confiture verre ; pas métal, pas plastique, pas papier, pas organique",

    # ORGANIQUE
    "organique: fruit, pomme, banane, pelures, épluchures, déchets alimentaires, restes nourriture, compost, légumes, peau fruit, aliment, biodégradable ; pas métal, pas verre, pas plastique, pas papier, pas électronique",

    # AUTRE (beaucoup plus petit)
    "autre: pile, batterie, chargeur, appareil électronique, câble, téléphone cassé, céramique, porcelaine, verre pyrex, objets dangereux ; pas métal recyclable, pas conserve, pas canette, pas bouteille plastique, pas fruit, pas papier"
]


CATEGORY_LABELS = ["plastique", "métal", "papier", "verre", "organique", "autre"]

category_embeddings = text_model.encode(CATEGORIES, convert_to_tensor=True)


CATEGORY_LABELS = ["plastique", "métal", "papier", "verre", "organique", "autre"]

category_embeddings = text_model.encode(CATEGORIES, convert_to_tensor=True)




# ----------- NIVEAU 2 : Sous-catégories par classe -----------
SUBCATEGORIES = {
    "plastique": ["recyclable", "non recyclable"],
    "métal": ["recyclable", "non recyclable"],
    "papier": ["recyclable", "non recyclable"],
    "verre": ["recyclable", "non recyclable"],
    "organique": ["compostable", "non compostable"],
    "autre": ["dangereux", "électronique", "non recyclable"]
}

# Pré-encoder toutes les sous-catégories
subcategory_embeddings = {
    cat: text_model.encode(subb, convert_to_tensor=True)
    for cat, subb in SUBCATEGORIES.items()
}


def predict_text_2levels(desc: str):
    """Renvoie (catégorie, sous-catégorie)"""

    # ----- NIVEAU 1 -----
    emb = text_model.encode(desc, convert_to_tensor=True)
    scores = util.cos_sim(emb, category_embeddings)[0]
    best_cat_idx = scores.argmax().item()
    #category = CATEGORIES[best_cat_idx]
    category = CATEGORY_LABELS[best_cat_idx]

    # ----- NIVEAU 2 -----
    sub_emb = subcategory_embeddings[category]
    scores2 = util.cos_sim(emb, sub_emb)[0]
    best_sub_idx = scores2.argmax().item()
    subcategory = SUBCATEGORIES[category][best_sub_idx]

    return category, subcategory


def predict_text(desc: str):
    text = desc.lower().strip()

    # ----- RÈGLES PRIORITAIRES (100% précises) -----

    # MÉTAL
    if any(w in text for w in ["canette", "conserve", "aluminium", "boîte de conserve", "cannette"]):
        return "métal (recyclable)"

    # PLASTIQUE
    if "plastique" in text:
        return "plastique (recyclable)"
    if "bouteille" in text and "plastique" in text:
        return "plastique (recyclable)"
    if any(w in text for w in ["sac plastique", "film plastique", "emballage plastique"]):
        return "plastique (recyclable)"

    # VERRE
    if "bouteille" in text and "verre" in text:
        return "verre (recyclable)"
    if any(w in text for w in ["verre", "bocal", "pot en verre"]):
        return "verre (recyclable)"

    # ORGANIQUE
    if any(w in text for w in ["fruit", "banane", "pomme", "pelure", "restes", "compost", "nourriture", "légume"]):
        return "organique (compostable)"

    # DANGEREUX / AUTRE
    if any(w in text for w in ["pile", "batterie", "chargeur", "électronique"]):
        return "autre (dangereux)"

    # ----- SINON : SBERT PREND LE RELAIS -----
    cat, sub = predict_text_2levels(desc)
    return f"{cat} ({sub})"

