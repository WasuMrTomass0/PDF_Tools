import PyPDF2
import pdf2image


POPLER_BIN_PATH = 'poppler-22.04.0/Library/bin'


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
        return self.pdf_file_handler.getPage(page_num)

    def get_page_as_image(self, page_num: int):
        if not 0 < page_num <= self.get_number_of_pages():
            raise ValueError(f'Page number ({page_num}) out of range (1 - {self.get_number_of_pages()})')
        
        pages = pdf2image.convert_from_path(
            pdf_path=self.path, 
            first_page=page_num,
            last_page=page_num,
            poppler_path=POPLER_BIN_PATH
        )

        # pages = pdf2image.convert_from_bytes(
        #     pdf_file=self.get_page(page_num).,
        #     poppler_path=POPLER_BIN_PATH
        # )

        if len(pages) != 1:
            raise ValueError(f'Invalid number of image pages from pdf! Got {len(pages)} pages')

        return pages[0]

    pass
