import json
import os
import settings


class Language:

    def __init__(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            self.lang_dict = json.loads(f.read())

        self.prev_page = self.lang_dict['prev_page']  # type: str
        self.next_page = self.lang_dict['next_page']  # type: str
        self.no_pages = self.lang_dict['no_pages']  # type: str
        self.sign_document = self.lang_dict['sign_document']  # type: str
        self.clear_page = self.lang_dict['clear_page']  # type: str
        self.overwrite = self.lang_dict['overwrite']  # type: str
        self.fixed_scale = self.lang_dict['fixed_scale']  # type: str
        self.add_signature = self.lang_dict['add_signature']  # type: str
        self.delete_signature = self.lang_dict['delete_signature']  # type: str
        self.error = self.lang_dict['error']  # type: str
        self.error_opening_pdf_file = self.lang_dict['error_opening_pdf_file']  # type: str
        self.path = self.lang_dict['path']  # type: str
        self.page = self.lang_dict['page']  # type: str
        self.info = self.lang_dict['info']  # type: str
        self.select_pdf = self.lang_dict['select_pdf']  # type: str
        self.add_signatures_to_document = self.lang_dict['add_signatures_to_document']  # type: str
        self.add_signatures_to = self.lang_dict['add_signatures_to']  # type: str
        self.signature_file_is_invalid = self.lang_dict['signature_file_is_invalid']  # type: str
        self.sure_to_delete = self.lang_dict['sure_to_delete']  # type: str
        self.update = self.lang_dict['update']  # type: str
        self.save = self.lang_dict['save']  # type: str
        self.edit_signature = self.lang_dict['edit_signature']  # type: str
        
    pass

lang = Language(os.path.join(settings.LANGUAGES_DIR, settings.LANG_POLISH))
