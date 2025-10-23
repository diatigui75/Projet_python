import urllib.request
import xmlrpc
import xmltodict
import pandas as pd
#Dans un premier temps nous importons la biblio praw
#Installé par la cmd pip : pip install praw
import praw
docs = [] #la liste qui stockera le contenu textuel des documents
#Initialisation de praw
reddit = praw.Reddit(client_id='4B6xFHATWb_huTaiPU7DAA',
                                    client_secret='ceXpXLS3ygoKw1FW8TxefW5a4CLQLA',
                                    user_agent='OurProjet')
#Utilisation de la function de recherche de praw
thematique = 'funny'
limit = 2
print(f"Récupération des documents Reddit aavec la réquêt : '{thematique}'")
for submission in reddit.subreddit('all').search(thematique, limit = limit):
    #Concatener le text avec le titre
    text = f"{submission.title}.{submission.selftext}".strip()
    #Ignorer les documents vides ou supprimés
    if text and submission.selftext != '[deleted]':
    #Ramplacer les sauts de lignes par espace(' ')
        clean_text = text.replace('\n', ' ').replace('\r', ' ')
        docs.append(clean_text)
print(f"Document Récupéré de Reddit : {docs}")

base_url = "http://export.arxiv.org/api/query?"
search_query = "funny"
max_resultat = 2
docs = []
entries = []
query_url = f"{base_url}search_query={search_query}&start=0&max_results={max_resultat}"

print(f"\nRécupération des documents avec la réquête : {search_query}")

try:
    with urllib.request.urlopen(query_url) as url:
        xml_data = url.read()
        data_dict = xmltodict.parse(xml_data)
        entries = data_dict['feed'].get('entry',[])
        if not isinstance(entries, list):
            entries = [entries]
        for entry in entries:
            title = entry.get('title', '').strip()
            summery = entry.get('summary', '').strip()
            text = f"{title}.{summery}".strip()
            if text :
                clean_text = text.replace('\n', ' ').replace('\r', ' ')
                docs.append(clean_text)
except Exception as e :
    print("Erreur lors de la récupération Arxiv :", e)

print("Documents récuperés d'Arxiv :", len(entries))
print("Documents récuperés d'Arxiv :", docs)

# 2.1 Création du DataFrame
data = {
    "id": list(range(1, len(docs) + 1)),
    "texte": docs,
    "origine": ["arxiv"] * len(docs)
}
df = pd.DataFrame(data)
# 2.2 Sauvegarde en CSV avec tabulation comme séparateur
df.to_csv("documents_sauvegardes.csv", sep='\t', index=False)
print("Fichier sauvegardé sous 'documents_sauvegardes.csv'.")
# 2.3 Chargement direct depuis le fichier CSV
df_charge = pd.read_csv("documents_sauvegardes.csv", sep='\t')
print("\nContenu du fichier chargé :")
print(df_charge)


#PARTIE 3

# 3.1 Taille du corpus
print(f"Taille du corpus (nombre de documents) : {len(df)}")

# 3.2 Nombre de mots et de phrases par document
df['nombre_de_mots'] = df['texte'].apply(lambda x: len(x.split()))
df['nombre_de_phrases'] = df['texte'].apply(lambda x: len(x.split('.')))
print("\nNombre de mots et de phrases par document :")
print(df[['id', 'nombre_de_mots', 'nombre_de_phrases']])

# 3.3 Suppression des documents trop petits
df = df[df['texte'].str.len() >= 20]
print(f"\nTaille du corpus après suppression des documents trop petits : {len(df)}")

# 3.4 Création d'une chaîne unique
corpus_unique = ' '.join(df['texte'])
print(f"\nLongueur de la chaîne unique : {len(corpus_unique)} caractères")