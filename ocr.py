import easyocr

# Create OCR reader (English)
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    """
    Extract text from medicine image
    """

    result = reader.readtext(image_path)

    text = ""

    for item in result:
        text += item[1] + " "

    return text.strip()

if __name__ == "__main__":

    image = "uploads/test.jpg"

    print(extract_text(image))