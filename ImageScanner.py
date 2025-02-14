import csv
import time
from PIL import Image, ImageDraw, ImageFont

# Start time
start_time = time.time()

# Scan the image and output a CSV file with pixel values
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

        # Check if the entire row has the same color
        if all(img.getpixel((x, y)) == first_pixel for x in range(width)):
            current_state = "whitespace"
        else:
            current_state = "non-whitespace"

        # If state changes, store the position and state change
        if previous_state is not None and previous_state != current_state:
            state_changes.append((y, previous_state, current_state))
        previous_state = current_state

    # After the loop ends, check the last state change if it exists
    if previous_state is not None:
        state_changes.append((height, previous_state, None))  # Mark the end of the last state

    chunk_of_data = []

    # Now, process the state changes and draw lines where necessary
    data_start = 0
    data_end = 0
    for i in range(1, len(state_changes)):
        y, prev_state, current_state = state_changes[i]

        # Draw a line on the last "whitespace" state
        if prev_state == "whitespace" and current_state == "non-whitespace":
            draw.line((0, y - 1, width, y - 1), fill=(128, 0, 128))  # Draw a line where the "whitespace" ends
            #if data_start == 0:
            data_start = y

        # Draw a line on the last "non-whitespace" state
        elif prev_state == "non-whitespace" and current_state == "whitespace":
            draw.line((0, y - 1, width, y - 1), fill=(128, 0, 128))  # Draw a line where the "non-whitespace" ends
            #if data_start != 0:
            data_end = y
        if data_start != 0 and data_end != 0:
            chunk_of_data.append([data_start, data_end])
            data_start = 0
            data_end = 0

    # Iterate through chunk_of_data and compare adjacent chunks
    threshold = 30  # Set a threshold for the gap between chunks
    for i in range(1, len(chunk_of_data)):
        prev_data_start, prev_data_end = chunk_of_data[i - 1]
        curr_data_start, curr_data_end = chunk_of_data[i]

        # Draw a line at the start of the data chunk
        #if i == 1:
            #draw.line((0, prev_data_start - 1, width, prev_data_start - 1), fill=(128, 0, 128))  # Draw a line at the end of the previous chunk
        
        # Calculate the difference between the end of the previous chunk and the start of the current chunk
        gap = curr_data_start - prev_data_end
        
        # If the gap between chunks is within the threshold, wait to draw a line
        if gap <= threshold:
            continue  # Skip drawing a line for this chunk pair
        # If the gap exceeds the threshold, draw a line at the end of the previous chunk
        else:
            continue
            #draw.line((0, prev_data_end - 1, width, prev_data_end - 1), fill=(128, 0, 128))  # Draw a line at the end of the previous chunk
            #draw.line((0, curr_data_end - 1, width, curr_data_end - 1), fill=(128, 0, 128))  # Draw a line at the end of the previous chunk
            #draw.line((0, curr_data_start - 1, width, curr_data_start - 1), fill=(128, 0, 128))  # Draw a line at the end of the previous chunk

    img.save(output_image)

# Output a CSV file with pixel values and an image with coordinates
scan_image_to_csv(
    r"C:\Users\jovan\OneDrive\Desktop\CS499\CleanDocumentFirstPage.png",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output.csv",
    r"C:\Users\jovan\OneDrive\Desktop\CS499\output_image.png"
)

# End time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")