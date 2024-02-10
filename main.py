from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/app/v1/documents', methods=['GET'])
def get_string():
    print("test")
    return "tu usuario"

app.run(debug=True)
