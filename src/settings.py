import os

SRC_DIR = os.path.normpath(os.path.dirname(__file__))

DATA_DIR = os.path.normpath(os.path.join(SRC_DIR, '..', 'data'))

POPPLER_DIR = os.path.normpath(os.path.join(DATA_DIR, 'poppler'))
SIGNATURES_DIR = os.path.normpath(os.path.join(DATA_DIR, 'signatures'))
INVALID_SIGNATURES_DIR = os.path.normpath(os.path.join(DATA_DIR, 'invalid_signatures'))
TEMP_DIR = os.path.normpath(os.path.join(DATA_DIR, 'temp'))
LANGUAGES_DIR = os.path.normpath(os.path.join(DATA_DIR, 'languages'))

POPPLER_BIN_PATH = os.path.normpath(os.path.join(POPPLER_DIR, 'Library', 'bin'))

# Language json file names
LANG_POLISH = 'polish.json'
# LANG_ENGLISH = 'english.json'
