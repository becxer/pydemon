#!/usr/bin/python
#
# use to run python program forever
# @author becxer
# @email becxer87@gmail.com
#
import signal
import sys
import subprocess
import time
import os
import datetime
import json

sleep_time = 1
bashCmd = ""
now_time = 1000
last_time = 1001
run_count = 0
pydemon_log = '.pydemon.log'
pydemon_dat = '.pydemon.dat'
dat_obj = {}

def set_bashCmd():
    global bashCmd
    bashCmd = ""
    if os.path.isfile(sys.argv[1]):
        if '.sh' in sys.argv[1]:
            f = open(sys.argv[1],"r")
            bashCmd = f.read()
            f.close()
        elif '.py' in sys.argv[1]:
            bashCmd = 'python ' + sys.argv[1]
    else:
        bashCmd = sys.argv[1]

    for i in range(2,len(sys.argv)):
        bashCmd += sys.argv[i] + " "
    print bashCmd

def set_now_time(path):
    global now_time
    global dat_obj
    dirs = os.listdir(path)
    for f in dirs:
        fnow = path+'/'+f
        isIgnored = False
        for postfix in dat_obj['ignore_postfix']:
            if f.endswith(postfix) :
                isIgnored = True
                break
        for prefix in dat_obj['ignore_prefix']:
            if f.startswith(prefix) :
                isIgnored = True
                break
        if not isIgnored:
            if os.path.isdir(fnow):
                set_now_time(fnow)
            elif os.path.getmtime(fnow) > now_time:
                print fnow + " is changed"
                now_time = os.path.getmtime(fnow)

def run_cmd(bashCmd):
    print str(bashCmd)
    print "[stdout]----------------------"
    process = subprocess.Popen(bashCmd, shell=True 
                ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = ''
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            res += output
            print output.strip()
        rc = process.poll()
    output, error = process.communicate()
    print "[stderr]----------------------"
    res += error
    print error
    if process.returncode != 0 :
        print "[ERROR] process error"
    print "pydemon is watching your directory..."
    return res

def load_dat(datpath):
    if os.path.isfile(datpath):
        datf = open(datpath,'r')
        js = json.loads(datf.read())
        datf.close()
        return js
    else:
        return {'run_count':0 , \
                                'ignore_prefix' :[\
                                ".","#","~"],
                'ignore_postfix':[\
                ".swp", ".log", ".git",".dat"]}

def save_dat(obj ,datpath):
    datf = open(datpath,'w')
    json.dump(obj,datf,indent=4)
    datf.close()
    return None

def main_while():
    global dat_obj
    global now_time
    global last_time
    dat_obj = load_dat(pydemon_dat)
    while True:
        if last_time != now_time :
            
            set_bashCmd()
            
            dat_obj = load_dat(pydemon_dat)
            dat_obj['run_count'] += 1
            
            print "[#"+str(dat_obj['run_count'])+"]---------------------------"
            logf = open(pydemon_log,"a")
            logf.write("T: " +str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        +" #"+str(dat_obj['run_count'])+" Log\n")
            logf.write(run_cmd(bashCmd))
            logf.close()
            
            save_dat(dat_obj,pydemon_dat)
            
            set_now_time('.')
            last_time = now_time
        else :    
            set_now_time('.')    
        time.sleep(sleep_time)

def main():
    if len(sys.argv) < 2:
        print 'usage : ./pydemon "bash command" or your-script.sh'
        exit()
    main_while()

if __name__  == "__main__":
    main()
