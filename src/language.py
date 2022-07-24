import json
import os
import settings


class Language:

    def __init__(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            self.lang_dict = json.loads(f.read())

        self.prev_page = self.lang_dict['prev_page']
        self.next_page = self.lang_dict['next_page']
        self.no_pages = self.lang_dict['no_pages']
        self.sign_document = self.lang_dict['sign_document']
        
        self.clear_page = self.lang_dict['clear_page']
        self.overwrite = self.lang_dict['overwrite']
        self.fixed_scale = self.lang_dict['fixed_scale']
        self.add_signature = self.lang_dict['add_signature']
        self.delete_signature = self.lang_dict['delete_signature']
        self.error = self.lang_dict['error']
        self.error_opening_pdf_file = self.lang_dict['error_opening_pdf_file']
        self.path = self.lang_dict['path']
        self.page = self.lang_dict['page']
        self.info = self.lang_dict['info']
        self.select_pdf = self.lang_dict['select_pdf']
        self.add_signatures_to_document = self.lang_dict['add_signatures_to_document']
        self.add_signatures_to = self.lang_dict['add_signatures_to']
        self.signature_file_is_invalid = self.lang_dict['signature_file_is_invalid']



    pass

lang = Language(os.path.join(settings.LANGUAGES_DIR, settings.LANG_POLISH))
