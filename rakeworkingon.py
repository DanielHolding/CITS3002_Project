class actions:
    def __init__(self, command, isRemote, numFiles):
        self.command = command
        self.isRemote = isRemote
        self.numFiles = numFiles
        
class actionSets(actions):
    def __init__(self, numActions):
        self.numActions = numActions
        
class portAndHosts:
    def __init__(self, portAddress, numHosts, hostNames):
        self.portAddress = portAddress
        self.numHosts = numHosts
        self.hostNames = hostNames

def main():
    
    f = open("rakefile", "r")
    text = f.read()
    words = text.splitlines()
    print(words)
    print(words[0])
    print(len(words))
    
    #Creating default values for port and host
    defaultportAddress = 'default'
    defaultnumHosts = 0
    defaulthostName = 'default'
    #Initializing port and host class with default values
    portandhost = portAndHosts(defaultportAddress, defaultnumHosts, defaulthostName)
    
    #Creating variables for while loop
    arraylength = len(words) - 1
    i = 0
    
    #Processing lines in while loop below
    while (i < arraylength):
        #Removing comment lines
        if (words[i].startswith('#')):
            print("starts with hash")
            words.pop(i)
            arraylength = arraylength - 1
        #Removing empty lines
        elif (words[i] == ''):
            print("is empty line line")
            words.pop(i)
            arraylength = arraylength - 1
        #Checking if line is port number, and storing port info
        elif (words[i].startswith('PORT')):
            portnumber = words[i].split()[2]
            portandhost.portAddress = portnumber
            print(words[i])
            print(portandhost.portAddress)
            i = i+1
            arraylength = arraylength - 1
        #Checking if a line is host info, and storing that info
        elif (words[i].startswith('HOSTS')):
            hosts = words[i].split()
            hosts = hosts[2:len(hosts)]
            portandhost.hostNames = hosts
            portandhost.numHosts = len(hosts)
            print(portandhost.hostNames)
            print(portandhost.numHosts)
            i = i+1
        elif (words[i].startswith('\t')):
            print(words[i])
            print("starts with tab")
            i = i+1
        else:
            i = i+1
    
    print(words)
    print(len(words))


    
