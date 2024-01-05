from colored import Fore, Back, Style

class Parser:
    code=None
    def __init__(self,code=None):
        if code != None:
            self.code=code

        else:
            while True:
                self.code=input("wifi code[b/q/data]: ")
                if self.code in ['q','quit']:
                    exit("user quit!")
                elif self.code in ['b','back']:
                    return
                else:
                    break
        self.processCode()
        self.printCode()

    def processCode(self):
        self.header="WIFI:"
        self.code.replace(self.header,'')
        self.code_split_fields=self.code.split(";")
        self.code_as_dict={}

        for line in self.code_split_fields:
            l=line.split(":")
            if len(l) > 1:
                #print(l)
                if l[0] == 'WIFI':
                    self.code_as_dict[l[0]]=l[-1]
                else:
                    #print(l)
                    if l[0] == 'T':
                        l[0]='Type'
                    elif l[0] == 'P':
                        l[0] = "Password"
                    elif l[0] == 'H':
                        l[0]="Hidden"
                    elif l[0]=="WIFI":
                        l[0]="WirelessNameString"
                    self.code_as_dict[l[0]]=l[1]
    def printCode(self):
        for k in self.code_as_dict.keys():
            print(Fore.red+k+Style.reset,":",Fore.green+self.code_as_dict[k]+Style.reset)
if __name__ == "__main__":        
    Parser()
