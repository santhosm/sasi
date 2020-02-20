import psycopg2
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)

class intentListener(Resource):
    def post(self):
        res = request.data.decode('UTF-8')
        res = res.split(":")[1]
        res =res.split("}")[0]
        try:
            connection = psycopg2.connect(user = "postgres",password = "postgres",host = "172.24.131.89",
                                  port = "5432",
                                  database = "sample")
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO sample (name1) VALUES ('{}'::name)""".format(str(res)))
            # cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)    
        finally:
            connection.close()
    def get(self):
        try:
            connection = psycopg2.connect(user = "postgres",password = "postgres",host = "172.24.131.89",
                                  port = "5432",
                                  database = "sample")
            cursor = connection.cursor()
            print ("***")
            cursor.execute("SELECT * FROM sample")            
            val = cursor.fetchall()  
            arr = []          
            for row in val:
                arr.append(row[0])
            print(arr)
            return arr
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)    

api.add_resource(intentListener, '/intents')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8180')
