from datetime import datetime
import uuid

# Dictionnaire global pour stocker les documents
id2doc = {}

class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = self.__convertir_date(date)
        self.url = url
        self.texte = texte
        self.id = str(uuid.uuid4())  # Identifiant unique
        self.type = "Document"  # Champ pour identifier le type
        id2doc[self.id] = self  # Ajoute l'instance au dictionnaire global

    def __convertir_date(self, date_str):
        """Convertit une chaîne de date en objet datetime."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.strptime(date_str, "%d/%m/%Y")

    def afficher_infos(self):
        """Affiche toutes les informations du document."""
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date.strftime('%Y-%m-%d')}")
        print(f"URL: {self.url}")
        print(f"Texte: {self.texte[:100]}...")

    def __str__(self):
        """Représentation simplifiée du document (pour print)."""
        return f"Document: {self.titre}"

    def __repr__(self):
        """Représentation détaillée du document (pour le débogage)."""
        return f"Document(titre='{self.titre}', auteur='{self.auteur}', date='{self.date.strftime('%Y-%m-%d')}')"

    def get_type(self):
        """Retourne le type du document."""
        return self.type

class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_commentaires = nb_commentaires
        self.type = "Reddit"

    def get_nb_commentaires(self):
        """Retourne le nombre de commentaires."""
        return self.nb_commentaires

    def set_nb_commentaires(self, nb_commentaires):
        """Met à jour le nombre de commentaires."""
        self.nb_commentaires = nb_commentaires

    def __str__(self):
        """Représentation simplifiée du document Reddit."""
        return f"RedditDocument: {self.titre} ({self.nb_commentaires} commentaires)"

class ArxivDocument(Document):
    def __init__(self, titre, auteurs, date, url, texte):
        super().__init__(titre, ", ".join(auteurs), date, url, texte)
        self.auteurs = auteurs  # Liste des co-auteurs
        self.type = "Arxiv"

    def get_auteurs(self):
        """Retourne la liste des auteurs."""
        return self.auteurs

    def set_auteurs(self, auteurs):
        """Met à jour la liste des auteurs."""
        self.auteurs = auteurs

    def __str__(self):
        """Représentation simplifiée du document Arxiv."""
        return f"ArxivDocument: {self.titre} (par {len(self.auteurs)} auteurs)"

class DocumentFactory:
    @staticmethod
    def create_document(type_doc, **kwargs):
        if type_doc == "Reddit":
            return RedditDocument(**kwargs)
        elif type_doc == "Arxiv":
            return ArxivDocument(**kwargs)
        else:
            return Document(**kwargs)

