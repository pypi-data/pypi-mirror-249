from colored import Fore,Style,Back
import time
import sys
import random
msg="For Irene... Written Using Python 3.10 on Manjaro Linux"
def printHeader(msg):
    print()
    count=0
    while count <=len(msg):
        sys.stdout.write(Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))+"="+Style.reset)
        sys.stdout.flush()
        count+=1
        t=random.random()
        while t > 0.1:
            t=random.random()
        time.sleep(t)
    print()
printHeader(msg)
for char in msg:
    sys.stdout.write(char)
    sys.stdout.flush()
    t=random.random()
    while t > 0.2:
        t=random.random()
    time.sleep(t)
printHeader(msg)
h="""Happy New Year, We hope to see you back soon, and well ;)
Change is a Good Thing We All Need it. 
If Day is for You then, then may the sun shine golden upon
you motherly smile.
"""
sys.stdout.write(Style.bold)
sys.stdout.flush()
count_r=30
count_g=20
count_b=60
for char in h:
    count_r+=5
    count_g+=10
    count_b+=2
    if count_r > 245:
        count_r=30
    if count_g > 245:
        count_g=20
    if count_b > 245:
        count_b=60
    sys.stdout.write(Fore.rgb(count_r,count_g,count_b)+char+Style.reset)
    sys.stdout.flush()
    t=random.random()
    while t > 0.2:
        t=random.random()
    time.sleep(t)
time.sleep(0.2)
sys.stdout.write(" "+Style.blink+Style.underline+Fore.RED_1+"\nK4R1-FZN!"+Style.reset)
sys.stdout.flush()
printHeader(msg)

