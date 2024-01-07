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

	Stock_Total=Column(Integer)

	EntriesId=Column(Integer,primary_key=True)
	Timestamp=Column(Float)
	def __repr__(self):
		return f"""Entries(
		Code={self.code},
		Barcode={self.barcode},
		EntriesId={self.EntriesId},
		Timestamp={self.timestamp}),
		Shelf={self.Shelf},
		BackRoom={self.BackRoom},
		Display={self.Display_1},
		Display={self.Display_2},
		Display={self.Display_3},
		Display={self.Display_4},
		Display={self.Display_5},
		Display={self.Display_6},
		Stock_Total={self.Stock_Total},
		"""
StartStop.metadata.create_all(ENGINE)
Entries.metadata.create_all(ENGINE)

#desired tools
	#add barcode,code with EntriesId 
	#-- code and barcode are tested before insertion to ensure they are correct
	#-- force a while true if code or barcode is found in table prior to insertion
	#--- to ensure valid data is stored
	#if code/barcode is in db already print to screen and increment qty field
	"""'commands are prefixed with '#'"""
	#list all barcodes/codes
	#remove barcode by EntriesId
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

	'''
