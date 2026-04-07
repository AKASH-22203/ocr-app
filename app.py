from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
import json
import os

app = Flask(__name__)

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

def process_image(image):
    image = image.convert("L")
    image = image.resize((image.width * 2, image.height * 2))
    image = image.point(lambda x: 0 if x < 140 else 255)
    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    try:
        if request.method == 'POST':

            if 'file' not in request.files:
                error = "No file uploaded"
                return render_template('index.html', result=result, error=error)

            file = request.files['file']

            if file.filename == '':
                error = "Empty file"
                return render_template('index.html', result=result, error=error)

            image = Image.open(file)

            image = process_image(image)

            # OCR
            text = pytesseract.image_to_string(image)

            if not text.strip():
                error = "No text detected"
                return render_template('index.html', result=result, error=error)

            # Convert to JSON
            data = {}
            for line in text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()

            result = json.dumps(data, indent=4)

            with open("output/result.json", "w") as f:
                json.dump(data, f, indent=4)

    except Exception as e:
        error = str(e)
        print("ERROR:", e)

    return render_template('index.html', result=result, error=error)


@app.route('/download')
def download():
    return send_file("output/result.json", as_attachment=True)


# IMPORTANT FOR RENDER
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
