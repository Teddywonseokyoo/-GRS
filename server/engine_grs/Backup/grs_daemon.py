#!/usr/bin/env python
import os
import subprocess
import time
import datetime
import commands
import logging
from daemon import runner
from pymongo import MongoClient
import pymongo
import urllib
from datetime import datetime

import preprocessor
import gaugedetector
import gaugeocr
import sys
import cv2

class App():
	def __init__(self):
        	self.stdin_path = '/dev/null'
        	self.stdout_path = '/dev/tty'
       		self.stderr_path = '/dev/tty'
        	self.pidfile_path =  '/home/aeye_grs/engine_grs/run/mydaemon.pid'
        	self.pidfile_timeout = 5
		self.password = urllib.quote_plus('gas1meter2iot')
    		self.client = MongoClient('mongodb://grsdatamanager:' + self.password + '@107.170.216.212')
		self.db = self.client.grsdata


    	def run(self):
        	while True:
			cursor = self.db.grstasks.find_one({'superviser' : '' },sort=[('importance',pymongo.DESCENDING),('inputdate', pymongo.ASCENDING)])
			if(cursor is not None):
				logger.debug(cursor)
				log = ('id : '+str(cursor['_id'])+' | filename :'+cursor['orgsourcefilename'])
				print(log) 
                                logger.info(log)
				#Update superviser
				self.db.grstasks.update({'_id' : cursor['_id']},{'$set' : {'superviser' : 'PID'}})
				self.db.grstasks.update({'_id' : cursor['_id']},{'$set' : {'starttime' : datetime.now()}})
				print(cursor['orgsourcepath']+cursor['orgsourcefilename'])
				filename = cursor['orgsourcefilename']
				path = cursor['orgsourcepath']
				opath = cursor['orgsourcepath']+'out_files/'
				#print(opath)
				image = cv2.imread(path+filename)
				if(image is not None):
			 		detector = gaugedetector.Gaugedetector(image,opath,'out_d_'+filename)
    					detected_image  = detector.gaugedetector()
					pre = preprocessor.Preprocessor(detected_image,opath,'out_p_'+filename)
    					preprocessed_image = pre.preprocessor()
    					ocr = gaugeocr.Gaugeocr(opath,'out_p_'+filename)
					gvalue =  ocr.startocr() 
					print ocr.startocr()
				#update data grstasks
				#insert grsrecorde
				self.insertgrsdata(cursor['userid'],cursor['gaugeid'],"",cursor['_id'],gvalue)

				print('end')
            		#logger.debug("Debug message")
            		#logger.info("Info message")
            		#logger.warn("Warning message")
            		#logger.error("Error message")
            		time.sleep(20)

	#def insertgrsrecord():
	#	self.db.
 	def insertgrsdata(self,userid,gaugeid,dauthkey,taskid,gvalue) :
        	#find userid
		#print(userid)
        	result = self.db.grsrecorde.find_one({"userid" : userid })
		print(result)
        	if( result is None):
            		result = self.db.grsrecorde.insert_one(
                	{
                    		"userid": userid,
                    		"gauge": [{
                            		"gaugeid": gaugeid,
                            		"dauthkey": dauthkey,
                            		"taskid": taskid,
                           	 	"inputdatefgvalue":  datetime.now(),
                            		"gvalue": gvalue
                        		}],
                	}
            		)
        	else:
           		result = self.updategrsdata(userid,gaugeid,dauthkey,taskid,gvalue)
        	return result

    	def updategrsdata(self,userid,gaugeid,dauthkey,taskid,gvalue):
		print(userid)
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
	

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/aeye_grs/engine_grs/run/log/mydaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()

