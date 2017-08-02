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
        root.protocol("WM_DELETE_WINDOW", root.destroy)

    def get_view(self, **kwargs):
        padding = b'\0'*int(self.offset) * 4
        height = int(math.floor(len(RAW_DATA) / 4 / self.width))
        position = int(self.offset_scrollbar.get()[0] * self.height)
        deletion = (int(position)) * 4 * int(self.width)
        if height > self.winfo_height():
            height = self.winfo_height()
        cropped_data = padding + RAW_DATA[deletion:]
        encoder = 'raw'
        image = Image.frombytes('RGBA', (self.width, height), cropped_data, encoder, self.mode)
        return image, position

    def get_image(self, **kwargs):
        padding = b'\0'*int(self.offset) * 4
        self.height = int(math.floor(len(RAW_DATA) / 4 / self.width))
        encoder = 'raw'
        image = Image.frombytes('RGBA', (self.width, self.height), padding + RAW_DATA, encoder, self.mode)
        return image

    def create_widgets(self):
        # self.y_offset_slider = tk.Scale(self, showvalue=False, from_=1, to=1024)
        # self.y_offset_slider['command'] = self.set_position
        # self.y_offset_slider['length'] = 800
        # self.y_offset_slider['label'] = "Vertical offset"
        # self.y_offset_slider.pack(side='right')

        self.offset_frame = tk.Frame(self)
        self.offset_frame.pack()

        self.left_btn = tk.Button(self.offset_frame)
        self.left_btn['text'] = "Offset -"
        self.left_btn['command'] = self.dec_offset
        self.left_btn.pack(side='left')

        self.offset_slider = tk.Scale(self.offset_frame, length=800, from_=0, to=1024, orient = tk.HORIZONTAL)
        self.offset_slider['command'] = self.set_offset
        self.offset_slider['showvalue'] = 0
        self.offset_slider.bind("<ButtonRelease-1>", self.refresh_image)
        # self.offset_slider['label'] = "Horizontal offset"
        self.offset_slider.pack(side='left')

        self.right_btn = tk.Button(self.offset_frame)
        self.right_btn['text'] = "Offset +"
        self.right_btn['command'] = self.inc_offset
        self.right_btn.pack(side='right')

        self.width_frame = tk.Frame(self)
        self.width_frame.pack()

        self.shrink_btn = tk.Button(self.width_frame)
        self.shrink_btn['text'] = "Width -"
        self.shrink_btn['command'] = self.shrink
        self.shrink_btn.pack(side='left')

        self.width_slider = tk.Scale(self.width_frame, length=800, from_=1, to=1024, orient = tk.HORIZONTAL)
        self.width_slider['command'] = self.set_width
        self.width_slider['showvalue'] = 0
        # self.width_slider['label'] = "Image width"
        self.width_slider.set(self.width)
        self.width_slider.bind("<ButtonRelease-1>", self.refresh_image)
        self.width_slider.pack(side='left')

        self.grow_btn = tk.Button(self.width_frame)
        self.grow_btn['text'] = "Width +"
        self.grow_btn['command'] = self.grow
        self.grow_btn.pack(side='left')

        # self.label = tk.Label(self, image=self.tkimage)
        # self.label.image = self.tkimage
        # self.label.pack(side = 'bottom', fill='both', expand = 'yes')

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='x')

        self.left_ctrl = tk.Frame(self.main_frame)
        self.left_ctrl.pack(side='left', fill='x')

        self.mode_mb = tk.Menubutton(self.left_ctrl)
        self.mode_mb['text'] = 'Mode'
        self.mode_mb['relief'] = tk.RAISED

        self.mode_mb.menu = tk.Menu(self.mode_mb, tearoff = 0)
        self.mode_mb['menu'] = self.mode_mb.menu
        self.mode_mb.menu.add_command(label='RGBA', command= lambda: self.set_mode('RGBA'))
        self.mode_mb.menu.add_command(label='BGRA', command= lambda: self.set_mode('BGRA'))
        self.mode_mb.menu.add_command(label='ARGB', command= lambda: self.set_mode('ARGB'))
        self.mode_mb.menu.add_command(label='ABGR', command= lambda: self.set_mode('ABGR'))
        self.mode_mb.pack(padx=10, side='left', fill='x')

        image = self.get_image()
        self.tkimage = ImageTk.PhotoImage(image)

        self.label = tk.Canvas(self.main_frame, width=600, height=400)
        self.label['background'] = 'black'
        self.label.create_image(0, 0, anchor=tk.NW, image=self.tkimage)

        self.offset_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.offset_scrollbar['command'] = self.label.yview
        self.offset_scrollbar.pack(side='right', fill=tk.Y)

        self.label['yscrollcommand'] = self.offset_scrollbar.set
        self.label['scrollregion'] = (0,0,600,self.tkimage.height())
        self.label.pack( fill='y', expand = 'yes')

        self.refresh_image()

    def set_mode(self, mode, *args):
        self.mode = mode
        self.refresh_image()
        pass

    def refresh_ui(self):
        self.offset_slider['to'] = int(self.width)
        self.label['scrollregion'] = (0,0,600,self.tkimage.height())

    def set_width(self, width):
        self.width = int(width)
        try:
            self.refresh_view()
        except:
            self.refresh_image()

    def set_position(self, position):
        self.position = position
        self.refresh_image()

    def inc_offset(self):
        if int(self.offset) < self.width:
            self.offset = int(self.offset) + 1
            # self.offset_slider.set(self.offset)
            self.update()
            self.refresh_image()

    def dec_offset(self):
        if int(self.offset) > 1:
            self.offset = int(self.offset) - 1
            # self.offset_slider.set(self.offset)
        self.refresh_ui()
        self.refresh_image()

    def set_offset(self, offset):
        self.offset = offset
        # self.refresh_ui()
        self.refresh_view()

    def grow(self):
        self.width += 1
        self.width_slider.set(self.width)
        self.update()
        self.refresh_image()

    def shrink(self):
        self.width -= 1
        self.width_slider.set(self.width)
        self.update()
        self.refresh_image()

    def refresh_view(self):
        # height = self.label.height
        view = self.get_view()
        image = view[0]
        position = view[1]
        # self.preview_tkimage = ImageTk.PhotoImage(image)
        self.tkimage = ImageTk.PhotoImage(image)
        # self.label.create_image(0, position, anchor = tk.NW, image=self.preview_tkimage)
        self.label.create_image(0, position, anchor = tk.NW, image=self.tkimage)
        # self.label.configure(image = self.tkimage)
        # self.update()

    def refresh_image(self, *args):
        image = self.get_image()
        self.tkimage = ImageTk.PhotoImage(image)
        self.label.create_image(0, 0, anchor = tk.NW, image=self.tkimage)
        # self.label.configure(image = self.tkimage)
        # self.update()
        self.refresh_ui()

RAW_DATA = open(sys.argv[1], 'rb').read()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
