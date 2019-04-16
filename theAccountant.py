import telnetlib
import getpass
import os, sys, csv
import argparse

parser = argparse.ArgumentParser(prog = 'The Accountant',usage='%(prog)s [options]')
parser.add_argument("-hf","--hostfile",type = argparse.FileType('r'),
        help = "Specify a hostfile in csv format. Format = IP's, port number.")
parser.add_argument("-uf","--usersfile",type = argparse.FileType('r'),
        help = "Specify a users file in csv format.")
parser.add_argument("-pf","--passfile",type = argparse.FileType('r'),
        help = "Specify a passwords file in csv format.")
parser.add_argument("-up","--userpass",type = argparse.FileType('r'),
        help = "Specify a user and password file. Format = User, password.")
args = parser.parse_args()

hostfile = args.hostfile
usersfile = args.usersfile
passfile = args.passfile
userpass = args.userpass

#For Kali Linux Telnet server
def testCreds(user, password, host, port):
    tn = telnetlib.Telnet(host = host, port = port)
    tn.read_until(b"login:")
    tn.write(user.encode('ascii')+b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii')+b"\n")
    res = tn.read_until(b"xxx", 0.5)
    if (b"Last login:") in res:
        return True
    else:
        return False

#Functions for reading CSV files
def getUsers(usersfile):
    readfile = usersfile
    readlines = readfile.readlines()
    result = []
    for line in readlines:
        result.append(line.rstrip().split("/n"))
    return result

def getPasswords(passfile):
    readfile = passfile
    readlines = readfile.readlines()
    result = []
    for line in readlines:
        result.append(line.rstrip().split("/n"))
    return result

def getUserPassword(userpass):
    readfile = userpass
    readlines = readfile.readlines()
    result = []
    for line in readlines:
        result.append(line.rstrip().split(","))
    return result

def getHostData(hostfile):
    readfile = hostfile
    readlines = readfile.readlines()
    result = []
    for line in readlines:
        result.append(line.rstrip().split(","))
    return result

# Test whether the creds worked - for user file and password file
if args.usersfile != None:
    for hd in getHostData(hostfile):
        host = hd[0]
        port = hd[1]
        passwords = getPasswords(passfile)
        for un in getUsers(usersfile):
            username = un[0]
            for pw in passwords:
                password = pw[0]
                credsValid = testCreds(username, password, host, port)
                print("{0}:{1} - {2}:{3} - {4}".format(host, port, username, password, credsValid))

# Test whether the creds worked - for user/password file
if args.userpass != None:
    for hd in getHostData(hostfile):
        host = hd[0]
        port = hd[1]
        for up in getUserPassword(userpass):
            username = up[0]
            password = up[1]
            credsValid = testCreds(username, password, host, port)
            print("{0}:{1} - {2}:{3} - {4}".format(host, port, username, password, credsValid))
