from flask import Flask, request, render_template, send_file, Response, make_response
from werkzeug.utils import secure_filename
from WorkflowGen import *
from io import BytesIO
from enter_prescription import OpenEMRWorkflow
import ast

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

@app.route('/download_output', methods=['POST'])
def download_output():
    output = request.form.get('output')

    if output is not None:
        bytes_io = BytesIO()
        bytes_io.write(output.encode('utf-8'))
        bytes_io.seek(0)

        response = make_response(bytes_io.getvalue())
        response.headers.set('Content-Type', 'text/plain')
        response.headers.set('Content-Disposition', 'attachment', filename='output.txt')
        return response

    return Response("No output found.", status=404)

@app.route('/run_workflow', methods=['GET', 'POST'])
def run_workflow():
    message = None
    if request.method == 'POST':
        try:
            actions = request.form.get('actions')
            action_list = ast.literal_eval(actions)
            workflow = OpenEMRWorkflow()

            # First, check if all actions are valid
            for action in action_list:
                action = action.strip()
                if not hasattr(workflow, action):
                    message = f"No such method: {action}. Please check again."
                    return render_template('run_workflow.html', message=message)

            # If all actions are valid, run the setup and actions
            workflow.run_setup()
            for action in action_list:
                action = action.strip()
                getattr(workflow, action)()

            message = "Workflow ran successfully."
        except Exception as e:
            message = f"Error occurred: {str(e)}"
    return render_template('run_workflow.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
