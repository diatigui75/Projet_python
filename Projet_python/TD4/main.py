from Document import Document, id2doc
from Auteur import Auteur
from Corpus import Corpus

# Exemple d'utilisation
corpus = Corpus("Mon Corpus de Documents")

# Ajout de documents au corpus
doc1 = Document(
    titre="Introduction à Python",
    auteur="Julien Velcin",
    date="2025-10-01",
    url="https://example.com/doc1",
    texte="Python est un langage de programmation puissant et facile à apprendre..."
)
corpus.ajouter_document(doc1)

doc2 = Document(
    titre="Les bonnes pratiques en Python",
    auteur="Julien Velcin",
    date="2025-10-02",
    url="https://example.com/doc2",
    texte="Voici quelques bonnes pratiques pour écrire du code Python propre et maintenable..."
)
corpus.ajouter_document(doc2)

doc3 = Document(
    titre="Introduction à la POO",
    auteur="Alice Martin",
    date="2025-09-15",
    url="https://example.com/doc3",
    texte="La programmation orientée objet est un paradigme de programmation..."
)
corpus.ajouter_document(doc3)

# Affichage des documents triés par date
print("Documents triés par date (les plus récents) :")
corpus.afficher_documents_par_date(n=2)

# Affichage des documents triés par titre
print("\nDocuments triés par titre :")
corpus.afficher_documents_par_titre(n=3)

# Sauvegarde du corpus
corpus.save_to_dataframe("corpus.csv")

# Chargement du corpus
corpus_charge = Corpus.load_from_dataframe("Mon Corpus Chargé", "corpus.csv")
print("\nCorpus chargé :")
print(corpus_charge)
