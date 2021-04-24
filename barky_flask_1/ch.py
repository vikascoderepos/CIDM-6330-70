from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services
from pprint import pprint
import json
from datetime import datetime, timezone
import uuid

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqllite_uri()))
app = Flask(__name__)

    
@app.route("/")
def index():
    return jsonify({'message': 'Barky App'}) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

