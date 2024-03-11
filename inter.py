import os
from PIL import Image

# Chemins des dossiers
input_directory = 'Interpol'
output_directory = 'Interpols'

# Facteur d'interpolation
alpha = 0.5

# Création du dossier de destination s'il n'existe pas
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Obtenir la liste de tous les fichiers image dans le dossier source
images = [f for f in os.listdir(input_directory) if f.endswith('.jpg') or f.endswith('.png')]  # Ajoutez d'autres formats si nécessaire
images.sort()  # Assurez-vous que les images sont triées si leur ordre est important

# Interpoler les images deux à deux
for i in range(len(images) - 1):  # -1 car on prend des paires
    # Ouvrir les images
    image1 = Image.open(os.path.join(input_directory, images[i])).convert('RGBA')
    image2 = Image.open(os.path.join(input_directory, images[i+1])).convert('RGBA')

    # Assurer que les deux images ont la même taille
    image2 = image2.resize(image1.size, Image.LANCZOS)

    # Créer l'image interpolée
    interpolated_image = Image.blend(image1, image2, alpha)

    # Construire le chemin de sortie et sauvegarder l'image interpolée
    output_path = os.path.join(output_directory, f'interpolated_{i}.png')
    interpolated_image.save(output_path)
