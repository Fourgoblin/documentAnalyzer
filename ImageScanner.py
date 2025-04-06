import csv
import time
import json
import os
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

# Perfmance Monitoring
start_time = time.time()

# Euclidean distance between two RGB values
def euclidean_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

# Function to detect horizontal state changes
def detect_state_changes(img, mode):
    width, height = img.size
    euclidian_threshold = 100

    state_changes = []
    previous_state = None
    # Horizontal mode
    if mode == "horizontal":
        for y in range(height):
            # Determine the state
            if all(euclidean_distance(img.getpixel((x, y)), img.getpixel((0, y))) < euclidian_threshold for x in
                   range(width)):
                current_state = "whitespace"
            else:
                current_state = "non-whitespace"
            # Record the state
            if previous_state is None:
                previous_state = current_state
            if previous_state is not None and previous_state != current_state:
                state_changes.append((y, previous_state, current_state))
            previous_state = current_state
    return state_changes


# Function to detect vertical state changes
def detect_vertical_state_changes(img, data_chunks):
    width, _ = img.size
    previous_state = None
    state_changes = []
    euclidian_threshold = 100

    for i in range(len(data_chunks)):
        y1, y2 = data_chunks[i]  # Unpack (start, end) directly
        previous_state = None
        for x in range(width):
            # Check if all pixels in the column (x) are similar within this chunk
            if all(euclidean_distance(img.getpixel((x, y)), img.getpixel((0, y))) < euclidian_threshold for y in
                   range(y1, y2)):
                current_state = "whitespace"
            else:
                current_state = "non-whitespace"
            # Track state changes
            if previous_state is None:
                previous_state = current_state
            if previous_state is not None and previous_state != current_state:
                state_changes.append((x, y1, y2, previous_state, current_state))
            previous_state = current_state

    return state_changes


# Go through the state changes to determine the relevant chunks of data (horizontal)
def state_change_analysis(state_changes):
    chunk_of_data = []
    y1 = None
    y2 = None

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
            if data_height > 3:  # Ignore single lines (likely a crease in the paper)
                chunk_of_data.append([y1, y2])
            y1 = None
            y2 = None

    return chunk_of_data


# Go through the state changes to determine the relevant chunks of data (vertical)
def vertical_state_change_analysis(state_changes):
    chunk_of_data = []
    x1 = None
    x2 = None

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
            if data_width > 3:  # Ignore single lines (likely a crease in the paper)
                chunk_of_data.append([x1, y1, x2, y2])
            x1 = None
            x2 = None

    return chunk_of_data


# Go through all the chunks of data and determine if the gap between them is within a certain threshold (horizontal analysis)
def threshold_analysis(chunk_of_data, img, mode):
    width, height = img.size
    draw = ImageDraw.Draw(img)
    data_chunks = []
    horizontal_chunks = []
    vertical_chunks = []
    threshold = 25
    y_start = 0
    y_end = 0

    if mode == "horizontal":
        pos = width
        data_chunks = horizontal_chunks
    elif mode == "vertical":
        pos = height
        data_chunks = vertical_chunks

    for i in range(1, len(chunk_of_data)):
        prev_data_start, prev_data_end = chunk_of_data[i - 1]
        curr_data_start, curr_data_end = chunk_of_data[i]
        if i == 1:  # Draw a line at the start of the first data chunk in the document
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


