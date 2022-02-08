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
    
print(lines)

USERNAME = lines[0]
HOSTNAME = lines[1]
PATH = lines[2]

#handling the arrows
def containsArrows(input):
    if (input.find("->") or input.find("->>")) == -1:
        #print("aint here chief")
        return
    
    #shelex preserves quotations
    #see echo "splitifcus maxiumus" -> output.txt
    list = shlex.split(input)

    print(list) 

    print('->' == list[1])
    
    #redirects the output of command to a file named filename. If a file with the
    #same name already exists it deletes it and creates a new one.
    
    #technically w/o an extention, it still writes the output to the given filename so w/e
    if os.path.exists(list[2]):
        os.remove(list[2])       
    if list[1] == '->':
        #creates file if doesn't exist
        file = open(list[2], 'w+')
        file.write(list[0])      
    

class BananaShell(cmd.Cmd):
    intro = 'Welcome to Banana shell.    Type help or ? to list commands.\n'
    prompt = USERNAME + '@' + HOSTNAME + '$ '
    file = None
    
    # ----- Commands -----------
    
    #for echo
    def do_echo(self, input):
        if containsArrows(input):
            return 0
        else:
            print(input)

            
        #os.system("echo {} ").format(input)
        
    def do_exit(self, input):
        subprocess.run("exit 1", shell=True, check=True)
    
 #It's boilerplate code that protects users 
 # from accidentally invoking the script when they didn't intend to   
if __name__ == '__main__':
    BananaShell().cmdloop()
