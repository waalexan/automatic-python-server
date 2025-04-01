from google import genai
from google.genai import types

# Definir a instrução para a IA
instruction = """O seu nome é MapaZZZ e você é uma IA, Angola, treinada por Alunas da escola 42 Luanda em um projeto de Hackathon. 
                Use termos angolanos como gírias e formas típicas de falas de angolanos."""

# Classe para interagir com a API do Gemini
class Gmini:
    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, contents):
        # Configuração da geração de conteúdo
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[types.Part.from_text(text=instruction)],
        )

        # Gerar conteúdo usando a API do Gemini
        response = ""
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        ):
            response += chunk.text

        return response
