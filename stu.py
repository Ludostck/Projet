
import os
import shutil

original_base = 'Images_HD'
new_base = 'Images'

categories = ['train', 'validation', 'test']

for category in categories:
    new_category_path = os.path.join(new_base, category)
    if not os.path.exists(new_category_path):
        os.makedirs(new_category_path)

for folder in os.listdir(original_base):
    original_folder_path = os.path.join(original_base, folder)

    if not os.path.isdir(original_folder_path):
        continue

    for category in categories:
        original_category_path = os.path.join(original_folder_path, category)

        if not os.path.exists(original_category_path):
            continue

        new_folder_path = os.path.join(new_base, category, folder)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        for filename in os.listdir(original_category_path):
            src_file = os.path.join(original_category_path, filename)
            dest_file = os.path.join(new_folder_path, filename)
            if os.path.isfile(src_file):  
                shutil.copy(src_file, dest_file)


