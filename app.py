from flask import Flask, render_template, request, send_file
import json
import os
import requests

app = Flask(__name__)

os.makedirs("output", exist_ok=True)

# 🔥 OCR using API (no Tesseract needed)
def extract_text_api(file):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': 'helloworld',  # free key
        'language': 'eng'
    }

    files = {
        'file': file
    }

    response = requests.post(url, files=files, data=payload)
    result = response.json()

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return "OCR Failed"


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

            # 🔥 OCR using API
            text = extract_text_api(file)

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


# Required for Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
