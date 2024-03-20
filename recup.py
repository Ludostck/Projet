import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm 
import time  

folder_name = 'Saturne'
max_images =1500  # Le nombre total d'images à télécharger
images_downloaded = 0  # Compteur du nombre d'images téléchargées

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Dossier '{folder_name}' créé.")

session = requests.Session()  
topic = "Saturne"

def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

start_time = time.time()
images_to_download = max_images  

pbar = tqdm(total=images_to_download, unit="img", ncols=200)

def scrape_and_download_image(detail_page_url, session, folder_name):
    global start_time
    global images_downloaded
    """Fonction pour extraire les liens d'une page et télécharger une image spécifique."""
    try:
        detail_response = session.get(detail_page_url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        img_url_tag = detail_soup.find('meta', {'property': 'og:image'})
        if img_url_tag:  
            img_url = img_url_tag['content'] 
           
            img_name = img_url.split('/')[3] + ".jpg"
          
            full_path = os.path.join(folder_name, img_name)

            img_data = requests.get(img_url).content
            with open(full_path, 'wb') as file:
                file.write(img_data)
                images_downloaded += 1
                
               
                elapsed_time = time.time() - start_time
                estimated_total_time = elapsed_time / images_downloaded * images_to_download if images_downloaded > 0 else float('inf')
                remaining_time = estimated_total_time - elapsed_time
                pbar.set_description(f"Temps restant estimé: {format_time(remaining_time)}")
                pbar.update(1)  
                        

     

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
    page = 5
    while images_downloaded < images_to_download:
        url = f"https://www.astrobin.com/search/?q={topic}&d=i&t=all&date_published_min=2011-11-09&date_published_max=2024-02-09&page={page}"
        scrape_page(url, session)
        
        page += 1
        if images_downloaded >= max_images:
            print("\nNombre maximal d'images téléchargées atteint.")
            break
        
        

finally:
    pbar.close()  
