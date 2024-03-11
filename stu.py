# Here is a Python script that accomplishes the directory structure transformation:

import os
import shutil

# Define the original and new structure base paths
original_base = 'Images_HD'
new_base = 'Images'

# Define the categories
categories = ['train', 'validation', 'test']

# Create new structure directories if they don't exist
for category in categories:
    new_category_path = os.path.join(new_base, category)
    if not os.path.exists(new_category_path):
        os.makedirs(new_category_path)

# Loop through each folder in the original structure
for folder in os.listdir(original_base):
    original_folder_path = os.path.join(original_base, folder)

    # Skip if it's not a directory
    if not os.path.isdir(original_folder_path):
        continue

    # Process each category within this directory
    for category in categories:
        original_category_path = os.path.join(original_folder_path, category)

        # Continue if the category does not exist in this folder
        if not os.path.exists(original_category_path):
            continue

        # Define new path for the category in the folder
        new_folder_path = os.path.join(new_base, category, folder)

        # Create new directory if it doesn't exist
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # Copy all files from the original to the new structure
        for filename in os.listdir(original_category_path):
            src_file = os.path.join(original_category_path, filename)
            dest_file = os.path.join(new_folder_path, filename)
            if os.path.isfile(src_file):  # Ensure it's a file, not a directory
                shutil.copy(src_file, dest_file)

# Note to user: This script should be run in the directory that contains 'original_structure'
# and 'new_structure' will be created in the same location. Ensure to back up your data
# before running this script as it copies files from one structure to another.
