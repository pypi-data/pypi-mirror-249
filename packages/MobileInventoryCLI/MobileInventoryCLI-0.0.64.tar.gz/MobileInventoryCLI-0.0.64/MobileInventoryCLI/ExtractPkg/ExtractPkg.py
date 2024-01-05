import tempfile
from pathlib import Path
import shutil
from copy import deepcopy
import json,os,base64,time
from datetime import datetime
from MobileInventoryCLI.error.error import *
from MobileInventoryCLI.updateCfg.updateCfg import UpdateConfig
import zipfile
from colored import Fore,Back,Style

class ExtractPkg:
	def __str__(self):
		return "ExtractPkg and Update Config"

	def __init__(self,tbl,config,error_log,engine):
		self.tbl=tbl
		self.config=config
		self.cfg=getConfig(self)
		self.error_log=error_log
		self.engine=engine

		while True:
			try:
				path2bck=input("MobileInventoryCLI-BCK Path[filepath+filename/q/b/c(clr sys db)]: ")
				if path2bck in ['q','quit']:
					exit("user quit!")
				elif path2bck in ['b','back']:
					return
				elif path2bck in ['c','clear_system_db','clr_sys_db','clr','csd']:
					shutil.rmtree(str(Path("./system.db").absolute()))
					try:
						UpdateConfig.updateByKey(self,'dbfile',"",self.config,self.engine,self.error_log,self.tbl)
					except Exception as e:
						writeError(e,self.error_log)
				else:
					path2bck=Path(path2bck)
					if path2bck.exists():
						with zipfile.ZipFile(path2bck,"r") as zip:
							#tmpdir=Path(tempfile.mkdtemp())
							for file in zip.namelist():
								if Path(file).suffix == ".db3":
									zip.extract(file,path=str(Path("./system.db").absolute()))
									UpdateConfig.updateByKey(self,'dbfile',str(Path("./system.db").absolute()/Path(file)),self.config,self.engine,self.error_log,self.tbl)
								else:
									zip.extract(file,path=str(Path("./system.db").absolute()))
								print("Extracting {s1}{v}{e} to {s2}{vv}{e}".format(v=file,vv=str(Path("./system.db").absolute()),e=Style.reset,s1=Fore.light_green,s2=Fore.red))
			except Exception as e:
				writeError(e,self.error_log)