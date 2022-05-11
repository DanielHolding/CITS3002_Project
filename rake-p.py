import socket 
import base64


class actions:
    def __init__(self, command, filenames):
        self.command = command
        self.files = filenames
        
class actionSets(actions):
    def __init__(self, numActions):
        self.numActions = numActions
        self.actionlist = []

class portAndHosts:
    def __init__(self, portAddress, numHosts, hostNames):
        self.portAddress = portAddress
        self.numHosts = numHosts
        self.hostNames = hostNames

def main():
    
    

    f = open("Rakefile1", "r")
    text = f.read()
    words = text.splitlines()
    #print(words)
    #print(words[0])
    #print(len(words))
    actionset = []
    no_sets = 0

    action = []
    remoteactions = []
    files = []
    
    #Creating default values for port and host
    defaultportAddress = 'default'
    defaultnumHosts = 0
    defaulthostName = 'default'
    #Initializing port and host class with default values
    portandhost = portAndHosts(defaultportAddress, defaultnumHosts, defaulthostName)
    
    #Creating variables for while loop
    arraylength = len(words) - 1
    i = 0
    j = 0
    
    #Processing lines in while loop below
    while (i < arraylength+1):
        #Removing comment lines
        if (words[i].startswith('#')):
            #print("starts with hash")
            words.pop(i)
            arraylength = arraylength - 1
        #Removing empty lines
        elif (words[i] == ''):
            #print("is empty line line")
            words.pop(i)
            arraylength = arraylength - 1
        #Checking if line is port number, and storing port info
        elif (words[i].startswith('PORT')):
            portnumber = words[i].split()[2]
            portandhost.portAddress = portnumber
            #print(words[i])
            #print(portandhost.portAddress)
            i = i+1
            arraylength = arraylength - 1
        #Checking if a line is host info, and storing that info
        elif (words[i].startswith('HOSTS')):
            hosts = words[i].split()
            hosts = hosts[2:len(hosts)]
            portandhost.hostNames = hosts
            portandhost.numHosts = len(hosts)
            #print(portandhost.hostNames)
            #print(portandhost.numHosts)
            i = i+1

        elif (words[i].startswith('actionset')):
            actionset.append(actionSets(0))
            no_sets = no_sets + 1
            i = i+1

        elif (words[i].startswith('\t') and not words[i].startswith('\t\t')):
            if(words[i].startswith('\tremote-')):
                if(i<arraylength and words[i+1].startswith('\t\t')):
                    actionset[no_sets-1].actionlist.append(actions(words[i][8:],words[i+1][11:]))
                    i = i+1
                    #print(words[i][8:])
                   # print(words[i+1][11:])
                else:
                    actionset[no_sets-1].actionlist.append(actions(words[i][8:],""))
                 #   print(words[i][8:])
            else:
                if(i<arraylength and words[i+1].startswith('\t\t')):
                    actionset[no_sets-1].actionlist.append(actions(words[i][1:],words[i+1][11:]))
                    i = i+1
                else:
                    actionset[no_sets-1].actionlist.append(actions(words[i][1:],""))
                    action.append(actions(words[i][1:],""))
                #print(words[i][1:])
            i = i+1

        elif (words[i].startswith('\t\t')):
            files.append(words[i][11:])
            print(words[i][11:])
            i = i+1
        else:
            i = i+1



    for i in range(len(actionset)):
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 9000))
            if(actionset[i].actionlist[0].files == "")
                break
            f1 = open(actionset[i].actionlist[0].files,'r')
            fileopen = f1.read()
            message = fileopen.splitlines()
            newfile = ""
            newfile += actionset[i].actionlist[0].files + '\n'

            for j in range(len(message)):
                newfile += message[j]+'\n'
            newfile += '\0'
            print(newfile)


            message_bytes = newfile.encode('ascii')
            s.sendall(message_bytes)
        
        #for j in range(len(remoteactions)):
         #   message = (remoteactions[j]+'\n').encode('ascii')
          #  s.sendall(message)
        



    #print(words)
    #print(len(words))

main()
    
