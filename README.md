# 📄 OCR Document Processing System

## 🚀 Overview

This project is an OCR-based document processing system that extracts structured data from images (such as invoices) and converts it into JSON format.

It also includes a web interface where users can upload images, view extracted data, copy it, and download it.

---

## 🧠 What is OCR?

OCR (Optical Character Recognition) is a technology used to convert different types of documents (images, scanned papers) into machine-readable text.

---

## ⚙️ OCR Techniques Used

### 1. Image Preprocessing

Before extracting text, we improve image quality:

- Convert to Grayscale → Reduces noise
- Resize Image → Improves text clarity
- Thresholding → Converts image to black & white

```python
image.convert("L")
image.resize()
image.point(lambda x: 0 if x < 140 else 255)
```


### 2. Text Extraction

- Using Tesseract OCR:

```python
pytesseract.image_to_string(image)
```

### 3. Data Structuring

We convert raw OCR text into structured JSON:
Example:

Name: Akash
Amount: 500

Converted to:
```
{
"Name": "Akash",
"Amount": "500"
}
```

### 4. Output

Display JSON in UI
Copy to clipboard
Download as .json file

### 🌐 Features
```
Upload image
Extract text using OCR
Convert to structured JSON
View JSON in UI
Copy JSON
Download JSON file
```

### 🛠️ Tech Stack
```Python
Flask
pytesseract
PIL (Pillow)
```

###▶️ How to Run

1. Install dependencies
  ```Python
   pip install -r requirements.txt
  ```
2. Install Tesseract OCR
Download:
https://github.com/tesseract-ocr/tesseract

Set path in code:
  ```Python
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
```
3. Run the application
```Python
python app.py
```
4. Open in browser
http://127.0.0.1:5000

### 📌 Future Improvements
```Support multiple file uploads
Add PDF OCR support
Improve accuracy using OpenCV
Add AI-based field detection
```

### 💼 Use Cases
```Invoice processing
Document digitization
Data extraction automation
```

### 👨‍💻 Author
Akash 
---