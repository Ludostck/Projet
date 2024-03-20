import os
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import UnidentifiedImageError,Image

# Charger le modèle pré-entraîné
model = load_model('Projet.keras')

# Dossier contenant les images à classifier
image_folder = 'Amas_2'
CLASSES = ['Galaxie', 'Nébuleuses', 'Comètes','Amas','Lunes']
# Dossier pour sauvegarder les images classifiées comme Nébuleuse
save_folder = 'Am_att'

IMAGE_SIZE = 128
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Parcourir toutes les images dans le dossier
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    
    try:
        # Charger l'image, ajuster les dimensions et prétraiter
        img = Image.open(image_path)
        img2 = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)

        img_array = np.array(img2) / 255.0  # Normalisation
        img_array = img_array.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))  # Ajout de la dimension du batch
            # Prédiction
        predictions = model.predict(img_array)
        predicted_class = CLASSES[np.argmax(predictions)]  # Remplacer CLASSES par vos classes réelles
        prob = np.max(predictions)
        # Vérifier si l'image est classifiée comme Nébuleuse avec proba >= 0.95
        if predicted_class== "Amas" and prob >= 0.95:
            # Sauvegarder l'image dans le nouveau dossier
            img = img.resize((600, 600), Image.Resampling.LANCZOS)
            save_path = os.path.join(save_folder, image_name)
            img.save(save_path)
            

            
        
    except UnidentifiedImageError:
        print(f"Erreur : Impossible d'identifier ou de lire l'image {image_name}. Elle sera supprimée.")
        os.remove(image_path)
    except Exception as e:
        print(f"Erreur inattendue avec l'image {image_name}: {e}")

print("Classification et nettoyage terminés.")
