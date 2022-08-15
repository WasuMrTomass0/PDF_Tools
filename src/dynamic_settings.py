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
            'WINDOW_INIT_DIMENSION': settings.WINDOW_INIT_DIMENSION
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
        self.data['WINDOW_INIT_DIMENSION'] = dim
        self.save()

    def get_window_dimension(self) -> "tuple[int, int]":
        return self.data['WINDOW_INIT_DIMENSION']
    
DynamicSettings = DynamicSettings()
