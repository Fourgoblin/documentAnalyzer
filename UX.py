from flask import Flask, render_template, request, jsonify
import os
import ImageScanner
import webbrowser
import json



app = Flask(__name__)

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

    # Save the file temporarily (this path can be customized)
    filepath = os.path.join('static', file.filename)
    global jsonFileName
    jsonFileName = filepath
    file.save(filepath)

    # Now, call the ImageScanner.initialize_scanner method
    result = ImageScanner.initialize_scanner(filepath, "./static", horizontal, vertical)

    # You can return a result to be displayed or a success message
    return "Image Scanned Successfully"

@app.route('/save-json', methods=['POST'])
def save_json():
    data = request.get_json()
    global jsonFileName
    newJsonFileName = jsonFileName
    if '.' in jsonFileName:
        newJsonFileName = jsonFileName.rsplit('.', 1)[0]  # Split off the extension
        newJsonFileName += '_analyzed.json'
        #print(jsonFileName)
    if not data:
        return jsonify({'message': 'no JSON data received'}), 400
    
    with open(newJsonFileName, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'message': 'JSON saved succesfully'})
        

if __name__ == '__main__':
    main()
