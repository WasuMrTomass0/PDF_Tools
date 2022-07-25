# e-sign

GUI Application that let's you quickly sign pdf files

## Instalation

1. Install `requirements.txt` with pip
2. Windows users must download [poppler (v22.04.0-0
)](https://github.com/oschwartz10612/poppler-windows/releases/) and unzip it it `data/poppler` directory
    ```
    my-app/
    ├─ data/
    │  ├─ poppler/
    │  ├─ invalid_signatures/
    │  ├─ signatures/
    │  ├─ work_dir/
    ├─ src/
    │  ├─ common.py
    │  ├─ gui.py
    │  ├─ pdf.py
    ├─ .gitignore
    ├─ requirements.txt
    ├─ README.md
    ```
3. Add your signatures to `data/signatures` - you can use transparent background!

---

TODO: Reformat signature image loader - now it loads image, resizes it to get fixed ratio dimensions - and then it read original image into pdf
