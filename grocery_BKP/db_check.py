# import psycopg2
# con = psycopg2.connect(database="vikas", user="vikas", password="postgres1234", host="localhost", port="5432")
# print("Database opened successfully")
from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData

db_string = "postgresql://vikas:postgres1234@localhost:5432/vikas"
engine = create_engine(db_string)
engine.connect()
# with engine.connect() as conn:
#     select_statement = 'SELECT CURRENT_TIME'
#     result_set = conn.execute(select_statement)
#     for r in result_set:
#         print(r)