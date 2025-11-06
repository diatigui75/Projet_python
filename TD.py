# Matrice des poids (comme sur le tableau)
matrice_poids = [
    [0, -1, 1, 1],
    [-1, 0, 1, -1],
    [1, 1, 0, 1],
    [1, -1, 1, 0]
]

# Fonction d'activation (comme sur le tableau)
f_activation = lambda x: 1 if x > 0 else 0

# Liste des configurations initiales (comme sur le tableau)
configs = [
    [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
    [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
    [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
    [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]
]

# Fonction pour calculer l'activation d'une cellule (comme sur le tableau)
def calculer_activation(matrice, config, cellule):
    somme = 0
    for j in range(4):
        somme += matrice[cellule][j] * config[j]
    return f_activation(somme)

# Fonction pour calculer l'état suivant en mode synchrone
def etat_suivant_synchrone(matrice, config):
    nouvelle_config = [0, 0, 0, 0]
    for cellule in range(4):
        nouvelle_config[cellule] = calculer_activation(matrice, config, cellule)
    return nouvelle_config

# Fonction pour calculer l'état suivant en mode asynchrone (ordre : a, b, c, d)
def etat_suivant_asynchrone(matrice, config):
    nouvelle_config = config.copy()
    for cellule in range(4):
        nouvelle_config[cellule] = calculer_activation(matrice, nouvelle_config, cellule)
    return nouvelle_config

# Fonction pour analyser les trajectoires (comme sur le tableau)
def analyser_trajectoires(matrice, configs, mode="synchrone"):
    trajectoires = {}
    for config in configs:
        etat_actuel = config.copy()
        trajectoire = [etat_actuel.copy()]
        while True:
            if mode == "synchrone":
                etat_actuel = etat_suivant_synchrone(matrice, etat_actuel)
            else:
                etat_actuel = etat_suivant_asynchrone(matrice, etat_actuel)

            if etat_actuel in trajectoire:
                trajectoire.append(etat_actuel.copy())
                break
            trajectoire.append(etat_actuel.copy())

        trajectoires[tuple(config)] = trajectoire
    return trajectoires

# Analyse des trajectoires synchrones
trajectoires_synchrones = analyser_trajectoires(matrice_poids, configs, mode="synchrone")

# Analyse des trajectoires asynchrones
trajectoires_asynchrones = analyser_trajectoires(matrice_poids, configs, mode="asynchrone")

# Affichage des résultats (comme sur le tableau)
def afficher_trajectoires(trajectoires):
    for config, trajectoire in trajectoires.items():
        print(f"Config initiale: {config}")
        print(f"Trajectoire: {trajectoire}\n")

print("Trajectoires synchrones :")
afficher_trajectoires(trajectoires_synchrones)

print("\nTrajectoires asynchrones :")
afficher_trajectoires(trajectoires_asynchrones)
