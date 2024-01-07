import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path


filename="codesAndBarcodes.db"
DEVMOD=True
if DEVMOD:
	if Path(filename).exists():
		Path(filename).unlink()
dbfile="sqlite:///"+str(filename)
print(dbfile)
#import sqlite3
#z=sqlite3.connect(filename)
#print(z)
ENGINE=create_engine(dbfile)
BASE=dbase()
#BASE.prepare(autoload_with=ENGINE)

class StartStop(BASE):
	__tablename__="StartStop"
	Start=Column(DateTime)
	Stop=Column(DateTime)
	Start_Location=Column(String)
	Stop_Location=Column(String)
	StartStopId=Column(Integer,primary_key=True)

	def __repr__(self):
		return f"StartStop(Start={self.start},Stop={self.stop},StartStopId={self.StartStopId},Start_Location={self.Start_Location},Stop_Location={self.Stop_Location})"
	def __init__(self,Start,Stop=None,Start_Location=None,Stop_Location=None,StartStopId=None):
		if StartStopId != None:
			self.StartStopId=StartStopId
		self.Start=Start
		if Stop != None:
			self.Stop=Stop
		if Stop_Location:
			self.Stop_Location=Stop_Location
		if Start_Location:
			self.Start_Location=Start_Location


class Entries(BASE):
	__tablename__="Entries"
	Code=Column(String)
	Barcode=Column(String)
	#not found in prompt requested by
	'''
	#name {entriesid}
	#name {entriesid} {new_value}
	
	#price {entriesid}
	#price {entriesid} {new_value}

	#note {entriesid}
	#note {entriesid} {new_value}
	
	#size {entriesid} 
	#size {entriesid} {new_value}
	'''
	Name=Column(String)
	Price=Column(String)
	Note=Column(String)
	Size=Column(String)
	
	CaseCount=Column(Integer)

	Shelf=Column(Integer)
	BackRoom=Column(Integer)
	Display_1=Column(Integer)
	Display_2=Column(Integer)
	Display_3=Column(Integer)
	Display_4=Column(Integer)
	Display_5=Column(Integer)
	Display_6=Column(Integer)
	InList=Column(Boolean)
	Stock_Total=Column(Integer)

	EntriesId=Column(Integer,primary_key=True)
	Timestamp=Column(Float)
	def __init__(self,Barcode,Code,Name='',InList=False,Price=0.0,Note='',Size='',CaseCount=0,BackRoom=0,Display_1=0,Display_2=0,Display_3=0,Display_4=0,Display_5=0,Display_6=0,Stock_Total=0,Timestamp=datetime.now().timestamp(),EntriesId=None):
		if EntriesId:
			self.EntriesId=EntriesId
		self.Barcode=Barcode
		self.Code=Code
		self.Name=Name
		self.Price=Price
		self.Note=Note
		self.Size=Size
		self.CaseCount=CaseCount
		self.BackRoom=BackRoom
		self.Display_1=Display_1
		self.Display_2=Display_2
		self.Display_3=Display_3
		self.Display_4=Display_4
		self.Display_5=Display_5
		self.Display_6=Display_6
		self.Stock_Total=Stock_Total
		self.Timestamp=Timestamp
		self.InList=InList

	def __repr__(self):
		return f"""Entries(
		Code={self.Code},
		Barcode={self.Barcode},
		Name={self.Name},
		EntriesId={self.EntriesId},
		Timestamp={self.Timestamp},
		Shelf={self.Shelf},
		BackRoom={self.BackRoom},
		Display={self.Display_1},
		Display={self.Display_2},
		Display={self.Display_3},
		Display={self.Display_4},
		Display={self.Display_5},
		Display={self.Display_6},
		Stock_Total={self.Stock_Total},
		InList={self.InList}
		)
		"""
