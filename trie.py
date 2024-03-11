import os
import shutil
from tkinter import Tk, Canvas, Button, Frame, Label
from PIL import Image, ImageTk, UnidentifiedImageError

class ImageEditor:
    def __init__(self, master, folder_path):
        self.master = master
        self.folder_path = folder_path
        self.images = [file for file in os.listdir(folder_path) if file.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.current_image = None
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Image Editor")
        self.canvas = Canvas(self.master, cursor="cross")
        self.canvas.pack()

        self.status_frame = Frame(self.master)
        self.status_frame.pack(side='top', pady=5)
        self.images_left_label = Label(self.status_frame, text=f"Images restantes: {len(self.images)}")
        self.images_left_label.pack()

        self.buttons_frame = Frame(self.master)
        self.buttons_frame.pack(side='bottom', pady=10)

        Button(self.buttons_frame, text="Supprimer", command=self.delete_image, height=2, width=15).pack(side='left', padx=5)
        Button(self.buttons_frame, text="Garder", command=self.keep_image, height=2, width=15).pack(side='left', padx=5)

        self.master.bind('<Left>', lambda event: self.delete_image())
        self.master.bind('<Right>', lambda event: self.keep_image())

        self.load_next_image()

    def load_next_image(self):
        if self.images:
            image_file = self.images.pop(0)
            self.current_image_path = os.path.join(self.folder_path, image_file)
            try:
                self.current_image = Image.open(self.current_image_path)
                self.display_image(self.current_image)
                self.images_left_label.config(text=f"Images restantes: {len(self.images)}")
            except (IOError, UnidentifiedImageError) as e:
                print(f"Error opening {self.current_image_path}: {e}")
                self.load_next_image()  
        else:
            self.master.quit()

    def display_image(self, image):
        self.canvas.delete("all")  

        max_width, max_height = 800, 600

        aspect_ratio = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * aspect_ratio)
        new_height = int(image.height * aspect_ratio)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(20, 20, anchor="nw", image=self.tk_image)
        self.canvas.config(width=new_width, height=new_height)

    def delete_image(self):
        self.move_image("Supprimé")
        self.load_next_image()

    def keep_image(self):
        self.move_image("Gardé")
        self.load_next_image()

    def move_image(self, folder_name):
        dest_folder = os.path.join(self.folder_path, folder_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(self.current_image_path, os.path.join(dest_folder, os.path.basename(self.current_image_path)))

if __name__ == "__main__":
    root = Tk()
    app = ImageEditor(root, 'Lunes')  #
    root.mainloop()

