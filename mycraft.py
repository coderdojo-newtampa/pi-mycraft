# mycraft.py
#
# Want to play networked minecraft with your Raspberry Pi and have each
# user (and server) have their own names? Then this script is for you
# (or have fun with manually editing with a Hex editor :-( )
#
# This script, prompts the user for a username to use in the game world
# After the first run, the script caches the name in a file called "default"
# so in subsequent runs the user doesn't have to type it again
#
# The script will ensure the name is exactly 7 characters long, and
# replaces the "StevePi" name from the executable
#
# The script with modify the binary file, and copy its contents to a local
# directory called .mycraft
#
# At the end, the script will then start the modified minecraft binary
#

import os

version="0.3"

print("Running mycraft ("+version+")")
print("------------------------------")

subdirs = ["api", "data"]
minedir="/opt/minecraft-pi"
mydir=".mycraft"
mymine=mydir+"/mycraft-pi-me"
defaultfile=mydir+"/default"
encoding="iso-8859-1"

done = False
defaultname = ""

if not os.path.exists(mydir):
    os.makedirs(mydir)

if os.path.exists(defaultfile):
    with open(defaultfile, "r") as input_file:
        defaultname = str(input_file.read())
     
prompt = "Enter your username "

if (len(defaultname) > 0):
    prompt += "["+defaultname+"] "

while not done:
    name = input(prompt +"> ")

    if (len(name) == 0):
        name = defaultname

    # Ensures lengh 7
    # The replace is not doing anything for now, it looked like
    # minecraft didn't like spaces in the name ... but it seems to work
    name = name.ljust(7)[:7].replace(" ", " ")

    if (len(name.strip()) > 0):
        done = True

print("Thanks ...")

with open(defaultfile, "w+") as output_file:
    output_file.write(name)

for subdir in subdirs:
    link = mydir + "/" + subdir
    if not os.path.exists(link):
        os.symlink(minedir + "/" + subdir, link)

with open(minedir+"/minecraft-pi", "rb") as input_file:
    s=str(input_file.read(), encoding)

s=s.replace("StevePi", name)

with open(mymine, "wb") as output_file:
    output_file.write(s.encode(encoding))

os.chmod(mymine, 0o775)

print("Starting minecraf as user ["+name+"]")

os.system(mymine)
