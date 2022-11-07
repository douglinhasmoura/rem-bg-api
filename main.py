from dotenv import load_dotenv
from flask import Flask, request, send_file, make_response
from rembg import remove
import os

load_dotenv()

app = Flask(__name__)

input_path = ''
output_path = ''


@app.route("/", methods=["POST"])
def post():

    try:
        authentication = request.headers.get('authorization')
        authBasic = os.environ['AUTH']

        if authentication is None or authentication.split(' ')[1] != authBasic:
            return make_response({"error": "Não autenticado"}, 401)

        if len(request.files) == 0:
            return make_response({"error": "Problemas ao processar a imagem"}, 400)

        if request.files.get('file') is None:
            return make_response({"error": "Arquivo inválido"}, 400)

        file = request.files['file']

        extension = file.filename.split('.')[1]
        mimetype = file.mimetype

        if extension != 'jpg' and extension != 'jpeg' and extension != 'png':
            return make_response({"error": "Extensão inválida"}, 400)

        file.save(f'input.{extension}')
        input_path = f'input.{extension}'

        output_path = f'output.png'

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)
        os.remove(input_path)
        return send_file(mimetype=mimetype, path_or_file=output_path)
    except:
        return make_response({"error": "Problemas ao processar a imagem"}, 500)


if __name__ == "__main__":
    app.run(debug=True)
