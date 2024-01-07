from MobileInventoryCLI.error.error import *
from barcode import Code128,Code39,EAN13,EAN8,UPCA
from barcode.writer import ImageWriter
import zipfile
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from colored import Fore,Back,Style
import shutil
from datetime import datetime,timedelta
from copy import deepcopy
import pandas as pd
import plyer,platform
import tempfile

class CustomFields:
    def __str__(self):
        return 'CustomFields/cf/0/customfields'
    def __init__(self,engine,config,tbl,error_log,objdict):
        self.engine=engine
        self.config=config
        self.error_log=error_log
        self.objdict=objdict
        self.tbl=self.tbl
        self.cfg=getConfig(self)
        print("In Dev RN!")


class DeleteList:
    def __str__(self):
        return "deletelist/del/delete/4/d"

    def __init__(self,config,engine,tbl,error_log):
        self.tbl=tbl
        self.error_log=error_log
        self.config=config
        self.engine=engine
        self.cfg=getConfig(self)
        self.promptForAction()

    def displayListItemMenu(self):
        msg="""
        {row1}Soft Delete [D/SD/1/soft_del]{end}
        {row0}Forever Delete[FD/forever_del/to_inf_&_begone/HD/hard_del/2]{end}
        {row1}Quit [Quit/Q/q/quit/3]{end}
        {row0}Back [Back/B/b/back/4]{end}
        {row1}Undel [ud/undelete]{end}
        Which would you like to do? : 
        """
        msg=msg.format(row0=fg("red"),row1=fg("green"),end=attr(0))
        print(msg)
        return msg

    def checkList(self,listid):
        with Session(self.engine) as session:
            try:
                listExists=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                if listExists:
                    return True
                else:
                    return False

            except Exception as e:
                writeError(e,self.error_log)

    def promptForAction(self):
        
        listid=None
        listTitle=None
        while True:
            try:
                listid=input("listid/#q/#b: ")
                if listid.lower() in ["#q","#quit"]:
                    exit("user quit!")
                elif listid.lower() in ["#b","#back"]:
                    break
                listid=int(listid)
                if self.checkList(listid):
                    
                    self.displayListItemMenu()
                    action=input("what would you like to do?: ")
                    if action.lower() in ['fd','forever_del','to_inf_&_begone','hd','hard_del','2']:
                        with Session(self.engine) as session:
                            listitems=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
                            for item in listitems:
                                cfs=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ListItemId==item.ListItemId).delete()
                                print(cfs,"cfs deleted!")
                            listitems=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).delete()
                            print(listitems,"ListItems Deleted!")
                            
                            listCFs=session.query(self.tbl.ListCustomField).filter(self.tbl.ListCustomField.ListId==listid).delete()
                            print(listCFs,"List CFS Deleted!")
                            list_=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                            name=deepcopy(str(list_.Title))
                            ID=deepcopy(int(list_.ListId))
                            print("List {name}:{id} Deleted!".format(name=name,id=ID))
                            list_=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).delete()

                            session.commit()
                    elif action.lower() in ['sd','d','soft_del','1']:
                        with Session(self.engine) as session:
                            list_=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                            list_.IsDeleted=1
                            
                            session.commit()
                            session.flush()
                            session.refresh(list_)
                            print(obj2dict(list_))

                    elif action.lower() in ['quit','q','3']:
                        exit("user quit!")
                    elif action.lower() in ['back','b','4']:
                        break
                    elif action.lower() in ['ud','undel','unrm','lazarus']:
                        with Session(self.engine) as session:
                            list_=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                            list_.IsDeleted=0
                            
                            session.commit()
                            session.flush()
                            session.refresh(list_)
                            print(obj2dict(list_))
                else:
                    print("that list does not exist!")
            except Exception as e:
                writeError(e,self.error_log)


class NewList:
    def __str__(self):
        return "NewList/N/New/7/NL"

    def __init__(self,config,engine,tbl,error_log):
        self.tbl=tbl
        self.error_log=error_log
        self.config=config
        self.engine=engine
        self.cfg=getConfig(self)
        self.promptForAction()

    def displayListItemMenu(self,dsp=True):
        msg="""
        {row1}New [n/nl/newlist/new_list/1]{end}
        {row1}Quit [Quit/Q/q/quit/3]{end}
        {row0}Back [Back/B/b/back/4]{end}
        Which would you like to do? : 
        """
        msg=msg.format(row0=fg("red"),row1=fg("green"),end=attr(0))
        if dsp:
            print(msg)
        return msg

    def checkList(self,listid):
        with Session(self.engine) as session:
            try:
                listExists=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                if listExists:
                    return True
                else:
                    return False

            except Exception as e:
                writeError(e,self.error_log)

    def makeNewList(self):
        with Session(self.engine) as session:
            new_list=self.tbl.List()
            for k in new_list.__table__.columns:
                if k.name not in ['ListId',]:
                    while True:
                        '''
                        cmd="{name}:{type} |[value/#q/#b=#n/#quit/#back=#next]: ".format(name=k.name,type=k.type)
                        new_value=input(cmd)
                        if new_value in ['#back','#b','#n','#next']:
                            break
                        elif new_value in ['#q','#quit']:
                            exit("user quit!")
                            #print(k.type,k.name,new_value)
                        '''
                        if str(k.type) == "VARCHAR":
                            cmd="{name}:{type} |[value/#q/#b=#n/#quit/#back=#next]: ".format(name=k.name,type=k.type)
                            new_value=input(cmd)
                            if new_value in ['#back','#b','#n','#next']:
                                break
                            elif new_value in ['#q','#quit']:
                                exit("user quit!")
                            setattr(new_list,k.name,new_value)
                            break
                        elif str(k.type) == 'BIGINT' and k.name == 'Date':
                            now=datetime.now()
                            today=date2Ticks(month=now.month,day=now.day,year=now.year)
                            print(today)
                            setattr(new_list,k.name,today)
                        elif str(k.type) == "INTEGER" and k.name == 'UserId':
                            with Session(self.engine) as session:
                                d={}
                                users=session.query(self.tbl.User).all()
                                for num,user in enumerate(users):
                                    d[num]=user
                                    print(num,obj2dict(user))
                                m="Which user [num/q/b/quit/back]: "
                                which=input(m)
                                if which in ['q','quit']:
                                    exit("user quit!")
                                elif which in ['b','back']:
                                    break
                                else:
                                    try:
                                        if which in ['-1','0']:
                                            break
                                        value=int(which)
                                        setattr(new_list,'UserId',d[value].UserId)
                                    except Exception as e:
                                        writeError(e,self.error_log)
                        elif str(k.type) == "INTEGER" and k.name == 'StockChange':
                            d={
                            'Incomming':0,
                            'Outgoing':1,
                            'set':2,
                            'noChange':3
                            }
                            
                            for num,user in enumerate(d.keys()):
                                print(num,str(user))
                            m="Which one[num/q/b/quit/back]?: "
                            which=input(m)
                            if which in ['q','quit']:
                                exit("user quit!")
                            elif which in ['b','back']:
                                setattr(new_list,'UserId',3)
                                break
                            else:
                                try:
                                    if which in ['-1','0']:
                                        break
                                    value=int(which)
                                    setattr(new_list,'UserId',d[value])
                                except Exception as e:
                                    writeError(e,self.error_log)
                        elif str(k.type) == "INTEGER" and str(k.name) == 'IsExported':
                            setattr(new_list,'IsExported',0)
                        elif str(k.type) == 'INTEGER' and str(k.name) == 'IsDeleted':
                            setattr(new_list,'IsDeleted',0)
                        elif str(k.type) == 'INTEGER' and str(k.name) == 'TypeId':
                            with Session(self.engine) as session:
                                d={}
                                users=session.query(self.tbl.ListType).all()
                                for num,user in enumerate(users):
                                    d[num]=user
                                    print(num,obj2dict(user))
                                m="Which num [num/q/b/quit/back]: "
                                which=input(m)
                                if which in ['q','quit']:
                                    exit("user quit!")
                                elif which in ['b','back']:
                                    break
                                else:
                                    try:
                                        if which in ['-1','0']:
                                            break
                                        value=int(which)
                                        setattr(new_list,'TypeId',d[value].TypeId)
                                    except Exception as e:
                                        writeError(e,self.error_log)
                        elif str(k.type) == 'INTEGER' and k.name == str('StorageId'):
                            setattr(new_list,'StorageId',self.cfg.get('storageId'))         
                            
                        break
            session.add(new_list)
            session.commit()
            session.refresh(new_list)
            print(obj2dict(new_list))
    def promptForAction(self):
        listid=None
        listTitle=None
        while True:
            try:
                m=self.displayListItemMenu(dsp=False)
                action=input(m)
                if action in ['n','nl','newlist','new_list','1']:
                    self.makeNewList()
                elif action in '[Quit/Q/q/quit/3]'.replace("[","").replace("]","").split("/"):
                    exit("user quit!")
                elif action in '[Back/B/b/back/4]'.replace("[","").replace("]","").split("/"):
                    break
            except Exception as e:
                writeError(e,self.error_log)
            
            

