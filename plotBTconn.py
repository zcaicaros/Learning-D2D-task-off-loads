from matplotlib import pyplot as plt
from datetime import timedelta as td
from time import strptime as st
import subprocess
import re

##################### The list holds time intervals '00:00:00:' #########################
timeintervals=[]
for i in range(24*60/5):
    timeintervals.append(td(minutes=(i)*5))
timeintervals.append(td(minutes=1439, seconds=59, microseconds=99999))

##################### The WifiRssi level list and the list counting # of users for each interval ###
accvalues_interval = [0 for i in range(len(timeintervals)-1)]
Itervalrecord_uCONN = [0 for i in range(len(timeintervals)-1)]

##################### The list holds the data file name 'Userxxxxx' #####################
fname = ["" for i in range(666)]
for i in range(len(fname)):
    fname[i]="User{0:05}".format(i+1)

##################### The list holds the data file name 'Userxxxxx' #####################
for n in fname[:]:
    temp_accvalues_interval = [0 for i in range(len(timeintervals)-1)]
    f = subprocess.Popen(['grep', '-E', 'bluetooth\|found', '/usr/666Users/'+n], stdout = subprocess.PIPE)     # subproess grep the file and retrn a file object stored in f
    lines = f.stdout.readlines()
    for i in range(len(lines)):
        try:
            tmatch = re.search('T(.+?)\.', lines[i]).group(1)# the regex searching for a time string eachline
        except :# except handling
            #print (can\'t find time 00:00:00 in line: , i )# apply error handling
            continue
        try:
            x = st(tmatch .split(', ')[0], '%H:%M:%S')# convert the string to format timedelta
            time_currentline = td(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec)
            total_minute = int(time_currentline.total_seconds()/60)
            timedelta_min = td(minutes=total_minute)
        except :
            print 'failed to convert string to timedelta object for line: '+ str(i)
        for j in range(len(timeintervals)-1):
            if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                temp_accvalues_interval[j]+=1

    for k in range(len(temp_accvalues_interval)):
        accvalues_interval[k]+=temp_accvalues_interval[k]
        if temp_accvalues_interval[k]!=0:
            Itervalrecord_uCONN[k]+=1
        
    print '\n'
    print n + " has loaded and current Itervalrecord_uCONN is : "
    print Itervalrecord_uCONN

h = open('/usr/666Users/pythonprograms/fun/data/666/BT_on/666BT_on.txt', 'w')
for num in accvalues_interval:
    h.write("%s\n" % num)
e = open('/usr/666Users/pythonprograms/fun/data/666/BT_on/666Dividor_BT_on.txt', 'w')
for num in Itervalrecord_uCONN:
    e.write("%s\n" % num)
