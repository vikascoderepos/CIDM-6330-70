import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
 
password = os.getenv("password")
user = os.getenv("user")
db_name = os.getenv("db_name")

# def get_postgres_uri():
#     host = os.environ.get("DB_HOST", "localhost")
#     port = 54321 if host == "localhost" else 5432
#     return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "grocery.db"))
    database_file = database_file + '?check_same_thread=False'
    return database_file


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    print(f"http://{host}:{port}")
    return f"http://{host}:{port}"

