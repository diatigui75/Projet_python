# ====================================================
# TD8 – Corpus simplifié et compatible avec le CSV
# ====================================================

from Document import Document

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.id2doc = {}   # id → Document
        self.ndoc = 0

    def ajouter_document(self, document):
        """Ajoute un document (phrase) au corpus."""
        if document.id not in self.id2doc:
            self.id2doc[document.id] = document
            self.ndoc += 1

    def search(self, mots_cles, k=10):
        """
        Recherche simple : retourne les documents contenant TOUS les mots-clés.
        """
        mots = mots_cles.lower().split()
        résultats = []

        for doc in self.id2doc.values():
            texte = doc.texte.lower()
            if all(m in texte for m in mots):
                résultats.append(doc)

        return résultats[:k]

    def concorde(self, mot, n=30):
        """
        Affiche le contexte autour d'un mot (concordancier).
        """
        results = []
        for doc in self.id2doc.values():
            txt = doc.texte
            pos = txt.lower().find(mot.lower())
            if pos != -1:
                gauche = txt[max(0, pos-n):pos]
                droite = txt[pos+len(mot):pos+len(mot)+n]
                results.append((gauche, mot, droite))
        return results
