#summarize_list.py
import os,json,base64,string
from MobileInventoryCLI.error.error import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from colored import Fore,Back,Style
from datetime import datetime

class SummarizeList:
	def __str__(self):
		return "SummarizeList (Better for ScreenShots)"


	def listById(self):
		while True:
			try:
				listid_user=input("ListId/q/b: ")
				if listid_user.lower() in ['q','quit']:
					exit("user quit!")
				elif listid_user.lower() in ['b','back']:
					break
				else:
					listid_user=int(round(float(listid_user),0))
					with Session(self.engine) as session:
						ListName=session.query(self.tbl.List.Title).filter(self.tbl.List.ListId==listid_user).first()
						if ListName:
							query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid_user)
							items=query.all()
							h="{startn}Na{end}{startnn}me{end}|{startq}Qty{end}|{startb}bCode{end}|{starts}SKU{end}|{startp}iPrice{end}|{start}i/Ttl{end}".format(startp=Fore.GREY_35,starts=Fore.gold_1,startb=Fore.green_yellow,startn=Fore.cyan,startnn=Fore.light_green,startq=Fore.ORANGE_RED_1,start=Fore.GREY_93,end=Style.reset)
							br=str('-'*20)
							print(br)
							print(ListName.Title)
							print(br)
							
							print(h)
							print(br)
							end=Fore.GREY_93+'{}/{}'+Style.reset
							total_cost=0
							total_pcs=0
							for num,r in enumerate(items):
								line=[]
								if num % 2 == 0:
									line.append(Fore.cyan+r.ItemName+Style.reset)
								else:
									line.append(Fore.light_green+r.ItemName+Style.reset)

								line.append(Fore.ORANGE_RED_1+str(r.Quantity)+Style.reset)
								line.append(Fore.green_yellow+str(r.ItemBarcode)+Style.reset)
								line.append(Fore.gold_1+str(r.ItemCode)+Style.reset)
								line.append(Fore.GREY_35+str(r.ItemPrice)+Style.reset)
								line.append(end.format(str(num+1),str(len(items))))
								print('|'.join(line))
								total_cost+=(r.Quantity*r.ItemPrice)
								total_pcs+=r.Quantity
							print("Total Price($): {s}{v}{e}".format(s=Fore.red,v=total_cost,e=Style.reset))
							print("Total PCS: {s}{v}{e}".format(s=Fore.red,v=total_pcs,e=Style.reset))
							print(br)
							
						else:
							raise Exception("No Such List! {}".format(listid))
				break
			except Exception as e:
				writeError(e,self.error_log)

	def searchAndSelect(self):
		menu=["Search and Select Menu",]
		

	def __init__(self,engine,config,tbl,error_log):
		self.error_log=error_log
		self.tbl=tbl
		self.config=config
		self.engine=engine

		self.cfg=getConfig(self)
		cmdlist={
		'1':{
			'names':['1','quit','q','exit'],
			'exec':lambda :exit("user quit")
			},
		'2':{
			'names':['2','back','b','prev'],
			'exec':False,
			},
		'3':{
			'names':['ListById','lbid','3'],
			'exec':lambda self=self:self.listById(),
			},
		'4':{
			'names':['searchselect','ss','4','search-select'],
			'exec':lambda self=self:self.searchAndSelect(),
			}
		}
		while True:
			for k in cmdlist:
				print(k,cmdlist[k]['names'])
			cmd=input("Do what? ")
			for k in cmdlist:
				if cmd.lower() in cmdlist[k]['names']:
					if k == '2':
						return
					else:
						cmdlist[k]['exec']()

