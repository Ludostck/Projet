import os
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import UnidentifiedImageError, Image

# Charger le modèle pré-entraîné
modele_charge = load_model('meilleur_modele_2.h5')

# Dossier contenant les images à classifier
image_folder = 'Com_gen'
IMAGE_SIZE = 225
CLASSES = ['Galaxie', 'Nébuleuse', 'Comète', 'Lune', "Saturne"]
i = 0
# Parcourir toutes les images dans le dossier
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    
    try:
        # Charger l'image, ajuster les dimensions et prétraiter
        img = Image.open(image_path)
        img = Image.open(image_path).convert('RGB')
        img2 = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
        
        img_array = np.array(img2) / 255.0  # Normalisation
        img_array = img_array.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))  # Ajout de la dimension du batch
        # Prédiction
        predictions = modele_charge.predict(img_array)
        predicted_class = CLASSES[np.argmax(predictions)]
        prob = np.max(predictions)
        
        # Supprimer l'image si elle n'est pas classifiée comme 'Lune'
        if predicted_class != "Comète":
            os.remove(image_path)
        else:
            # Renommer le fichier si l'image est classifiée comme 'Lune'
            i = i +1
            new_name = f"Com_{prob:.2f}_{i}.jpg"
            new_path = os.path.join(image_folder, new_name)
            os.rename(image_path, new_path)
            
    except UnidentifiedImageError:
        print(f"Erreur : Impossible d'identifier ou de lire l'image {image_name}. Elle sera supprimée.")
        os.remove(image_path)
    except Exception as e:
        print(f"Erreur inattendue avec l'image {image_name}: {e}")

print("Classification et nettoyage terminés.")
