import pandas as pd
from datetime import datetime
from Document import Document, RedditDocument, ArxivDocument
from Auteur import Auteur
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # Dictionnaire des auteurs (nom: Auteur)
        self.id2doc = {}   # Dictionnaire des documents (id: Document)
        self.ndoc = 0      # Nombre total de documents
        self.naut = 0      # Nombre total d'auteurs

    def ajouter_document(self, document):
        """Ajoute un document au corpus et met à jour les statistiques."""
        if document.id not in self.id2doc:
            self.id2doc[document.id] = document
            self.ndoc += 1

            # Mise à jour des auteurs
            if document.auteur not in self.authors:
                self.authors[document.auteur] = Auteur(document.auteur)
                self.naut += 1
            self.authors[document.auteur].add(document.id, document)

    def afficher_documents_par_date(self, n=5):
        """Affiche les n documents les plus récents."""
        documents_tries = sorted(self.id2doc.values(), key=lambda doc: doc.date, reverse=True)
        for doc in documents_tries[:n]:
            print(doc)

    def afficher_documents_par_titre(self, n=5):
        """Affiche les n documents triés par titre."""
        documents_tries = sorted(self.id2doc.values(), key=lambda doc: doc.titre)
        for doc in documents_tries[:n]:
            print(doc)

    def afficher_documents_par_type(self):
        """Affiche les documents avec leur type."""
        for doc in self.id2doc.values():
            print(f"{doc.get_type()}: {doc}")

    def __repr__(self):
        """Représentation détaillée du corpus."""
        return f"Corpus(nom='{self.nom}', ndoc={self.ndoc}, naut={self.naut})"

    def save_to_dataframe(self, chemin_fichier):
        """Sauvegarde le corpus dans un fichier CSV en utilisant pandas."""
        data = []
        for doc in self.id2doc.values():
            data.append({
                "id": doc.id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date.strftime("%Y-%m-%d"),
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.get_type()
            })
        df = pd.DataFrame(data)
        df.to_csv(chemin_fichier, index=False)
        print(f"Corpus sauvegardé dans {chemin_fichier}")

    @classmethod
    def load_from_dataframe(cls, nom, chemin_fichier):
        """Charge un corpus depuis un fichier CSV."""
        df = pd.read_csv(chemin_fichier)
        corpus = cls(nom)
        for _, row in df.iterrows():
            if row["type"] == "Reddit":
                doc = RedditDocument(
                    titre=row["titre"],
                    auteur=row["auteur"],
                    date=row["date"],
                    url=row["url"],
                    texte=row["texte"],
                    nb_commentaires=0  # À adapter si tu as cette info dans le CSV
                )
            elif row["type"] == "Arxiv":
                doc = ArxivDocument(
                    titre=row["titre"],
                    auteurs=row["auteur"].split(", "),
                    date=row["date"],
                    url=row["url"],
                    texte=row["texte"]
                )
            else:
                doc = Document(
                    titre=row["titre"],
                    auteur=row["auteur"],
                    date=row["date"],
                    url=row["url"],
                    texte=row["texte"]
                )
            corpus.ajouter_document(doc)
        print(f"Corpus chargé depuis {chemin_fichier}")
        return corpus
class CorpusSingleton:
    _instance = None

    def __new__(cls, nom):
        if cls._instance is None:
            cls._instance = super(CorpusSingleton, cls).__new__(cls)
            cls._instance.corpus = Corpus(nom)
        return cls._instance

    def get_corpus(self):
        return self.corpus
