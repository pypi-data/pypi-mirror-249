from typing import List

from PIL import Image, ImageTk
import tkinter as tk

class FramesPlayer(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, frames: List[Image.Image], fps: int = 16):
        self.loc = 0
        self.frames = []

        for f in frames:
            self.frames.append(ImageTk.PhotoImage(f.copy()))
        
        self.delay = 1000 // fps

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def play_frames(frames: List[Image.Image], fps: int = 16):
    root = tk.Tk()
    lbl = FramesPlayer(root)
    lbl.pack()
    lbl.load(frames, fps)
    root.mainloop()


def export_gif(frames: List[Image.Image], file_path: str, fps: int = 16):
    frames[0].save(
        file_path,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / fps),
        loop=0,
        compress_level=4,
    )