StartStop.metadata.create_all(ENGINE)
Entries.metadata.create_all(ENGINE)
tables={
	'ss':StartStop,
	'Entries':Entries
}
class Main:
	def __init__(self,engine,tables,error_log):
		self.engine=engine
		self.tables=tables
		self.error_log=error_log
		self.modes={
		'1':{
		'cmds':['collect','1'],
		'exec':self.startCollectItemMode,
		'desc':'use to collect item data rapidly'
		},
		'2':{
		'cmds':['list','2'],
		'exec':self.startListMode,
		'desc':"use as a list maker",
		},
		'3':{
		'cmds':['quit','q','3','e'],
		'exec':lambda self=self:exit("User Quit!"),
		'desc':"exit program"
		},
		}
		self.modeString=''.join([f"{Fore.cyan}{self.modes[i]['cmds']} - {self.modes[i]['desc']}{Style.reset}\n" for i in self.modes])
		while True:
			self.currentMode=input(f"which mode do you want to use \n{self.modeString}: ").lower()
			for k in self.modes:
				if self.currentMode in self.modes[k]['cmds']:
					self.modes[k]['exec']()


	def unified(self,line):
		args=line.split(" ")
		#print(args)
		if len(args) > 1:
			if args[0] == "#remove":
				try:
					with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).delete()
						print(result)
						session.commit()
						session.flush()
				except Exeption as e:
					print(e)
				return True
			elif args[0] == '#name':
				with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
						if result:
							print(result.Name)
						else:
							print("Nothing by that EntriesId")			
				return True
			elif args[0] == '#code':
				with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
						if result:
							print(result.Code)
						else:
							print("Nothing by that EntriesId")			
				return True
			elif args[0] == '#barcode':
				with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
						if result:
							print(result.Barcode)
						else:
							print("Nothing by that EntriesId")			
				return True
			elif args[0] == '#note':
				with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
						if result:
							print(result.Note)
						else:
							print("Nothing by that EntriesId")			
				return True
			elif args[0] == '#price':
				with Session(self.engine) as session:
						result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
						if result:
							print(result.Price)
						else:
							print("Nothing by that EntriesId")			
				return True
			elif args[0] == '#shelf':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Shelf)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#backroom':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.BackRoom)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#inlist':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_1':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_1)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_2':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_2)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_3':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_3)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_4':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_4)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_5':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_5)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#display_6':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.Display_6)
							else:
								print("Nothing by that EntriesId")			
					return True
			elif args[0] == '#inlist':
					with Session(self.engine) as session:
							result=session.query(Entries).filter(Entries.EntriesId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print("Nothing by that EntriesId")			
					return True
		elif args[0] == "#list_all":
			with Session(self.engine) as session:
					result=session.query(Entries).all()
					for num,e in enumerate(result):
						print(num,e)
			return True		

		return False

	def startCollectItemMode(self):
		code=''
		barcode=''
		options=['q - quit - 1','2 - b - back','#skip','#?']
		while True:
			while True:
				fail=False
				barcode=input(f"Barcode{options}: ")
				if barcode.lower() in ['q','quit','1']:
					exit('user quit!')
				elif barcode in ['2','b','back']:
					return
				elif barcode.lower() in ['#skip',]:
					barcode='0'*11
					break
				elif barcode.lower() in ['#?']:
					self.help()
					break
				elif self.unified(barcode):
					return
				elif barcode == '':
					barcode='0'*11
					break
				else:					
					for num,test in enumerate([UPCA,EAN8,EAN13]):
						try:
							t=test(barcode)
							print(t)
							break
						except Exception as e:
							print(e)
							if num >= 3:
								fail=True
				print("break",fail)
				if fail:
					barcode='0'*11
					break
				else:
					break

			while True:
				fail=False
				code=input(f"Code{options}: ")
				if code.lower() in ['q','quit','1']:
					exit('user quit!')
				elif code in ['2','b','back']:
					return
				elif code.lower() in ['#skip',]:
					code='0'*8
					break
				elif code.lower() in ['#?']:
					self.help()
					break
				elif self.unified(code):
					return
				elif code == '':
					code='0'*8
					break
				else:
					fail=False
					for num,test in enumerate([Code39,]):
						try:
							t=test(code,add_checksum=False)
							break
						except Exception as e:
							print(e)
							if num >= 1:
								fail=True
					if fail:
						code='0'*8
						break
					else:
						break
			with Session(self.engine) as session:
				query=session.query(self.tables['Entries']).filter(or_(self.tables['Entries'].Barcode.icontains(barcode),self.tables['Entries'].Code.icontains(code)))
				results=query.all()
				if len(results) < 1:
					print(code)
					print(barcode)
					if (code != '0'*8 and barcode != '0'*11):
						entry=self.tables['Entries'](Barcode=barcode,Code=code)
						session.add(entry)
						session.commit()
						session.flush()
						session.refresh(entry)
						print(entry)
				else:
					for num,e in enumerate(results):
						print(f"{num}->{e}")
					while True:
						msg=input("Do you want to edit one? if so enter its entry number(or -1 to quit,-2 to go back): ")
						try:
							num=int(msg)
							if num == -1:
								exit("user quit!")
							elif num == -2:
								break
							else:
								print(results[num])
								self.editEntry(session,results[num])
								break
						except Exception as e:
							print(e)

	def editEntry(self,session,item):
		print(session,item)
		for column in item.__table__.columns:
			while True:
				try:
					if column.name not in ['Timestamp','EntriesId']:
						new_value=input(f"{column.name}->{getattr(item,column.name)}('n','s','d','q'): ")
						if new_value in ['s','n']:
							break
						elif new_value in ['d']:
							session.query(self.tables['Entries']).filter(self.tables['Entries'].EntriesId==item.EntriesId).delete()
							print(item,"Was Deleted!")
							return
						elif new_value in ['b']:
							return	
						elif new_value in ['q']:
							exit("user quit!")

						if isinstance(column.type,Float):
							new_value=float(new_value)
						elif isinstance(column.type,Integer):
							new_value=int(new_value)
						elif str(column.type) == "VARCHAR":
							pass
						elif isinstance(column.type,Boolean):
							if new_value.lower() in ['true','yes','1','y',]:
								setattr(item,column.name,1)
							else:
								setattr(item,column.name,0)
						if str(column.type) not in ['BOOLEAN',]:
							#exit(str((column.name,column.type,isinstance(column.type,Boolean))))
							setattr(item,column.name,new_value)
						session.commit()
					break
				except Exception as e:
					print(e)




	def startListMode(self):
		pass

	def help(self):
		msg="""
#desired tools
	DONE{
	#add barcode,code with EntriesId 
	#-- code and barcode are tested before insertion to ensure they are correct
	#-- force a while true if code or barcode is found in table prior to insertion
	#--- to ensure valid data is stored
	}
	#if code/barcode is in db already print to screen and increment qty field
	'commands are prefixed with '#'
	#list all barcodes/codes
	#remove {EntriesId} -> barcode by EntriesId
	#edit a barcode,code pair by EntriesId
	#have colored display
	#edit_start
	#edit_stop
	#save
	#save_csv
	#quit 
	#factor_reset -- clear db of all items and startstop of entries
	#reset-ss -- reset start/stop
	#set-ss -- prompt for start stop (will reset start and stop times by prompt) 
	#search {fieldname}
		#prompts for data to search by in {fieldname}
		#searches entries for "like %{fieldname}%" and displays them with their entriesID
	#help,#? -- displays info found here, or help page
	#locater {code}
		#a prompt then shows where the user then inputs/scans barcodes until the entry for the 
		#first code is scanned again, either by the first product, or a shelf label containing 
		#the upc or the item_code for the item
		#if multiple entries
			#display entries and leave locator mode
		#if single entry is found dislay in bright bold text and leave locator mode

		#if scanned code does not match the first entry, then display nothing and wait for next scan

	#on start prompt for list mode or item mode
		#item mode use as is

		#list mode will:
		#--iterate through entries
		# set to zero
		#  display_x/stock_total/backroom/shelf
		#  listitem will be set to false
		#entry prompt for codes/barcodes shows
		#each scan will check and set to to true listitem
		#when '#summary' is entered all items in with listitem=True will be displayed

	#not found in prompt requested by
	'''
	#name {entriesid}
	#name {entriesid} {new_value}
	
	#price {entriesid}
	#price {entriesid} {new_value}

	#note {entriesid}
	#note {entriesid} {new_value}
	
	#size {entriesid} 
	#size {entriesid} {new_value}

	#Shelf {entriesid}
	#Shelf {entriesid} {new_value}

	#BackRoom {entriesid}
	#BackRoom {entriesid} {new_value}

	#Display {entriesid}
	#Display {entriesid} {new_value}
	

	###only for scanned barcodes/codes as scanned base inventory###
	if +/-{num} at barcode/code input use as qty value:
		set qty to qty+({+/-num})
	else:
	#Qty {entriesid}
	#Qty {entriesid} {new_value}
	{barcode}/{code} adds 1 to found entry

	#Stock_Total {entriesid} -- calculates from above entries and updates value automatically

	'''"""
		print(msg)
		return msg


if __name__ == "__main__":
	Main(engine=ENGINE,tables=tables,error_log=Path("error_log.log"))