from flask import Flask, request, jsonify, render_template
import ImageScanner
app = Flask(__name__, instance_relative_config=True)

@app.route('/')
def boxes():
    return render_template('UX.html')

@app.route('/Image_Scanner')
def Image_Scanner():
    file = request.form['file']
    result = ImageScanner.initialize_scanner(file, "./static")
    return "Image Scanned"


if __name__ == '__main__':
    app.run(debug=True)


    