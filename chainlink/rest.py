from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/python_issues", methods=['POST'])
def python_issues():
    req_json = request.get_json()
    issues = get_issues_from_requirements_text(req_json["requirements_text"])
    return jsonify(issues), 200
