from flask import Flask, request, jsonify, render_template

app = Flask(__name__, instance_relative_config=True)

@app.route('/')
def boxes():
    return render_template('UX.html')

if __name__ == '__main__':
    app.run(debug=True)


    