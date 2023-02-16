from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import sklearn
import joblib

 
app = Flask(__name__)
CORS(app)

@cross_origin
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)

