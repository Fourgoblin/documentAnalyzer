import pdfplumber
import easyocr
import cv2
import numpy as np
import json
import time
import os
from PIL import Image, ImageDraw
from multiprocessing import Pool, cpu_count
from flask import Flask, request, jsonify, render_template, send_file
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Enable OpenCV optimizations
#cv2.setUseOptimized(True)
#cv2.setNumThreads(5)  # Adjust based on available CPU cores, there is not much difference when unlocking this feature

# Initialize EasyOCR once (before multiprocessing)
reader = easyocr.Reader(['en'])  # Supports multiple languages

def euclidean_distance(color1, color2):
    """Calculate Euclidean distance between two RGB color values."""
    return np.linalg.norm(np.array(color1) - np.array(color2))


def process_page(page_num, pdf_path, pdf_name):
    """Process a single PDF page using EasyOCR (Runs in parallel)."""
    print(f"Processing Page {page_num + 1}...")

    # **Reopen PDF inside the function (fix multiprocessing issue)**
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]

        # Load image for analysis
        image = page.to_image(resolution=150).original  # Reduce resolution for speed
        draw = ImageDraw.Draw(image)

        # Convert image to NumPy array for EasyOCR
        np_image = np.array(image)

        # Extract text using EasyOCR
        text_lines = reader.readtext(np_image, detail=0)  # Returns a list of words
        text = " ".join(text_lines)  # Join words into a full text string

        # Extract word coordinates for bounding boxes
        coordinates = []
        ocr_results = reader.readtext(np_image)  # Returns bounding boxes + text

        for bbox, word, conf in ocr_results:
            if conf < 0.4 or not word:  # Low confidence = possible image/logo
                label = "Image/Logo/Symbol Detected"
            else:
                label = word

            x, y, w, h = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0] - bbox[0][0]), int(bbox[2][1] - bbox[0][1])
            coordinates.append({
                "text": label,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

            # Draw Green Rectangle for Words
            draw.rectangle([(x, y), (x + w, y + h)], outline="green", width=2)

        # Save highlighted image per page
        pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)
        os.makedirs(pdf_output_folder, exist_ok=True)  # Ensure folder exists

        output_image_path = os.path.join(pdf_output_folder, f"output_visualized_page_{page_num + 1}.png")
        image.save(output_image_path)

        # Save extracted text as JSON
        page_data = {"page": page_num + 1, "words": coordinates, "text": text}
        json_output_path = os.path.join(pdf_output_folder, f"text_extraction_page_{page_num + 1}.json")
        with open(json_output_path, "w") as f:
            json.dump(page_data, f, indent=4)

        return page_data

def extract_text_and_convert_to_json(pdf_path):
    """Extract text and images from PDF using multiprocessing and EasyOCR."""
    start_time = time.time()

    pdf_name = os.path.basename(pdf_path).replace(".pdf", "")
    pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)

    # Clear old files for this PDF (Prevents overwriting issues)
    if os.path.exists(pdf_output_folder):
        for file in os.listdir(pdf_output_folder):
            os.remove(os.path.join(pdf_output_folder, file))

    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)

    # Use multiprocessing to process pages in parallel
    with Pool(min(5, cpu_count())) as pool:
        results = pool.starmap(process_page, [(i, pdf_path, pdf_name) for i in range(num_pages)])

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

    return results  # List of JSON results per page

def detect_paragraphs(img, threshold=100):
    """Detect paragraph separations based on whitespace analysis."""
    width, height = img.size
    state_changes = []
    previous_state = None

    for y in range(height):
        first_pixel = img.getpixel((0, y))
        is_whitespace = all(
            euclidean_distance(img.getpixel((x, y)), first_pixel) < threshold
            for x in range(width)
        )
        current_state = "whitespace" if is_whitespace else "non-whitespace"

        if previous_state is None:
            previous_state = current_state

        if previous_state != current_state:
            state_changes.append(y)  # Store Y-coordinate of paragraph separation
        
        previous_state = current_state

    return state_changes

def clean_text(text):
    """Clean extracted text by removing non-ASCII characters and extra spaces."""
    cleaned = re.sub(r'[^\x00-\x7F]+', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF uploads and trigger text extraction."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    pdf_name = os.path.splitext(file.filename)[0]  # Extract filename without extension
    pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)
    os.makedirs(pdf_output_folder, exist_ok=True)  # Ensure directory exists

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    extract_text_and_convert_to_json(filepath)

    return jsonify({"status": "success", "redirect": f"/results/{pdf_name}"})

@app.route('/results/<pdf_name>')
def display_results(pdf_name):
    """Display the number of processed pages in the results page."""
    pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)
    if not os.path.exists(pdf_output_folder):
        return jsonify({"error": "PDF results not found"}), 404

    num_pages = sum(1 for f in os.listdir(pdf_output_folder) if f.endswith(".png"))
    return render_template('results.html', num_pages=num_pages, pdf_name=pdf_name)

@app.route('/json_data/<pdf_name>/<int:page>')
def get_json_data(pdf_name, page):
    """Retrieve JSON data for a specific PDF and page."""
    pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)
    json_output_path = os.path.join(pdf_output_folder, f"text_extraction_page_{page}.json")

    if not os.path.exists(pdf_output_folder):
        return jsonify({"error": "PDF not found"}), 404
    if not os.path.exists(json_output_path):
        return jsonify({"error": "JSON file not found"}), 404

    return send_file(json_output_path, mimetype='application/json')

@app.route('/highlighted_image/<pdf_name>/<int:page>')
def get_highlighted_image(pdf_name, page):
    """Retrieve highlighted image for a specific PDF and page."""
    pdf_output_folder = os.path.join(STATIC_FOLDER, pdf_name)
    image_path = os.path.join(pdf_output_folder, f"output_visualized_page_{page}.png")

    if not os.path.exists(pdf_output_folder):
        return jsonify({"error": "PDF not found"}), 404
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)