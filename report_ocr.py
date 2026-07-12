import easyocr
import fitz
import os

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader


def extract_text(file_path):

    reader = get_reader()

    text = ""

    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(file_path)

        for i, page in enumerate(pdf):

            page_text = page.get_text()

            if page_text.strip():
                text += page_text + "\n"

            pix = page.get_pixmap(dpi=150)

            image_path = f"temp_{i}.png"

            pix.save(image_path)

            result = reader.readtext(image_path, detail=0)

            text += " ".join(result) + "\n"

            os.remove(image_path)

        pdf.close()

    else:

        result = reader.readtext(file_path, detail=0)

        text = " ".join(result)

    return text