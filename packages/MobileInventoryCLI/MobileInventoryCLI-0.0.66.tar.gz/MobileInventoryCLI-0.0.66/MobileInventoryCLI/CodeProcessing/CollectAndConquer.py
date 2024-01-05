import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
class CaC:
    def beforeQuit(self):
        self.endLocation=input("End Location: ")
        self.log_file_name_f=Path(self.log_file_name.parent)/Path(f"{self.endLocation}END-{self.log_file_name.name}")
        o=Path(self.log_file_name)
        o.rename(self.log_file_name_f)

    def __str__(self):
        return "Collect and Conquer"

    def __init__(self,log_file_name,mode="a"):
        self.log_file_name=Path(log_file_name)
        self.startLocation=input(f"Start Location\n[Example]\n{Fore.red}008/{Fore.yellow}001/{Fore.cyan}310{Style.reset}\naisle/[SHELF|DOOR]/shelf location #]:").replace("/",".")

        self.log_file_name=Path(self.log_file_name.parent)/Path(f"{self.startLocation}START_{self.log_file_name.name}")
        addHeaders=False
        if mode != 'a' or not Path(self.log_file_name).exists():
            addHeaders=True
        with open(self.log_file_name,mode) as log:
            writer=csv.writer(log,delimiter=",")
            if addHeaders:
                print('Adding Headers!')
                writer.writerow(['Barcode/UPC','OrderCode/ItemCode/iSKU','TimeStamp'])
            counter=0
            while True:
                counter+=1
                line=[]
                cmd='quit'
                while True:
                    barcode=input(f"{Fore.cyan}{Style.bold}Barcode{Style.reset}[{Fore.light_blue}{Style.underline}#{cmd}{Style.reset}]: ")
                    if barcode == f"#{cmd}":
                        self.beforeQuit()
                        exit(f'{Fore.dark_orange}User{Style.reset} {Fore.light_red}{Style.bold}Quit!{Style.reset}')
                    elif barcode == "#na":
                        barcode="Not Availabl"
                    
                    TRY=[UPCA,EAN8,EAN13,Code39]
                    failed_search=0
                    for CODE in TRY:
                        try:
                            if CODE == Code39:
                                barcode=CODE(barcode,add_checksum=False)
                            else:
                                barcode=CODE(barcode)
                            print(f"{Fore.dark_sea_green_5a}{barcode}{Style.reset}:{Fore.red_3b}{CODE}{Style.reset}")
                            break
                        except Exception as e:
                            failed_search+=1
                            #print("Attempt at Encoding Failed...")
                            #print(e)
                    if failed_search != len(TRY):
                        break

                
                while True:
                    item_code=input(f"{Fore.green_yellow}{Style.underline}OrderCode/ItemCode/iSKU{Style.reset}[{Fore.red}{Style.bold}#{cmd}{Style.reset}]: ")
                    if item_code == f"#{cmd}":
                        self.beforeQuit()
                        exit(f'{Fore.dark_orange}User{Style.reset} {Fore.light_red}{Style.bold}Quit!{Style.reset}')
                    elif item_code == "#na":
                        item_code='Not_Avbl'
                    if len(item_code) != 8:
                        item_code=input(f"{Fore.light_goldenrod_2c}{Style.underline}OrderCode/ItemCode/iSKU{Style.reset}[{Fore.orange_1}{Style.bold}#{cmd}{Style.reset}]: ")
                        if item_code == f"#{cmd}":
                            exit(f'{Fore.dark_orange}User{Style.reset} {Fore.light_red}{Style.bold}Quit!{Style.reset}')
                        elif item_code == "#na":
                            item_code='Not_Avbl'

                        if len(item_code) == 8:
                            break

                    else:
                        break


                line.extend([barcode,item_code,datetime.now().timestamp()])
                writer.writerow(line)
                
                print(f"{Fore.light_red}---{Style.reset} {Fore.dark_goldenrod}endEntry{Style.reset} {Fore.green}{Style.underline}{counter}{Style.reset} {Fore.light_red}---{Style.reset}")

            


