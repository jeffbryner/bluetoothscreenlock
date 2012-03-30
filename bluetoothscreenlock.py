#!/usr/bin/python2

#2012 jeff bryner 
#@p0wnlabs
#
#Simple python script to ping a bluetooth device and lock the screen using xscreensaver when it goes away
#Requires pybluez library
#
#

import os
import sys
import time 
import bluetooth

DEFAULT_TIMEOUT = 5                                 # time between searches for device in seconds 
DEFAULT_LOCK_COMMAND = 'xscreensaver-command -lock' # The command to run when the device is out of range
DEFAULT_MISSED_PINGS = 3                            # threshold for missed out of range/pings before we lock
VERBOSE=False

if len(sys.argv) < 2:
    print("usage bluetoothscreenlock.py <btaddr>")
    sys.exit(1)

btaddr= sys.argv[1]
deviceInRange=True
screenLocked=False
hitcount=0


if VERBOSE: 
    print("monitoring bluetooth device address: " +  btaddr)

while True:
    btsocket=bluetooth.BluetoothSocket(bluetooth.L2CAP)
    if VERBOSE:
        print("searching for device...")
    #lame method relying on non-python commands ;-]
    #retval = os.system('l2ping -s 1 -c 1 ' + btaddr + ' > /dev/null')
    try:
        btsocket.connect((btaddr,3))
        if btsocket.send("hey"):
            if VERBOSE: 
                print("found device..")
            if not deviceInRange:
                os.system("alsaplayer -q back.wav")
            deviceInRange=True
            hitcount=0
            screenLocked=False
            btsocket.close()        
    except bluetooth.btcommon.BluetoothError as e:
        if VERBOSE:
            print("no device...")
        deviceInRange=False
        hitcount+=1     

    if hitcount  > DEFAULT_MISSED_PINGS and not screenLocked:
        print("Locking screen at: " + time.ctime())
        os.system(DEFAULT_LOCK_COMMAND)
        screenLocked=True        
    time.sleep(DEFAULT_TIMEOUT)
