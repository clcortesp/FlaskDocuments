from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/app/v1/documents', methods=['POST'])
def receive_attachment():
    binary_data = request.get_data()

    print(binary_data)

    return 'Archivo recibido con éxito.', 200

app.run(debug=True)