class GotoLists:
    def __str__(self):
        return "GotoLists/gtl/2"

    def __init__(self,config,engine,tbl,error_log):
        self.tbl=tbl
        self.error_log=error_log
        self.config=config
        self.engine=engine
        self.cfg=self.getConfig()
        self.promptForAction()

    def displayListItemMenu(self):
        msg="""
    {row1}strings with a return line that do not start with '#' 
    symbol and will search barcode|code|itemid and use 
    the first located item, and will be treated as entries
        -if this is not correct please see below[r2u]{end}

    {row0}"+[num]" will search for an entry, if there is none, 
        make one, and increment its quantity by the number 
        provided after the plus[r2u]{end}

    {row1}"-[num]" will search for an entry, if there is none, 
        make one, and decrement its quantity by the number 
        provided after the minus[r2u]{end}

    {row0}"#quit" "#q" "#6" will exit the application [r2u]{end}

    {row1}"#deleteItem [ListItemId]" or "#deleteItem" "#di [ListItemId]" or "#di"  
    will search for item identified by ListItemId provided 
    immediately after cmd, or the immediate last ListItemId 
    entered if none is provided. [r2u]{end}

    {row0}"#back" "#b" "#5" will go back a menu [r2u]{end}

    {row1}"#search" "#s" will search for codes using code|barcode|itemid|name|note
        and display them with a prompt to select code for use{end}-

    {row0}"#barcode []" will only search barcode field{end}-

    {row1}"#itemCode [] will only search code field{end}-

    {row0}#itemid []" will only search itemid field{end}-

    {row0}#listitemid []" will only search listitemid field{end}-

    {row1}"#?" will display THIS [r2u]{end}

    {row0}"#showBarcode" [barcode] displays item by barcode in List[r2u]{end}
    {row1}'cyan colored items existed in list{end}
    {row0}'green' colored items were just created in list{end}
    {row1}#zeroId $code,#zeroItemId $code ,#zeroItemCode $code, #zeroBarcode $code -> set Quantity of result to zero(0)[r2u]{end}
    {row0}#clearId $code,#clearItemId $code, #clearItemCode $code, #clearBarcode $code -> delete result forever[r2u]{end}
    {row0}#zeroall -> set all qty's to zero in List[r2u]{end}
    {row1}#clearall -> remove all items from list[r2u]{end}
    {row0}#showTP -> show total price for list{end}
    {row1}#count -> show total items in list{end}
{row0}#expub_pkg -> export unknown barcodes to User's Downloads folder as zipfile
    containing:
        manifest.txt
        Barcodes.csv
        GeneratedImages/
            upca/
            code39/
            code128/
    #1 image for each barcode in unknownBarcodes.csv{end}
        {row1}#expub b|c|n|p
        where:
            p : price
            c : code
            n : name
            b : barcode
            once prompted for system:
            type either 'linux' or 'android' without single quotes, hit return
            type either .xlsx for excel in default location, just hit enter for csv in default
            location, or overrode with a path+filename, and hit enter{end}
        """
        msg=msg.format(row0=fg("red"),row1=fg("green"),end=attr(0))
        print(msg)
        return msg

    def searchAndCreate(self,itemcode,listid,icr=None,dcr=None,like=False):
        if itemcode in ['','#']:
            print("invalid code!")
            return
        with Session(self.engine) as session:
            query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid)
            if like:
                result=query.filter(or_(self.tbl.ListItem.ListItemId==itemcode,self.tbl.ListItem.ItemCode==itemcode,self.tbl.ListItem.ItemBarcode==itemcode))                   
            else:
                result=query.filter(or_(self.tbl.ListItem.ListItemId==itemcode,self.tbl.ListItem.ItemCode==itemcode,self.tbl.ListItem.ItemBarcode==itemcode))                   
            r=result.first()
            if r:
                if icr:
                    r.Quantity+=icr
                elif dcr:
                    r.Quantity+=dcr
                else:
                    r.Quantity+=1
                session.commit()
                session.flush()
                session.refresh(r)
                d=obj2dict(r)
                self.printListItem(r,created=False)
                
            else:
                resultSub=session.query(self.tbl.Item).filter(self.tbl.Item.StorageId==self.cfg.get('storageId'))
                resultSub=resultSub.filter(or_(self.tbl.Item.ItemId==itemcode,self.tbl.Item.Code==itemcode,self.tbl.Item.Barcode==itemcode))
                rSub=resultSub.first()
                print(rSub)
                if rSub != None:
                    newLI=self.tbl.ListItem()
                    for field in rSub.__table__.columns:
                        try:
                            f="Item{}".format(field.name)
                            v=getattr(rSub,field.name)
                            setattr(newLI,f,v)
                        except Exception as e:
                            "#ignore"
                            writeError(e,self.error_log)
                    setattr(newLI,"ListId",listid)
                    setattr(newLI,"ItemId",rSub.ItemId)
                    setattr(newLI,"Quantity",1)

                    session.add(newLI)
                    session.commit()
                    session.flush()
                    session.refresh(newLI)
                    #d=obj2dict(newLI)
                    #d=obj2dict(r)
                    
                
                    cf=session.query(self.tbl.ItemCustomField).filter(self.tbl.ItemCustomField.ItemId==rSub.ItemId).all()
                    for c in cf:
                        nlcf=self.tbl.ListItemCustomField()
                        
                        nlcf.ListItemId=newLI.ListItemId
                        nlcf.Value=c.Value
                        nlcf.CustomFieldId=c.CustomFieldId

                        session.add(nlcf)
                        session.commit()
                    self.printListItem(newLI,created=True)
                else:
                    blankListItem=self.tbl.ListItem()
                    blankListItem.ItemName=itemcode
                    blankListItem.ItemBarcode=itemcode
                    blankListItem.ItemCode=itemcode
                    blankListItem.ItemPrice=0
                    blankListItem.Quantity=1
                    blankListItem.ItemNote="Unknown Item/Barcode!"
                    blankListItem.ListId=listid
                    blankListItem.ItemId=-1
                    blankListItem.ItemMeasurementUnit='pcs'
                    blankListItem.ItemTags="@Unknown"
                    session.add(blankListItem)
                    session.commit()
                    session.flush()
                    session.refresh(blankListItem)
                    print(obj2dict(blankListItem))
                #make new ListItem with Corresponding fields and custom fields
                pass

    def searchAndCreateLike(self,itemcode,listid,icr=None,dcr=None,mode="insert"):
        if itemcode in ['','#']:
            print("invalid code!")
            return
        with Session(self.engine) as session:
            query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid)
            result=query.filter(or_(self.tbl.ListItem.ListItemId==itemcode,self.tbl.ListItem.ItemCode==itemcode,self.tbl.ListItem.ItemBarcode==itemcode))                   
            r=result.first()
            if r:
                if icr:
                    r.Quantity+=icr
                elif dcr:
                    r.Quantity+=dcr
                else:
                    r.Quantity+=1
                session.commit()
                session.flush()
                session.refresh(r)
                d=obj2dict(r)
                self.printListItem(r,created=False)
                
            else:
                resultSub=session.query(self.tbl.Item).filter(self.tbl.Item.StorageId==self.cfg.get('storageId'))
                resultSub=resultSub.filter(or_(self.tbl.Item.ItemId.icontains(itemcode),self.tbl.Item.Code.icontains(itemcode),self.tbl.Item.Barcode.icontains(itemcode)))
                rSub=resultSub.first()
                print(rSub)
                if rSub != None:
                    newLI=self.tbl.ListItem()
                    for field in rSub.__table__.columns:
                        try:
                            f="Item{}".format(field.name)
                            v=getattr(rSub,field.name)
                            setattr(newLI,f,v)
                        except Exception as e:
                            "#ignore"
                            writeError(e,self.error_log)
                    setattr(newLI,"ListId",listid)
                    setattr(newLI,"ItemId",rSub.ItemId)
                    setattr(newLI,"Quantity",1)

                    session.add(newLI)
                    session.commit()
                    session.flush()
                    session.refresh(newLI)
                    #d=obj2dict(newLI)
                    #d=obj2dict(r)
                    
                
                    cf=session.query(self.tbl.ItemCustomField).filter(self.tbl.ItemCustomField.ItemId==rSub.ItemId).all()
                    for c in cf:
                        nlcf=self.tbl.ListItemCustomField()
                        
                        nlcf.ListItemId=newLI.ListItemId
                        nlcf.Value=c.Value
                        nlcf.CustomFieldId=c.CustomFieldId

                        session.add(nlcf)
                        session.commit()
                    self.printListItem(newLI,created=True)
                #make new ListItem with Corresponding fields and custom fields
                pass
    def printListItem(self,listItem,created=True,printCF=False):
        d=obj2dict(listItem)
        for k in d.keys():
            if k == "ListItemId":
                print(attr(5)+k+attr(0)+":"+fg("red")+str(d[k])+attr(0))
            elif k == "Quantity":
                print(attr(5)+k+attr(0)+":"+fg("yellow")+str(d[k])+attr(0))
            else:
                if created:
                    print(k+":"+fg("green")+str(d[k])+attr(0))
                else:
                    print(k+":"+fg("cyan")+str(d[k])+attr(0))
        if printCF:
            with Session(self.engine) as session:
                if isinstance(listItem,self.tbl.ListItem):
                    cf=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ListItemId==listItem.ListItemId).all()
                elif isinstance(listItem,self.tbl.Item):
                    cf=session.query(self.tbl.ItemCustomField).filter(self.tbl.ItemCustomField.ItemId==listItem.ItemId).all()
                else:
                    raise Exception(listItem)
                
                for num,c1 in enumerate(cf):
                    print("---CF {}---".format(num))
                    cfname=session.query(self.tbl.CustomField).filter(self.tbl.CustomField.CustomFieldId==c1.CustomFieldId).first() 
                    if cfname:
                        for col in c1.__table__.columns:
                            if col.name == "Value":
                                print("{f}Name{e}: {v}".format(f=fg("blue"),e=attr(0),v=cfname.Name))
                                print("{f}Type{e}: {v}".format(f=fg("blue"),e=attr(0),v=cfname.Type))
                                print("{f}Value{e}: {v}".format(f=fg("blue"),e=attr(0),v=c1.Value))
                            else:
                                print("{s}{f}{e}: {v}".format(e=attr(0),s=fg("green"),f=col,v=getattr(c1,col.name)))
                    print("---CF {}---".format(num))

    def searchAndDelete(self,code):
        try:
            with Session(self.engine) as session:
                query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListItemId==int(code)).delete()
                session.commit()
                print(query)
        except Exception as e:
            writeError(e,self.error_log)

    def showList(self,listid):
        try:
            with Session(self.engine) as session:
                query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
                showCF=input("show CF's [y/N]: ")
                if showCF.lower() in ['y','yes']:
                    showCF=True
                else:
                    showCF=False
                for num,row in enumerate(query):
                    print("=======Entry {}/{} Start=========".format(num+1,len(query)))
                    if num % 2 == 0:
                        self.printListItem(row,created=False,printCF=showCF)
                    else:
                        self.printListItem(row,created=True,printCF=showCF)
                    print("=======Entry {}/{} End=========".format(num+1,len(query)))
        except Exception as e:
            writeError(e,self.error_log)

    def checkList(self,listid):
        with Session(self.engine) as session:
            try:
                listExists=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
                if listExists:
                    return True
                else:
                    return False

            except Exception as e:
                writeError(e,self.error_log)
    def showListItemBarcode(self,code,returnable=False):
        with Session(self.engine) as session:
            query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ItemBarcode==code)
            result=query.first()
            if result:
                if returnable:
                    return obj2dict(result)
                else:
                    if input("print custom fields? [y/N]").lower() in ['y','yes']:
                        self.printListItem(result,printCF=True)
                    else:
                        self.printListItem(result,created=True,printCF=False)

    def promptForAction(self):
        listid=None
        listTitle=None
        while True:
            self.like=input("=/e/ee/==->==|?/%/like/l/ll/li->like/q/b? ")
            if self.like.lower() in ['q','quit']:
                exit("user quit!")
            elif self.like.lower() in ["b",'back']:
                return
            elif self.like.lower() in ['=','e','ee','==','']:
                self.like=False
                break
            elif self.like.lower() in ['%','?','like','li','lik','s']:
                self.like=True
                break
        while True:
            listid=input("listid/#q/#b: ")
            if listid.lower() in ["#q","#quit"]:
                exit("user quit!")
            elif listid.lower() in ["#b","#back"]:
                return
            try:
                listid=int(listid)
                if self.checkList(listid):
                    break
                else:
                    print("that list does not exist!")
            except Exception as e:
                writeError(e,self.error_log)
        while True:
            action=input("code/#[cmd]/#quit/#back/#show/#?: ")
            if action.lower() in ["#quit","#6","#q"]:
                exit("user quit")
            elif action.lower() in ["#back","#5","#b"]:
                break
            elif action.lower() == "#?":
                self.displayListItemMenu()
            elif action.split(' ')[0] in ["#deleteItem","#di"]:
                code=[]
                if len(action.split(" ")) > 1:
                    code=action.split(" ")[1:]
                else:
                    code=input("ListItemId to delete: ")
                    code=[i for i in code.split(" ")]
                for c in code:
                    self.searchAndDelete(c)
            elif action.lower() == "#show":
                self.showList(listid)
            elif action.split(" ")[0] == "#showBarcode":
                if len(action.split(" ")) > 1:
                    self.showListItemBarcode(action.split(" ")[-1])
                else:
                    p=input("itembarcode: ")
                    if p.lower() in ["#q","#quit"]:
                        exit("user quit!")
                    elif p.lower() in ["#b",'#back']:
                        break
                    else:
                        self.showListItemBarcode(p)
            elif action.split(" ")[0] == "#barcode":
                a=self.searchCode(action,listid=listid,mode="barcode")
                if a == False:
                    break
                else:
                    pass
            elif action.split(" ")[0] == "#itemcode":
                a=self.searchCode(action,listid=listid,mode="itemcode")
                if a == False:
                    break
                else:
                    pass
            elif action.split(" ")[0] == "#listitemid":
                a=self.searchCode(action,listid=listid,mode="listitemid")
                if a == False:
                    break
                else:
                    pass
            elif action.split(" ")[0] == "#itemid":
                a=self.searchCode(action,listid=listid,mode="itemid")
                if a == False:
                    break
                else:
                    pass
                '''#clearId {}, #clearItemCode {}, #clearBarcode {} -> set Quantity of result to zero(0){end}
            {row0}#zeroAll -> set all qty's to zero in List{end}'''
            elif action.split(" ")[0].lower() == "#zeroall":
                with Session(self.engine) as session:
                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
                    for r in results:
                        setattr(r,'Quantity',0)
                    session.commit()
            elif action.split(" ")[0].lower() == "#clearall":
                with Session(self.engine) as session:
                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).delete()
                    session.commit()
                    print(results)
            elif action.split(" ")[0].lower() == "#clearid":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ListItemId/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)

                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ListItemId==liid).delete()
                    session.commit()
                    print("deleted",results,"items!")
                        
            elif action.split(" ")[0].lower() == "#zeroid":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ListItemId/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)


                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ListItemId==liid).first()
                    results.Quantity=0

                    session.commit()
                    print(obj2dict(results))

            elif action.split(" ")[0].lower() == "#clearitemcode":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ItemCode/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)
                            
                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemCode==liid).delete()
                    session.commit()
                    print("deleted",results,"items!")
                        
            elif action.split(" ")[0].lower() == "#zeroitemcode":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ItemCode/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)

                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemCode==liid).first()
                    results.Quantity=0

                    session.commit()
                    print(obj2dict(results))
            elif action.split(" ")[0].lower() == "#clearbarcode":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[Barcode/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)
                            
                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemBarcode==liid).delete()
                    session.commit()
                    print("deleted",results,"items!")
                        
            elif action.split(" ")[0].lower() == "#zerobarcode":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[Barcode/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)

                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemBarcode==liid).first()
                    results.Quantity=0

                    session.commit()
                    print(obj2dict(results))
            elif action.split(" ")[0].lower() == "#clearitemid":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ItemId/q/b]: """
                                liid=input(cmd).split(" ")
                            else:
                                liid=action.split(" ")[1:]

                            if liid[0].lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid[0].lower() in ['b','back']:
                                break
                            else:
                                liid=[int(i) for i in liid]
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)
                    for i in liid:  
                        results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemId==i).delete()
                        session.commit()
                        print("deleted",results,"items!")
                        
            elif action.split(" ")[0].lower() == "#zeroitemid":
                liid=None
                with Session(self.engine) as session:
                    while True:
                        try:
                            if len(action.split(" ")) < 2:
                                cmd="""[ItemId/q/b]: """
                                liid=input(cmd)
                            else:
                                liid=action.split(" ")[-1]
                            if liid.lower() in ['q','quit']:
                                exit("user quit!")
                            elif liid.lower() in ['b','back']:
                                break
                            else:
                                liid=int(liid)
                                break
                        except Exception as e:
                            if len(action.split(" ")) > 1:
                                break
                            writeError(e,self.error_log)

                    results=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemId==liid).all()
                    for r in results:
                        r.Quantity=0
                        session.commit()
                        session.flush()
                        session.refresh(r)
                        print(obj2dict(r))

                    session.commit()
            elif action.split(" ")[0].lower() == "#showtp":
                with Session(self.engine) as session:
                    items=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
                    total=0
                    for item in items:
                        total+=(item.Quantity*item.ItemPrice)
                    print("{}ListTotal ($Dollars){}: {}{}{}".format(fg("green"),attr(0),fg("yellow"),total,attr(0)))
            elif action.split(" ")[0].lower() == "#count":
                with Session(self.engine) as session:
                    items=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
                    print("{}Total Items{}: {}{}{}".format(fg("green"),attr(0),fg("yellow"),len(items),attr(0)))
            elif action.lower() == "#exportcsv":
                with Session(self.engine) as session:
                    q=session.query(self.tbl.ListItem,self.tbl.ListItemCustomField,self.tbl.CustomField).join(self.tbl.ListItemCustomField,self.tbl.ListItemCustomField.ListItemId==self.tbl.ListItem.ListItemId).join(self.tbl.CustomField,self.tbl.CustomField.CustomFieldId==self.tbl.ListItemCustomField.CustomFieldId).filter(self.tbl.ListItem.ListId==listid)
                    df=pd.read_sql(q.statement,q.session.bind)
                    while True:
                        if 'arm' in platform.machine():
                            default=Path("/storage/emulated/0/download/export.csv")
                        else:
                            default=Path(plyer.storagepath.get_downloads_dir())/Path("export.csv")
                        to=input("save where(q/b/Path|default={}): ".format(default))
                        if to in ['q','quit']:
                            exit("user quit!")
                        elif to in ['b','back']:
                            break
                        elif to == '':
                            to=str(default)
                        if not Path(to).is_dir():
                            try:
                                df.to_csv(to,index=False)
                                break
                            except Exception as e:
                                writeError(e,self.error_log)
            elif action.lower() == "#exportexcel":
                with Session(self.engine) as session:
                    q=session.query(self.tbl.ListItem,self.tbl.ListItemCustomField,self.tbl.CustomField).join(self.tbl.ListItemCustomField,self.tbl.ListItemCustomField.ListItemId==self.tbl.ListItem.ListItemId).join(self.tbl.CustomField,self.tbl.CustomField.CustomFieldId==self.tbl.ListItemCustomField.CustomFieldId).filter(self.tbl.ListItem.ListId==listid)
                    df=pd.read_sql(q.statement,q.session.bind)
                    while True:
                        if 'arm' in platform.machine():
                            default=Path("/storage/emulated/0/download/export.xlsx")
                        else:
                            default=Path(plyer.storagepath.get_downloads_dir())/Path("export.xlsx")
                        to=input("save where(q/b/Path|default={}): ".format(default))
                        if to in ['q','quit']:
                            exit("user quit!")
                        elif to in ['b','back']:
                            break
                        elif to == '':
                            to=str(default)
                        if not Path(to).is_dir():
                            try:
                                df.to_excel(to,index=False)
                                break
                            except Exception as e:
                                writeError(e,self.error_log)
            elif action.lower().split(" ")[0] == "#expub_pkg":
                if len(action.lower().split(" ")) > 1:
                    mode=action.lower().split(" ")[1]
                else:
                    modes=[
                        Fore.cyan+'expub -> export unknownBarcodes'+Style.reset,
                        Fore.green+'exkb  -> export knownBarcodes'+Style.reset,
                        Fore.yellow+"b/back -> Go Back"+Style.reset,
                        Fore.red+"q/quit -> Quit!"+Style.reset, 
                    ]
                    mode='\n'.join(modes)+"\nwhat would you like to do? "
                    mode=input(mode)
                    if mode.lower() in ["q","quit"]:
                        exit("user quit!")
                    elif mode.lower() in ["b","back"]:
                        break
                    elif mode.lower() == "expub":
                        b,c,n,p,m,q=True,True,True,True,True,True
                        
                        ss=[
                            Fore.cyan+"q : Quantity"+Style.reset,
                            Fore.green+"m : ItemMeasurementUnit"+Style.reset,
                            Fore.cyan+"n : ItemName"+Style.reset,
                            Fore.green+"p : ItemPrice"+Style.reset,
                            Fore.cyan+"C : ItemCode"+Style.reset,
                            Fore.green+"b : barcode"+Style.reset,
                            Fore.yellow+"B/back -> Go Back"+Style.reset,
                            Fore.red+"q/quit -> Quit!"+Style.reset, 
                        ]
                        si='\n'.join(ss)+"\nwhat would you like to do? "
                        si=input(si)
                        if si.lower() in ['B','back']:
                            break
                        elif si.lower() in ['q','quit']:
                            exit("user quit!")
                        else:
                            pass
                        mode_string=si
                        if 'b' not in mode_string.lower():
                            b=False
                        if 'C' not in mode_string:
                            c=False
                        if 'n' not in mode_string.lower():
                            n=False
                        if 'p' not in mode_string.lower():
                            p=False
                        if 'm' not in mode_string.lower():
                            m=False
                        if 'q' not in mode_string.lower():
                            q=False
                        self.expub(listid,barcode=b,itemcode=c,name=n,price=p,qty=q,mu=m,format="pkg")
                    elif mode.lower() == "exkb":
                        b,c,n,p,m,q=True,True,True,True,True,True
                        
                        ss=[
                            Fore.cyan+"q : Quantity"+Style.reset,
                            Fore.green+"m : ItemMeasurementUnit"+Style.reset,
                            Fore.cyan+"n : ItemName"+Style.reset,
                            Fore.green+"p : ItemPrice"+Style.reset,
                            Fore.cyan+"C : ItemCode"+Style.reset,
                            Fore.green+"b : barcode"+Style.reset,
                            Fore.yellow+"B/back -> Go Back"+Style.reset,
                            Fore.red+"q/quit -> Quit!"+Style.reset, 
                        ]
                        si='\n'.join(ss)+"\nwhat would you like to do? "
                        si=input(si)
                        if si.lower() in ['B','back']:
                            break
                        elif si.lower() in ['q','quit']:
                            exit("user quit!")
                        else:
                            pass
                        mode_string=si
                        if 'b' not in mode_string.lower():
                            b=False
                        if 'C' not in mode_string:
                            c=False
                        if 'n' not in mode_string.lower():
                            n=False
                        if 'p' not in mode_string.lower():
                            p=False
                        if 'm' not in mode_string.lower():
                            m=False
                        if 'q' not in mode_string.lower():
                            q=False
                        self.expub(listid,barcode=b,itemcode=c,name=n,price=p,qty=q,mu=m,format="pkg",known=True)
                    print(mode)
                #self.expub_pkg(listid,mode=mode)
            elif action.lower().split(" ")[0] == "#expub":
                b,c,n,p,m,q=True,True,True,True,True,True
                if len(action.split(" ")) > 1:
                    mode_string=action.replace("#expub","")
                    if 'b' not in mode_string.lower():
                        b=False
                    if 'c' not in mode_string.lower():
                        c=False
                    if 'n' not in mode_string.lower():
                        n=False
                    if 'p' not in mode_string.lower():
                        p=False
                    if 'm' not in mode_string.lower():
                        m=False
                    if 'q' not in mode_string.lower():
                        q=False
                    self.expub(listid,barcode=b,itemcode=c,name=n,price=p,qty=q,mu=m)
                else:
                    print("you need to specify a mode")
            else:
                try:
                    if action.startswith("+"):
                        try:
                            icr=float(action[1:])
                        except Exception as e:
                            icr=1
                        code=input("code/q/skip: ")
                        if self.like:
                            self.searchAndCreate(code,listid,icr=icr,like=True)
                        else:
                            self.searchAndCreate(code,listid,icr=icr)
                    elif action.startswith("-"):
                        try:
                            dcr=-float(action[1:])
                        except Exception as e:
                            dcr=-1
                        code=input("code/q/skip: ")
                        if self.like:
                            self.searchAndCreate(code,listid,dcr=dcr,like=True)
                        else:
                            self.searchAndCreate(code,listid,dcr=dcr)
                    else:
                        code=action
                        if self.like:
                            self.searchAndCreate(code,listid,like=True)
                        else:
                            self.searchAndCreate(code,listid)

                except Exception as e:
                    print(e)
                    writeError(e,error_log=self.error_log)
    default_export={
        '':'export.csv',
    }
    def expub(self,listid,barcode=True,itemcode=True,price=True,name=True,qty=True,mu=True,format=None,known=False):
        #export unknown barcodes
        with Session(self.engine) as session:
            if known:
                query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemId!=-1)
            else:
                query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemId==-1)
            df=pd.read_sql(query.statement,query.session.bind)
            fields=[]
            if barcode:
                fields.append("ItemBarcode")
            if itemcode:
                fields.append("ItemCode")
            if price:
                fields.append("ItemPrice")
            if name:
                fields.append("ItemName")
            if qty:
                fields.append("Quantity")
            if mu:
                fields.append("ItemMeasurementUnit")

            df=df[fields]
            default=None
            if format == "pkg":
                while True:
                    sys=''
                    #sys=input("q/b/OS{}:".format(list(self.default_export.keys())))
                    if sys.lower() in self.default_export.keys():
                        default=self.default_export[sys]
                        break
                    elif sys.lower() in ['q','quit']:
                        exit("user quit!")
                    elif sys.lower() in ['b','back','cancel']:
                        return
                tmp=Path(tempfile.mkdtemp())
                images=Path(tmp/Path("generatedImages"))
                if not images.exists():
                    images.mkdir()
                else:
                    shutil.rmtree(images)
                    images.mkdir()
                codes_images=images/Path('Codes')
                subs_code={
                'upca':codes_images/Path("upca"),
                'code39':codes_images/Path("code39"),
                'code128':codes_images/Path("code128"),
                }
                if not codes_images.exists():
                    codes_images.mkdir(parents=True)
                for p in subs_code:
                    if not subs_code[p].exists():
                        subs_code[p].mkdir(parents=True)

                barcodes_images=images/Path("Barcodes")
                subs_barcode={
                'upca':barcodes_images/Path("upca"),
                'code128':barcodes_images/Path("code128"),
                'code39':barcodes_images/Path("code39"),
                }
                if not barcodes_images.exists():
                    barcodes_images.mkdir(parents=True)
                for p in subs_barcode:
                    if not subs_barcode[p].exists():
                        subs_barcode[p].mkdir(parents=True)

                df.to_csv("Barcodes.csv",index=False)
                tries=[UPCA,Code39,Code128]
                try:
                    for ItemBarcode in df['ItemBarcode']:
                        for t in tries:
                            print(ItemBarcode,t)
                            if t == Code39:
                                try:
                                    local_code=t(ItemBarcode,add_checksum=False,writer=ImageWriter())
                                    local_code.save(str(subs_barcode['code39']/Path(str(local_code)+"_"+str(t.name)))+"-"+str(ItemBarcode))
                                except Exception as e:
                                    writeError(e,self.error_log)
                            else:
                                try:
                                    local_code=t(ItemBarcode,writer=ImageWriter())
                                    print(t.name.replace(" ","").lower())

                                    l=subs_barcode[t.name.replace(" ","").lower().replace("-","")]
                                    local_code.save(str(l/Path(str(local_code)+"_"+str(t.name)))+"-"+str(ItemBarcode))
                                except Exception as e:
                                    writeError(e,self.error_log)
                except Exception as e:
                    print("ItemBarcode was not Selected by user!")
                    writeError(e,self.error_log)            
                    
                try:
                    for ItemCode in df['ItemCode']:
                        for t in tries:

                            if t == Code39:
                                try:
                                    local_code=t(ItemCode,add_checksum=False,writer=ImageWriter())
                                    local_code.save(str(subs_code['code39']/Path(str(local_code)+"_"+str(t.name)))+":"+str(ItemCode))
                                except Exception as e:
                                    writeError(e,self.error_log)        
                            else:
                                try:
                                    local_code=t(ItemCode,writer=ImageWriter())
                                    l=subs_code[t.name.replace(" ","").lower().replace("-","")]
                                    local_code.save(str(l/Path(str(local_code)+"_"+str(t.name)))+"-"+str(ItemCode))
                                except Exception as e:
                                    writeError(e,self.error_log)
                            print("itemcode",t)
                except Exception as e:
                    print("ItemCode was not Selected by user!")
                    writeError(e,self.error_log)
                
                
                if Path(self.default_export[sys].replace("csv","zip")).exists():
                    Path(self.default_export[sys].replace("csv","zip")).unlink()

                with zipfile.ZipFile(self.default_export[sys].replace("csv","zip"),"w") as export:
                    with open("manifest.txt","w+") as out:
                        for d in images.iterdir():
                            out.write(str(d)+"\n")
                            export.write(d)
                            if "Codes" in d.name:
                                for f in codes_images.iterdir():
                                    out.write(str(f)+"\n")
                                    export.write(f)
                                for f in subs_code:
                                    for line in subs_code[f].iterdir():
                                        out.write(str(line)+"\n")
                                        export.write(line)

                            elif "Barcode" in d.name:
                                for f in barcodes_images.iterdir():
                                    out.write(str(f)+"\n")
                                    export.write(f)
                                for f in subs_barcode:
                                    for line in subs_barcode[f].iterdir():
                                        out.write(str(line)+"\n")
                                        export.write(line)
                        out.write("manifest.txt\n")
                        out.write("Barcodes.csv\n")

                    export.write('manifest.txt')
                    export.write('Barcodes.csv')
                try:
                    shutil.rmtree(images)
                    Path('manifest.txt').unlink()
                    Path('Barcodes.csv').unlink()
                    print(Fore.light_green+"finished exporting list: {}!".format(listid)+Style.reset)
                except Exeption as e:
                    self.write(e,self.error_log)
                try:
                    shutil.copy(self.default_export[sys].replace("csv","zip"),'/storage/emulated/0/Download/')
                except Exception as e:
                    print(e)


            elif format == None:
                while True:
                    sys=input("q/b/OS{}:".format(list(self.default_export.keys())))
                    if sys.lower() in self.default_export.keys():
                        default=self.default_export[sys]
                        break
                    elif sys.lower() in ['q','quit']:
                        exit("user quit!")
                    elif sys.lower() in ['b','back','cancel']:
                        return
                saveTo=input(str(Fore.green+str(len(df[fields]))+" "+Style.reset+"Records Will Be Exported to?[{}]".format(default)))
                try:
                    if saveTo == "":
                        saveTo=default
                    elif saveTo.lower() == ".xlsx":
                        saveTo=self.default_export[sys.lower()]
                        saveTo=Path(saveTo.replace("csv","xlsx"))
                    saveTo=Path(saveTo)
                    if saveTo.parent.exists():
                        if saveTo.suffix.lower() in ".csv":
                            df.to_csv(saveTo,index=False)
                        elif saveTo.suffix.lower() in ".xlsx":
                            df[fields].to_excel(saveTo,index=False)
                except Exception as e:
                    writeError(e,self.error_log)
            

    def getConfig(self,key=None):
        with self.config.open("r") as cfgfile:
            config=json.load(cfgfile)
            if key:
                return config.get(key)
            else:
                return config

    #more modes will be added to this searcher
    def searchCode(self,action,listid,mode="barcode"):
        code=None
        if len(action.split(" ")) > 1:
            code=action.split(" ")[-1]
        else:
            code=input("barcode [q|b]: ")
            if code.lower() in ['q','quit']:
                exit('user quit')
            elif code.lower in ['b','back']:
                return False
        print(mode,code)
        with Session(self.engine) as session:
            if mode.lower() == "barcode":
                result=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemBarcode==code).all()
            elif mode.lower() == "itemcode":
                result=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemCode==code).all()
            elif mode.lower() == "listitemid":
                result=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ListItemId==int(code)).all()
            elif mode.lower() == "itemid":
                result=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid,self.tbl.ListItem.ItemId==int(code)).all()
            else:
                raise Exception("invalid mode! "+mode)

            showCF=input("show CustomField? [y/N/q/b]: ")
            incr=input("+/-Quantity[y/N/+Val/-Val]: ")


            if incr.startswith("+") or incr.startswith("-"):
                if len(incr) == 1:
                    incr=0
                else:
                    incr=float(incr)
            else:
                if incr.lower() in ["y","yes"]:
                    while True:
                        try:
                            incr=input("+/-Val|q|b: ")
                            if incr.lower() == "q":
                                exit("user quit")
                            elif incr.lower() == "b":
                                break
                            else:
                                incr=float(incr)
                                break
                        except Exception as e:
                            writeError(e,self.error_log)
                else:
                    incr=str('No')
            if showCF.lower() in ['y','yes']:
                showCF=True
            elif showCF.lower() in ['q','quit','#q','#quit','#quit#']:
                exit("user quit!")
            elif showCF.lower() in ['b','back','#back#','#b#','#back']:
                return False
            else:
                showCF=False
            if len(result) > 0:
                for li in result:
                    editLI=input(str("-"*10)+"Start Next\n"+"LI[{itemcode}|{barcode}|{name}]\nedit ListItem[y/N/q/b/d]: ".format(
                        itemcode=li.ItemCode,
                        barcode=li.ItemBarcode,
                        name=li.ItemName,
                        )
                    )
                    if editLI.lower() in ['q','quit','#q','#quit','#quit#']:
                        exit("user quit!")
                    elif editLI.lower() in ['b','back','#back#','#b#','#back']:
                        break
                    elif editLI.lower() in ['y','yes','#y','#yes','#y#','#yes#']:
                        editCF=input("edit CustomFields? [y/N/q/b]: ")
                        if editCF.lower() in ['q','quit','#q','#quit','#quit#']:
                            exit("user quit!")
                        elif editCF.lower() in ['b','back','#back#','#b#','#back']:
                            break
                    elif editLI.lower() in ['d','delete','#delete','#d','#delete#','#d#','del']:
                        with Session(self.engine) as session:
                            d=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ListItemId).delete()
                            print(d)
                            session.commit()
                            d=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListItemId==li.ListItemId).delete()
                            print(d)
                            session.commit()
                            session.flush()

                    else:
                        if editLI in ['n',"no"]:
                            print("skipping edit!")
                        elif editLI in  ['y','yes']:
                            for k in li.__table__.columns:
                                if k.name in ['ListId','ListItemId','ItemId','ItemImagePath',]:
                                    pass
                                else:
                                    valstring=input("LI[{itemcode}|{barcode}|{name}|{type}|{value}]\nnewValue/q/n/#q#/#next#,#n,#b#,#n#,#back# : ".format(
                                        name=k.name,
                                        type=k.type,
                                        value=getattr(li,k.name),
                                        itemcode=li.ItemCode,
                                        barcode=li.ItemBarcode,
                                        ))
                                    if valstring.lower() in ['q','quit','#q','#quit','#quit#','#q#']:
                                        exit("user quit!")
                                    elif valstring.lower() in ['b','back','#back#','#b#','#back',]:
                                        break
                                    elif valstring.lower() in ['n','#n','next','#next','#next#']:
                                        pass
                                    else:
                                        #new_value=input("ListItem {name}:{type}:{value} [newValue/q/n/#q#/#next#,#n,#b#,#n#,#back#)]: ".format(
                                        new_value=valstring
                                        #name=k.name,
                                        #type=k.type,
                                        #value=getattr(li,k.name)))
                                        if k.type == 'FLOAT':
                                            new_value=float(new_value)
                                        elif k.type == 'INTEGER':
                                            new_value=integer(new_value)
                                        elif k.type == 'VARCHAR':
                                            new_value=str(new_value)
                                        print(new_value,type(new_value))
                                        setattr(li,k.name,new_value)
                                        session.commit()
                                        session.flush()
                                        session.refresh(li)

                                    #need to know why its add new lis
                            if editCF.lower() in ['yes','y','ye']:
                                cfs=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ListItemId==li.ListItemId).all()
                                if len(cfs) < 1:
                                    asign=input("there are no custom fields assigned for this item. would you like to? ")
                                    if assign.lower() in ['y','yes']:
                                        CustomFields(self.engine,self.config,self.tbl,self.error_log,obj2dict(li))
                                    else:
                                        pass
                                else:
            
                                    for num,cf in enumerate(cfs):
                                        deleted=False
                
                                        attr=session.query(self.tbl.CustomField).filter(self.tbl.CustomField.CustomFieldId==cf.CustomFieldId).first()
                
                                        if attr:
                                            while True:
                                                try:
                                                    edit=input("LIC[{liname}|{liid}:|{name}|{type}|{current_value}|({t}/{total})]\nnew_value/#q#/#b#/#delete#\n\t: ".format(
                                                        liname=li.ItemName,
                                                        liid=li.ListItemId,
                                                        name=attr.Name,
                                                        type=attr.Type,
                                                        current_value=cf.Value,
                                                        t=num,total=len(cfs)
                                                        ))
                                                    if edit.lower() in ['#q#','#q','#quit#',]:
                                                        exit("user quit!")
                                                    elif edit.lower() in ['#b#','#b','#back#']:
                                                        break
                                                    elif edit.lower() in ['#d',"#del","#delete",'#delete#']:
                                                        result=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ItemCustomFieldId==cf.ItemCustomFieldId).delete()
                                                        session.commit()
                                                        deleted=True
                                                        print(result)
                                                        break
                                                    else:
                                                        delete=False
                                                        
                                                        
                                                    if not deleted:
                                                        if attr.Type == 1:
                                                            edit=float(edit)
                                                            if edit.is_integer():
                                                                edit=int(edit)
                                                            edit=str(edit)
                                                        elif attr.Type == 0:
                                                            edit=str(edit)
                                                        elif attr.Type == 2:
                                                            dt=datetime.strptime(edit,"%m/%d/%Y")
                                                            edit=dt.strftime("%D")
                                                        cf.Value=str(edit)
                                                        session.commit()
                                                        session.flush()
                                                        if edit.lower() not in ['#d',"#del","#delete"]:
                                                            session.refresh(cf)
                                                        break
                                                except Exception as e:
                                                    print(e)

                                
                        elif editLI in ['#b#','#back#','#next#','#n#',]:
                            break
                        elif editLI in ['q','quit']:
                            exit("user quit!")

                        if isinstance(incr,float):
                            li.Quantity+=incr
                            session.commit()
                            session.flush()
                            session.refresh(li)
                        self.printListItem(li,printCF=showCF)
                else:
                    print("not found in list...")
                    #this should only be a search function
            

class SelectList:
    def __str__(self):
        return 'SelectList'
    def __init__(self,engine,tbl,config,error_log):
        self.engine=engine
        self.tbl=tbl
        self.config=config
        self.error_log=error_log

        #self.displayListMenu()
        self.promptForAction()

    def promptForAction(self):
        while True:
            self.displayListMenu()
            action=input("what would you like to do?: ")
            if action.lower() in ["quit","6","q"]:
                exit("user quit")
            elif action.lower() in ["back","5","b"]:
                break
            else:
                try:
                    try:
                        value=int(action)
                    except:
                        value=action
                    if value == 1 or action == "sl":
                        self.search_lists()
                    elif value == 3 or action == "sd":
                        self.search_lists(isDeleted=1)
                    elif value == 2 or action == "gtl":
                        GotoLists(self.config,self.engine,self.tbl,self.error_log)
                    elif value == 4 or action in ['delete','del','rm','d']:
                        DeleteList(self.config,self.engine,self.tbl,self.error_log)
                    elif value == 7 or action in ['nl','n','new_list']:
                        NewList(self.config,self.engine,self.tbl,self.error_log)
                except Exception as e:
                    print(e)
                    writeError(e,error_log=self.error_log)

    def getConfig(self,key=None):
        with self.config.open("r") as cfgfile:
            config=json.load(cfgfile)
            if key:
                return config.get(key)
            else:
                return config

    def search_lists(self,title=None,note=None,isDeleted=0):
        with Session(self.engine) as session:
            storageId=self.getConfig(key='storageId')
            query=session.query(self.tbl.List)
            if title:
                query=query.filter(self.tbl.List.Title==title)
            if note:
                query=query.filter(self.tbl.List.Note==note)
            query=query.filter(self.tbl.List.IsDeleted==isDeleted)
            query=query.filter(self.tbl.List.StorageId==storageId)
            results=query.all()
            data={}
            keys2Display=['ListId','Date','Title','Note','IsDeleted','UserId','StockChange','TypeId','StorageId','IsExported',]
            print(fg("light_green")+' '.join(keys2Display)+attr(0))
            for num,r in enumerate(results):
                data[num]=r
                asDict=obj2dict(r)
                print()
                for k in []:
                    asDict.drop(k)
                try:
                    ticks=asDict['Date']
                    converted_ticks=datetime(1,1,1)+timedelta(microseconds=ticks/10)
                    asDict['Date']=converted_ticks.ctime()
                except Exception as e:
                    print(fg("red")+attr(5)+"entry needs fixing in the date section"+attr(0))
                
                try:
                    line=[]
                    for k in keys2Display:
                        asDict[k]=asDict[k]
                        if k in ["IsDeleted","IsExported"]:
                            asDict[k]=bool(asDict[k])
                        elif k == "StockChange":
                            v=asDict[k]
                            if v == 0:
                                asDict[k]="NoChange"
                            elif v == 1:
                                asDict[k]="Incomming"
                            elif v == 2:
                                asDict[k]="Outgoing"
                            elif v == 3:
                                asDict[k]="Set"
                        if asDict[k] == None:
                            asDict[k]=''
                        line.append("{}{}{}:{}'{}'{}\n".format(fg('light_green'),k,attr(0),fg('cyan'),asDict[k],attr(0)))
                    l='----Entry {n0} Start----\n '+' '.join(line)+'----Entry {n1} Stop----'
                    print(l.format(
                        n1=str(fg("red")+str(num)+attr(0)),
                        n0=str(fg("red")+str(num)+attr(0)),
                    ))
                except Exception as e:
                    writeError(e,self.error_log)
                

    def displayListMenu(self):
        msg="""
        show Lists -> 1/sl
        goto List -> 2/gtl
        new list -> 7/nl/n/new_list
        show deleted Lists -> 3/sd
        delete list -> 4/d/delete
        back -> 5/b/back
        quit -> 6/q/quit
        """
        print(msg)
        return msg
