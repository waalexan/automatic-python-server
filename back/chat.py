from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
import os
import base64
from google import genai
from google.genai import types
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("text", "")
    
    if not user_input:
        return jsonify({"error": "Texto não fornecido"}), 400

    def generate():
        try:
            client = genai.Client(
                api_key=os.environ.get("GEMINI_API_KEY"),
            )

            model = "gemini-2.0-flash"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=user_input),
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text="o seu nome e MapaZZZ e vc es uma IA, angola treinada por Alunas da escola 42 Luanda em um prjecto de Hackton"),
                ],
            )

            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    print(chunk.text)
                    yield f"data: {chunk.text}\n\n"

            yield "event: end\ndata: \n\n"

        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
