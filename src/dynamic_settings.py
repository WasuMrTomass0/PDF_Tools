import os

import settings
import common


class DynamicSettings:

    def __init__(self) -> None:
        self._path = settings.DYNAMIC_SETTINGS_PATH
        self.data = None  # type: dict
        self.read()

    def init_data(self) -> None:
        self.data = {
            'ESIGN_WINDOW_DEFAULT_DIMENSION': settings.ESIGN_WINDOW_DEFAULT_DIMENSION,
            'LANGUAGE': settings.DEFAULT_LANGUAGE
        }
        self.save()

    def save(self) -> None:
        common.save_json(path=self._path, dictionary=self.data)

    def read(self) -> None:
        if os.path.isfile(self._path):
            self.data = common.read_json(path=self._path)
        else:
            self.init_data()

    def set_window_dimension(self, dim: "tuple[int, int]") -> None:
        self.data['ESIGN_WINDOW_DEFAULT_DIMENSION'] = dim
        self.save()

    def get_window_dimension(self) -> "tuple[int, int]":
        return self.data['ESIGN_WINDOW_DEFAULT_DIMENSION']

    def set_language(self, language: str) -> None:
        self.data['LANGUAGE'] = language
        self.save()

    def get_language(self) -> str:
        if 'LANGUAGE' not in self.data:
            self.set_language(language=settings.DEFAULT_LANGUAGE)
        return self.data['LANGUAGE']
    
DynamicSettings = DynamicSettings()
