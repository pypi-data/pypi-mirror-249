import pandas as pd
import csv
from datetime import datetime
class CaC:
    def __str__(self):
        return "Collect and Conquer"

    def __init__(self,log_file_name,mode="a"):
        self.log_file_name=log_file_name
        with open(self.log_file_name,mode) as log:
            log.write("EntryStart_{}\n".format(datetime.now().ctime()))
            writer=csv.writer(log,delimiter=",")
            writer.writerow(['Barcode','ItemCode'])
            counter=0
            while True:
                counter+=1
                print("--- startEntry {} ---".format(counter))
                line=[]
                barcode=input("Barcode[#terminate]: ")
                if barcode == "#terminate":
                    break

                item_code=input("ItemCode[#terminate]: ")
                if item_code == "#terminate":
                    break
                line.extend([barcode,item_code])
                writer.writerow(line)
                print("--- endEntry {} ---".format(counter))
            log.write("EntryEnd_{}\n".format(datetime.now().ctime()))



