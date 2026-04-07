from flask import Flask, render_template, request, send_file
import json
import os
import requests

app = Flask(__name__)

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# 🔥 OCR using API
def extract_text_api(file):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': 'helloworld',
        'language': 'eng'
    }

    # 🔥 FIX: read file properly
    files = {
        'file': (file.filename, file.read())
    }

    response = requests.post(url, files=files, data=payload)
    result = response.json()

    print("OCR API RESPONSE:", result)  # DEBUG

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return ""

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

            # 🔥 Extract text
            file.seek(0)
            text = extract_text_api(file)
            print("OCR TEXT:\n", text)  # Debug

            if not text.strip():
                error = "No text detected"
                return render_template('index.html', result=result, error=error)

            # 🔥 Process lines
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            data = {}

            # ✅ Case 1: Key: Value parsing
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()

            # ✅ Case 2: Smart detection (fallback)
            if not data:
                for line in lines:
                    if any(char.isdigit() for char in line):
                        data["Amount"] = line
                    elif "paid" in line.lower():
                        data["Status"] = "Paid"
                    elif "pending" in line.lower():
                        data["Status"] = "Pending"
                    elif len(line.split()) <= 3:
                        data["Name"] = line

            # ✅ Final fallback
            if not data:
                data["raw_text"] = lines

            result = json.dumps(data, indent=4)

            # Save JSON
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
