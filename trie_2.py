import os
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import UnidentifiedImageError

# Charger le modèle pré-entraîné
model = load_model('Projet.keras')

# Dossier contenant les images à classifier
image_folder = 'Lunes_2'

# Dossier pour sauvegarder les images classifiées comme Nébuleuse
save_folder = 'Lu_att'


if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Parcourir toutes les images dans le dossier
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    
    try:
        # Charger l'image, ajuster les dimensions et prétraiter
        image = load_img(image_path, target_size=(128, 128))  # Ajuster à la taille attendue par le modèle
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)  # Faire correspondre la forme attendue par le modèle
        
        # Prédire la classe de l'image
        predictions = model.predict(image_array)
        
        # Vérifier si l'image est classifiée comme Nébuleuse avec proba >= 0.95
        if predictions[0][4] >= 0.98:
            # Sauvegarder l'image dans le nouveau dossier
            print(predictions[0])
            save_path = os.path.join(save_folder, image_name)
            image.save(save_path)
        else:
            # Supprimer l'image si elle ne correspond pas à la classification désirée
            os.remove(image_path)

    except UnidentifiedImageError:
        print(f"Erreur : Impossible d'identifier ou de lire l'image {image_name}. Elle sera supprimée.")
        os.remove(image_path)
    except Exception as e:
        print(f"Erreur inattendue avec l'image {image_name}: {e}")

print("Classification et nettoyage terminés.")
