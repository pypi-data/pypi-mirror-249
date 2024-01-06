# What is pyxlimg

Pyxlimg is for extracting images from xlsx. It has a high affinity with other libraries. This is because you can treat the image as an instance of Pillow.Image.

![PyPI - License](https://img.shields.io/pypi/l/pyxlimg)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/pyxlimg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyxlimg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyxlimg)
![PyPI - Version](https://img.shields.io/pypi/v/pyxlimg)

## Concept

Images are difficult to handle with xlwings, openpyxl, and pylightxl. Especially linter and type annotation are difficult. Complement these. And the goal is to make it easier to do OCR etc. using xlsx in Python.

## Install

Recommended to install using pip.

```sh
pip install pyxlimg
```

## Usage

```py
from PIL import Image
from pyxlimg import xlimg

TestBookName = "./your-test-data/TestBook.xlsx"


if __name__ == "__main__":
    TargetBook: xlimg.ImageBook = xlimg.ImageBook()
    TargetBook.open(TestBookName)
    print("This book named '" + TargetBook.name + "'.")
    print("This book has " + len(TargetBook.Sheets) + " sheets.")
    print("First sheet name is '" + TargetBook.Sheets[0].displayName + "'.")
    print("First sheet has " + len(TargetBook.Sheets[0].Pictures + " pictures.")
    TargetBook.Sheets[1].Pictures[0].Image().show() # Show you the Image
```

In this way, you can easily assign images to variable.

```py
    DisplayImage: Image = TargetBook.Sheets[1].Pictures[0].Image()
    DisplayImage.show() # Show you the Image too.
```

## FAQ

### What image format does this support?

If it is supported by [Pillow](https://pypi.org/project/Pillow/), it can be supported. If the original image is in a commonly used format such as png, jpg, bmp when pasted or inserted into xlsx.

### What kind of library is this supposed to be used with?

For example, `Tesseract OCR`, `pylightxl`, `openpyxl`, `matplotlib`. It is also ideal for matching with other `pillow` related libraries.

## Build

How to build package.

```bash
poetry install
poetry shell
poetry build
```

How to build sphinx docs.

```bash
poetry export --with dev -f requirements.txt > requirements.txt
sphinx-apidoc -f -o ./docs ./pyxlimg
sphinx-build -b html ./docs ./docs/_build
```

In Windows

```pwsh
pyenv install 3.11.0
pyenv local 3.11.0
poetry install
poetry shell
pytest
poetry build
```

Docker

```bash
docker compose up -d --build
docker compose logs -f
```
