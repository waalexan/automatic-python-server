from flask import Flask, Response
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/get_names', methods=['GET'])
def get_names():
    commands = ["ipconfig"]
    
    def generate_names():
        for command in commands:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            try:
                output = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                output = result.stdout.decode('utf-8', errors='replace')
            
            try:
                error = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                error = result.stderr.decode('utf-8', errors='replace')
            
            if result.returncode != 0:
                yield f"data: Error {error}\n\n"
            else:
                yield f"data: Sucess {output}\n\n"

    return Response(generate_names(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
