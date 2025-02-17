import csv
import time
import json
from PIL import Image, ImageDraw, ImageFont

# Perfmance Monitoring
start_time = time.time()

# JSON file structure
data = {
    "Data Chunk": {
        "Index": None,
        "X-Pos": None,
        "Y-Pos": None
    }
}

# Euclidean distance between two RGB values
def euclidean_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

# Function to detect state changes
def detect_state_changes(img, mode):
    width, height = img.size
    euclidean_threshold = 100
    state_changes = []
    previous_state = None

    # Horizontal mode
    if mode == "horizontal":
        for y in range(height):
            first_pixel = img.getpixel((0, y))  # Get the first pixel in the row
            if all(euclidean_distance(img.getpixel((x, y)), first_pixel) < euclidean_threshold for x in range(width)):
                current_state = "whitespace"
            else:
                current_state = "non-whitespace"
            # Record the state changes
            if previous_state is None:
                previous_state = current_state
            if previous_state is not None and previous_state != current_state:
                state_changes.append((y, previous_state, current_state))
            
            previous_state = current_state
    # Vertical mode
    else:
        for x in range(width):
            first_pixel = img.getpixel((x, 0))  # Get the first pixel in the column
            if all(euclidean_distance(img.getpixel((x, y)), first_pixel) < euclidean_threshold for y in range(height)):
                current_state = "whitespace"
            else:
                current_state = "non-whitespace"
            # Record the state changes
            if previous_state is None:
                previous_state = current_state
            if previous_state is not None and previous_state != current_state:
                state_changes.append((y, previous_state, current_state))
            
            previous_state = current_state

    return state_changes


# Scan the image and produce a visual output of non-whitespace areas
def image_scanner(image_path, output_csv, output_image):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    draw = ImageDraw.Draw(img)
    #font = ImageFont.load_default()
    state_changes = []
    line_positions = []
    
    # Determine the state changes in the horizontal direction
    state_changes = detect_state_changes(img, "horizontal")

    # Go through the state changes to determine the relevant chunks of data
    chunk_of_data = []
    data_start = 0
    data_end = 0
    for i in range(len(state_changes)):
        y, prev_state, current_state = state_changes[i]

        # If starting with non-whitespace, ensure data_start is set
        if i == 0 and prev_state == "non-whitespace":
            data_start = 0  # Start from the top
        # Determine the starting y coordinate of a non-whitespace area
        elif prev_state == "whitespace" and current_state == "non-whitespace":
            data_start = y
        # Determine the ending y coordinate of a non-whitespace area
        elif prev_state == "non-whitespace" and current_state == "whitespace":
            data_end = y

        # Store this chunk of data
        if data_start != 0 and data_end != 0:
            data_width = data_end - data_start
            #print(f"Data chunk {i}: {data_start}, {data_end}, {data_width}")
            if data_width > 1: #Ignore single lines (likely a crease in the paper)
                chunk_of_data.append([data_start, data_end])
            data_start = 0
            data_end = 0
            
    # Go through all the chunks of data and determine if the gap between them is within a certain threshold
    threshold = 25
    for i in range(1, len(chunk_of_data)):
        prev_data_start, prev_data_end = chunk_of_data[i - 1]
        curr_data_start, curr_data_end = chunk_of_data[i]

        # Draw a line at the start of the first data chunk in the document
        if i == 1:
            draw.line((0, prev_data_start, width, prev_data_start), fill=(0, 0, 0))
            line_positions.append(prev_data_start)
        
        
        # Calculate the difference between the end of the previous chunk and the start of the current chunk
        gap = curr_data_start - prev_data_end
        
        # If the gap between chunks is within the threshold, wait to draw a line
        if gap <= threshold:
            continue
        # If the gap exceeds the threshold, draw a line at the end of the previous chunk and at the start of the current one
        else:
            draw.line((0, prev_data_end, width, prev_data_end), fill=(255, 0, 0))
            draw.line((0, curr_data_start, width, curr_data_start), fill=(0, 0, 0))
            line_positions.append(prev_data_end)
            line_positions.append(curr_data_start)

        # If at the last data chunk, draw a line at the end of it
        if i == len(chunk_of_data) - 1:
            draw.line((0, curr_data_end, width, curr_data_end), fill=(0, 255, 255))
            line_positions.append(curr_data_end)
    
    # Ensure the last chunk gets a line at its end
    last_data_start, last_data_end = chunk_of_data[-1]
    draw.line((0, last_data_end, width, last_data_end), fill=(0, 0, 255))
    
    # Export the image with the lines drawn
    img.save(output_image)
    # Export the line positions to a JSON file
    custom_path = r"C:\Users\jovan\OneDrive\Desktop\CS499\line_positions.json"
    with open(custom_path, "w") as json_file:
        json.dump(line_positions, json_file, indent=4)

# Output a CSV file with pixel values and an image with coordinates
image_scanner(
    #r"C:\Users\jovan\OneDrive\Desktop\CS499\CleanDocumentFirstPage.png",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\Sample2.jpg",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output.csv",
    #r"C:\Users\jovan\OneDrive\Desktop\CS499\output_image.png"
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output_Sample2.jpg",
)

# Performance Monitoring
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")