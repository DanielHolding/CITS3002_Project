import select
import time
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


class host:
    def __init__(self, hostname, portnumber):
        self.hostname = hostname
        self.hostnumber = portnumber

def main():
    

    f = open("Rakefile9", "r")
    text = f.read()
    words = text.splitlines()
    #print(words)
    #print(words[0])
    #print(len(words))
    actionset = []
    no_sets = 0

    hostset = []

    action = []
    remoteactions = []
    files = []
    
    #Creating default values for port and host
    defaultportAddress = 'default'
    defaultnumHosts = 0
    defaulthostName = 'default'
    #Initializing port and host class with default values
    
    #Creating variables for while loop
    arraylength = len(words) - 1
    i=0

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
            defaultportAddress = int(portnumber)
            #print(words[i])
            i = i+1 
        #Checking if a line is host info, and storing that info
        elif (words[i].startswith('HOSTS')):
            hosts = words[i].split()
            hosts = hosts[2:len(hosts)]
            for j in range(len(hosts)):
                hsplit = hosts[j].split(':')
                if (len(hsplit) == 1):
                    hostset.append(host(hsplit[0], defaultportAddress))
                elif (len(hsplit) == 2):
                    hostset.append(host(hsplit[0], int(hsplit[1])))
            i = i+1
        #
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

    
    

        
    
    for aset in actionset:
        for action in aset.actionlist:
            rd = []
            socks = []

            for h in range(len(hostset)):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socks.append(sock)
                print(hostset[h].hostname)
                print(hostset[h].hostnumber)
                sock.connect((hostset[h].hostname, hostset[h].hostnumber))
                newaction = 'quote\0'
                message = newaction.encode('ascii')
                sock.sendall(message)
                rd.append(sock)

    

            wd = []
            xd = []

            readready =[]
            writeready = []
            xready = []

            lowest = 1000

            while(1):
                readready, writeready, xready = select.select(rd,[],[])
                if(len(readready) == len(rd)):
                    break
       
    
            for read in readready:
                data = read.recv(1024)
                message = data.decode('ascii')
                print(read)
                quote = int(message[0:2])
                print(quote)
                if(quote<lowest):
                    lowest = quote
                    executor = read.getpeername()
                    read.close()
                else:
                    read.close()

            print(executor)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(executor)
            newfile = 'File: ' + action.files + '\n'
            f1 = open(action.files,'r')
            fileopen = f1.read()
            message = fileopen.splitlines()
    
            for j in range(len(message)):
                newfile += message[j]+'\n'
            
            newfile += '\0'
            
            print(newfile)
            
            message_bytes = newfile.encode('ascii')
            sock.sendall(message_bytes)
            sock.close()
        

        



        #ret = sock.recv(10)
        #print(ret)
        #filename = ret.decode('ascii')
        #TODO get rid of trailing /0 bytes filename = filename[:len(filename)-1]
        #print(filename)
        #print(len(ret))
        #f2 = open(filename, "a")
        #f2.write("test")
        #f2.close()




    #for i in range(len(actionset)):
            

            #for j in range(len(portandhost.hostNames)):
             #   s.connect((portandhost.hostNames[j], portandhost.portAddress))
              #  newfile = actionset[i].actionlist[0].command + '\0'
               # print(newfile)
               # message_bytes = newfile.encode('ascii')
               # s.sendall(message_bytes)

            


            #f1 = open(actionset[i].actionlist[0].files,'r')
            #fileopen = f1.read()
            #message = fileopen.splitlines()
            #newfile = ""
            #newfile += actionset[i].actionlist[0].files + '\n'

            #for j in range(len(message)):
            #    newfile += message[j]+'\n'
            #newfile += '\0'
            #print(newfile)


            #message_bytes = newfile.encode('ascii')
            #s.sendall(message_bytes)
            #data = s.recv(1024)
        
        #for j in range(len(remoteactions)):
         #   message = (remoteactions[j]+'\n').encode('ascii')
          #  s.sendall(message)
        



    #print(words)
    #print(len(words))
main()
