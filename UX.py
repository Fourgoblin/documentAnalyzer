from flask import Flask, render_template, request, jsonify
import os
import sys
import ImageScanner
import webbrowser
import json


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

app = Flask(__name__)

# Make sure the outputs directory exists
outputs_dir = get_resource_path('outputs')
os.makedirs(outputs_dir, exist_ok=True)

# Keeping the static directory for now
static_dir = get_resource_path('static')
os.makedirs(static_dir, exist_ok=True)

def main():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:2000/')
    app.run(host="127.0.0.1", port=2000)

@app.route('/')
def boxes():
    return render_template('UX.html')

@app.route('/Image_Scanner', methods=['POST'])
def Image_Scanner():
    # Get the uploaded file from the request
    file = request.files['file']
    horizontal = int(request.form.get('slider1'))
    vertical = int(request.form.get('slider2'))

    # If no file is provided, return an error
    if not file:
        return "No file provided", 400

    # Save the file temporarily to the static directory (for web access)
    filepath = os.path.join(get_resource_path('static'), file.filename)
    file.save(filepath)

    # Get the document name for dynamic naming
    document_name = os.path.splitext(os.path.basename(file.filename))[0]
    global jsonFileName
    jsonFileName = f"{document_name}_analyzed.json"

    # Now, call the ImageScanner.initialize_scanner method with outputs directory
    result = ImageScanner.initialize_scanner(filepath, get_resource_path('outputs'), horizontal, vertical, 0, 0)
    
    # Copy the JSON file to static directory so frontend can access it
    output_json_path = os.path.join(get_resource_path('outputs'), jsonFileName)
    static_json_path = os.path.join(get_resource_path('static'), jsonFileName)
    
    # Copy file if it exists with proper formatting 
    if os.path.exists(output_json_path):
        with open(output_json_path, 'r') as source_file:
            json_content = json.load(source_file)
        with open(static_json_path, 'w') as dest_file:
            json.dump(json_content, dest_file, indent=4)
    
    # You can return a result to be displayed or a success message
    return "Image Scanned Successfully"

def get_outputs_folder():
    """Returns the correct outputs folder path based on execution context."""
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'outputs')

@app.route('/save-json', methods=['POST'])
def save_json():
    try:
        data = request.get_json()
        
        # Use the global jsonFileName for consistent naming
        filename = jsonFileName if 'jsonFileName' in globals() else 'output_analyzed.json'
        
        # Save to outputs directory
        outputs_path = get_outputs_folder()
        os.makedirs(outputs_path, exist_ok=True)
        save_path = os.path.join(outputs_path, filename)
        
        with open(save_path, 'w') as f:
            json.dump({"document_sections": data}, f, indent=4)
            
        # Save to static directory
        static_path = get_resource_path('static')
        static_save_path = os.path.join(static_path, filename)
        
        with open(static_save_path, 'w') as f:
            json.dump({"document_sections": data}, f, indent=4)

        return jsonify({"message": f"JSON saved successfully at {save_path}"})

    except Exception as e:
        return jsonify({"message": f"Failed to save JSON: {str(e)}"}), 500
        

if __name__ == '__main__':
    main()
