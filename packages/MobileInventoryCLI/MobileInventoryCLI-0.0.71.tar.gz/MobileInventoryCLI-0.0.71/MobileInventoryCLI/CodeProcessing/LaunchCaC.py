from MobileInventoryCLI.CodeProcessing.CollectAndConquer import CaC
from datetime import datetime
from pathlib import Path

def launch(directory=None):
    dat=datetime.now().strftime('%D-%T').replace('/','_').replace(':','_')
    if not directory:
        directory=Path('/storage/emulated/0/Download/collected/')

    if not directory.exists():
    	dir.mkdir(parents=True)
    filename=Path(f'codesandbarcodes-{dat}.csv')
    print(directory/filename)
    CaC(directory/filename,mode="w")
if __name__ == "__main__":
    launch()
