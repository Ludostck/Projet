import os
from PIL import Image

input_directory = 'Interpol'
output_directory = 'Interpols'

alpha = 0.5

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

images = [f for f in os.listdir(input_directory) if f.endswith('.jpg') or f.endswith('.png')] 
images.sort() 

for i in range(len(images) - 1): 
    image1 = Image.open(os.path.join(input_directory, images[i])).convert('RGBA')
    image2 = Image.open(os.path.join(input_directory, images[i+1])).convert('RGBA')

    image2 = image2.resize(image1.size, Image.LANCZOS)

    interpolated_image = Image.blend(image1, image2, alpha)

    output_path = os.path.join(output_directory, f'interpolated_{i}.png')
    interpolated_image.save(output_path)
