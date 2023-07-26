from flask import Flask, render_template, request, send_file
import itertools
from itertools import combinations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Your code here, use request.form to access POST data
        iniWorkflow = request.form.get('workflow').split(';')
        errType = request.form.get('error_type').lower()
        level = int(request.form.get('level'))
        # rest of your code...
        # Write the result to a .txt file
        with open('output.txt', 'w') as f:
            for item in r:
                f.write("%s\n" % item)
        return render_template('index.html')

    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('output.txt', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
