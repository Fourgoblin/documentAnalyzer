import time
import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import pytesseract
import threading
import queue

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Performance Monitoring
start_time = time.time()


# Euclidean distance between two RGB values
def euclidean_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


# This function scans the image and identifies data-containing rows/columns
def detect_state_changes(img, mode, horizontal_data_chunks=None):
    width, height = img.size
    euclidian_threshold = 100
    state_changes = []
    previous_state = None

    # For horizontal analysis, scan document row by row
    if mode == "horizontal":
        for y in range(height):
            # Check if all pixels in the row are within the same range of RGB values and set state accordingly
            if all(euclidean_distance(img.getpixel((x, y)), img.getpixel((0, y))) < euclidian_threshold for x in
                   range(width)):
                current_state = "whitespace"
            else:
                current_state = "non-whitespace"
            # Detect and save all state changes for future analysis
            if previous_state is None:
                previous_state = current_state
            if previous_state is not None and previous_state != current_state:
                state_changes.append((y, previous_state, current_state))
            previous_state = current_state
    # For vertical analysis, scan chunks of data column by column
    # (Limits the scope of the vertical scan to the horizontal data chunks only, not the entire image)
    elif mode == "vertical":
        for i in range(len(horizontal_data_chunks)):
            y1, y2 = horizontal_data_chunks[i]
            previous_state = None
            for x in range(width):
                # Check if all pixels in the col are within the same range of RGB values and set state accordingly
                if all(euclidean_distance(img.getpixel((x, y)), img.getpixel((0, y))) < euclidian_threshold for y in
                       range(y1, y2)):
                    current_state = "whitespace"
                else:
                    current_state = "non-whitespace"
                # Detect and save all state changes for future analysis
                if previous_state is None:
                    previous_state = current_state
                if previous_state is not None and previous_state != current_state:
                    state_changes.append((x, y1, y2, previous_state, current_state))
                previous_state = current_state

    return state_changes


# Go through the state changes to determine the relevant chunks of data
def state_change_analysis(state_changes, mode):
    chunk_of_data = []
    x1 = y1 = x2 = y2 = None

    if mode == "horizontal":
        for i in range(len(state_changes)):
            pos, prev_state, current_state = state_changes[i]
            # Start of data chunk
            if i == 0 and prev_state == "non-whitespace":
                y1 = 0
            if prev_state == "whitespace" and current_state == "non-whitespace":
                y1 = pos
            # End of data chunk
            elif prev_state == "non-whitespace" and current_state == "whitespace":
                y2 = pos
            # Store chunk of data if both start and end are found
            if y1 is not None and y2 is not None:
                data_height = y2 - y1
                if data_height > 0:  # Ignore single lines (likely a crease in the paper)
                    chunk_of_data.append([y1, y2])
                y1 = None
                y2 = None
    elif mode == "vertical":
        for i in range(len(state_changes)):
            x, y1, y2, prev_state, current_state = state_changes[i]
            # Start of data chunk
            if i == 0 and prev_state == "non-whitespace":
                x1 = 0
            if prev_state == "whitespace" and current_state == "non-whitespace":
                x1 = x
            # End of data chunk
            elif prev_state == "non-whitespace" and current_state == "whitespace":
                x2 = x
            # Store chunk of data if both start and end are found
            if x1 is not None and x2 is not None:
                data_width = x2 - x1
                if data_width > 0:  # Ignore single lines (likely a crease in the paper)
                    chunk_of_data.append([x1, y1, x2, y2])
                x1 = None
                x2 = None

    return chunk_of_data


# Go through all the chunks of data and determine if the gap between them is within a certain threshold (horizontal analysis)
def horizontal_threshold_analysis(chunk_of_data, img, input_threshold):
    draw = ImageDraw.Draw(img)
    data_chunks = []
    threshold = input_threshold
    y_start = 0
    y_end = 0

    for i in range(1, len(chunk_of_data)):
        prev_data_start, prev_data_end = chunk_of_data[i - 1]
        curr_data_start, curr_data_end = chunk_of_data[i]
        if i == 1:
            y_start = prev_data_start

        # Determine if data chunks are close enough to each other based on threshold
        gap = curr_data_start - prev_data_end
        if gap <= threshold:
            continue
        else:
            y_end = prev_data_end
            data_chunks.append((y_start, y_end))
            y_start = curr_data_start
        if i == len(chunk_of_data) - 1:
            y_end = curr_data_end
            data_chunks.append((y_start, y_end))
    # Must account for the last one
    y_end = curr_data_end
    data_chunks.append((y_start, y_end))

    return img, data_chunks


