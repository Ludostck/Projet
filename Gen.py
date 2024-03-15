import PIL
from PIL import Image
import numpy as np
import os
import glob  # Ajout pour utiliser glob.glob
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Reshape, Flatten, Conv2D, Conv2DTranspose, LeakyReLU, BatchNormalization, Dropout, Input
import time

# Paramètres de configuration
image_directory = 'generated_images/Neb'
images_list = []
IM_SIZE = 128  # Vous pouvez changer cette valeur pour ajuster la taille des images
BASE_DEPTH = 64  # Profondeur de base pour les couches du modèle, peut être ajustée

# Charger et préparer les images
for image_path in glob.glob(f'{image_directory}/*.jpg'):
    with Image.open(image_path) as img:
        img = img.resize((IM_SIZE, IM_SIZE))
        img_array = np.asarray(img)
        images_list.append(img_array)

x_train = np.array(images_list)
x_train = (x_train.astype(np.float32) - 127.5) / 127.5
print("Nombre d'images chargées :", x_train.shape[0])

# Paramètres du modèle
noise_dim = 100
start_size = IM_SIZE // 8  # Taille de départ pour le Reshape dans le générateur

# Modèle du générateur
generator_input = Input(shape=(noise_dim,))
x = Dense(start_size * start_size * BASE_DEPTH * 8)(generator_input)  # Adaptation dynamique à IM_SIZE
x = LeakyReLU(alpha=0.2)(x)
x = Reshape((start_size, start_size, BASE_DEPTH * 8))(x)

# Expansion progressive de l'image
x = Conv2DTranspose(BASE_DEPTH * 4, kernel_size=4, strides=2, padding='same')(x)
x = BatchNormalization()(x)
x = LeakyReLU(alpha=0.2)(x)

x = Conv2DTranspose(BASE_DEPTH * 2, kernel_size=4, strides=2, padding='same')(x)
x = BatchNormalization()(x)
x = LeakyReLU(alpha=0.2)(x)

x = Conv2DTranspose(BASE_DEPTH, kernel_size=4, strides=2, padding='same')(x)
x = BatchNormalization()(x)
x = LeakyReLU(alpha=0.2)(x)

x = Conv2DTranspose(3, kernel_size=4, strides=1, padding='same', activation='tanh')(x)  # La sortie est (IM_SIZE, IM_SIZE, 3)
generator_model = Model(generator_input, x)

# Modèle du discriminateur
discriminator_input = Input(shape=(IM_SIZE, IM_SIZE, 3))
y = Conv2D(BASE_DEPTH, kernel_size=3, strides=2, padding='same')(discriminator_input)
y = LeakyReLU(alpha=0.2)(y)
y = Dropout(0.3)(y)

y = Conv2D(BASE_DEPTH * 2, kernel_size=3, strides=2, padding='same')(y)
y = LeakyReLU(alpha=0.2)(y)
y = Dropout(0.3)(y)

y = Conv2D(BASE_DEPTH * 4, kernel_size=3, strides=2, padding='same')(y)
y = LeakyReLU(alpha=0.2)(y)
y = Dropout(0.3)(y)

y = Flatten()(y)
y = Dense(1, activation='sigmoid')(y)

discriminator_model = Model(discriminator_input, y)
discriminator_model.compile(loss='binary_crossentropy', optimizer='adam')

# Compilation du modèle GAN (inutile de le changer)
discriminator_model.trainable = False  # Assurez-vous que cela est fait avant de compiler le modèle GAN
gan_input = Input(shape=(noise_dim,))
gan_output = discriminator_model(generator_model(gan_input))
gan_model = Model(gan_input, gan_output)
gan_model.compile(loss='binary_crossentropy', optimizer='adam')

import matplotlib.pyplot as plt
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def generate_and_visualize_images(generator_model, noise_dim, epoch, examples=2):
    # Générer le bruit et les images
    noise = np.random.normal(0, 1, (examples, noise_dim))
    generated_images = generator_model.predict(noise)

    # Sauvegarder les images générées
    save_dir = 'generated_images'  # S'assurer que ce répertoire est correct
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i in range(examples):
        # Convertir l'image à une échelle de 0 à 255
        img = (generated_images[i] * 127.5 + 127.5).astype(np.uint8)
        img = Image.fromarray(img)  # Convertir le tableau en objet Image PIL
        file_name = f'generated_{epoch + 1}_{i + 1}.png'  # Format de nom de fichier unique pour chaque image
        img.save(os.path.join(save_dir, file_name))


def train_gan(gan_model, generator_model, discriminator_model, dataset, epochs, batch_size, noise_dim, display_interval=100):
    start_time = time.time()  # Début du suivi du temps total

    for epoch in range(epochs):
        # Début de l'époque
        epoch_start_time = time.time()

        # Partie Discriminateur
        idx = np.random.randint(0, dataset.shape[0], batch_size)

        real_images = dataset[idx]

        noise = np.random.normal(0, 1, (batch_size, noise_dim))
        fake_images = generator_model.predict(noise)

        discriminator_model.trainable = True
        d_loss_real = discriminator_model.train_on_batch(real_images, np.ones((batch_size, 1)))
        d_loss_fake = discriminator_model.train_on_batch(fake_images, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Partie GAN (générateur)
        noise = np.random.normal(0, 1, (batch_size, noise_dim))
        discriminator_model.trainable = False
        g_loss = gan_model.train_on_batch(noise, np.ones((batch_size, 1)))

        # Temps écoulé pour l'époque
        epoch_elapsed_time = time.time() - epoch_start_time
        print(f'Époque {epoch + 1}/{epochs}, D Loss: {d_loss}, G Loss: {g_loss}, Temps écoulé: {epoch_elapsed_time:.2f}s')


        # Afficher la progression
        if (epoch) % display_interval == 0:
            print(f'Époque {epoch + 1}/{epochs}, D Loss: {d_loss}, G Loss: {g_loss}, Temps écoulé: {epoch_elapsed_time:.2f}s')
            generate_and_visualize_images(generator_model, noise_dim, epoch,examples=5)  # Ici, ajustez 'examples' selon le nombre d'images que vous souhaitez générer

    total_elapsed_time = time.time() - start_time
    print(f'Entraînement terminé. Temps total écoulé: {total_elapsed_time:.2f}s')

# Maintenant, lancez l'entraînement avec votre nouvelle configuration
train_gan(gan_model, generator_model, discriminator_model, x_train, epochs=10000, batch_size=16, noise_dim=noise_dim)  # Réduit la taille du batch
