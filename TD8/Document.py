# ====================================================
# TD8 – Version simplifiée et compatible de Document
# ====================================================

import uuid

class Document:
    def __init__(self, texte, auteur):
        self.texte = texte
        self.auteur = auteur
        self.id = str(uuid.uuid4())

    def __str__(self):
        return f"{self.auteur} : {self.texte[:80]}..."

    def get_text(self):
        return self.texte

    def get_author(self):
        return self.auteur
