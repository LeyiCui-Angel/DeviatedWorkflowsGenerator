from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from WorkflowGen import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    data = {
        'workflow': '',
        'error_type': '',
        'level': ''
    }

    if request.method == 'POST':
        workflow = request.form.get('workflow')
        error_type = request.form.get('error_type')
        level = int(request.form.get('level'))

        data = {
            'workflow': workflow,
            'error_type': error_type,
            'level': level
        }

        if error_type == "omission":
            output = omission(workflow.split(';'), level)
        elif error_type == "repetition":
            output = repetition(workflow.split(';'), level)
        elif error_type == "permutation":
            output = permutation(workflow.split(';'), level)

    return render_template('index.html', output="\n".join([str(elem) for elem in output]) if output else None, data=data)

if __name__ == '__main__':
    app.run(debug=True)
