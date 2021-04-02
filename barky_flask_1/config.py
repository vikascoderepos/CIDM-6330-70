import os
from flask import Flask

# app.run(host='0.0.0.0', debug=True)

def get_sqllite_uri():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookmarks.db"))
    return database_file


def get_api_url():
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = 5005 if host == "0.0.0.0" else 80
    return f"http://{host}:{port}"