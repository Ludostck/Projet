import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm  # Importation de la bibliothèque tqdm
import time  # Pour mesurer le temps d'exécution

# Configuration initiale
folder_name = 'Lunes'
max_images = 2500  # Le nombre total d'images à télécharger
images_downloaded = 0  # Compteur du nombre d'images téléchargées

# Créer un dossier pour sauvegarder les images
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Dossier '{folder_name}' créé.")

# Définir la session et les autres paramètres
session = requests.Session()  # Utiliser une session pour maintenir les cookies et la connexion
topic = "Moon"

# Fonction pour convertir les secondes en hh:mm:ss
def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

# Pour la barre de progression et le suivi du temps
start_time = time.time()
images_to_download = max_images  

# Initialisez la barre de progression
pbar = tqdm(total=images_to_download, unit="img", ncols=200)

def scrape_and_download_image(detail_page_url, session, folder_name):
    global start_time
    global images_downloaded
    """Fonction pour extraire les liens d'une page et télécharger une image spécifique."""
    try:
        # Accès à la page de détail
        detail_response = session.get(detail_page_url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        # Vous pouvez ajuster cette partie pour mieux cibler l'image si nécessaire
        # Exemple ici : chercher une balise meta qui contient l'URL de l'image
        img_url_tag = detail_soup.find('meta', {'property': 'og:image'})
        if img_url_tag:  # Vérifie si la balise existe
            img_url = img_url_tag['content']  # Extrayez l'URL de l'image
           
            # Générer le nom de fichier et le chemin complet
            img_name = img_url.split('/')[3] + ".png"# Extrayez le nom de fichier de l'URL
          
            full_path = os.path.join(folder_name, img_name)

            # Télécharger l'image
            img_data = requests.get(img_url).content
            with open(full_path, 'wb') as file:
                file.write(img_data)
                images_downloaded += 1
                 # Mettre à jour la barre de progression toutes les 5 images
                
               
                elapsed_time = time.time() - start_time
                estimated_total_time = elapsed_time / images_downloaded * images_to_download if images_downloaded > 0 else float('inf')
                remaining_time = estimated_total_time - elapsed_time
                pbar.set_description(f"Temps restant estimé: {format_time(remaining_time)}")
                pbar.update(1)  # Mettre à jour d'une image à la fois
                        

     

    except Exception as e:
        print(f"Erreur lors de l'accès à la page ou du téléchargement de l'image : {e}")





def scrape_page(url, session):
    """Fonction pour extraire les liens d'une page et télécharger les images."""
    global images_downloaded
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    thumbnails = soup.find_all('li', class_='thumbnail astrobin-thumbnail')
    for thumb in thumbnails:
        if images_downloaded >= max_images:
            break  # Arrête la boucle si le nombre maximal d'images est atteint
        link = thumb.find('a', href=True)
        
        if link:
            detail_page_url = f"https://www.astrobin.com{link['href']}"
            
            scrape_and_download_image(detail_page_url,session,folder_name)



try:
    page = 1
    while images_downloaded < images_to_download:
        url = f"https://www.astrobin.com/search/?q={topic}&d=i&t=all&date_published_min=2011-11-09&date_published_max=2024-02-09&page={page}"
        scrape_page(url, session)
        
        page += 1
        if images_downloaded >= max_images:
            print("\nNombre maximal d'images téléchargées atteint.")
            break
        
        

finally:
    pbar.close()  # Assurez-vous de fermer la barre de progression à la fin