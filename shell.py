from datetime import datetime
from string import join

import cmd, sys, os
import subprocess
import shlex


#https://docs.python.org/3/library/cmd.html
#https://danishpraka.sh/2018/09/27/shell-in-python.html


#i have to read some stupid input file
# read 1: username
# read 2: host name
# read 3: PATH file

with open("user_input.txt") as file:
    lines = [line.rstrip() for line in file]
    
#Print out all the lines read by the shell.    
print(lines)

#Global variables containing the user data.
USERNAME = lines[0]
HOSTNAME = lines[1]
PATH = lines[2]

#Handling arrows.
def containsArrows(input):
    if (input.find("->") or input.find("->>")) == -1:
        #print("aint here chief")
        return 0
    
    list = shlex.split(input)
    if (list[len(list)-2] == '->'): #Check if there is a file specified, not just ->
        return list[len(list)-1] #return the output filename.. (last argument)
    
    return 0

def cleanLine(input):
    if (input.find("->") or input.find("->>")) == -1:
        return input;
    
    list = shlex.split(input)
    if (list[len(list)-2] == '->'): #Check if there is a file specified, not just ->
        del list[len(list)-1];
        del list[len(list)-1];
        return " ".join(list);
    
    return input
   

class BananaShell(cmd.Cmd):
    intro = 'Welcome to Banana shell.    Type help or ? to list commands.\n'
    prompt = USERNAME + '@' + HOSTNAME + '$ '
    file = None
    
    # ---- Configurations ------
    
    def preloop(self):
        cmd.Cmd.preloop(self)  # # sets up command completion
        self._output = "";
        
    def postcmd(self, stop, line):
        self._output = "";
        return stop
        
    #Validate command before excution. (Can be used to check for -> or &)
    def precmd(self, line):
        checkArrows = containsArrows(line);
        if(checkArrows != 0): #Exists a filename after the ->
            self._output = checkArrows;

        return cmd.Cmd.precmd(self, line)
    
    # ----- Commands -----------
    
    #for echo
    def do_echo(self, input):
        if(self._output != ""): #If an output is specified
            if os.path.exists(self._output):
                os.remove(self._output)       
            file = open(self._output, 'w+')
            file.write(cleanLine(input))
        else:  
            print(input)
        
    #for datetime        
    def do_datetime(self, input):
        outputStr = datetime.now().strftime("%B %d, %Y, %H:%M:%S");
        
        if(self._output != ""): #If an output is specified
            if os.path.exists(self._output):
                os.remove(self._output)       
            file = open(self._output, 'w+')
            file.write(outputStr)
        else:
            print(outputStr)
            
    def do_exit(self, input):
        subprocess.run("exit 1", shell=True, check=True)
    
 #It's boilerplate code that protects users 
 # from accidentally invoking the script when they didn't intend to   
if __name__ == '__main__':
    BananaShell().cmdloop()