def vertical_threshold_analysis(vertical_chunk_of_data, img, input_threshold):
    draw = ImageDraw.Draw(img)
    threshold = input_threshold

    horizontal_row_complete = False
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    zone_start = True

    # Store vertical section data
    vertical_sections = []
    x1 = y1 = x2 = y2 = None
    current_section = None

    for i in range(1, len(vertical_chunk_of_data)):
        prev_x1, prev_y1, prev_x2, prev_y2 = vertical_chunk_of_data[i - 1]
        curr_x1, curr_y1, curr_x2, curr_y2 = vertical_chunk_of_data[i]

        if (i == 1):  # First data point is always the start of a zone
            zone_start = True

        if (prev_y1 != curr_y1):  # or i == len(vertical_chunk_of_data) - 1)
            horizontal_row_complete = True
        else:
            horizontal_row_complete = False

        gap = curr_x1 - prev_x2

        if zone_start:
            #draw.line((prev_x1, prev_y1, prev_x1, prev_y2), fill=red)
            x1, y1, x2, y2 = prev_x1, prev_y1, prev_x2, prev_y2
            current_section = {
                'top_left_x': x1,
                'top_left_y': y1,
                # 'width': not quite ready to determine width yet
                'height': y2 - y1
            }
            zone_start = False
        # Last data in the set it always the end of a zone
        # BUG: Prematurely draws lines (claimacknowledgement) w/ 45/210 thresholds if it's the last data chunk AND the prev. horizontal row is comp
        if i == len(vertical_chunk_of_data) - 1 and not horizontal_row_complete:
            # draw.line((curr_x2, curr_y1, curr_x2, curr_y2), fill=black)
            # draw.line((x1, y1, curr_x2, y1), fill=black)
            # draw.line((x1, y2, curr_x2, y2), fill=black)
            current_section['width'] = curr_x2 - x1
            vertical_sections.append(current_section)
        elif horizontal_row_complete:
            # draw.line((prev_x2, prev_y1, prev_x2, prev_y2), fill=red)
            # draw.line((x1, y1, prev_x2, y1), fill=red)
            # draw.line((x1, y2, prev_x2, y2), fill=red)
            current_section['width'] = prev_x2 - x1
            vertical_sections.append(current_section)
            zone_start = True
        # Large gap also marks the completion of a zone
        elif gap > threshold:
            # draw.line((prev_x2, prev_y1, prev_x2, prev_y2), fill=red)
            # draw.line((x1, y1, prev_x2, y1), fill=red)
            # draw.line((x1, y2, prev_x2, y2), fill=red)
            current_section['width'] = prev_x2 - x1
            vertical_sections.append(current_section)
            zone_start = True

        # Special case scenario: Only one chunk of data and it's the last one
        if horizontal_row_complete and i == len(vertical_chunk_of_data) - 1:
            # # Draw a line at the start of the current data chunk
            # draw.line((curr_x1, curr_y1, curr_x1, curr_y2), fill=red)
            # # Draw a line at the end of the current data chunk
            # draw.line((curr_x2, curr_y1, curr_x2, curr_y2), fill=red)
            # # Draw horizontal lines between them
            # draw.line((curr_x1, curr_y1, curr_x2, curr_y1), fill=red)
            # draw.line((curr_x1, curr_y2, curr_x2, curr_y2), fill=red)
            # Store coordinates
            current_section = {
                'top_left_x': curr_x1,
                'top_left_y': curr_y1,
                'width': curr_x2 - curr_x1,
                'height': curr_y2 - curr_y1
            }
            vertical_sections.append(current_section)

    return img, vertical_sections

def detect_barcode(cv_image, result_queue):
    pil_section = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    barcode = decode(pil_section)
    if barcode:
        result_queue.put(("barcode: " + barcode[0].type, barcode[0].data.decode('utf-8')))
    
def detect_text(cv_image, result_queue):
    text = pytesseract.image_to_string(cv_image)
    text = text if text else pytesseract.image_to_string(cv_image, config='--psm 10')
    if len(text.strip()) > 3:
        result_queue.put(("text", text))


