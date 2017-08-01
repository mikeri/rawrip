#!/usr/bin/python
import sys
import math
import tkinter as tk
from PIL import Image, ImageTk

class Application(tk.Frame, object):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.width = 512
        self['width'] = 1000
        self['height'] = 800
        self.offset = 0
        self.position = 0
        self.pack()
        self.mode = 'BGRA'
        self.create_widgets()

    def get_image(self, **kwargs):
        padding = b'\0'*int(self.offset) * 4
        deletion = (int(self.position) * 4) * int(self.width)
        raw_data = open(sys.argv[1], 'rb').read()
        moved_data = padding + raw_data[deletion:]
        height = int(math.floor(len(raw_data) / 4 / self.width))
        # if height > self.winfo_height():
        #     height = self.winfo_height()
        encoder = 'raw'
        image = Image.frombytes('RGBA', (self.width, height), moved_data, encoder, self.mode)
        return image

    def create_widgets(self):
        self.tkimage = ImageTk.PhotoImage(self.get_image())

        # self.y_offset_slider = tk.Scale(self, showvalue=False, from_=1, to=1024)
        # self.y_offset_slider['command'] = self.set_position
        # self.y_offset_slider['length'] = 800
        # self.y_offset_slider['label'] = "Vertical offset"
        # self.y_offset_slider.pack(side='right')

        self.offset_slider = tk.Scale(self, length=800, from_=0, to=1024, orient = tk.HORIZONTAL)
        self.offset_slider['command'] = self.set_offset
        self.offset_slider['label'] = "Horizontal offset"
        self.offset_slider.pack()

        self.width_slider = tk.Scale(self, length=800, from_=1, to=1024, orient = tk.HORIZONTAL)
        self.width_slider['command'] = self.set_width
        self.width_slider['label'] = "Image width"
        self.width_slider.set(self.width)
        self.width_slider.pack()

        self.btn = tk.Button(self)
        self.btn['text'] = "Width -"
        self.btn['command'] = self.shrink
        self.btn.pack(side='top')

        self.btn = tk.Button(self)
        self.btn['text'] = "Width +"
        self.btn['command'] = self.grow
        self.btn.pack(side='left')

        # self.label = tk.Label(self, image=self.tkimage)
        # self.label.image = self.tkimage
        # self.label.pack(side = 'bottom', fill='both', expand = 'yes')

        self.label = tk.Canvas(self, width = 600, height = 400) 
        self.label['background'] = 'black'
        self.label.create_image(0, 0, anchor = tk.CENTER, image=self.tkimage)

        self.offset_scrollbar = tk.Scrollbar(self, orient = tk.VERTICAL)
        self.offset_scrollbar['command'] = self.label.yview
        self.offset_scrollbar.pack(side='right', fill=tk.Y)

        self.label['yscrollcommand'] = self.offset_scrollbar.set
        self.label['scrollregion'] = (0,0,600,self.tkimage.height())
        self.label.pack(side = 'bottom', fill='y', expand = 'yes')

    def refresh_ui(self):
        self.offset_slider['to'] = int(self.width)
        self.label['scrollregion'] = (0,0,600,self.tkimage.height())

    def set_width(self, width):
        self.width = int(width)
        self.refresh_ui()
        self.refresh_image()

    def set_position(self, position):
        self.position = position
        self.refresh_image()

    def set_offset(self, offset):
        self.offset = offset
        self.refresh_image()

    def grow(self):
        self.width += 1
        self.width_slider.set(self.width)
        self.refresh_image()

    def shrink(self):
        self.width -= 1
        self.width_slider.set(self.width)
        self.refresh_image()

    def refresh_image(self):
        self.tkimage = ImageTk.PhotoImage(self.get_image())
        self.label.create_image(0, 0, anchor = tk.NW, image=self.tkimage)
        # self.label.configure(image = self.tkimage)
        self.update_idletasks()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
