from flask import Flask, render_template, request, send_file
import os
import easyocr
from PIL import Image

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = "uploads"
TEXT_FOLDER = "extracted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

# EasyOCR Reader
reader = easyocr.Reader(['en'])

@app.route("/", methods=["GET", "POST"])
def index():

    extracted_text = ""

    if request.method == "POST":

        file = request.files["image"]

        if file:

            # Save uploaded image
            image_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(image_path)

            # Open image
            img = Image.open(image_path)

            result = reader.readtext(image_path, detail=0)
            print("OCR RESULT:", result)

            if result:
                extracted_text = " ".join(result)
            else:
                extracted_text = "No text found in image"

            # Save text file
            text_path = os.path.join(
                TEXT_FOLDER,
                file.filename + ".txt"
            )

            with open(text_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)

            return render_template(
                "index.html",
                text=extracted_text,
                download_file=file.filename + ".txt"
            )

    return render_template(
        "index.html",
        text=extracted_text
    )

@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(TEXT_FOLDER, filename)

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
