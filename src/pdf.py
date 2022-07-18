import PyPDF2


class PDF:

    def __init__(self) -> None:
        self.path = ''
        self.file_handler = None
        self.pdf_file_handler = None
        pass

    def get_number_of_pages(self) -> int:
        if self.pdf_file_handler:
            return self.pdf_file_handler.getNumPages()

    def open(self, path: str) -> None:
        if self.file_handler:
            self.file_handler.close()

        self.path = path
        self.file_handler = open(self.path, 'rb')
        self.pdf_file_handler = PyPDF2.PdfFileReader(self.file_handler)

        pass

    pass
