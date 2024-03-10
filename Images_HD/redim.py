import os
from PIL import Image

def resize_and_compress_images_in_folder(folder_path, size=(600, 600), quality=90):
  
    extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if file_path.lower().endswith(extensions):
            try:
                with Image.open(file_path) as img:
                    if img.mode in ['RGBA', 'P']:
                        img = img.convert('RGB')
                    
                    resized_img = img.resize(size, Image.Resampling.LANCZOS)
                    
                    output_file_path = os.path.splitext(file_path)[0] + '.jpg'
                    
                    resized_img.save(output_file_path, 'JPEG', optimize=True, quality=quality)
                   
                    
                    if output_file_path != file_path:
                        os.remove(file_path)
                        
                        
            except Exception as e:
                print(f"Error processing image {file_path}: {e}")

folder_path = 'Galaxie' 
resize_and_compress_images_in_folder(folder_path)

