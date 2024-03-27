import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class ImageSelector:
    def __init__(self, master, image_folder):
        self.master = master
        self.image_folder = image_folder
        self.image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        self.current_image_index = 0
        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self._drag_data = {"x": 0, "y": 0, "width": 0, "height": 0}
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.load_image()

    def load_next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.image_files):
            self.load_image()
        else:
            self.master.quit()

    def load_image(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        file_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
        self.image = Image.open(file_path)
        self.tkimage = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tkimage)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.file_name = self.image_files[self.current_image_index]

    def on_button_press(self, event):
        # Convert mouse event to canvas coordinates
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # Create rectangle if not yet exist, or if previous one was deleted
        if self.rect is None:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x + 1, self.start_y + 1, outline="red")

    def on_move_press(self, event):
        curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # Update the coordinates of the rectangle to match the current mouse position
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
    def on_button_release(self, event):
        self._drag_data["x"] = self.start_x
        self._drag_data["y"] = self.start_y
        self._drag_data["width"] = abs(event.x - self.start_x)
        self._drag_data["height"] = abs(event.y - self.start_y)
        self.save_coords()
        self.load_next_image()

    def save_coords(self):
        coords = f"{self.file_name} - ({self._drag_data['x']},{self._drag_data['y']}) / {self._drag_data['width']} / {self._drag_data['height']}\n"
        with open("selected_area.txt", "a") as file:
            file.write(coords)

if __name__ == "__main__":
    root = tk.Tk()
    folder_selected = filedialog.askdirectory()
    img_selector = ImageSelector(root, folder_selected)
    root.mainloop()