import pytesseract
from PIL import Image
import os
import json
from datetime import datetime

# Setup paths
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Step 1: Load Image
def load_image(image_path):
    try:
        image = Image.open(image_path).convert("L")
        image = image.resize((image.width * 2, image.height * 2))
        image = image.point(lambda x: 0 if x < 140 else 255)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Step 2: Extract Text
def extract_text(image):
    try:
        text = pytesseract.image_to_string(image, lang='eng')
        if not text.strip():
            raise ValueError("No text extracted")
        print("\nRaw OCR Output:\n", text)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

# Step 3: Convert Text → JSON
def convert_to_json(text):
    data = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data

# Step 4: Clean Data
def clean_data(data):
    if "Amount" in data:
        data["Amount"] = data["Amount"].replace("O", "0").replace("o", "0")
    if "Name" in data:
        data["Name"] = data["Name"].strip().title()
    if "Status" in data:
        data["Status"] = data["Status"].strip().capitalize()
    return data

# Step 5: Validate Data
def validate_data(data):
    errors = []

    required_fields = ["Name", "Amount", "Date"]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is missing")

    if "Amount" in data:
        try:
            data["Amount"] = int(data["Amount"])
            if data["Amount"] <= 0:
                errors.append("Amount must be > 0")
        except:
            errors.append("Amount invalid")

    if "Date" in data:
        try:
            datetime.strptime(data["Date"], "%d-%m-%Y")
        except:
            errors.append("Invalid Date format")

    if "Status" in data:
        if data["Status"] not in ["Paid", "Pending"]:
            errors.append("Invalid Status")

    return errors

# Step 6: Output Result
def output_results(data, errors):
    return {
        "data": data,
        "errors": errors,
        "is_valid": len(errors) == 0
    }

# Step 7: Save JSON
def save_results(result, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(result, f, indent=4)
    print(f"\nSaved to {path}")

# MAIN
if __name__ == "__main__":
    image_path = "input/sample_invoice.png"
    output_path = "output/result.json"

    image = load_image(image_path)
    if image:
        text = extract_text(image)
        if text:
            data = convert_to_json(text)
            data = clean_data(data)
            errors = validate_data(data)
            result = output_results(data, errors)
            print("\nFinal Result:", result)
            save_results(result, output_path)