# Determine the content type and actual content in each section
def detect_content(img, section):
    x = section['top_left_x']
    y = section['top_left_y']
    width = section['width']
    height = section['height']
    # Crop the section from the image
    section_img = img.crop((x, y, x + width, y + height))
    # Convert section to openCV format
    cv_image = cv2.cvtColor(np.array(section_img), cv2.COLOR_RGB2BGR)

    # For multi-threading - queues are safe to use between threads
    result_queue = queue.Queue()

    # Check for barcodes
    t1 = threading.Thread(target=detect_barcode, args=(cv_image,result_queue))
    # Check for text with OCR    
    t2 = threading.Thread(target=detect_text, args=(cv_image,result_queue))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    data = None

    while not result_queue.empty():
        result, data = result_queue.get()
        if "text" in result:
            return result, data
        elif "barcode" in result:
            return result, data

    # If section does not contain a barcode or text assume it is an image
    return "image", "undetermined"


# Scan the image and produce a visual output of non-whitespace areas
def image_scanner(image_path, output_json, output_image, horizontal_threshold, vertical_threshold,
                  content_detection_toggle):
    img = Image.open(image_path).convert("RGB")
    original_img = Image.open(image_path).convert("RGB")
    horizontal_chunks = []
    vertical_chunks = []

    # Determine the state changes in the horizontal direction
    state_changes = detect_state_changes(img, "horizontal")
    # Go through the state changes to determine the relevant chunks of data
    chunk_of_data = state_change_analysis(state_changes, "horizontal")
    # Document Analysis using Threshold
    img, horizontal_chunks = horizontal_threshold_analysis(chunk_of_data, img, horizontal_threshold)

    # Determine the state changes in the vertical direction
    vertical_state_changes = detect_state_changes(original_img, "vertical", horizontal_chunks)
    # Go through the state changes to determine the relevant chunks of data
    vertical_chunk_of_data = state_change_analysis(vertical_state_changes, "vertical")
    # Document Analysis using Threshold
    img, vertical_chunks = vertical_threshold_analysis(vertical_chunk_of_data, img, vertical_threshold)

    # Export the image with the lines drawn
    #img.save(output_image)

    # Add detected content data to each section
    if content_detection_toggle == 1:
        for section in vertical_chunks:
            content_type, content = detect_content(original_img, section)
            section['content_type'] = content_type
            section['content'] = content

    # Output JSON data
    output_data = {
        "document_sections": [
            {
                "section_id": f"section_{i + 1}",
                **section
            } for i, section in enumerate(vertical_chunks)
        ]
    }

    # Export the data to JSON file
    with open(output_json, "w") as json_file:
        json.dump(output_data, json_file, indent=2)

    # Print the number of sections detected
    print(f"Detected {len(vertical_chunks)} document sections")


def initialize_scanner(input_file_path, output_file_path, horizontal_threshold, vertical_threshold,
                       content_detection_toggle):
    # Ensure output directory exists, if not create it
    os.makedirs(output_file_path, exist_ok=True)

    # Get the document name
    document_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Get the file extension
    ext = os.path.splitext(input_file_path)[1].lower()

    # If the file is a pdf, convert it to images and analyze each image
    if ext == ".pdf":
        try:
            images = convert_from_path(input_file_path, dpi=150)
            print(f"Converted {len(images)} page(s) from PDF.")

            for i, img in enumerate(images):
                new_image_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}.png")
                json_output_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}_analyzed.json")
                analyzed_image_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}_analyzed.png")
                img.save(new_image_path, "PNG")
                # Perform analysis on each page
                image_scanner(new_image_path, json_output_path, analyzed_image_path, horizontal_threshold,
                              vertical_threshold, content_detection_toggle)
        except Exception as e:
            print(f"Error converting PDF: {e}")
    # If the file is already an image, proceed with analysis
    elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        json_output_path = os.path.join(output_file_path, f"{document_name}_analyzed.json")
        analyzed_image_path = os.path.join(output_file_path, f"{document_name}_analyzed.png")
        image_scanner(input_file_path, json_output_path, analyzed_image_path, horizontal_threshold, vertical_threshold,
                      content_detection_toggle)
    else:
        print(f"Skipping: Unsupported file type → {input_file_path}")


initialize_scanner(

    r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\ReleaseAndAuthorizationOfPayment-2.jpg",
    #r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\claimacknowledgement.jpg",
    #r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\CleanDocumentAnalysisBase.pdf", 
    #"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\CleanDocumentAnalysisBase_page_4.png",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\Test Results",
    10,  # Horizontal threshold
    50,  # Vertical threshold - 70 worked well
    0  # Turn content detection on or off
)

# Performance Monitoring
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
