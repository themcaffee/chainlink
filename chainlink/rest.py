from flask import Flask, request, jsonify
from flask_cors import CORS

from chainlink.core import mp_get_github_from_pypi
from config import ENV


# Setup flask and get it's configuration from config.py
app = Flask(__name__)
app.config.from_object("config")
# Allow cross origin requests when in development mode
if ENV == "development":
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/pypi_github', methods=['POST'])
def pypi_github():
    """
    Gets a list of github repos from a requirements.txt file string
    :return: List of github repos
    """
    req_json = request.get_json()
    github_repos = mp_get_github_from_pypi(req_json["requirements_text"])
    return jsonify(github_repos), 200
