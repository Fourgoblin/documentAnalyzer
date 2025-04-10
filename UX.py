from flask import Flask, render_template, request
import os
import ImageScanner
import webbrowser

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
    file.save(filepath)

    # Now, call the ImageScanner.initialize_scanner method
    result = ImageScanner.initialize_scanner(filepath, "./static", horizontal, vertical)

    # You can return a result to be displayed or a success message
    return "Image Scanned Successfully"

if __name__ == '__main__':
    main()
