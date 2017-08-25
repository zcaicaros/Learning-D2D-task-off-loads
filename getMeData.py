from matplotlib import pyplot as plt
from datetime import timedelta as td
from time import strptime as st
import subprocess
import re

##################### Helper Function #########################################
def divide(a,b):
    avr = []
    for i in range(len(b)):
        if b[i]!=0:
            avr.append(a[i]*1.0/b[i])
        else:
            avr.append(a[i])
    return avr

##################### The list holds time intervals '00:00:00:' #########################
timeintervals=[]
for i in range(24*60/5):
    timeintervals.append(td(minutes=(i)*5))
timeintervals.append(td(minutes=1439, seconds=59, microseconds=99999))

##################### The list holds the data file name 'Userxxxxx' #####################
fname = ["" for i in range(666)]
for i in range(len(fname)):
    fname[i]="User{0:05}".format(i+1)

##################### The main part to read data and process data ####################
for n in fname[0:1]:
    acc_BL = [0 for i in range(len(timeintervals)-1)]
    timestamps_BL = [0 for i in range(len(timeintervals)-1)]
    acc_freeCPU = [0 for i in range(len(timeintervals)-1)]
    timestamps_freeCPU = [0 for i in range(len(timeintervals)-1)]
    acc_wifiRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_wifiRSSI = [0 for i in range(len(timeintervals)-1)]
    acc_btRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_btRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_wifiOn = [0 for i in range(len(timeintervals)-1)]
    timestamps_btOn = [0 for i in range(len(timeintervals)-1)]

    # helper variables for counting WIFI and BT on
    eachlinecount_wifi = [0 for i in range(len(timeintervals)-1)]
    eachlinecount_bt = [0 for i in range(len(timeintervals)-1)]

    # helper variables for RSSI
    avrBTrssi = [0 for i in range(len(timeintervals)-1)]
    avrWIFIrssi = [0 for i in range(len(timeintervals)-1)]
############################ find time objects #################################
    g = subprocess.Popen(['grep','-E', 'bluetooth\|found|wifi\|connected|bluetooth\|found.*rssi|wifi\|connected.*rssi|battery\|level|timeinstates', '/usr/666Users/'+n], stdout = subprocess.PIPE)
    lines = g.stdout.readlines()
    for i in range(len(lines)):
        try:
            tmatch = re.search('T(.+?)\.', lines[i]).group(1)
        except :
            continue
        try:
            x = st(tmatch .split(', ')[0], '%H:%M:%S')# convert the string to format timedelta
            time_currentline = td(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec)
            total_minute = int(time_currentline.total_seconds()/60)
            timedelta_min = td(minutes=total_minute)
        except :
            print "failed to convert string to timedelta object for line: " + str(i)
            continue
############################ find  Battery Level #################################            
        if 'battery' in lines[i]:
            BLmatch = re.findall(r"(?<!\d)\d{1}(?!\d)$|(?<!\d)\d{2}(?!\d)$|(?<!\d)\d{3}(?!\d)$", lines[i])       
            BL = int(BLmatch[0])
            for j in range(len(timeintervals)-1):
                if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                    acc_BL[j]+=BL
                    timestamps_BL[j]+=1
            avrBL = divide(acc_BL, timestamps_BL)
############################ find free CUP time #################################
        if 'timeinstates' in lines[i]:
            lis =  re.findall('timeinstates\;(.+?)$', lines[i])
            temp_numbers_perDataLine=re.findall('\d+', lis[0])
            toint = map(int, temp_numbers_perDataLine)
            totalTimeEachline=sum(toint[1:-2:2])
            for j in range(len(timeintervals)-1):
                if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                    acc_freeCPU[j]+=totalTimeEachline
                    timestamps_freeCPU[j]+=1
            avrFreeCPUTime = divide(acc_freeCPU, timestamps_freeCPU)
############################ find wifi RSSI #####################################
        if all(x in lines[i] for x in ['wifi','rssi']):
            wifi_rssimatch = re.findall(r"rssi\;(.+?)$", lines[i])
            wifirssi = int(wifi_rssimatch[0])
            for j in range(len(timeintervals)-1):
                if wifirssi >= -999:
                    if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                        acc_wifiRSSI[j]+=wifirssi
                        timestamps_wifiRSSI[j]+=1
            avrWIFIrssi = divide(acc_wifiRSSI, timestamps_wifiRSSI)
############################ find bluetooth rssi objects ############################
        if all(x in lines[i] for x in ['bluetooth','rssi']):
            print lines[i]
            print 'yes'
            bt_rssimatch = re.findall(r"rssi\;(.+?)$", lines[i])
            btrssi = int(bt_rssimatch[0])
            for j in range(len(timeintervals)-1):
                if btrssi >= -999:
                    if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                        acc_btRSSI[j]+=btrssi
                        timestamps_btRSSI[j]+=1
            avrBTrssi = divide(acc_btRSSI, timestamps_btRSSI)
############################ find wifi and bluetooth connected #######################            
        if all(x in lines[i] for x in ['wifi','connected']):
            for j in range(len(timeintervals)-1):
                if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                    eachlinecount_wifi[j]+=1                    
        if all(x in lines[i] for x in ['bluetooth','found']):
            print no
            for j in range(len(timeintervals)-1):
                if (timedelta_min>=timeintervals[j] and timedelta_min<timeintervals[j+1]):
                    eachlinecount_bt[j]+=1            
    for k in range(len(eachlinecount_wifi)):
        if eachlinecount_wifi[k] != 0:
            timestamps_wifiOn[k]+=1
    for k in range(len(eachlinecount_bt)):
        if eachlinecount_bt[k] != 0:
            timestamps_btOn[k]+=1
########################### write the data to file ###################################
    h = open('/usr/666Users/pythonprograms/fun/data/666/getDataEachUser/' +n, 'w')
    for i in range(288):
        h.write(str(avrBL[i]) + "                                        " + str(avrFreeCPUTime[i]) + "                                        " + str(avrWIFIrssi[i]) + "                                        " + str(avrBTrssi[i]) + "                                        " + str(timestamps_wifiOn[i]) + "                                        "+ str(timestamps_btOn[i]) + "\n")
    



'''
print avrBL
print avrFreeCPUTime
print avrWIFIrssi
print avrBTrssi
print timestamps_wifiOn
print timestamps_btOn
'''
'''
    acc_BL = [0 for i in range(len(timeintervals)-1)]
    timestamps_BL = [0 for i in range(len(timeintervals)-1)]
    acc_freeCPU = [0 for i in range(len(timeintervals)-1)]
    timestamps_freeCPU = [0 for i in range(len(timeintervals)-1)]
    acc_wifiRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_wifiRSSI = [0 for i in range(len(timeintervals)-1)]
    acc_btRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_btRSSI = [0 for i in range(len(timeintervals)-1)]
    timestamps_wifiOn = [0 for i in range(len(timeintervals)-1)]
    timestamps_btOn = [0 for i in range(len(timeintervals)-1)]
'''

