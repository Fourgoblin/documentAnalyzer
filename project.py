import pdfplumber
import pytesseract
import cv2
import numpy as np
import json
import os
from flask import Flask, request, jsonify, render_template
import re


def clean_text(text):
    # Remove non-ASCII characters and extra spaces
    cleaned = re.sub(r'[^\x00-\x7F]+', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Remove isolated punctuation or unwanted characters
    cleaned = re.sub(r'\b\W+\b', ' ', cleaned)
    return cleaned

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text_content = extract_text_with_hybrid_method(filepath)

    # Save extracted text as JSON
    output_path = "document_analysis.json"
    with open(output_path, "w") as f:
        json.dump(text_content, f, indent=4)

    return jsonify(text_content)

def extract_text_with_hybrid_method(pdf_path):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            tables = page.extract_tables()
            
            # Clean the text
            text = clean_text(text) if text else ""
            
            # If pdfplumber fails, fallback to OCR
            coordinates = []
            if not text:
                image = page.to_image(resolution=300).original
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                text = pytesseract.image_to_string(gray, config='--psm 6 --oem 3').strip()
                text = clean_text(text)

                # Get OCR bounding boxes
                data = pytesseract.image_to_data(gray, config='--psm 6 --oem 3', output_type=pytesseract.Output.DICT)
                for i in range(len(data['text'])):
                    if data['text'][i].strip():
                        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        coordinates.append({
                            "text": data['text'][i],
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h
                        })

            # Segment into Header, Body, and Footer
            header, body, footer = [], [], []
            for coord in coordinates:
                if coord["y"] < 200:
                    header.append(coord)
                elif coord["y"] > 1000:
                    footer.append(coord)
                else:
                    body.append(coord)

            result.append({
                "page": page_num + 1,
                "header": header,
                "body": body,
                "footer": footer,
                "text": text,
                "tables": tables
            })

    return result

if __name__ == '__main__':
    app.run(debug=True)
