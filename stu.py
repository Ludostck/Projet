import os
import shutil
from glob import glob
import math

# Définir les pourcentages pour les dossiers Train, Validation et Test
pourcentages = {'Train': 0.8, 'Validation': 0.15, 'Test': 0.05}

# Définir les dossiers originaux
dossiers_originaux = ['Galaxie', 'Nébuleuse', 'Comète', 'Ama', 'Lune']
dossier_principal = 'Images'

# Créer les nouveaux dossiers pour chaque catégorie et sous-dossier
for cat in pourcentages:
    for dossier in dossiers_originaux:
        chemin_nouveau_dossier = os.path.join(dossier_principal, cat, dossier)
        os.makedirs(chemin_nouveau_dossier, exist_ok=True)

# Distribuer les images dans les nouveaux dossiers
for dossier in dossiers_originaux:
    chemin_dossier_orig = os.path.join(dossier_principal, dossier)
    images = glob(f'{chemin_dossier_orig}/*.jpg')  # Assurez-vous que ce sont des fichiers .jpg
    total_images = len(images)

    for cat, pourcentage in pourcentages.items():
        nb_images = math.ceil(total_images * pourcentage)
        for image in images[:nb_images]:
            shutil.move(image, os.path.join(dossier_principal, cat, dossier))
        # Mettre à jour la liste des images restantes
        images = images[nb_images:]
