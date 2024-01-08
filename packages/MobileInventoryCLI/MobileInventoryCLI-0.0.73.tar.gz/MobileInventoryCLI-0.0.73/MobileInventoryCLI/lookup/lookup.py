from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from colored import Fore,Back,Style
from datetime import datetime

class Search:
	def __str__(self):
		return "LookupCode"
	def seeCustomFields(self,result,config,engine,error_log,tbl):
		if not result:
			raise Exception('result is "{}":{}'.format(result,type(result)))
		else:
			with Session(engine) as session:
				print("___CustomFields___")
				query=session.query(tbl.ItemCustomField)
				result=query.filter(tbl.ItemCustomField.ItemId==result.ItemId).all()
				for num,r in enumerate(result):
					print(fg('green')+'++++ICF {}:{}++++'.format(num,r.CustomFieldId)+attr(0))
					name,typeNo,typeStr='',0,'Text'
					q=session.query(tbl.CustomField)
					q=q.filter(tbl.CustomField.CustomFieldId==r.CustomFieldId)
					qr=q.first()
					name,typeNo=qr.Name,qr.Type
					if typeNo == 0:
						typeStr='Text'
					elif typeNo == 1:
						typeStr='Numbers'
					elif typeNo == 2:
						typeStr='Date'
					print(fg('RED')+'Name:'+attr(0),name)
					print(fg('DARK_ORANGE')+'\tType: '+attr(0),typeStr)
					for column in r.__table__.columns:
						if column.name in ['Value']:
							print(fg('RED')+column.name+attr(0),getattr(r,column.name),sep=" -> : ")
						else:
							print(fg('DARK_ORANGE')+column.name+attr(0),getattr(r,column.name),sep=" -> : ")
					
					print(fg('green')+'++++ICF {}:{}++++'.format(num,r.CustomFieldId)+attr(0))
				print("___CustomFields___")
		#lookup item result custom fields
	def __init__(self,config,engine,error_log,tbl):
		self.tbl=tbl
		self.engine=engine
		self.error_log=error_log
		self.config=config
		with config.open('r') as d:
			self.cfg=json.load(d)
		self.cmds={
			'1':'lookup by itemCode',
			'2':'lookup by Barcode',
			'3':'lookup by ItemId',
			'4':'lookup by barcode|itemcode|itemid',
			'5':'edit item by itemCode',
			'6':'edit item by Barcode',
			'7':'edit item byItemId',
			'8':'quit',
			's|S|9':'Search',
			'quit':'quit',
			'q':'quit',
			'back':'go back a menu',
		}
		msg='\n'.join(['{}->{}'.format(i,self.cmds[i]) for i in self.cmds.keys()])
		while True:
			print(msg)
			cmd=input('{}\n----------\nwhat do you want to do? '.format(msg))
			if cmd.lower() in ('q','quit','8'):
				exit('user quit!')
			elif cmd.lower() == "back":
				break
			else:
				if cmd  == '1':
					while True:
						itemcode=input('itemcode[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								result=result.filter(tbl.Item.StorageId==self.cfg.get('storageId'))
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								result=result.filter(tbl.Item.Code==itemcode)
								results=result.all()
								self.processResults(results)
				elif cmd  == '2':
					while True:
						itemcode=input('barcode[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")

						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								result=result.filter(tbl.Item.StorageId==self.cfg.get('storageId'))
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								result=result.filter(tbl.Item.Barcode==itemcode)
								results=result.all()
								self.processResults(results)
				elif cmd  == '3':
					while True:
						itemcode=input('ItemId[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								result=result.filter(tbl.Item.StorageId==self.cfg.get('storageId'))
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								result=result.filter(tbl.Item.ItemId==itemcode)
								results=result.all()
								self.processResults(results)
				elif cmd  == '4':
					while True:
						itemcode=input('ItemId|Barcode|ItemCode[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")

						'''
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
						'''
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								#if self.cfg.get('storageid'):
								#print(self.cfg.get('storageId'))
								result=result.filter(tbl.Item.StorageId==self.cfg.get('storageId'))
								#if t == "like":
								result=result.filter(or_(tbl.Item.ItemId.icontains(itemcode),tbl.Item.Code.icontains(itemcode),tbl.Item.Barcode.icontains(itemcode)))
								#else:
								#	result=result.filter(or_(tbl.Item.ItemId==itemcode,tbl.Item.Code==itemcode,tbl.Item.Barcode==itemcode))
								results=result.all()
								self.processResults(results)
				elif cmd.lower()  == 's' or cmd == '9':
					while True:
						itemcode=input('Name Search[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								if t == "like":
									result=result.filter(tbl.Item.Name.icontains(itemcode))
								else:
									result=result.filter(tbl.Item.Name==itemcode)
								results=result.all()
								self.processResults(results)
				elif cmd == '5':
					while True:
						itemcode=input('Item Code[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								if t == "like":
									result=result.filter(tbl.Item.Code.icontains(itemcode))
								else:
									result=result.filter(tbl.Item.Code==itemcode)
								self.processResultsEdit(result,tbl,session)
				elif cmd == '6':
					while True:
						itemcode=input('Barcode[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								if t == "like":
									result=result.filter(tbl.Item.Barcode.icontains(itemcode))
								else:
									result=result.filter(tbl.Item.Barcode==itemcode)
								self.processResultsEdit(result,tbl,session)
				elif cmd == '7':
					while True:
						itemcode=input('ItemId[or #back,#quit]: ')
						if itemcode == '#back':
							break
						if itemcode == '#quit':
							exit("user quit!")
						t=input('==/like: ')
						while t not in ['==','like','#back']:
							t=input('==/like: ')
							
						if itemcode.lower() == '#back':
							break
						else:
							with Session(engine) as session:
								result=session.query(tbl.Item)
								if self.cfg.get('storageid'):
									result=result.filter(tbl.Item.StorageId==self.cfg.get('storageid'))
								if t == "like":
									result=result.filter(tbl.Item.ItemId.icontains(itemcode))
								else:
									result=result.filter(tbl.Item.ItemId==itemcode)
								self.processResultsEdit(result,tbl,session)

	def processStorageId(self,data_itemNum,session,tbl):
		storages=session.query(tbl.Storage).all()
		if len(storages) < 1:
			print("there are no storages available!")
			return
		else:
			data={}
			for num,s in enumerate(storages):
				data[num]=s
				print(num,obj2dict(data[num]))
			while True:
				value=input("Which Storage Id?[value/quit(q/Q)/back(b/B)]: ")
				if value.lower() in ['quit','q']:
					exit("user quit")
				elif value.lower() in ['back','b']:
					print(value)
					break
				else:
					try:
						print(value)
						value=int(value)
						setattr(data_itemNum,'StorageId',value)
						session.commit()
						break
					except Exception as e:
						print(e)
	def processCategoryId(self,data_itemNum,session,tbl):
		storages=session.query(tbl.Category).all()
		if len(storages) < 1:
			print("there are no Categories available!")
			return
		else:
			data={}
			for num,s in enumerate(storages):
				data[num]=s
				print(num,obj2dict(data[num]))
			while True:
				value=input("Which CategoryId?[value/quit(q/Q)/back(b/B)]: ")
				if value.lower() in ['quit','q']:
					exit("user quit")
				elif value.lower() in ['back','b']:
					print(value)
					break
				else:
					try:
						print(value)
						value=int(value)
						setattr(data_itemNum,'CategoryId',value)
						session.commit()
						break
					except Exception as e:
						print(e)		
	def processTags(self,data_itemNum,session,tbl):
		storages=session.query(tbl.Tag).all()
		if len(storages) < 1:
			print("there are no tags available!")
			return
		else:
			data={}
			for num,s in enumerate(storages):
				data[num]=s
				print(num,obj2dict(data[num]))
			while True:
				build=data_itemNum.Tags.split(",")
				doWhat=input("do what? [+|-|done]?")
				if doWhat == "done":
					break
				value=input("Which TagId?[value/quit(q/Q)/back(b/B)]: ")
				if value.lower() in ['quit','q']:
					exit("user quit")
				elif value.lower() in ['back','b']:
					print(value)
					break
				else:
					try:
						print(value)
						found=False
						if doWhat == '+':
							value=int(value)
							for s in storages:
								if value == s.TagId:
									found=True
									build.append(s.Name)
						elif doWhat == "-":
							found=False
							value=int(value)
							for s in storages:
								if value == s.TagId:
									found=True
									if s.Name in build:
										build.pop(build.index(s.Name))
					except Exception as e:
						print(e)
							
						
				setattr(data_itemNum,'Tags',",".join(build))
				session.commit()
					

	def processMeasurementUnit(self,data_itemNum,session,tbl):
		storages=session.query(tbl.MeasurementUnit).all()
		if len(storages) < 1:
			print("there are no MeasurementUnit's available!")
			return
		else:
			data={}
			for num,s in enumerate(storages):
				data[num]=s
				print(num,obj2dict(data[num]))
			while True:
				value=input("Which MeasurementUnit Name?[value/quit(q/Q)/back(b/B)]: ")
				if value.lower() in ['quit','q']:
					exit("user quit")
				elif value.lower() in ['back','b']:
					print(value)
					break
				else:
					try:
						print(value)
						value=str(value)
						fail=True
						for s in storages:
							if value == s.Name:
								fail=False
								break
						if not fail:
							setattr(data_itemNum,'MeasurementUnit',value)
						else:
							raise Exception("Invalid MeasurementUnit!")
						session.commit()
						break
					except Exception as e:
						print(e)

	def processResultsEdit(self,result,tbl,session):
		results=result.all()
		data={}
		for num,i in enumerate(results):
			data[num]=i
			print(num,obj2dict(i),sep="->")
		if data != {}:
			msg="which item do you want to edit[value/quit/back]?: "
			itemNum=0
			while True:
				try:
					m=input(msg)
					if m.lower() == 'quit':
						exit("user quit!")
					if m.lower() == "back":
						break
					itemNum=int(m)
					if itemNum == -1:
						break
					for field in data[itemNum].__table__.columns:
						d=getattr(data[itemNum],field.name)
						x="Edit {field}[{fieldData}]({type}) [y/n/quit/back]: ".format(field=field.name,fieldData=d,type=field.type)
						edit_field=input(x)
						while True:
							if edit_field.lower() in ['y','n','quit','back']:
								if edit_field.lower() == 'quit':
									exit("user quit!")
								elif edit_field.lower() == "back":
									break
								elif edit_field.lower() == "y":
									if field.name in ['StorageId','CategoryId','Tags','MeasurementUnit']:
										if field.name == 'StorageId':
											self.processStorageId(data[itemNum],session,tbl)
										elif field.name == "CategoryId":
											self.processCategoryId(data[itemNum],session,tbl)
										elif field.name == "Tags":
											self.processTags(data[itemNum],session,tbl)
										elif field.name == "MeasurementUnit":
											self.processMeasurementUnit(data[itemNum],session,tbl)
										else:
											raise Exception(field.name)
										break
									else:
										new_value=input("new value #quit#/#back#: ")
										if new_value in ['#quit#','#back#']:
											if new_value == '#quit#':
												exit("user quit")
											else:
												break
										if field.type == "INTEGER":
											new_value=int(new_value)
										elif field.type == "FLOAT":
											new_value=float(new_value)
										else:
											new_value=str(new_value)
										setattr(data[itemNum],field.name,new_value)
										session.commit()
										session.flush()
										session.refresh(data[itemNum])
										print(obj2dict(data[itemNum]),"refreshed!",sep="\n")
									
								elif edit_field.lower() == "n":
									break
							else:
								edit_field=input(x)
					customfields=session.query(tbl.ItemCustomField)
					customfields=customfields.filter(tbl.ItemCustomField.ItemId==data[itemNum].ItemId)
					customfields=customfields.all()
					if len(customfields) < 1:
						print("no customfields available for item!")
						while True:
							answer=input("add a CustomField to this Item?[Y/n]: ")
							if answer.lower() == "n":
								break
							else:
								fields=session.query(tbl.CustomField)
								fields=fields.filter(tbl.CustomField.CustomFieldFor==0).all()
								if len(fields) < 1:
									print("in development... no custom fields available")
								else:
									dataCF={}
									for num,cf in enumerate(fields):
										print(num,cf.Name,cf.Type)
										dataCF[num]=cf
										add=input("add item?[Y/n/done]: ")
										if add.lower() == "n":
											pass
										elif add.lower() == "done":
											break
										else:
											#here1
											nicf=tbl.ItemCustomField()
											setattr(nicf,"ItemId",data[itemNum].ItemId)
											setattr(nicf,"CustomFieldId",dataCF[num].CustomFieldId)
											if cf.Type == 0:
												while True:
													value=input("Value: ")
													if value.lower() == "quit":
														exit("user quit")
													if value.lower() == "back":
														break
													setattr(nicf,"Value",value)
											elif cf.Type == 1:
												while True:
													value=input("Value: ")
													if value.lower() == "quit":
														exit("user quit")
													if value.lower() == "back":
														break
													try:
														value=float(value)
														if value.is_integer():
															value=int(value)

														setattr(nicf,"Value",str(value))
													except Exception as e:
														print(e)
											elif cf.Type == 2:
												while True:
													value=input("Value: ")
													if value.lower() == "quit":
														exit("user quit")
													if value.lower() == "back":
														break
													try:
														d=datetime.strptime(value,"%m/%d/%Y")
														print(d.ctime())
														setattr(nicf,"Value",str(value))
														break
													except Exception as e:
														print(e)
											try:
												session.add(nicf)
												session.commit()
											except Exception as e:
												print(e)

					else:
						for cf in customfields:
							index=["Text","Numbers","Date"]
							attrs=session.query(tbl.CustomField).filter(tbl.CustomField.CustomFieldId==cf.CustomFieldId).first()
							
							edit=input("{}({})={} [y/n/back/quit/delete]: ".format(attrs.Name,index[attrs.Type],cf.Value))
							if edit.lower() == "delete":
								a=session.query(tbl.ItemCustomField).filter(tbl.ItemCustomField.ItemCustomFieldId==cf.ItemCustomFieldId).delete()
								session.commit()
								print(a)
								
							elif edit == "y":
								while True:
									new_value=input("new value[value/#back#/#quit#]? ")
									if new_value == "#quit#":
										exit("user quit!")
									elif new_value == "#back#":
										break
									else:
										if attrs.Type == 1:
											try:
												new_value=float(new_value)
												if new_value.is_integer():
													new_value=int(new_value)
												new_value=str(new_value)
											except Exception as e:
												print(e)
										elif attrs.Type == 2:
											print("working on that")
											try:
												dt=datetime.strptime(new_value,"%m/%d/%Y")
												print(dt.ctime(),"confirms!")
											except Exception as e:
												print(e)
											#new_value=float(new_value)
										elif attrs.Type == 0:
											new_value=str(new_value)
										setattr(cf,"Value",new_value)
										session.commit()
										session.flush()
										session.refresh(cf)
										print("refreshed customfield!")
										break
							else:
								break
								
					break
				except Exception as e:
					print(e)
			
		else:
			print("zero results!")
		#self.processResults(results)
	def processResults(self,results):
		for num,r in enumerate(results):
			print(fg('blue')+'---Item ({})---'.format(num)+attr(0))
			o=obj2dict(r)
			for k in o.keys():
				print(fg('RED')+k+attr(0),':',fg("dark_orange")+str(o[k])+attr(0))
			self.seeCustomFields(r,self.config,self.engine,self.error_log,self.tbl)
			print('===Item ({})==='.format(num))
