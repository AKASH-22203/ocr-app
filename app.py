from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
import json
import os

app = Flask(__name__)

# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def process_image(image):
    image = image.convert("L")
    image = image.resize((image.width * 2, image.height * 2))
    image = image.point(lambda x: 0 if x < 140 else 255)
    return image

def extract_text(image):
    return pytesseract.image_to_string(image)

def convert_to_json(text):
    data = {}
    for line in text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        file = request.files['file']
        image = Image.open(file)

        image = process_image(image)
        text = extract_text(image)
        data = convert_to_json(text)

        result = json.dumps(data, indent=4)

        os.makedirs("output", exist_ok=True)
        with open("output/result.json", "w") as f:
            json.dump(data, f, indent=4)

    return render_template('index.html', result=result)

@app.route('/download')
def download():
    return send_file("output/result.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)