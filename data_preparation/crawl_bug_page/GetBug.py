#!/usr/bin/python
import os
import re
import subprocess

bugIds = []
def prepareCookieData():
    out = subprocess.call("curl --cookie-jar cookie.data \"https://bugzilla-hostname/index.cgi?Bugzilla_login=name&Bugzilla_password=password&GoAheadAndLogIn=LogIn\" > login.txt", shell=True)        

def gerateBugFile(bugid):
    out = subprocess.call("touch bugsSample/bug_" + str(bugid) + ".txt", shell=True)
    out = subprocess.call("curl --cookie cookie.data \"https://bugzilla-hostname/show_bug.cgi?id=" + str(bugid) + "\" > bugsSample/bug_" + str(bugid) + ".txt ", shell=True)        

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        print path+' created.'
        os.makedirs(path)
        return True
    else:
        print path+' exist!'
        return False

def regxBugId(line):
    m = re.search(r'<\s*a\s.*?href\s*="show_bug\.cgi\?id=[0-9]+', line)
    if m:
        bid= re.search(r'[0-9]+',m.group(0))
        if bid:
            if bid.group(0) not in bugIds:
                print bid.group(0)
                gerateBugFile(bid.group(0))
                bugIds.append(bid.group(0))
                return True
            else:
                return False
        else:
            #print "Bug id search error!"
           return False
    else:
        #print "Bug URL search error!"
        return False

def readBugId(path):
    f = open(path)
    line = f.readline()
    count = 0
    while line:
        line = f.readline()
        isOK = regxBugId(line)
        if isOK:
            count += 1   
    f.close()
    print "Total " + str(count) + " bugs have been store!" 


        

mkpath="bugsSample"
buglistPath="buglist.txt"

# create directory where bugs situate
mkdir(mkpath)
prepareCookieData()
readBugId(buglistPath)
