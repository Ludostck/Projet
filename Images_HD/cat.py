import os
import shutil
from sklearn.model_selection import train_test_split

def split_dataset_into_train_validation_test(src_folder, train_size=0.85, validation_size=0.1, test_size=0.05):
    if (train_size + validation_size + test_size) != 1.0:
        raise ValueError("Les proportions doivent s'ajouter à 1.")

    train_folder = os.path.join(src_folder, 'train')
    validation_folder = os.path.join(src_folder, 'validation')
    test_folder = os.path.join(src_folder, 'test')
    for folder in [train_folder, validation_folder, test_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    all_files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
    
    train_files, test_files = train_test_split(all_files, test_size=(validation_size + test_size), random_state=42)
    validation_files, test_files = train_test_split(test_files, test_size=test_size/(validation_size + test_size), random_state=42)

    def move_files(files, destination):
        for f in files:
            shutil.move(os.path.join(src_folder, f), os.path.join(destination, f))

    move_files(train_files, train_folder)
    move_files(validation_files, validation_folder)
    move_files(test_files, test_folder)

    print("Les fichiers ont été divisés en entraînement, validation, et test avec succès.")

split_dataset_into_train_validation_test('Comètes')

