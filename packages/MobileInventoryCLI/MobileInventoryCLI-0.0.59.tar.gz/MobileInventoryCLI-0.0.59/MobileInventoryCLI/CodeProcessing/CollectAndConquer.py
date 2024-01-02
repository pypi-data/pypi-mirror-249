import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
class CaC:
    def __str__(self):
        return "Collect and Conquer"

    def __init__(self,log_file_name,mode="a"):
        self.log_file_name=log_file_name
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
                barcode=input(f"{Fore.cyan}{Style.bold}Barcode{Style.reset}[{Fore.light_blue}{Style.underline}#{cmd}{Style.reset}]: ")
                if barcode == f"#{cmd}":
                    exit(f'{Fore.dark_orange}User{Style.reset} {Fore.light_red}{Style.bold}Quit!{Style.reset}')

                item_code=input(f"{Fore.green_yellow}{Style.underline}OrderCode/ItemCode/iSKU{Style.reset}[{Fore.red}{Style.bold}#{cmd}{Style.reset}]: ")
                if item_code == f"#{cmd}":
                    exit(f'{Fore.dark_orange}User{Style.reset} {Fore.light_red}{Style.bold}Quit!{Style.reset}')

                line.extend([barcode,item_code,datetime.now().timestamp()])
                writer.writerow(line)
                
                print(f"{Fore.light_red}---{Style.reset} {Fore.dark_goldenrod}endEntry{Style.reset} {Fore.green}{Style.underline}{counter}{Style.reset} {Fore.light_red}---{Style.reset}")



