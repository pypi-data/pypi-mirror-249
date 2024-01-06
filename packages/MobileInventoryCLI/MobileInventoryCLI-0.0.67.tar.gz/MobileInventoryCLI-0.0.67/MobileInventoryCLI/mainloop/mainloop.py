#import made modules

from MobileInventoryCLI.lookup import lookup
from MobileInventoryCLI.error.error import writeError
from MobileInventoryCLI.updateCfg import updateCfg
from MobileInventoryCLI.lists import lists
from MobileInventoryCLI.SummarizeList import summarize_list
from MobileInventoryCLI.ExtractPkg import ExtractPkg

class MainLoop:
	#interactive modules go here
	#use def __str__ to define command name
	Modules=[
	[updateCfg.UpdateConfig,'0'],
	[updateCfg.Quit,'1'],
	[updateCfg.StorageConfig,'2'],
	[updateCfg.ListConfig,'3'],
	[lookup.Search,'4'],
	[lists.SelectList,'5'],
	[summarize_list.SummarizeList,'6'],
 [ExtractPkg.ExtractPkg,'7']
	]
	def __init__(self,engine,config,error_log,tbl):
		self.engine=engine
		self.config=config
		self.error_log=error_log
		self.tbl=tbl
		if error_log.exists():
			with error_log.open('w+') as log:
				log.write('')
		while True:
			msg='\n'.join([i.__str__(None)+" -> {}".format(k) for i,k in self.Modules if not isinstance(i,str)])
			cmd=input('-'*10+'\n{}\n__________\nwhat do you want to do: '.format(msg))
			if isinstance(cmd,str) and cmd.lower() == "quit" or cmd == "1":
				updateCfg.Quit(config=config,engine=engine,error_log=error_log,tbl=tbl)
			else:
				try:
					if cmd.lower() == 'updateconfig' or cmd == '0':
						updateCfg.UpdateConfig(config,error_log,tbl)
					elif cmd.lower()=="storageconfig" or cmd == '2':
						updateCfg.StorageConfig(tbl=tbl,config=config,error_log=error_log,engine=engine)
					elif cmd.lower()=="listconfig" or cmd == "3":
						updateCfg.ListConfig(tbl=tbl,config=config,error_log=error_log,engine=engine)	
					elif cmd.lower()=="lookupcode" or cmd == "4":
						lookup.Search(tbl=tbl,config=config,error_log=error_log,engine=engine)
					elif cmd.lower()=="selectlist" or cmd == "5":
						lists.SelectList(tbl=tbl,config=config,error_log=error_log,engine=engine)
					elif cmd.lower()=="summarizelist" or cmd == "6":
						summarize_list.SummarizeList(tbl=tbl,config=config,error_log=error_log,engine=engine)
					elif cmd.lower()=="extractpkg" or cmd == "7":
						ExtractPkg.ExtractPkg(tbl=tbl,config=config,error_log=error_log,engine=engine)
				except Exception as e:
					writeError(e,self.error_log)