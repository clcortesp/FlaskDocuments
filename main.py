from flask import Flask, request, send_file, jsonify
import os
import json

app = Flask(__name__)

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
    archivo = request.files['archivo']
    binary_data = archivo.read()

    # Obtener el ID del JSON enviado en la solicitud
    request_data = json.loads(request.form.get('json_data'))
    id_cliente = request_data.get('id_cliente')
    id_caso = request_data.get('id_caso')
    id_correo = request_data.get('id_correo')

    # Obtener el nombre original del archivo
    original_filename = archivo.filename

    # Obtener la extensión del archivo
    _, file_extension = os.path.splitext(original_filename)

    # Obtener el tipo de contenido basado en la extensión del archivo
    content_type = get_content_type(file_extension)

    # Crear la estructura de carpetas
    cliente_folder = os.path.join('/home/claudio/archivos_adjuntos', id_cliente)
    caso_folder = os.path.join(cliente_folder, id_caso)
    correo_folder = os.path.join(caso_folder, id_correo)

    # Crear las carpetas si no existen
    os.makedirs(cliente_folder, exist_ok=True)
    os.makedirs(caso_folder, exist_ok=True)
    os.makedirs(correo_folder, exist_ok=True)

    # Construir la ruta del archivo
    file_path = os.path.join(correo_folder, original_filename)

    # Guardar el archivo en el sistema local
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
        return send_file(file_path, as_attachment=True, mimetype=get_content_type(os.path.splitext(file_path)[1]))
    else:
        return 'Archivo no encontrado', 404

if __name__ == '__main__':
    app.run(debug=True)
