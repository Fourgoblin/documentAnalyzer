import csv
import time
from PIL import Image, ImageDraw, ImageFont

# Perfmance Monitoring
start_time = time.time()

# Scan the image and output an image showing the selection of data containing elements (non-white space)
def scan_image_to_csv(image_path, output_csv, output_image):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    state_changes = []
    '''
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y", "R", "G", "B"])  # Column headers
           # Loop through each row
    '''
    previous_state = None
    for y in range(height):
        first_pixel = img.getpixel((0, y))  # Get the first pixel in the row
        r1, g1, b1 = first_pixel

        # Determine whether the row is whitespace or non-whitespace
        if all(img.getpixel((x, y)) == first_pixel for x in range(width)):
            current_state = "whitespace"
        else:
            current_state = "non-whitespace"
        
        # Record the state changes
        if previous_state is None:
            previous_state = current_state
        if previous_state is not None and previous_state != current_state:
            state_changes.append((y, previous_state, current_state))
        
        previous_state = current_state

    # Go through the state changes to determine the relevant chunks of data
    chunk_of_data = []
    data_start = 0
    data_end = 0
    for i in range(len(state_changes)):
        y, prev_state, current_state = state_changes[i]

        # Determine the starting y coordinate of a non-whitespace area
        if prev_state == "whitespace" and current_state == "non-whitespace":
            data_start = y
        # Determine the ending y coordinate of a non-whitespace area
        elif prev_state == "non-whitespace" and current_state == "whitespace":
            data_end = y

        # Store this chunk of data
        if data_start != 0 and data_end != 0:
            chunk_of_data.append([data_start, data_end])
            data_start = 0
            data_end = 0

            
    # Go through all the chunks of data and determine if the gap between them is within a certain threshold
    threshold = 18  
    chunk_start = 0 # Flag to determine whether a line needs to be drawn at the start of a chunk
    for i in range(1, len(chunk_of_data)):
        prev_data_start, prev_data_end = chunk_of_data[i - 1]
        curr_data_start, curr_data_end = chunk_of_data[i]

        # Draw a line at the start of the first data chunk in the document
        if i == 1:
            chunk_start = 1
        
        if chunk_start == 1:
            draw.line((0, prev_data_start - 1, width, prev_data_start - 1), fill=(128, 0, 128))
            chunk_start = 0
        
        # Calculate the difference between the end of the previous chunk and the start of the current chunk
        gap = curr_data_start - prev_data_end
        
        # If the gap between chunks is within the threshold, wait to draw a line
        if gap <= threshold:
            continue
        # If the gap exceeds the threshold, draw a line at the end of the previous chunk
        else:
            draw.line((0, prev_data_end + 1, width, prev_data_end + 1), fill=(128, 0, 128))
            chunk_start = 1 # Draws a line at the start of the next chunk

        # If at the last data chunk, draw a line at the end of it
        if i == len(chunk_of_data) - 1:
            draw.line((0, curr_data_end + 1, width, curr_data_end + 1), fill=(128, 0, 128))
            # If threshold gap is still too large from previous data chunk, draw a line at the start of the last data chunk
            draw.line((0, curr_data_start - 1, width, curr_data_start - 1), fill=(128, 0, 128))
    
    # Export the image with the lines drawn
    img.save(output_image)

# Output a CSV file with pixel values and an image with coordinates
scan_image_to_csv(
    r"C:\Users\jovan\OneDrive\Desktop\CS499\CleanDocumentFirstPage.png",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output.csv",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output_image.png"
)

# Performance Monitoring
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")