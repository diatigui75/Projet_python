

# Dictionnaire global pour les auteurs
id2aut = {}

def ajouter_document(titre, auteur_nom, date, url, texte):
    """Ajoute un document et met à jour les dictionnaires id2doc et id2aut."""
    doc = Document(titre, auteur_nom, date, url, texte)

    # Mise à jour de id2aut
    if auteur_nom not in id2aut:
        id2aut[auteur_nom] = Auteur(auteur_nom)
    id2aut[auteur_nom].add(doc.id, doc)

    return doc

# Exemple d'utilisation
doc1 = ajouter_document(
    titre="Introduction à Python",
    auteur_nom="Julien Velcin",
    date="2025-10-01",
    url="https://example.com/doc1",
    texte="Python est un langage de programmation puissant et facile à apprendre..."
)

# Affichage des informations de l'auteur
print(id2aut["Julien Velcin"])
print(f"Taille moyenne des documents: {id2aut['Julien Velcin'].get_taille_moyenne_doc()} caractères")
