from barcode import Code39,UPCA
from barcode.writer import ImageWriter as iw
from PIL import Image
import csv
from colored import Fore,Back,Style
from pathlib import Path

#C39='32801110'
#UPC='12345678901'
codefile=None

EXIT="#quit"
while True:
    codefile=input(f"codes csv[{EXIT}]: ")
    if Path(codefile).exists():
        break
    else:
        print(f"{codefile} does not exist!")
    
with open(codefile,"r") as files:
    try:
        reader=csv.reader(files,delimiter=",")
        for num,line in enumerate(reader):
            if num > 0:
                C39=line[1]
                UPC=line[0]
            
                code39=Code39(C39,add_checksum=False,writer=iw()).save("code39")
                upca=UPCA(UPC,writer=iw()).save("upca")
                with Image.open(code39) as c39, Image.open(upca) as upc:
                    with Image.new(mode="RGB",size=(c39.size[0]+upc.size[0],upc.size[1]),color=(255,255,255)) as final:
                        print(c39.size,upc.size,final.size)
                        
                        final.paste(c39,(0,0))
                        final.paste(upc,(final.size[0]-c39.size[0],0))
                        final.save(f"{C39}_{UPC}.png")
                Path(code39).unlink()
                Path(upca).unlink()
            else:
                print(f"{Fore.red}First Line is a header...{Style.reset}")

    except Exception as e:
        print(e)
        if Path('code39.png').exists():
            Path('code39.png').unlink()
        if Path('upca.png').exists():
            Path('upca.png').unlink()
