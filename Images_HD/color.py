import cv2
import numpy as np
import os
import shutil
from pathlib import Path
from sklearn.cluster import KMeans

# Paramètres
nombre_clusters = 5  # Modifier selon le besoin
seuil_diversite = 3  # Modifier selon le besoin

# Dossiers de sortie
dossier_colore = 'Coloré'
dossier_non_colore = 'Non_Coloré'

# Créer les dossiers s'ils n'existent pas
Path(dossier_colore).mkdir(exist_ok=True)
Path(dossier_non_colore).mkdir(exist_ok=True)

def analyser_image(chemin_image):
    
    nom_image = os.path.basename(chemin_image)

    image = cv2.imread(chemin_image)
    
    # Vérifier si l'image a été chargée correctement
    if image is None:
        print(f"Impossible de lire l'image : {chemin_image}")
        return  # Sortir de la fonction si l'image n'est pas lue
    
    # Continuer le traitement si l'image a été chargée correctement
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except cv2.error as e:
        print(f"Erreur lors de la conversion de l'image : {chemin_image}")
        print(e)
        return  # Sortir de la fonction si la conversion échoue

    # Réduire la taille de l'image pour accélérer le processus
    image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
    
    # Reshape l'image pour être une liste de pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # Utiliser KMeans pour quantifier les couleurs
    clt = KMeans(n_clusters=nombre_clusters)
    labels = clt.fit_predict(image)
    
    # Compter le nombre d'occurrences de chaque couleur quantifiée
    _, counts = np.unique(labels, return_counts=True)
    
    # Nombre de couleurs significatives (plus de 5% de l'image)
    nombre_couleurs_significatives = np.sum(counts > (0.05 * image.shape[0]))
    print(f"{nom_image}: {nombre_couleurs_significatives} couleurs significatives")

    # Classer l'image et déplacer dans le dossier approprié
    dossier_cible = dossier_colore if nombre_couleurs_significatives > seuil_diversite else dossier_non_colore
    chemin_destination = os.path.join(dossier_cible, nom_image)
    shutil.move(chemin_image, chemin_destination)

# Parcourir toutes les images dans le dossier spécifié
chemin_dossier = 'Amas'  # Modifier selon le besoin
for fichier in os.listdir(chemin_dossier):
    if fichier.lower().endswith(('.png', '.jpg', '.jpeg')):
        analyser_image(os.path.join(chemin_dossier, fichier))
