import os


def get_sqllite_uri():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    return f"sqlite:///{}".format(os.path.join(project_dir, "bookmarks.db"))


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{0.0.0.0}:{port}"




