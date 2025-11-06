class Auteur:
    def __init__(self, name):
        self.name = name
        self.nbdocs = 0
        self.production = {}  # {doc_id: document}

    def add(self, doc_id, document):
        """Ajoute un document à la production de l'auteur et met à jour le nombre de documents."""
        self.production[doc_id] = document
        self.nbdocs += 1

    def __str__(self):
        """Représentation simplifiée de l'auteur (pour print)."""
        return f"Auteur: {self.name} - {self.nbdocs} document(s)"

    def __repr__(self):
        """Représentation détaillée de l'auteur (pour le débogage)."""
        return f"Auteur(name='{self.name}', nbdocs={self.nbdocs})"

    def get_taille_moyenne_doc(self):
        """Calcule la taille moyenne des documents de l'auteur (en nombre de caractères)."""
        if self.nbdocs == 0:
            return 0
        total_carac = sum(len(doc.texte) for doc in self.production.values())
        return total_carac / self.nbdocs
