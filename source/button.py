from tkinter import Button
from PIL import Image, ImageTk, ImageEnhance


class Button(Button):
    def load_image(self, rel_path: str):
        # open file and make brightness effect from it
        image = Image.open(rel_path)
        enhancer = ImageEnhance.Brightness(image)

        # using ImageTk to store it correctly
        self.normal_image = ImageTk.PhotoImage(image)
        self.hover_image = ImageTk.PhotoImage(enhancer.enhance(1.3))
        self.clicked_image = ImageTk.PhotoImage(enhancer.enhance(0.7))

        # adding image reaction to button events
        self.bind("<Leave>", lambda w: self._load_normal_image())
        self.bind("<Enter>", lambda w: self._load_hover_image())
        self.bind("<ButtonRelease-1>", lambda w: self._load_hover_image())
        self.bind("<Button-1>", lambda w: self._load_clicked_image())

        # load current image
        self._load_normal_image()
        

    def _load_normal_image(self):
        print("loading normal_image")
        self["image"] = self.normal_image
        
    def _load_hover_image(self):
        print("loading hover_image")
        self["image"] = self.hover_image
        
    def _load_clicked_image(self):
        print("loading clicked_image")
        self["image"] = self.clicked_image
