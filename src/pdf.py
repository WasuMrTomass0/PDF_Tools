from genericpath import isfile
from tkinter import Image
import PyPDF2
import pdf2image
import common
import shutil
import os
from reportlab.pdfgen import canvas

import settings
import images
from logger import logger


class PDF:

    def __init__(self) -> None:
        self.path = ''
        self.file_handler = None
        self.pdf_file_handler = None
        pass

    def __bool__(self) -> bool:
        return self.pdf_file_handler is not None

    def get_number_of_pages(self) -> int:
        if self.pdf_file_handler:
            return self.pdf_file_handler.getNumPages()
        else:
            raise Exception(f'PDF file is not opened!')

    def open(self, path: str) -> None:
        # Close file before opening new one
        self.close()
        # Update data, open file and load pdf
        self.path = path
        self.file_handler = open(self.path, 'rb')
        self.pdf_file_handler = PyPDF2.PdfFileReader(self.file_handler)
        pass

    def close(self) -> None:
        # If file is opened close it
        if self.file_handler:
            self.file_handler.close()
            self.file_handler = None
            self.pdf_file_handler = None

    def get_page(self, page_num: int):
        if not 0 < page_num <= self.get_number_of_pages():
            raise ValueError(f'Page number ({page_num}) out of range (1 - {self.get_number_of_pages()})')
        page_index = page_num - 1
        return self.pdf_file_handler.getPage(page_index)

    def get_page_as_image(self, page_num: int):
        if not 0 < page_num <= self.get_number_of_pages():
            raise ValueError(f'Page number ({page_num}) out of range (1 - {self.get_number_of_pages()})')
        
        pages = pdf2image.convert_from_path(
            pdf_path=self.path, 
            first_page=page_num,
            last_page=page_num,
            poppler_path=settings.POPPLER_BIN_PATH
        )

        if len(pages) != 1:
            raise ValueError(f'Invalid number of image pages from pdf! Got {len(pages)} pages')

        return pages[0]

    def sign(self, pdf_signatures_data: "list[list]", overwrite: bool) -> str:
        # Writer for new pdf document
        out_pdf = PyPDF2.PdfFileWriter()

        files_to_close = []  # type: list[tuple]

        # Iterate through pages
        for pdf_page_number in range(1, self.get_number_of_pages()+1):
            pdf_page = self.get_page(pdf_page_number)
            page_signatures_data = pdf_signatures_data[pdf_page_number-1]

            # Temp pdf file - ONE page with signatures
            pdf_signed_page_fname = common.get_tmp_filename(prefix='signed_page_', suffix='.pdf')
            c = canvas.Canvas(pdf_signed_page_fname, pagesize=pdf_page.cropBox)

            # Iterate though signatures
            for single_signature_data in page_signatures_data:
                if single_signature_data:
                    # Load signature and resize it
                    signature_img = images.load_signature_image(
                        signature_data=single_signature_data,
                        width=float(pdf_page.cropBox.getWidth()),
                        height=float(pdf_page.cropBox.getHeight())
                    )
                    # Draw it onto canvas
                    _, _, x, y, _, _ = single_signature_data
                    # Convert to int
                    x = int(x * float(pdf_page.cropBox.getWidth()))
                    w = signature_img.width
                    y = int((1.0 - y) * float(pdf_page.cropBox.getHeight())) - signature_img.height
                    h = signature_img.height
                    c.drawImage(single_signature_data[0], x, y, w, h, mask='auto')

            c.showPage()
            c.save()

            # Merge PDF in to original page
            pdf_signed_page_fh = open(pdf_signed_page_fname, 'rb')
            pdf_signed_pages = PyPDF2.PdfFileReader(pdf_signed_page_fh)
            pdf_signed_page = pdf_signed_pages.getPage(0)
            pdf_signed_page.mediaBox = pdf_page.mediaBox
            pdf_page.mergePage(pdf_signed_page)

            # Add page to output
            out_pdf.addPage(pdf_page)
            # Append fh and fname to close and remove file
            files_to_close.append((pdf_signed_page_fh, pdf_signed_page_fname))

        # Save new PDF file
        out_fname = common.get_tmp_filename(prefix='signed_pdf_document_', suffix='.pdf')
        with open(out_fname, 'wb') as out_fh:
            out_pdf.write(out_fh)
            del out_pdf

        # Close files
        for fh, _ in files_to_close:
            fh.close()
            
        # Overwrite origin or create copy
        dst_path = common.add_suffix_to_path(path=self.path, suffix='_signed')
        dst_path = common.get_unused_path(path=dst_path)
        shutil.copyfile(out_fname, dst_path)

        # Delete files
        os.remove(out_fname)
        for _, fname in files_to_close:
            os.remove(fname)

        # Return name of new PDF file
        return dst_path

    pass
