from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from rq import Queue

from chainlink.core import get_issues_from_requirements_text, mp_get_issues_from_requirements, mp_get_github_from_pypi

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object("config")


@app.route("/api/python_issues", methods=['POST'])
def python_issues():
    req_json = request.get_json()
    issues = mp_get_issues_from_requirements(req_json["requirements_text"])
    return jsonify(issues), 200


@app.route('/api/pypi_github', methods=['POST'])
def pypi_github():
    req_json = request.get_json()
    github_repos = mp_get_github_from_pypi(req_json["requirements_text"])
    return jsonify(github_repos), 200
