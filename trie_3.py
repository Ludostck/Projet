import os
from PIL import Image

# Chemin du dossier contenant les images
image_folder = 'Moon_gen/zoom'
# Création des sous-dossiers pour le tri
os.makedirs(os.path.join(image_folder, 'Bordures_noires'), exist_ok=True)
os.makedirs(os.path.join(image_folder, 'Bordures_autres'), exist_ok=True)

# Définir la taille de la zone de coin à analyser
taille_zone = 50  # par exemple, une zone de 10x10 pixels dans chaque coin

# Pourcentage requis de pixels noirs
pourcentage_noir_requis = 80

# Parcourir toutes les images dans le dossier
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    if os.path.isfile(image_path):
        try:
            with Image.open(image_path) as img:
                # Convertir en niveaux de gris pour simplifier
                img_gray = img.convert('L')
                width, height = img.size

                # Définir les zones des coins
                zones_coins = [
                    (0, 0, taille_zone, taille_zone),  # coin en haut à gauche
                    (width - taille_zone, 0, width, taille_zone),  # coin en haut à droite
                    (0, height - taille_zone, taille_zone, height),  # coin en bas à gauche
                    (width - taille_zone, height - taille_zone, width, height)  # coin en bas à droite
                ]

                # Compter les pixels noirs dans les zones des coins
                noirs_total = 0
                total_pixels = 0
                for zone in zones_coins:
                    coin = img_gray.crop(zone)
                    pixels = list(coin.getdata())
                    noirs_total += sum(1 for pixel in pixels if pixel < 30)  # considérer noir si < 30 sur échelle de gris
                    total_pixels += len(pixels)

                # Calculer le pourcentage total de pixels noirs dans les coins
                pourcentage_noir = (noirs_total / total_pixels) * 100

                # Trier dans les sous-dossiers appropriés
                dest_folder = 'Bordures_noires' if pourcentage_noir >= pourcentage_noir_requis else 'Bordures_autres'
                new_path = os.path.join(image_folder, dest_folder, image_name)
                os.rename(image_path, new_path)

        except Exception as e:
            print(f"Erreur lors du traitement de l'image {image_name}: {e}")
