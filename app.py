from flask import Flask, send_from_directory, jsonify, request
import json
from backend.src.arya_compiler import arya_compiler
from backend.src.gemini_api import gemini

app = Flask(__name__, static_folder='build', static_url_path='/')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/arya_compiler_endpoint', methods=['GET', 'POST'])
def arya_compiler_interface():
    try:
        # Log the incoming request
        print('Received request to Arya compiler endpoint')

        # Get the code from the request data
        code_input = json.loads(request.get_data())["code"]
        print(f"Code input: {code_input}")

        # Call the compiler
        compiler_output = arya_compiler(code_input)

        # Log the compiler output
        print('Arya compiler output:', compiler_output)

        # Return the output from the compiler as a string
        return [compiler_output]
    except Exception as e:
        # Log any errors
        print("Python error: ", e)

        # Return an error response
        return ["Python error: " + str(e)]


@app.route('/gemini_endpoint', methods=['GET', 'POST'])
def gemini_interface():
    try:
        # Log the incoming request
        print('Received request to Gemini AI endpoint')

        # Get the input data from the request
        user_input = request.get_json().get('input_data')
        print(f"User input: {user_input}")

        # Call the Gemini AI function
        gemini_output = gemini(str(user_input))

        # Log the response
        print('Gemini AI output:', gemini_output)

        # Return the output from Gemini  as a string
        return jsonify({'output': gemini_output})
    except Exception as e:
        # Log any errors
        print("Gemini error: ", e)
        # Return an error response
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
