import os
import shutil
from tkinter import Tk, Canvas, Button, Frame
from PIL import Image, ImageTk, UnidentifiedImageError

class ImageEditor:
    def __init__(self, master, folder_path):
        self.master = master
        self.folder_path = folder_path
        self.images = [file for file in os.listdir(folder_path) if file.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.current_image = None
        self.crop_rectangle = {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Image Editor")
        self.canvas = Canvas(self.master, cursor="cross")
        self.canvas.pack()

        # Buttons frame
        self.buttons_frame = Frame(self.master)
        self.buttons_frame.pack(side='bottom', pady=10)

        # Control buttons
        Button(self.buttons_frame, text="Supprimer", command=self.delete_image, height=2, width=15).pack(side='left', padx=5)
        Button(self.buttons_frame, text="Garder", command=self.keep_image, height=2, width=15).pack(side='left', padx=5)

        # Crop controls are always visible now
        self.crop_controls_frame = Frame(self.master)
        self.crop_controls_frame.pack(side='bottom', pady=5)

        Button(self.crop_controls_frame, text="Haut", command=lambda: self.adjust_crop('top')).pack(side='top')
        Button(self.crop_controls_frame, text="Bas", command=lambda: self.adjust_crop('bottom')).pack(side='bottom')
        Button(self.crop_controls_frame, text="Gauche", command=lambda: self.adjust_crop('left')).pack(side='left')
        Button(self.crop_controls_frame, text="Droite", command=lambda: self.adjust_crop('right')).pack(side='right')

        self.load_next_image()

        # Bind arrow keys to actions
        self.master.bind("<Left>", lambda event: self.delete_image())
        self.master.bind("<Right>", lambda event: self.keep_image())

    def load_next_image(self):
        while self.images:
            image_file = self.images.pop(0)
            self.current_image_path = os.path.join(self.folder_path, image_file)
            try:
                self.current_image = Image.open(self.current_image_path)
                self.original_image = self.current_image.copy()  # Save original for cropping
                
                # Réinitialiser le crop_rectangle pour correspondre aux dimensions de la nouvelle image
                self.crop_rectangle = {
                    'left': 0,
                    'top': 0,
                    'right': 0,
                    'bottom': 0
                }
                
                self.display_image(self.current_image)
                break  # Image successfully loaded, break the loop
            except (IOError, UnidentifiedImageError) as e:
                print(f"Error opening {self.current_image_path}: {e}")
        else:
            # No more images to display, exit the program
            self.master.quit()

    def display_image(self, image):
        self.canvas.delete("all")  # Clear the canvas

        # Max size for the displayed image
        max_width, max_height = 800, 600  # Change these values as needed

        # Resize image to fit within max dimensions while maintaining aspect ratio
        aspect_ratio = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * aspect_ratio)
        new_height = int(image.height * aspect_ratio)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Update the Tk image and canvas size
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(20, 20, anchor="nw", image=self.tk_image)
        self.canvas.config(width=new_width, height=new_height)


    def delete_image(self):
        self.move_image("Supprimé")
        self.load_next_image()

    def keep_image(self):
        # Check if the image was cropped, then save the cropped part
        if self.crop_rectangle != {'left': 0, 'top': 0, 'right': self.original_image.size[0], 'bottom': self.original_image.size[1]}:
            cropped_image = self.original_image.crop(self.get_crop_coordinates())
            cropped_image.save(self.current_image_path)  # Save over original or create new naming scheme
        self.move_image("Gardé")
        self.load_next_image()

    def adjust_crop(self, direction):
        step = 5  # Change the size for each button press
        if direction == 'top':
            self.crop_rectangle['top'] += step
        elif direction == 'bottom':
            self.crop_rectangle['bottom'] += step
        elif direction == 'left':
            self.crop_rectangle['left'] += step
        elif direction == 'right':
            self.crop_rectangle['right'] += step

        # Show updated crop rectangle
        self.show_crop_rectangle()

    def show_crop_rectangle(self):
        # Clear existing drawing on canvas
        self.canvas.delete("crop_rect")
        # Get current crop coordinates
        x1, y1, x2, y2 = self.get_crop_coordinates()
        # Draw a new rectangle on the canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, tags="crop_rect")

    def get_crop_coordinates(self):
        # Ensure crop coordinates are within the image bounds
        left = max(0, self.crop_rectangle['left'])
        top = max(0, self.crop_rectangle['top'])
        right = min(self.current_image.size[0], self.current_image.size[0] - self.crop_rectangle['right'])
        bottom = min(self.current_image.size[1], self.current_image.size[1] - self.crop_rectangle['bottom'])
        return left, top, right, bottom


    def move_image(self, folder_name):
        dest_folder = os.path.join(self.folder_path, folder_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(self.current_image_path, os.path.join(dest_folder, os.path.basename(self.current_image_path)))

if __name__ == "__main__":
    root = Tk()
    app = ImageEditor(root, 'C:/Users/Eliott/Desktop/Projet-main/Images_HD/Galaxie')  # Replace 'Nébuleuses' with your actual folder path
    root.mainloop()
