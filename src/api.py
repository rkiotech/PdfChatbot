
from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)

@app.route('/myapi', methods=['GET'])
def hit():

    return "API is working"
if __name__ == '__main__':
    app.run(debug=True)