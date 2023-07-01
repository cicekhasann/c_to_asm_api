from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Translate C code to assembly
@app.route('/translate', methods=['POST'])
def translate():
    c_code = request.form['c_code']

    # Create a temporary C file
    c_file = 'temp.c'
    with open(c_file, 'w') as file:
        file.write(c_code)

    # Use gcc to generate the assembly code
    asm_file = 'output.s'
    try:
        subprocess.check_output(['gcc', '-S', c_file, '-o', asm_file])
        with open(asm_file, 'r') as file:
            asm_code = file.read()
        return render_template('result.html', c_code=c_code, asm_code=asm_code)
    except subprocess.CalledProcessError as e:
        return render_template('result.html', error_message=str(e))
    finally:
        # Delete the temporary files
        os.remove(c_file)
        os.remove(asm_file)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
