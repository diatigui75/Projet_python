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