def vertical_threshold_analysis(vertical_chunk_of_data, horizontal_chunk_of_data, img, mode):
    width, height = img.size
    draw = ImageDraw.Draw(img)
    threshold = 70 #30 worked well for the test cases

    horizontal_row_complete = False
    purple = (255, 0, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    cyan = (0, 255, 255)
    black = (0, 0, 0)
    zone_start = True

    # Store vertical section data
    vertical_sections = []

    x1, y1, x2, y2 = None, None, None, None
    current_section = None

    for i in range(1, len(vertical_chunk_of_data)):
        prev_x1, prev_y1, prev_x2, prev_y2 = vertical_chunk_of_data[i - 1]
        curr_x1, curr_y1, curr_x2, curr_y2 = vertical_chunk_of_data[i]

        if (i == 1):  # First data point is always the start of a zone
            zone_start = True

        if (prev_y1 != curr_y1):
            # print("Horizontal Row Complete")
            horizontal_row_complete = True
        else:
            horizontal_row_complete = False

        gap = curr_x1 - prev_x2

        if zone_start:
            draw.line((prev_x1, prev_y1, prev_x1, prev_y2), fill=black)
            x1, y1, x2, y2 = prev_x1, prev_y1, prev_x2, prev_y2
            current_section = {
                'top_left_x': prev_x1,
                'top_left_y': prev_y1,
                #'width': not quite ready to determine width yet
                'height': prev_y2 - prev_y1
            }
            #vertical_sections.append(current_section)
            zone_start = False
        # Last data in the set it always the end of a zone
        if i == len(vertical_chunk_of_data) - 1:
            # print("Reached the end ")
            draw.line((curr_x2, curr_y1, curr_x2, curr_y2), fill=green)
            draw.line((x1, y1, curr_x2, y1), fill=purple)
            draw.line((x1, y2, curr_x2, y2), fill=purple)
            current_section['width'] = curr_x2 - x1
            vertical_sections.append(current_section)
        # The end of a row always marks the completion of a zone
        elif horizontal_row_complete:
            draw.line((prev_x2, prev_y1, prev_x2, prev_y2), fill=blue)
            draw.line((x1, y1, prev_x2, y1), fill=purple)
            draw.line((x1, y2, prev_x2, y2), fill=purple)
            current_section['width'] = prev_x2 - x1
            vertical_sections.append(current_section)
            zone_start = True
        # Large gap also marks the completion of a zone
        elif gap > threshold:
            draw.line((prev_x2, prev_y1, prev_x2, prev_y2), fill=red)
            draw.line((x1, y1, prev_x2, y1), fill=purple)
            draw.line((x1, y2, prev_x2, y2), fill=purple)
            current_section['width'] = prev_x2 - x1
            vertical_sections.append(current_section)
            zone_start = True

    return img, vertical_sections


# Scan the image and produce a visual output of non-whitespace areas
def image_scanner(image_path, output_json, output_image):
    img = Image.open(image_path).convert("RGB")
    original_img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    line_positions = []
    horizontal_chunks = []
    vertical_chunks = []

    # Determine the state changes in the horizontal direction
    state_changes = detect_state_changes(img, "horizontal")
    # Go through the state changes to determine the relevant chunks of data
    chunk_of_data = state_change_analysis(state_changes)
    # Document Analysis using Threshold
    img, horizontal_chunks = threshold_analysis(chunk_of_data, img, "horizontal")

    # Determine the state changes in the vertical direction
    vertical_state_changes = detect_vertical_state_changes(original_img, horizontal_chunks)
    # Go through the state changes to determine the relevant chunks of data
    vertical_chunk_of_data = vertical_state_change_analysis(vertical_state_changes)
    # Document Analysis using Threshold
    img, vertical_chunks = vertical_threshold_analysis(vertical_chunk_of_data, horizontal_chunks, img, "vertical")

    # Export the image with the lines drawn
    img.save(output_image)

    # Create JSON output
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


def initialize_scanner(input_file_path, output_file_path):
    # Get the document name
    document_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Get the file extension
    ext = os.path.splitext(input_file_path)[1].lower()

    # If the file is a pdf, convert it to images and analyze each image
    if ext == ".pdf":
        try:
            images = convert_from_path(input_file_path, dpi=300)
            print(f"Converted {len(images)} page(s) from PDF.")

            for i, img in enumerate(images):
                new_image_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}.png")
                json_output_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}_analyzed.json")
                analyzed_image_path = os.path.join(output_file_path, f"{document_name}_page_{i + 1}_analyzed.png")
                img.save(new_image_path, "PNG")
                # Perform analysis on each page
                image_scanner(new_image_path, json_output_path, analyzed_image_path)
        except Exception as e:
            print(f"Error converting PDF: {e}")
    # If the file is already an image, proceed with analysis
    elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        json_output_path = os.path.join(output_file_path, f"{document_name}_analyzed.json")
        analyzed_image_path = os.path.join(output_file_path,f"{document_name}_analyzed.png")
        image_scanner(input_file_path, json_output_path, analyzed_image_path)
    else:
        print(f"Skipping: Unsupported file type → {input_file_path}")


initialize_scanner(
    #r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\ReleaseAndAuthorizationOfPayment-2.jpg"
    r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\CleanDocumentAnalysisBase.pdf", 
    r"C:\Users\jovan\OneDrive\Desktop\CS499\PDF Scanner\cs-499 Test Cases\Test Results"
    )



# Performance Monitoring
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
