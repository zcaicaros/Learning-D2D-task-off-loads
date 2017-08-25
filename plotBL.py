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

##################### The battery level list and the list counting # of users for each interval ####
accvalues_interval = [0 for i in range(len(timeintervals)-1)]
Itervalrecord_uBL = [0 for i in range(len(timeintervals)-1)]

##################### The list holds the data file name 'Userxxxxx' #####################
fname = ["" for i in range(666)]
for i in range(len(fname)):
    fname[i]="User{0:05}".format(i+1)

##################### The main part to read data and process data ####################
for n in fname[:]:
    temp_accvalues_interval = [0 for i in range(len(timeintervals)-1)] # accvalues for each user
    count_timestamps_eachinterval = [0 for i in range(len(timeintervals)-1)] # count time stamps in interv
    g = subprocess.Popen(['grep', 'battery|level', '/usr/666Users/'+n], stdout = subprocess.PIPE)
    lines = g.stdout.readlines() # subproess grep the file and retrn a file object stored in g
    for i in range(len(lines)):
        try:
            BLmatch = re.findall(r"(?<!\d)\d{1}(?!\d)$|(?<!\d)\d{2}(?!\d)$|(?<!\d)\d{3}(?!\d)$", lines[i])
            lv = int(BLmatch[0])
        except :# except handling
            print ('can\'t find patter in line: ', index(i))# apply error handling
            continue        
        try:
            tmatch = re.search('T(.+?)\.', lines[i]).group(1)# the regex searching for a time string eachline
        except :# except handling
            print ('can\'t find time 00:00:00 in line: ', i )# apply error handling
            continue
        try:
            x = st(tmatch .split(', ')[0], '%H:%M:%S')# convert the string to format timedelta
            time_currentline = td(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec)
            total_minute = int(time_currentline.total_seconds()/60)
            timedelta_min = td(minutes=total_minute)
        except :
            print ("failed to convert string to timedelta object for line: ", i)
            continue
        for j in range(len(timeintervals)-1):
            if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                temp_accvalues_interval[j]+=lv
                count_timestamps_eachinterval[j]+=1
    for k in range(len(temp_accvalues_interval)):
        if temp_accvalues_interval[k] != 0:
            Itervalrecord_uBL[k]+=1
    
    for i in range(len(temp_accvalues_interval)):
        if temp_accvalues_interval[i]!=0:
            temp_accvalues_interval[i] /= count_timestamps_eachinterval[i]
            accvalues_interval[i]+=temp_accvalues_interval[i]


    
    print '\n'
    print n + " has loaded and current BLlevel is : "
    print accvalues_interval
    

h = open('/usr/666Users/pythonprograms/fun/data/666/666BL.txt', 'w')
for num in accvalues_interval:
    h.write("%s\n" % num)
e = open('/usr/666Users/pythonprograms/fun/data/666/Dividor_666BL.txt', 'w')
for num in Itervalrecord_uBL:
    e.write("%s\n" % num)

