# ==============================================
# TD8 – SearchEngine simplifié compatible TD7/TD8
# ==============================================

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus

    def search(self, query, k=5):
        """
        Recherche les documents qui contiennent TOUS les mots-clés.
        Retourne une liste de documents.
        """
        keywords = query.lower().split()
        résultats = []

        for doc in self.corpus.id2doc.values():
            texte = doc.texte.lower()

            # Vérifie que tous les mots clés sont dans le document
            if all(mot in texte for mot in keywords):
                résultats.append(doc)

        # Retourner les k premiers
        return résultats[:k]
