import time
from threading import Thread

from PIL import Image, ImageSequence
from PIL.ImageTk import PhotoImage
from customtkinter import CTkLabel


class MyGif(CTkLabel):
    def __init__(self, master, gif_path):
        super().__init__(master=master, text="")
        self.frames = []
        self.animate = False
        image = Image.open(gif_path)
        for im in ImageSequence.Iterator(image):
            self.frames.append(PhotoImage(im.convert('P')))
        image.close()

    def start_animate(self):
        t = Thread(target=self.animate_gif)
        t.start()

    def animate_gif(self):
        curr = 0
        delay = 0.1
        timer = time.time()
        self.animate = True
        while self.animate:
            if time.time() < timer + delay:
                continue
            curr_frame = self.frames[curr]
            self.configure(image=curr_frame)
            self.update()
            curr = (curr + 1) % len(self.frames)
            timer = time.time()

    def stop_animate(self):
        self.animate = False
        self.configure(image="")
        self.update()
