import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.preprocessing.image import save_img

input_directory = "Images_HD/Lunes/validation"
output_directory = "Images_HD/Lunes/validation_bis"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Définition du générateur d'augmentation d'image
train_datagen = ImageDataGenerator(
    rotation_range=90,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip = True,
    brightness_range = [0.25,1],
    channel_shift_range = 100,
    
)

for filename in os.listdir(input_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        img = load_img(os.path.join(input_directory, filename))
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        i = 0
        for batch in train_datagen.flow(x, batch_size=1, save_to_dir=output_directory, save_prefix='aug', save_format='jpeg'):
            i += 1
            if i >= 1: 
                break  
