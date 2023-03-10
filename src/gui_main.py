from datetime import datetime
from genericpath import isfile
import shutil
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import PIL
from PIL import Image
from PIL import ImageTk
from pdf import PDF
import glob
import os
from urllib.parse import unquote

import settings
import common
import images
import popup_windows
from language import Language
from logger import log_exceptions
from dynamic_settings import DynamicSettings
from gui_remove_bground import RemoveBackgroundGUI


class ESignGUI:

    def __init__(self) -> None:
        # Data
        self.pdf_file_path = ''  # type: str
        self.pdf_page_number = None  # type: int
        self.pdf_number_of_pages = None  # type: int

        self.pdf = PDF()

        self.signature_files = []  # type: list
        self.signature_image = None  # type: ImageTk.PhotoImage
        self.pdf_image = None  # type: ImageTk.PhotoImage
        self.pdf_signatures_data = None  # type: list[list[tuple[str, bool, float, float, float, float]]]
        self.rect_press_cord = None  # type: tuple[float, float]
        self.overwrite_status = None  # type: tkinter.BooleanVar
        self.signature_fixed_scale = None  # type: tkinter.BooleanVar
        self.state = tkinter.NORMAL

        # Layout
        self.WIDTH_INIT, self.INIT_HEIGHT = settings.ESIGN_WINDOW_DEFAULT_DIMENSION
        self.width, self.height = DynamicSettings.get_window_dimension()
        self.WIDTH_MIN, self.HEIGHT_MIN = settings.ESIGN_WINDOW_MINIMUM_DIMENSION

        # Window
        self.window = tkinter.Tk()
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.minsize(width=self.WIDTH_MIN, height=self.HEIGHT_MIN)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.window.resizable(False, False)
        self.window.title(f'eSign')
        self.window.bind(f'<Configure>', self.resize_window)

        try:
            common.init_check()
        except Exception as error:
            popup_windows.error_popup(
                title=Language.error,
                msg=f'{Language.error}:\n{str(error)}'
            )

        self.create_widgets()
        self.load_signature_files()
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def create_widgets(self) -> None:
        # PDF File selection
        self.pdf_selection_entry = ttk.Entry(self.window)
        self.pdf_selection_entry.bind('<Return>', self.handler_pdf_selection_entry)
        self.pdf_selection_button = ttk.Button(self.window, text=Language.select_pdf)
        self.pdf_selection_button.bind('<Button-1>', self.handler_select_pdf_file)

        # Signature selection
        self.signature_selection = ttk.Combobox(self.window)
        self.signature_selection.bind('<<ComboboxSelected>>', self.handler_update_signature_preview)
        # Signature preview image
        self.signature_preview = ttk.Label(self.window, image=self.signature_image)

        # PDF page preview
        self.pdf_first_page_button = ttk.Button(self.window, text='<<')
        self.pdf_prev_page_button = ttk.Button(self.window, text=Language.prev_page)
        self.pdf_page_number_label = ttk.Label(self.window, text=Language.no_pages, anchor='center')
        self.pdf_next_page_button = ttk.Button(self.window, text=Language.next_page)
        self.pdf_last_page_button = ttk.Button(self.window, text='>>')
        #
        self.pdf_first_page_button.bind('<Button-1>', self.handler_pdf_first_page_button)
        self.pdf_prev_page_button.bind('<Button-1>', self.handler_pdf_prev_page_button)
        self.pdf_next_page_button.bind('<Button-1>', self.handler_pdf_next_page_button)
        self.pdf_last_page_button.bind('<Button-1>', self.handler_pdf_last_page_button)
        #
        self.pdf_preview = ttk.Label(self.window, image=self.pdf_image, anchor='center')
        self.pdf_preview.bind('<ButtonPress-1>', self.handler_pdf_preview_clicked)
        self.pdf_preview.bind('<ButtonRelease-1>', self.handler_pdf_preview_clicked)

        # Control
        self.sign_pdf_button = ttk.Button(self.window, text=Language.sign_document)
        self.sign_pdf_button.bind('<Button-1>', self.handler_sign_pdf)
        #
        self.clear_page_button = ttk.Button(self.window, text=Language.clear_page)
        self.clear_page_button.bind('<Button-1>', self.handler_clear_page)
        #
        self.overwrite_status = tkinter.BooleanVar()
        self.overwrite_checkbox = ttk.Checkbutton(self.window, text=Language.overwrite, var=self.overwrite_status)
        self.overwrite_status.set(True)
        #
        self.signature_fixed_scale = tkinter.BooleanVar()
        self.signature_fixed_scale_checkbox = ttk.Checkbutton(self.window, text=Language.fixed_scale, var=self.signature_fixed_scale)
        self.signature_fixed_scale.set(True)

        #
        self.add_signature_button = ttk.Button(self.window, text=Language.add_signature)
        self.add_signature_button.bind('<Button-1>', self.handler_add_signature)
        self.del_signature_button = ttk.Button(self.window, text=Language.delete_signature)
        self.del_signature_button.bind('<Button-1>', self.handler_del_signature)
        self.edit_signature_button = ttk.Button(self.window, text=Language.edit_signature)
        self.edit_signature_button.bind('<Button-1>', self.handler_edit_signature)

        self.update_widget_position()
        self.window.update()
        pass

    def resize_window(self, event = None) -> None:
        w = self.window.winfo_width()
        h = self.window.winfo_height()

        # Init resize. On start w, h = (1, 1)
        if w == 1 and h == 1:
            w, h = self.width, self.height
            init_resize = True
        else:
            init_resize = False

        if init_resize or (w != self.width or h != self.height):
            # Scale
            w, h = images.get_new_dimensions_fixed_scale(
                old_dim=(self.WIDTH_INIT, self.INIT_HEIGHT),
                new_dim=(w, h)
            )
            # Saturate
            if w < self.WIDTH_MIN or h < self.HEIGHT_MIN:
                w, h = self.WIDTH_MIN, self.HEIGHT_MIN
            # Save new dimensions and update window size
            self.width, self.height = w, h
            DynamicSettings.set_window_dimension(dim=(self.width, self.height))
            self.window.geometry(f'{self.width}x{self.height}')
            #
            self.update_widget_position()

    def update_widget_position(self) -> None:

        wps = (
            # (widget, pos, size)
            (self.pdf_selection_entry,  (0.01, 0.01), (0.75, 0.05)),
            (self.pdf_selection_button, (0.77, 0.01), (0.22, 0.05)),
            #
            (self.signature_selection,   (0.77, 0.07), (0.22, 0.05)),
            (self.signature_preview,     (0.77, 0.13), (0.22, 0.1)),
            (self.add_signature_button,  (0.77, 0.24), (0.22, 0.05)),
            (self.del_signature_button,  (0.77, 0.30), (0.22, 0.05)),
            (self.edit_signature_button, (0.77, 0.36), (0.22, 0.05)),
            #
            (self.pdf_first_page_button, (0.01, 0.07), (0.05, 0.05)),
            (self.pdf_prev_page_button,  (0.06, 0.07), (0.20, 0.05)),
            (self.pdf_page_number_label, (0.27, 0.07), (0.23, 0.05)),
            (self.pdf_next_page_button,  (0.51, 0.07), (0.20, 0.05)),
            (self.pdf_last_page_button,  (0.71, 0.07), (0.05, 0.05)),
            #
            (self.pdf_preview, (0.01, 0.13), (0.76, 0.86)),
            #
            (self.signature_fixed_scale_checkbox, (0.77, 0.72), (0.22, 0.05)),
            (self.overwrite_checkbox, (0.77, 0.76), (0.22, 0.05)),
            (self.clear_page_button, (0.77, 0.82), (0.22, 0.05)),
            (self.sign_pdf_button, (0.77, 0.88), (0.22, 0.11)),

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

        # Changed with size update
        self.window.update()
        self.update_signature_preview()
        self.update_pdf_page_preview()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def select_signature_file(self) -> None:
        selected_path = filedialog.askopenfilename()
        if selected_path:
            images.save_as_png(
                src_path=selected_path,
                dst_dir=settings.SIGNATURES_DIR
            )
            self.load_signature_files()
        pass

    def delete_signature_file(self) -> None:
        selected = self.signature_selection.get()
        if selected:
            confirmation = messagebox.askokcancel(
                title=Language.info,
                message=f'{Language.sure_to_delete} {selected}?'
            )
            if confirmation:
                os.remove(os.path.join(settings.SIGNATURES_DIR, selected))
                self.load_signature_files()
        pass

    def edit_signature_file(self) -> None:
        selected = self.signature_selection.get()
        if selected:
            path = os.path.join(settings.SIGNATURES_DIR, selected)
            if os.path.isfile(path):
                app = RemoveBackgroundGUI(
                    path=path
                )
                self.window.wait_window(window=app.window)
                self.update_signature_preview()
        pass

    def select_pdf_file(self, pdf_file: str = None) -> None:
        # Select file
        self.pdf_file_path = filedialog.askopenfilename() if not pdf_file else pdf_file
        self.update_pdf_file()

    def pdf_file_from_entry(self) -> None:
        entry = unquote(self.pdf_selection_entry.get())
        entry = entry.replace('file:///', '')  # Edge
        if entry != self.pdf_file_path:
            self.pdf_file_path = entry
            self.update_pdf_file()

    def update_pdf_file(self) -> None:
        # Only if path was selected
        if self.pdf_file_path:
            # Clear entry
            self.pdf_selection_entry.delete(0, tkinter.END)
            # Close opened file
            self.pdf.close()
            # Reset values
            self.pdf_number_of_pages = None
            self.pdf_page_number = None
            self.pdf_signatures_data = None
            # Update pdf file
            try:
                # Open pdf file
                self.pdf.open(self.pdf_file_path)
                # Update pages
                self.pdf_number_of_pages = self.pdf.get_number_of_pages()
                self.pdf_page_number = 1
                self.clear_all_signatures()
            except Exception as error:
                popup_windows.error_popup(
                    title=Language.error,
                    msg=f'{Language.error_opening_pdf_file}:\n{Language.path}: {self.pdf_file_path}\n{error}'
                )
            else:
                # Update entry
                self.pdf_selection_entry.insert(0, self.pdf_file_path)

            # Update pdf preview and number
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    def load_signature_files(self) -> None:
        # List files
        self.signature_files = os.listdir(path=settings.SIGNATURES_DIR)
        # Update widget
        self.signature_selection['values'] = self.signature_files
        if len(self.signature_files) > 0:
            self.signature_selection.current(0)
        else:
            self.signature_selection.set('')
        self.update_signature_preview()

    def update_signature_preview(self) -> None:
        # Update image preview
        img_path = os.path.join(settings.SIGNATURES_DIR, self.signature_selection.get())
        if img_path and os.path.isfile(img_path):
            # Read and resize image
            try:
                img = Image.open(img_path)
            except PIL.UnidentifiedImageError:
                # Move invalid file
                shutil.move(
                    img_path,
                    os.path.join(settings.INVALID_SIGNATURES_DIR, self.signature_selection.get())
                )
                return self.load_signature_files()
            else:
                # Load correct image file
                img = images.resize_image_fixed_scale(
                    img=img,
                    new_width=self.signature_preview.winfo_width(),
                    new_height=self.signature_preview.winfo_height()
                )
                # Load to widget
                self.signature_image = ImageTk.PhotoImage(img)
                self.signature_preview.configure(image=self.signature_image)
        else:
            self.signature_image = None
            self.signature_preview.configure(image=self.signature_image)

    def update_pdf_page_number(self) -> None:
        if self.pdf_page_number and self.pdf_page_number > 0 and self.pdf_number_of_pages > 0:
            self.pdf_page_number_label.configure(text=f'{Language.page} {self.pdf_page_number} / {self.pdf_number_of_pages}')
        else:
            self.pdf_page_number_label.configure(text=Language.no_pages)
        pass

    def update_pdf_page_preview(self, img = None) -> None:
        # Open and resize image
        if self.pdf:
            if img is None:
                img = self.pdf.get_page_as_image(self.pdf_page_number)
            img = images.resize_image_fixed_scale(
                img=img,
                new_width=self.pdf_preview.winfo_width(),
                new_height=self.pdf_preview.winfo_height()
            )
            # Add signatures
            if self.pdf_page_number:
                for signature_data in self.pdf_signatures_data[self.pdf_page_number-1]:
                    _, _, x, y, _, _ = signature_data
                    # Load signature and resize it
                    signature_img = images.load_signature_image(
                        signature_data=signature_data,
                        width=self.pdf_preview.winfo_width(),
                        height=self.pdf_preview.winfo_height()
                    )
                    # Merge signature image and page image
                    img = images.merge_images(
                        bg_img=img,
                        fg_img=signature_img,
                        pos=(x, y)
                    )
            # Load to widget
            self.pdf_image = ImageTk.PhotoImage(img)
            self.pdf_preview.configure(image=self.pdf_image)
        else:
            self.pdf_image = None
            self.pdf_preview.configure(image=self.pdf_image)
        pass

    def clear_all_signatures(self) -> None:
        self.pdf_signatures_data = [list() for _ in range(self.pdf_number_of_pages)]

    def sign_pdf(self) -> None:
        if not self.pdf:
            messagebox.showinfo(Language.info, Language.select_pdf)
            return

        if not any(self.pdf_signatures_data):
            messagebox.showinfo(Language.info, Language.add_signatures_to_document)
            return

        # Disable handlers
        self.state = tkinter.DISABLED
        self.sign_pdf_button['state'] = tkinter.DISABLED

        # Sign pdf file - read (new) path to signed pdf
        path = self.pdf.sign(pdf_signatures_data=self.pdf_signatures_data, overwrite=self.overwrite_status.get())

        # Reload file and clear existing signatures
        self.clear_all_signatures()
        self.select_pdf_file(path)

        # Enable handlers
        self.state = tkinter.NORMAL
        self.sign_pdf_button['state'] = tkinter.NORMAL
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @log_exceptions
    def on_closing(self):
        # Remove temp/ content
        files = glob.glob(os.path.join(settings.TEMP_DIR, '*'))
        for f in files:
            os.remove(f)

        # Close window
        self.window.destroy()
        pass

    @log_exceptions
    def handler_pdf_next_page_button(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        # Increment page number
        if self.pdf_page_number and self.pdf_page_number < self.pdf_number_of_pages:
            self.pdf_page_number += 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    @log_exceptions
    def handler_pdf_prev_page_button(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        # Decrement page number
        if self.pdf_page_number and self.pdf_page_number > 1:
            self.pdf_page_number -= 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    @log_exceptions
    def handler_pdf_first_page_button(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        # Go to first page
        if self.pdf_page_number and self.pdf_page_number > 1:
            self.pdf_page_number = 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    @log_exceptions
    def handler_pdf_last_page_button(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        # Go to last page
        if self.pdf_page_number and self.pdf_page_number < self.pdf_number_of_pages:
            self.pdf_page_number = self.pdf_number_of_pages
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    @log_exceptions
    def handler_update_signature_preview(self, event = None) -> None:
        self.update_signature_preview()

    @log_exceptions
    def handler_select_pdf_file(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.select_pdf_file()

    @log_exceptions
    def handler_pdf_selection_entry(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.pdf_file_from_entry()

    @log_exceptions
    def handler_sign_pdf(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.sign_pdf()

    @log_exceptions
    def handler_clear_page(self, event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.pdf_signatures_data[self.pdf_page_number-1].clear()
        # Update page preview
        self.update_pdf_page_preview()

    @log_exceptions
    def handler_pdf_preview_clicked(self, event: tkinter.Event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        if self.pdf:
            if not self.signature_files and event.type == tkinter.EventType.ButtonPress:
                messagebox.showinfo(Language.error, f'{Language.add_signatures_to} "{settings.SIGNATURES_DIR}"')
                return

            if event.type == tkinter.EventType.ButtonPress:
                # Read first point of rectangle
                self.rect_press_cord = event.x, event.y
            elif event.type == tkinter.EventType.ButtonRelease and self.rect_press_cord is not None:
                # Read second point of rectangle and calculate its dimensions
                rectangle = images.rectangle_from_two_points(
                    p1=(event.x, event.y),
                    p2=self.rect_press_cord,
                    width=self.pdf_preview.winfo_width(),
                    height=self.pdf_preview.winfo_height()
                )
                signature_img_path = os.path.join(settings.SIGNATURES_DIR, self.signature_selection.get())

                if not signature_img_path or not os.path.isfile(signature_img_path):
                    messagebox.showinfo(Language.error, Language.signature_file_is_invalid)
                    return

                self.pdf_signatures_data[self.pdf_page_number-1].append(
                    (signature_img_path, self.signature_fixed_scale.get(), *rectangle)
                )
                # Reset first pooint
                self.rect_press_cord = None
                # Update page preview
                self.update_pdf_page_preview()
        pass

    @log_exceptions
    def handler_add_signature(self, event: tkinter.Event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.select_signature_file()
        pass

    @log_exceptions
    def handler_del_signature(self, event: tkinter.Event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.delete_signature_file()
        pass

    @log_exceptions
    def handler_edit_signature(self, event: tkinter.Event = None) -> None:
        if self.state == tkinter.DISABLED:
            return
        self.edit_signature_file()
        pass

    pass
