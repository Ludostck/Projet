import os
from PIL import Image

def resize_and_compress_images_in_folder(folder_path, size=(600, 600), quality=90):
    """
    Redimensionne et compresse toutes les images du dossier spécifié.
    
    Args:
        folder_path: Chemin du dossier contenant les images.
        size: Nouvelle taille des images (largeur, hauteur).
        quality: Qualité de compression pour les images JPEG (1-100).
    """
    # Liste de toutes les extensions d'image acceptées
    extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(folder_path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(folder_path, filename)
        # Vérifier si le fichier est une image (par extension)
        if file_path.lower().endswith(extensions):
            try:
                # Ouvrir l'image
                with Image.open(file_path) as img:
                    # Convertir l'image en RGB si ce n'est pas le cas
                    if img.mode in ['RGBA', 'P']:
                        img = img.convert('RGB')
                    
                    # Redimensionner l'image
                    resized_img = img.resize(size, Image.Resampling.LANCZOS)
                    
                    # Construire le chemin de sortie pour les images JPEG
                    output_file_path = os.path.splitext(file_path)[0] + '.jpg'
                    
                    # Sauvegarder l'image redimensionnée et compressée
                    resized_img.save(output_file_path, 'JPEG', optimize=True, quality=quality)
                   
                    
                    # Supprimer l'image originale si différente de la nouvelle
                    if output_file_path != file_path:
                        os.remove(file_path)
                        
                        
            except Exception as e:
                # Imprimer l'erreur si quelque chose ne va pas
                print(f"Error processing image {file_path}: {e}")

# Remplacer 'your_folder_path' par le chemin du dossier contenant vos images
folder_path = 'Galaxie'  # Remplacer par le chemin de votre dossier
resize_and_compress_images_in_folder(folder_path)

