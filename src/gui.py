import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import Image
from PIL import ImageTk
from pdf import PDF
import common

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
class ESignGUI:

    def __init__(self) -> None:
        # Data
        self.pdf_file_path = ''  # type: str
        self.pdf_page_number = -1  # type: int
        self.pdf_number_of_pages = -1  # type: int

        self.pdf = PDF()

        self.work_dir = 'C:/Projekty/eSign/data/work_dir'  # type: str
        self.signature_dir = 'C:/Projekty/eSign/data/signatures'  # type: str
        self.signature_files = []  # type: list
        self.signature_image = None  # type: ImageTk.PhotoImage
        self.pdf_image = None  # type: ImageTk.PhotoImage

        # Layout
        self.width, self.height = 600, 600
        self.width_min, self.height_min = 400, 300
        self.padx, self.pady = 10, 10

        # Window
        self.window = tkinter.Tk()
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.minsize(width=self.width_min, height=self.height_min)
        self.window.resizable(False, False)
        self.window.title(f'Signign PDF file')
        self.window.bind('<Return>', self.update_widget_position)

        self.create_widgets()
        self.load_signature_files()
        pass


    def create_widgets(self) -> None:
        # PDF File selection
        self.pdf_selection_entry = ttk.Entry(self.window)
        self.pdf_selection_button = ttk.Button(self.window, text='Select PDF')
        self.pdf_selection_button.bind('<Button-1>', self.handler_select_pdf_file)

        # Signature selection
        self.signature_selection = ttk.Combobox(self.window)
        self.signature_selection.bind('<<ComboboxSelected>>', self.handler_update_signature_preview)
        # Signature preview image
        self.signature_preview = ttk.Label(self.window, image=self.signature_image)

        # PDF page preview
        self.pdf_first_page_button = ttk.Button(self.window, text='<<')
        self.pdf_prev_page_button = ttk.Button(self.window, text='Previous page')
        self.pdf_page_number_label = ttk.Label(self.window, text='No pages', anchor='center')
        self.pdf_next_page_button = ttk.Button(self.window, text='Next page')
        self.pdf_last_page_button = ttk.Button(self.window, text='>>')
        #
        self.pdf_first_page_button.bind('<Button-1>', self.handler_pdf_first_page_button)
        self.pdf_prev_page_button.bind('<Button-1>', self.handler_pdf_prev_page_button)
        self.pdf_next_page_button.bind('<Button-1>', self.handler_pdf_next_page_button)
        self.pdf_last_page_button.bind('<Button-1>', self.handler_pdf_last_page_button)
        #
        self.pdf_preview = ttk.Label(self.window, image=self.pdf_image)

        self.update_widget_position()
        self.window.update()
        pass

    def update_widget_position(self) -> None:
        wps = (
            # (widget, pos, size)
            (self.pdf_selection_entry,  (0.01, 0.01), (0.75, 0.05)),
            (self.pdf_selection_button, (0.77, 0.01), (0.22, 0.05)),
            #
            (self.signature_selection, (0.77, 0.07), (0.22, 0.05)),
            (self.signature_preview,   (0.77, 0.13), (0.22, 0.1)),
            # 
            (self.pdf_first_page_button, (0.01, 0.07), (0.05, 0.05)),
            (self.pdf_prev_page_button,  (0.06, 0.07), (0.20, 0.05)),
            (self.pdf_page_number_label, (0.27, 0.07), (0.23, 0.05)),
            (self.pdf_next_page_button,  (0.51, 0.07), (0.20, 0.05)),
            (self.pdf_last_page_button,  (0.71, 0.07), (0.05, 0.05)),
            # 
            (self.pdf_preview, (0.01, 0.13), (0.76, 0.86)),
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
        self.update_signature_preview()
            
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def select_pdf_file(self) -> None:
        # Select file
        self.pdf_file_path = filedialog.askopenfilename()
        # Only if path was selected
        if self.pdf_file_path:
            # Clear entry
            self.pdf_selection_entry.delete(0, tkinter.END)
            # Update pdf file
            try:
                # Open pdf file
                self.pdf.open(self.pdf_file_path)
                # Update pages
                self.pdf_number_of_pages = self.pdf.get_number_of_pages()
                self.pdf_page_number = 1
                # Update pdf preview and number
                self.update_pdf_page_preview()
                self.update_pdf_page_number()
            except Exception as error:
                messagebox.showinfo("Error", f'Error while opening pdf file:\n{error}\nPath: {self.pdf_file_path}')
            else:    
                # Update entry
                self.pdf_selection_entry.insert(0, self.pdf_file_path)

    def load_signature_files(self) -> None:
        # List files
        self.signature_files = os.listdir(path=self.signature_dir)
        # Update wodget
        self.signature_selection['values'] = self.signature_files
        if len(self.signature_files) > 0:
            self.signature_selection.current(0)
            self.update_signature_preview()
        pass

    def update_signature_preview(self) -> None:
        # Update image preview
        img_path = os.path.join(self.signature_dir, self.signature_selection.get())
        if img_path and os.path.isfile(img_path):
            # Read and resize image
            img = Image.open(img_path)
            img = common.resize_image_fixed_scale(
                img=img, 
                new_width=self.signature_preview.winfo_width(), 
                new_height=self.signature_preview.winfo_height()
            )
            # Load to widget
            self.signature_image = ImageTk.PhotoImage(img)
            self.signature_preview.configure(image=self.signature_image)

    def update_pdf_page_number(self) -> None:
        if self.pdf_page_number > 0 and self.pdf_number_of_pages > 0:
            self.pdf_page_number_label.configure(text=f'Page {self.pdf_page_number} / {self.pdf_number_of_pages}')
        else:
            self.pdf_page_number_label.configure(text=f'No pages')
        pass

    def update_pdf_page_preview(self) -> None:
        # Open and resize image
        img = Image.open(r'data\work_dir\empty.png')
        img = common.resize_image_fixed_scale(
            img=img, 
            new_width=self.pdf_preview.winfo_width(), 
            new_height=self.pdf_preview.winfo_height()
        )
        # Load to widget
        self.pdf_image = ImageTk.PhotoImage(img)
        self.pdf_preview.configure(image=self.pdf_image)
        # TODO: Implement me!
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def handler_pdf_next_page_button(self, event = None) -> None:
        # Increment page number
        if self.pdf_page_number < self.pdf_number_of_pages:
            self.pdf_page_number += 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    def handler_pdf_prev_page_button(self, event = None) -> None:
        # Decrement page number
        if self.pdf_page_number > 1:
            self.pdf_page_number -= 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    def handler_pdf_first_page_button(self, event = None) -> None:
        # Go to first page
        if self.pdf_page_number > 1:
            self.pdf_page_number = 1
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    def handler_pdf_last_page_button(self, event = None) -> None:
        # Go to last page
        if self.pdf_page_number < self.pdf_number_of_pages:
            self.pdf_page_number = self.pdf_number_of_pages
            self.update_pdf_page_preview()
            self.update_pdf_page_number()

    def handler_update_signature_preview(self, event = None) -> None:
        self.update_signature_preview()

    def handler_select_pdf_file(self, event = None) -> None:
        self.select_pdf_file()

    pass

app = ESignGUI()

app.window.mainloop()