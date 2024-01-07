from datetime import datetime,timedelta
import sys,os
from time import sleep
from colored import Fore,Style
from threading import Thread
import multiprocessing

def timer(hours,minutes,seconds):
    now=datetime.now()
    future=datetime.now()+timedelta(hours=hours,minutes=minutes,seconds=seconds)
    print(f"{Fore.cyan}Now{Style.reset} : {now}\n{Fore.red}Future{Style.reset} : {future}")
    while now <= future:
        os.sys.stdout.write('\b'*os.get_terminal_size()[0])
        os.sys.stdout.flush()
        os.sys.stdout.write(datetime.now().ctime())
        os.sys.stdout.flush()
        sleep(1)
        now=datetime.now()
    os.sys.stdout.write("\n")
    os.sys.stdout.flush()

def displayThread(start):
    now=datetime.now()
    while True:
        os.sys.stdout.write('\b'*os.get_terminal_size()[0])
        os.sys.stdout.flush()
        sys.stdout.write(str(now.ctime())+f" {Fore.yellow}Elapsed{Style.reset}: "+str(datetime.now()-start))
        sys.stdout.flush()
        sleep(1)
        now=datetime.now()

def elapsed():
    now=datetime.now()
    print(f"{Fore.cyan}Start{Style.reset}:{now}")
    print(f"{Fore.green}Use {Style.reset}{Fore.light_blue}<Enter>,{Fore.light_blue}<Return>{Style.reset},{Fore.light_blue}Ctrl+D{Style.reset} to exit.")
    stop=None
    disp=multiprocessing.Process(target=displayThread,args=(now,))
    disp.start()
    while True:
        line=sys.stdin.readline()
        if line in ["","\n"," "]:
            stop=datetime.now()
            disp.terminate()
            break 
        os.sys.stdout.write('\b'*os.get_terminal_size()[0])
        os.sys.stdout.flush()
        print(now.ctime())
        sleep(1)
        now=datetime.now()
    print("\n")
    if stop != None:
        el=stop-now
        print(f"{Fore.green_yellow}Elapsed Time is{Style.reset}: {el}")
        print(f"{Fore.yellow}Stop DateTime{Style.reset}: {stop}")
    else:
        raise Exception("stop var was None")

