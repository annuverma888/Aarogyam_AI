import easyocr
import fitz  # PyMuPDF
from PIL import Image

# Load OCR model only once
reader = easyocr.Reader(['en'])


def extract_text(file_path):

    text = ""

    # ---------- PDF ----------
    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(file_path)

        for page in pdf:

            # Extract normal text
            page_text = page.get_text()

            if page_text.strip():
                text += page_text + "\n"

            # If scanned PDF, perform OCR on image
            pix = page.get_pixmap(dpi=300)

            image_path = "temp_page.png"

            pix.save(image_path)

            result = reader.readtext(image_path, detail=0)

            text += " ".join(result)

        pdf.close()

    # ---------- Image ----------
    else:

        result = reader.readtext(file_path, detail=0)

        text = " ".join(result)

    return text