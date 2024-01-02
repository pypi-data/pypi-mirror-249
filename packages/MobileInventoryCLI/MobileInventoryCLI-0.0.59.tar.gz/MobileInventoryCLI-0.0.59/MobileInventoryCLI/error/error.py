import csv,json
from datetime import datetime as DT
from datetime import datetime as TD
from datetime import datetime

def writeError(e,error_log):
	print(e)
	with error_log.open("a") as log:
		writer=csv.writer(log,delimiter=";")
		writer.writerow([str(e),])
		writer.writerow([repr(e),])
		
def obj2dict(obj):
	d={}
	for col in obj.__table__.columns:
		d[col.name]=getattr(obj,col.name)
	return d

def getConfig(self,key=None):
		with self.config.open("r") as cfgfile:
			config=json.load(cfgfile)
			if key:
				return config.get(key)
			else:
				return config

def date2Ticks(year=1,month=1,day=1):
		diff=datetime(year,month,day)-datetime(1,1,1)
		d=(diff.days*8.64e+10)+(diff.seconds*1000000)+diff.microseconds
		d=d*10
		return d

def ticks2Date(ticks):
	return DT(1,1,1)+TD(microseconds=ticks/10)