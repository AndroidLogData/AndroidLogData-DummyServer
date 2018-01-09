# -*- encoding=utf-8 -*-
import pymongo
from flask_pymongo import PyMongo
from Logdata.Log_Data_Logger import Log
from pymongo import errors


class DBManager:
    @staticmethod
    def init(app):
        try:
            global mongo
            mongo = PyMongo(app)
        except pymongo.errors.ConnectionFailure as e:
            Log.error("mongodb 연결 실패 : %s" % e)

    @staticmethod
    def logDataInsert(request):
        try:
            print(request.headers)
            print(request.form)
            print(request.content_type)
            mongo.db.logdata_android.insert({'message': request.form['message'],
                                             'tag': request.form['tag'],
                                             'level': request.form['level'],
                                             'time': request.form['time'],
                                             'totalMemory': request.form['totalMemory'],
                                             'availMemory': request.form['availMemory'],
                                             'memoryPercentage': request.form['memoryPercentage'],
                                             'threshold': request.form['threshold'],
                                             'lowMemory': request.form['lowMemory'],
                                             'dalvikPss': request.form['dalvikPss'],
                                             'otherPss': request.form['otherPss'],
                                             'totalPss': request.form['totalPss']})
        except Exception as e:
            print(e)
        except pymongo.errors.DuplicateKeyError as e:
            Log.error("중복되는 키가 존재합니다.: %s" % e)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            Log.error("서버 연결 실패 : %s" % e)

    @staticmethod
    def crashDataInsert(request):
        try:
            mongo.db.logdata_android.insert({'os': request.form['message']})
        except pymongo.errors.DuplicateKeyError as e:
            Log.error("중복되는 키가 존재합니다.: %s" % e)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            Log.error("서버 연결 실패 : %s" % e)

    @staticmethod
    def getLogdata():
        try:
            return mongo.db.logdata_android.find().sort([('time', pymongo.DESCENDING)])
        except Exception as e:
            print(e)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            Log.error("서버 연결 실패 : %s" % e)