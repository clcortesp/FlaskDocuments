from flask import Flask, request, send_file, jsonify
import os
import json

app = Flask(__name__)

def get_file_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower()

def get_content_type(file_extension):
    content_type_mapping = {
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.jpg': 'image/jpeg',
        # Agregar más extensiones y tipos de contenido según sea necesario
    }
    return content_type_mapping.get(file_extension, 'application/octet-stream')

@app.route('/api/test_adjunto', methods=['POST'])
def receive_attachment():
    # Obtener el contenido del archivo adjunto desde la solicitud
    binary_data = request.files['archivo'].read()

    # Obtener el ID del JSON enviado en la solicitud
    request_data = json.loads(request.form.get('json_data'))
    file_id = request_data.get('id')

    # Determinar la extensión del archivo
    file_extension = get_file_extension(request.files['archivo'].filename)

    # Obtener el tipo de contenido basado en la extensión del archivo
    content_type = get_content_type(file_extension)

    # Guardar el archivo en el sistema local
    file_path = os.path.join('ruta_local', f'{file_id}_{str(os.urandom(24).hex())}{file_extension}')
    with open(file_path, 'wb') as file:
        file.write(binary_data)

    # Construir la URL de descarga para Salesforce
    download_url = f'http://tu-servidor-flask.com/api/descargar_adjunto?fileId={os.path.basename(file_path)}'

    # Enviar la URL de descarga como parte de la respuesta
    response_data = {
        'mensaje': f'Archivo recibido con éxito. Tipo de contenido: {content_type}',
        'url_descarga': download_url
    }

    return jsonify(response_data), 200

@app.route('/api/descargar_adjunto', methods=['GET'])
def descargar_adjunto():
    fileId = request.args.get('fileId')
    file_path = os.path.join('ruta_local', fileId)

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype=get_content_type(get_file_extension(file_path)))
    else:
        return 'Archivo no encontrado', 404

if __name__ == '__main__':
    app.run(debug=True)