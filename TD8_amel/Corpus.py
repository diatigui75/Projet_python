import re
import numpy as np
import pandas as pd
from collections import defaultdict
from datetime import datetime
from scipy.sparse import csr_matrix
from Document import Document, RedditDocument, ArxivDocument
from Auteur import Auteur

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # Dictionnaire des auteurs (nom: Auteur)
        self.id2doc = {}   # Dictionnaire des documents (id: Document)
        self.ndoc = 0      # Nombre total de documents
        self.naut = 0      # Nombre total d'auteurs
        self._texte_concatene = None  # Pour stocker la concaténation des textes

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

    def _concatener_textes(self):
        """Concatène tous les textes du corpus en une seule chaîne."""
        if self._texte_concatene is None:
            self._texte_concatene = " ".join(doc.texte for doc in self.id2doc.values())
        return self._texte_concatene

    def search(self, mot_cle):
        """
        Recherche les passages contenant le mot-clé dans le corpus.
        Retourne une liste des passages trouvés.
        """
        texte = self._concatener_textes()
        pattern = re.compile(rf"\b{mot_cle}\b", re.IGNORECASE)
        return [texte[max(0, m.start()-20):m.end()+20] for m in pattern.finditer(texte)]

    def concorde(self, expression, taille_contexte=20):
        """
        Construit un concordancier pour une expression donnée.
        Retourne un DataFrame pandas avec les colonnes :
        contexte gauche | motif trouvé | contexte droit
        """
        texte = self._concatener_textes()
        pattern = re.compile(rf"\b({expression})\b", re.IGNORECASE)
        matches = []
        for match in pattern.finditer(texte):
            start, end = match.span()
            contexte_gauche = texte[max(0, start - taille_contexte):start]
            contexte_droit = texte[end:end + taille_contexte]
            matches.append((contexte_gauche, match.group(), contexte_droit))
        df = pd.DataFrame(matches, columns=["contexte gauche", "motif trouvé", "contexte droit"])
        return df

    def nettoyer_texte(self, texte):
        """
        Nettoie le texte en appliquant des transformations :
        - minuscules
        - suppression des sauts de ligne
        - suppression des ponctuations et chiffres
        """
        texte = texte.lower()
        texte = re.sub(r"\n", " ", texte)
        texte = re.sub(r"[^\w\s]", "", texte)  # Supprime la ponctuation
        texte = re.sub(r"\d+", "", texte)  # Supprime les chiffres
        return texte

    def stats(self, n=10):
        """
        Affiche des statistiques textuelles sur le corpus :
        - Nombre de mots différents
        - Les n mots les plus fréquents
        """
        vocabulaire = defaultdict(int)
        document_frequency = defaultdict(int)
        documents_par_mot = defaultdict(set)
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            mots_uniques = set(mots)
            for mot in mots:
                vocabulaire[mot] += 1
            for mot in mots_uniques:
                documents_par_mot[mot].add(doc.id)
        for mot in documents_par_mot:
            document_frequency[mot] = len(documents_par_mot[mot])
        freq = pd.DataFrame({
            "mot": list(vocabulaire.keys()),
            "term frequency": list(vocabulaire.values()),
            "document frequency": list(document_frequency.values())
        }).sort_values(by="term frequency", ascending=False)
        print(f"Nombre de mots différents dans le corpus : {len(vocabulaire)}")
        print(f"Les {n} mots les plus fréquents :")
        print(freq.head(n))

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
                    nb_commentaires=0
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

    def build_vocab(self):
        vocab = {}
        id = 0
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = set(texte_nettoye.split())
            for mot in mots:
                if mot not in vocab:
                    vocab[mot] = {"id": id, "term_frequency": 0, "document_frequency": 0}
                    id += 1
                vocab[mot]["term_frequency"] += texte_nettoye.split().count(mot)
                vocab[mot]["document_frequency"] += 1
        return vocab

    def build_tf_matrix(self, vocab):
        n_docs = len(self.id2doc)
        n_terms = len(vocab)
        rows, cols, data = [], [], []
        for doc_id, doc in enumerate(self.id2doc.values()):
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            for mot in set(mots):
                term_id = vocab[mot]["id"]
                count = mots.count(mot)
                rows.append(doc_id)
                cols.append(term_id)
                data.append(count)
        mat_TF = csr_matrix((data, (rows, cols)), shape=(n_docs, n_terms))
        return mat_TF

    def build_tfidf_matrix(self, mat_TF, vocab):
        n_docs = len(self.id2doc)
        n_terms = len(vocab)
        idf = np.zeros(n_terms)
        for i, mot in enumerate(vocab):
            idf[i] = np.log(n_docs / vocab[mot]["document_frequency"])
        mat_TFxIDF = mat_TF.multiply(idf)
        return mat_TFxIDF

    def query_to_vector(self, query, vocab, mat_TFxIDF):
        query_terms = self.nettoyer_texte(query).split()
        vector = np.zeros(len(vocab))
        for term in query_terms:
            if term in vocab:
                vector[vocab[term]["id"]] = 1
        return vector

class CorpusSingleton:
    _instance = None

    def __new__(cls, nom):
        if cls._instance is None:
            cls._instance = super(CorpusSingleton, cls).__new__(cls)
            cls._instance.corpus = Corpus(nom)
        return cls._instance

    def get_corpus(self):
        return self.corpus
