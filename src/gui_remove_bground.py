from PIL import Image
from PIL import ImageTk
import tkinter
from tkinter import ttk
from tkinter import Scale
from tkinter import HORIZONTAL

import settings
from language import Language
import images
import common


class RemoveBackgroundGUI:

    def __init__(self, path: str) -> None:
        # Window
        self.window = tkinter.Toplevel()
        self.width, self.height = settings.RMV_BGND_WINDOW_INIT_DIMENSION
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.resizable(False, False)
        self.window.title(f'Remove background')
        
        self.path = path
        self.img_transparent = Image.open(path)  # type: Image.Image
        self.imgtk_preview = None  # type: ImageTk
        self.create_widgets()
        pass

    def create_widgets(self) -> None:
        self.img_preview = ttk.Label(self.window, image=self.imgtk_preview)
        
        self.r_range_from = tkinter.IntVar(value=50)
        self.r_range_to = tkinter.IntVar(value=255)
        self.entry_r_range_from = ttk.Entry(self.window, textvariable=self.r_range_from)
        self.entry_r_range_to   = ttk.Entry(self.window, textvariable=self.r_range_to)
        self.label_r_range = ttk.Label(self.window, text='0 - 255')
        
        self.g_range_from = tkinter.IntVar(value=50)
        self.g_range_to = tkinter.IntVar(value=255)
        self.entry_g_range_from = ttk.Entry(self.window, textvariable=self.g_range_from)
        self.entry_g_range_to   = ttk.Entry(self.window, textvariable=self.g_range_to)
        self.label_g_range = ttk.Label(self.window, text='0 - 255')
        
        self.b_range_from = tkinter.IntVar(value=50)
        self.b_range_to = tkinter.IntVar(value=255)
        self.entry_b_range_from = ttk.Entry(self.window, textvariable=self.b_range_from)
        self.entry_b_range_to   = ttk.Entry(self.window, textvariable=self.b_range_to)
        self.label_b_range = ttk.Label(self.window, text='0 - 255')

        self.button_update = ttk.Button(self.window, text=Language.update)
        self.button_update.bind('<Button-1>', self.handler_button_update)
        self.button_save   = ttk.Button(self.window, text=Language.save)
        self.button_save.bind('<Button-1>', self.handler_button_save)

        self.update_widget_position()
        pass

    def update_widget_position(self) -> None:
        wps = (
            # (widget, pos, size)
            (self.img_preview,  (0.01, 0.01), (0.98, 0.5)),

            (self.entry_r_range_from, (0.2, 0.52), (0.2, 0.05)),
            (self.entry_r_range_to,   (0.6, 0.52), (0.2, 0.05)),
            (self.label_r_range,      (0.45, 0.52), (0.1, 0.05)),
            
            (self.entry_g_range_from, (0.2, 0.58), (0.2, 0.05)),
            (self.entry_g_range_to,   (0.6, 0.58), (0.2, 0.05)),
            (self.label_g_range,      (0.45, 0.58), (0.1, 0.05)),
            
            (self.entry_b_range_from, (0.2, 0.64), (0.2, 0.05)),
            (self.entry_b_range_to,   (0.6, 0.64), (0.2, 0.05)),
            (self.label_b_range,      (0.45, 0.64), (0.1, 0.05)),

            (self.button_update,      (0.20, 0.7), (0.2, 0.05)),
            (self.button_save,        (0.60, 0.7), (0.2, 0.05)),

        )
        for widget, pos, size in wps:
            pos_x, pos_y = pos
            size_x, size_y = size

            if pos_x:
                pos_x = int(pos_x * self.width)
                widget.place(x=pos_x)
            if pos_y:
                pos_y = int(pos_y * self.height)
                widget.place(y=pos_y)
            if size_x:
                size_x = int(size_x * self.width)
                widget.place(width=size_x)
            if size_y:
                size_y = int(size_y * self.height)
                widget.place(height=size_y)

        self.window.update()
        #
        self.update_image_preview()
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_image_preview(self) -> None:
        img = images.resize_image_fixed_scale(
            img=self.img_transparent,
            new_width=self.img_preview.winfo_width(),
            new_height=self.img_preview.winfo_height()
        )
        self.imgtk_preview = ImageTk.PhotoImage(img)
        if self.imgtk_preview:
            self.img_preview.configure(image=self.imgtk_preview)
        else:
            print('self.imgtk_preview -> False')
        pass

    def update_image(self) -> None:
        r = self.r_range_from.get(), self.r_range_to.get()
        g = self.g_range_from.get(), self.g_range_to.get()
        b = self.b_range_from.get(), self.b_range_to.get()

        self.img_transparent = images.remove_background(
            img=self.img_transparent,
            r_range=r,
            g_range=g,
            b_range=b
        )
        self.update_image_preview()
        pass

    def save_image(self) -> None:
        self.img_transparent.save(self.path)
        self.window.destroy()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def handler_button_update(self, event = None) -> None:
        self.update_image()
        pass

    def handler_button_save(self, event = None) -> None:
        self.save_image()
        pass

    pass


# path = r'C:\Projekty\eSign\data\signatures\test_podpis.png'

# app = RemoveBackgroundGUI(path)
# app.window.mainloop()
