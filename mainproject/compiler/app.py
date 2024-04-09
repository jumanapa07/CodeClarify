import subprocess
import json
import sys
from io import StringIO
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/compile_and_execute', methods=['POST'])
def compile_and_execute_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    inputs = data.get('inputs')

    if not code or not language:
        return jsonify({'success': False, 'error': 'Code or language not provided'})

    return execute_code(code, language, inputs)

def execute_code(code, language, inputs=None):
    
    if language == 'python':
        return execute_python_code(code,inputs)
    elif language == 'cpp':
        return execute_cpp_code(code, inputs)
    elif language == 'java':
        return execute_java_code(code, inputs)
    else:
        return {'success': False, 'message': 'Unsupported language'}


def execute_python_code(code, inputs):
    try:
        # Redirect stdout to capture the output
        stdout_orig = sys.stdout
        sys.stdout = StringIO()

        # Redirect stderr to capture any error messages
        stderr_orig = sys.stderr
        sys.stderr = StringIO()

        # Store the original input function
        input_orig = __builtins__.input

        # Define a custom input function to provide input
        def custom_input(prompt=""):
            return inputs

        # Override the input function with the custom_input function
        __builtins__.input = custom_input

        # Execute the Python code
        exec(code)

        # Get the captured output and restore stdout
        output = sys.stdout.getvalue()
        sys.stdout = stdout_orig

        # Get any error messages
        error = sys.stderr.getvalue()
        sys.stderr = stderr_orig

        # Restore the original input function
        __builtins__.input = input_orig

        return {'success': True, 'output': output, 'error': error}
    except Exception as e:
        return {'success': False, 'error': f'Error executing Python code: {e}'}



def execute_cpp_code(code,inputs):
    try:
        print("This is the code that we have received:\n", code)
        
        # Write the received C++ code to a temporary source file
        with open("/tmp/temp.cpp", "w") as cpp_file:
            cpp_file.write(code)
        
        # Compile the C++ source file
        compile_result = subprocess.run(["g++", "/tmp/temp.cpp", "-o", "/tmp/temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print('Compilation result:', compile_result.returncode)
        
        # If compilation failed, return the error message
        if compile_result.returncode != 0:
            return compile_result.stderr.decode()
        
        # Run the compiled C++ code
        if inputs is not None:
            run_result = subprocess.run(["/tmp/temp"], input=inputs.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            run_result = subprocess.run(["/tmp/temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        return {'success': True, 'output': run_result.stdout.decode(), 'error': run_result.stderr.decode()}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def execute_java_code(code, inputs=None):
    try:
        with open('Main.java', 'w') as file:
            file.write(code)

        # Compile Java code
        subprocess.check_output(['javac', 'Main.java'])

        # Execute compiled Java code
        result = subprocess.check_output(['java', 'Main'], input=inputs.encode() if inputs else None, text=True)
        return {'success': True, 'output': result}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': f'Error executing Java code: {e.output}'}
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
