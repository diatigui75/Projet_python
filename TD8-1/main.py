from Document import Document, RedditDocument, ArxivDocument, id2doc, DocumentFactory
from Auteur import Auteur
from Corpus import Corpus, CorpusSingleton
from SearchEngine import SearchEngine  # Import depuis SearchEngine.py

# Exemple d'utilisation
corpus = Corpus("Mon Corpus de Documents")

# Ajout de documents classiques
doc1 = Document(
    titre="Introduction à Python",
    auteur="Julien Velcin",
    date="2025-10-01",
    url="https://example.com/doc1",
    texte="Python est un langage de programmation puissant et facile à apprendre..."
)
corpus.ajouter_document(doc1)

# Ajout de documents Reddit
doc2 = RedditDocument(
    titre="Pourquoi Python est-il si populaire ?",
    auteur="u/PythonLover",
    date="2025-10-02",
    url="https://reddit.com/r/Python/comments/123456",
    texte="Python est populaire grâce à sa simplicité et sa polyvalence...",
    nb_commentaires=42
)
corpus.ajouter_document(doc2)

# Ajout de documents Arxiv
doc3 = ArxivDocument(
    titre="Nouvelle approche en Machine Learning",
    auteurs=["Alice Smith", "Bob Johnson", "Charlie Brown"],
    date="2025-09-15",
    url="https://arxiv.org/abs/2509.12345",
    texte="Nous proposons une nouvelle approche pour l'apprentissage automatique..."
)
corpus.ajouter_document(doc3)

# Affichage des documents avec leur type
print("Documents avec leur type :")
corpus.afficher_documents_par_type()

# Sauvegarde du corpus
corpus.save_to_dataframe("corpus.csv")

# Chargement du corpus
corpus_charge = Corpus.load_from_dataframe("Mon Corpus Chargé", "corpus.csv")
print("\nCorpus chargé :")
print(corpus_charge)

# Exemple d'utilisation du Singleton
corpus_singleton = CorpusSingleton("Mon Corpus Singleton")
corpus_singleton.get_corpus().ajouter_document(doc1)
print("\nCorpus Singleton :")
print(corpus_singleton.get_corpus())

# Exemple d'utilisation de la Factory
factory = DocumentFactory
doc_reddit = factory.create_document(
    "Reddit",
    titre="Pourquoi utiliser des design patterns ?",
    auteur="u/DesignPatternFan",
    date="2025-10-03",
    url="https://reddit.com/r/DesignPatterns/comments/654321",
    texte="Les design patterns sont utiles pour structurer son code...",
    nb_commentaires=15
)
corpus.ajouter_document(doc_reddit)

doc_arxiv = factory.create_document(
    "Arxiv",
    titre="Étude sur les design patterns en Python",
    auteurs=["David Smith", "Emma Johnson"],
    date="2025-09-20",
    url="https://arxiv.org/abs/2509.65432",
    texte="Cette étude explore l'utilisation des design patterns en Python..."
)
corpus.ajouter_document(doc_arxiv)

print("\nDocuments créés avec la Factory :")
corpus.afficher_documents_par_type()

# Utiliser le corpus chargé pour les statistiques
corpus_charge.stats(n=10)

# Recherche un mot-clé (méthode existante)
resultats_recherche = corpus_charge.search("Python")
print("\nRésultats de la recherche pour 'Python' (méthode existante) :")
print(resultats_recherche)

# Construction du concordancier
concordancier = corpus_charge.concorde("Python", taille_contexte=20)
print("\nConcordancier pour 'Python' :")
print(concordancier)

# --- NOUVEAU : Utilisation du moteur de recherche du TD 7 ---
print("\n--- Moteur de recherche TD 7 ---")
engine = SearchEngine(corpus)
results = engine.search("Python", k=3)
print("\nRésultats de la recherche pour 'Python' (moteur TD 7) :")
print(results)
