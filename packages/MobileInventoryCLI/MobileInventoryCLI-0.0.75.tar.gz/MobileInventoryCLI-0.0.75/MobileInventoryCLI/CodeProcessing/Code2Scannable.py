import csv,os,sys
from barcode import EAN8,UPCA
from barcode.writer import ImageWriter
from pathlib import Path
from colored import Fore,Style

class Code2Scannable:
    def __init__(self,filename=Path("scannable.csv"),):
        self.filename=filename
        self.dir=Path("collected")
        if not self.dir.exists():
            self.dir.mkdir()
        with self.filename.open("r") as ifile:
            reader=csv.reader(ifile,delimiter=',')
            duplicates=0
            for num,line in enumerate(reader):
                if num > 0:
                    for c in [UPCA,EAN8]:
                        print(c,line)
                        try:
                            if len(line) >= 1:
                                x=c(line[0],writer=ImageWriter())
                                print(f"{Fore.green}{x}{Style.reset} {Fore.red}{num}{Style.reset}")
                                p=self.dir/Path(line[0]+".png")
                                if p.exists():
                                    duplicates+=1
                                    print(f"{Fore.yellow}Overwriting {p}{Style.reset}{Fore.green_yellow} {duplicates}{Style.reset}")

                                x.save(str(self.dir/Path(line[0])))
                                break
                        except Exception as e:
                            print(e,c,line)
if __name__ == "__main__":
    Code2Scannable()
