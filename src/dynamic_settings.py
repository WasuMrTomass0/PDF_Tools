import os

import file_manager
import settings


class DynamicSettings:

    def __init__(self) -> None:
        self._path = settings.DYNAMIC_SETTINGS_PATH
        self.data = None  # type: dict
        self.read()

    def init_data(self) -> None:
        """Initialise data dict
        """
        self.data = {
            'ESIGN_WINDOW_DEFAULT_DIMENSION': settings.ESIGN_WINDOW_DEFAULT_DIMENSION,
            'LANGUAGE': settings.DEFAULT_LANGUAGE
        }
        self.save()

    def save(self) -> None:
        """Save dictionary to file
        """
        file_manager.save_json(path=self._path, dictionary=self.data)

    def read(self) -> None:
        """Read data from file
        """
        if os.path.isfile(self._path):
            self.data = file_manager.read_json(path=self._path)
        else:
            self.init_data()

    def set_window_dimension(self, dim: "tuple[int, int]") -> None:
        """Setter for window dimensions

        Args:
            dim (tuple[int, int]): dimension tuple (width, height)
        """
        self.data['ESIGN_WINDOW_DEFAULT_DIMENSION'] = dim
        self.save()

    def get_window_dimension(self) -> "tuple[int, int]":
        """Get window dimension

        Returns:
            tuple[int, int]: dimension tuple (width, height)
        """
        return self.data['ESIGN_WINDOW_DEFAULT_DIMENSION']

    def set_language(self, language: str) -> None:
        """Seter for app language

        Args:
            language (str): language json file name
        """
        self.data['LANGUAGE'] = language
        self.save()

    def get_language(self) -> str:
        """Get language json file name

        Returns:
            str: language json file name
        """
        if 'LANGUAGE' not in self.data:
            self.set_language(language=settings.DEFAULT_LANGUAGE)
        return self.data['LANGUAGE']
    
DynamicSettings = DynamicSettings()
