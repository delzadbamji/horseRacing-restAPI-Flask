# # import shelve
# #
# #
# # def get_db():
# #     db=getattr(g,'_database',None)
# #     if db is None:
# #         db=g._database=shelve.open('horseData.db')
# #     return db
# # @app.teardown_appcontext
# # def teardown_db(exception):
# #     db=getattr(g,'_database',None)
# #     if db is not None:
# #         db.close()
# #
# #
# #
# # def getHorse(name):
# #     pass
#
# import pandas as pd
#
# data=pd.read_csv('HorsePricesREST.csv')
# # print(data)
# data=data.to_dict()
# # horseNames=data["name"]
# # print(data["name"])
# index=list(data["name"].keys())[list(data["name"].values()).index("stally")]
# # print(index)
# obj={'id':data["HorseID"][index],'name':data["name"][index],'Price':data["Price"][index],'Age':data["Age"][index],'Height':data["Height"][index],'Sex':data["Sex"][index]}
# # print(obj)