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
			if(cursor != None):
				logger.debug(cursor)
                                logger.info(cursor['orgsourcefilename'])
				print(cursor['orgsourcefilename'])
				#Update superviser
				self.db.grstasks.update({'_id' : cursor['_id']},{'$set' : {'superviser' : 'PID'}})
				self.db.grstasks.update({'_id' : cursor['_id']},{'$set' : {'starttime' : datetime.now()}})
				print(cursor['orgsourcepath']+fcursor['orgsourcefilename'])
   				image = cv2.imread(cursor['orgsourcepath']+fcursor['orgsourcefilename'])
				opath = cursor['orgsourcepath']+'/out_file/'
    				detector = gaugedetector.Gaugedetector(image,opath,'out_d_'+fileName)
    				detected_image  = detector.gaugedetector()
            		#logger.debug("Debug message")
            		#logger.info("Info message")
            		#logger.warn("Warning message")
            		#logger.error("Error message")
            		time.sleep(100)

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

