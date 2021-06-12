'''

Author: Delzad Bamji
'''

from flask import Flask, render_template, request, redirect, g

import shelve
from flask_restful import Resource, Api, reqparse
import sqlite3
import requests
import pandas as pd
import json
import configparser

app = Flask(__name__)
api = Api(app)

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#
#         db = g._database = sqlite3.connect("HORSEDATA.db")
#         cur = db.cursor()
#         cur.execute(
#             """create table if not exists {} (
#             id integer PRIMARY KEY NOT NULL,
#             name  text,
#             price  integer,
#             age    integer,
#             height  float,
#             sex text)""".format("Horse")
#         )
#
#         with open("HorsePrices.csv", "r") as f:
#             content = f.read().split("\n")
#             i = len(content)
#             for line in content:
#                 if i == 1:
#                     break
#                 # print(line)
#                 line = line.split(",")
#                 sql = "insert into Horse(id,name,price,age,height,sex) values(" + line[1] + "," + "'" + line[
#                     2] + "'" + "," + line[3] + "," + line[4] + "," + line[5] + "," + "'" + line[6] + "'" + ")"
#                 cur.execute(sql)
#                 i -= 1
#
#     return db

#
# @app.teardown_appcontext
# def teardown_db(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

config = configparser.ConfigParser()
config.read('configheader.properties')
config["configheader"]["flag"] = "False"
with open('configheader.properties', 'w') as configfile:
    config.write(configfile)



@app.route("/", methods=["GET", "POST"])
def index():
    horse_data = ""
    warning = ""
    sqlstring = ""
    endpoint_info={}
    querying=""
    # if post method is called after form submission
    if request.method == "POST":
        print("FORM DATA RECEIVED IN POST METHOD")


# /////////////////////////

        if "nm" in request.form:
            print(request.form["nm"])
            horseName = request.form["nm"]
            getSql = "http://localhost:5000/horses/"+horseName
            print(getSql)
            response = requests.get(getSql)
            print(response)
            json_data = response.json()
            horse_data = json_data["data"]
            print(json_data)
            sqlstring = getSql
            endpoint_info=json_data
            querying="full"
            # -------------------setting config header-----------------------#
            config["configheader"]["flag"] = "True"
            with open('configheader.properties', 'w') as configfile:
                config.write(configfile)

            if config["configheader"]["flag"] == "True" or config["configheader"]["flag"] == True:
                print("config is true")
            else:
                print("config is still false")

        if "HorseId" in request.form:
            print(request.form["HorseId"])
            if config["configheader"]["flag"] == "True" or config["configheader"]["flag"] == True:

                HorseId = request.form["HorseId"]
                HorseId = int(HorseId)
                if "account" in request.form:
                    print(request.form["account"])
                    account = request.form["account"]
                    account = float(account)
                sqlstring="http://localhost:5000/horselist"
                response2 = requests.get(sqlstring)

                all_horses = response2.json()["data"]

                listall = list(all_horses["HorseID"].values())

                if HorseId in listall:

                    inde = list(all_horses["HorseID"].keys())[list(all_horses["HorseID"].values()).index(HorseId)]

                    horse_data = {'id': all_horses["HorseID"][inde], 'name': all_horses["name"][inde], 'Price': all_horses["Price"][inde],
                           'Age': all_horses["Age"][inde], 'Height': all_horses["Height"][inde], 'Sex': all_horses["Sex"][inde]}

                    if account>= float(horse_data['Price']):
                        endpoint_info={"message":"Successfully placed a bet on the horse","data":horse_data}
                    else:
                        endpoint_info = {"message": "OOPS!!! Insufficient funds, check the price for the horse and try again", "data": {}}
                else:
                    horse_data="{}"
                    endpoint_info={"message":"no horse found","data":{}}

                config["configheader"]["flag"] = "False"
                with open('configheader.properties', 'w') as configfile:
                    config.write(configfile)

            else:
                warning="{\"message\":FATAL ERROR! Please send a query in 1. before placing a bet here,\"data\":{}}"


    else:
        # redirect(request.url)
        return render_template('index.html', ISO="")
    return render_template('index.html', sql_string=sqlstring, horse_data=horse_data, endpoint_info=endpoint_info,querying=querying, warning=warning)


# class HorseList(Resource):


class Horse(Resource):
    def get(self):
        data = pd.read_csv('HorsePricesREST.csv')
        data = data.to_dict()
        return {"message":"success","data":data},200

    def get(self, name):

        try:
            data = pd.read_csv('HorsePricesREST.csv')
            data = data.to_dict()
            inde = list(data["name"].keys())[list(data["name"].values()).index(name)]
            # print(inde)
            obj = {'id': data["HorseID"][inde], 'name': data["name"][inde], 'Price': data["Price"][inde],
                   'Age': data["Age"][inde], 'Height': data["Height"][inde], 'Sex': data["Sex"][inde]}
            # print(obj)
            if not obj:
                return {'message': "no horse found", "data": {}}, 404
            else:
                return {'message': "success", "data": obj}, 200

        except Exception as e:
            return {'message':"no horse found","data":{}},404


class User(Resource):
    pass

class horseList(Resource):
    def get(self):
        data = pd.read_csv('HorsePricesREST.csv')
        data = data.to_dict()
        return {"message":"success","data":data},200

api.add_resource(User, '/users')

api.add_resource(Horse, '/horses/<string:name>')

api.add_resource(horseList, '/horselist')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

