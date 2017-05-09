from pymongo import MongoClient
import pymongo
import urllib
from datetime import datetime

class Mdbmanager:

    def __init__(self):
        #self.m_image = Gaugedetector(image,savepath,savefileName)
        password = urllib.quote_plus('gas1meter2iot')
        client = MongoClient('mongodb://grsdatamanager:' + password + '@107.170.216.212')
        print client
        self.db = client.grsdata

    def insertgrsdata(slef,userid,gaugeid,dauthkey,taskid,gvalue) :
        #find userid
        result = slef.db.grsrecorde.find_one({"userid" : userid })
        if( result is None):
            result = slef.db.grsrecorde.insert_one(
                {
                    "userid": userid,
                    "gauge": [
                        {
                            "gaugeid": gaugeid,
                            "dauthkey": dauthkey,
                            "taskid": taskid,
                            "inputdatefgvalue":  datetime.now(),
                            "gvalue": gvalue
                        }
                    ],
                }
            )
        else:
           result = slef.updategrsdata(userid,gaugeid,dauthkey,taskid,gvalue)
        return result

    def updategrsdata(self,userid,gaugeid,dauthkey,taskid,gvalue):
        result = self.db.grsrecorde.update(
            { "userid": userid},
            { "$push":
                { "gauge":
                    {
                        "gaugeid": gaugeid,
                        "dauthkey": dauthkey,
                        "taskid": taskid,
                        "inputdatefgvalue":  datetime.now(),
                        "gvalue": gvalue
                    }
                }
            }
        )
        return result


if __name__ == "__main__":
    db = Mdbmanager()
    #db.insertgrsdata()
