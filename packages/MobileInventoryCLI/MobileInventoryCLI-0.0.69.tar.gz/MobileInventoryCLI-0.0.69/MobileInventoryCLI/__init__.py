#!/usr/bin/env python3
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
from MobileInventoryCLI.updateCfg import updateCfg
from MobileInventoryCLI.ExtractPkg import ExtractPkg
from MobileInventoryCLI.error.error import writeError,getConfig

def run():
    BASE=automap_base()
    cfg=None
    p='dbpath.config'
    P=Path(__file__).parent/Path(p)
    script_dir=P
    try:
        with open(P,'r') as config:
            cfg=json.load(config)
    except Exception as e:
        with open(P,"w") as out:
            json.dump({'dbfile':'','storageId':None},out)
        ExtractPkg.ExtractPkg(tbl=None,config=P,error_log=Path(__file__).parent/Path("error.log"),engine=None)
        updateCfg.UpdateConfig.updateByKey(None,'storageId',2,P,None,Path(__file__).parent/Path("error.log"),None)
        with open(P,'r') as config:
            cfg=json.load(config)


        
    if cfg.get('dbfile') == '':
        with open(P,'w') as config:
            while cfg['dbfile'] in ['']:
                cfg['dbfile']=input('dbfile Path to save: ')
            json.dump(cfg,config)
    #filename=Path("/storage/emulated/0/Download/Database/MobileInventoryDB_13-12-2023_01-26-13.db3")
    filename=Path(cfg.get('dbfile'))
    if not filename.exists():
        try:
            updateCfg.UpdateConfig(config=P,error_log=Path(__file__).parent/Path("error.log"),tbl=None)
            with open(P,'r') as config:
                cfg=json.load(config)
            filename=Path(cfg.get('dbfile'))
        except Exception as e:
            raise Exception(str(filename.exists())+":"+str(filename))



    dbfile="sqlite:///"+str(filename)
    print(dbfile)
    import sqlite3
    #z=sqlite3.connect(filename)
    #print(z)
    ENGINE=create_engine(dbfile)
    BASE.prepare(autoload_with=ENGINE)
    TABLE=BASE.classes


    from MobileInventoryCLI.mainloop import mainloop
    from MobileInventoryCLI.error.error import writeError

    #if __name__ == "__main__":
    #    mainloop.MainLoop(engine=ENGINE,config=P,error_log=Path(__file__).parent/Path("error.log"),tbl=TABLE)

    def testStartPC():
        mainloop.MainLoop(engine=ENGINE,config=P,error_log=Path(__file__).parent/Path("error.log"),tbl=TABLE)
    testStartPC()
    #begin making modules and importing them here
