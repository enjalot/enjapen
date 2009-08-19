#
#  enjapenAppDelegate.py
#  enjapen
#
#  Created by Ian Johnson on 1/24/08.
#  Copyright 2008. All rights reserved.
#

from Foundation import *
from AppKit import *

import time

import objc
import WiiMote
from objc import IBOutlet, IBAction

class enjapenAppDelegate(NSObject):
    discovery = objc.ivar('discovery')
    remote = objc.ivar('wii')
    canvas = IBOutlet()
    calibrating = False
    
    def init(self):
        self = super(enjapenAppDelegate, self).init()
        if self:
            self.discovery = WiiMote.WiiRemoteDiscovery.new()
            #disc = WiiMote.wii_remote_discovery_delegate.new()
            self.discovery.setDelegate_(self)
            
        return self
        
    @IBAction
    def startDiscovery_(self,sender):
        print "discovering..."
        self.discovery.start()
        self.canvas.mouseMode = True

    @IBAction    
    def stopDiscovery_(self,sender):
        self.discovery.stop()
        self.discovery.close()
        print "stopped discovering!"
        
    @IBAction
    def disconnect_(self,sender):
        self.remote.closeConnection()
        print "disconnected!"
        self.canvas.mouseMode = False
        
    @IBAction
    def calibrate_(self,sender):
        #calibrate the wiimote
        print "lets calibrate!"
        self.canvas.calibrate()
    
    @IBAction
    def stopCalibrating_(self, sender):
        self.canvas.stopCalibrating()

    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        
    #This gives us access to the wiiremote when discovered
    def WiiRemoteDiscovered_(self, remote):
        print "discovered!"
        self.remote = remote.retain()
        print "stored"
        delegate = wii_remote_delegate_extended.new()
        #this is our custom canvas class for drawing on!
        print "lets set the canvas"
        delegate.setCanvas(self.canvas)
        print "canvas set"
        self.remote.setDelegate_(delegate)
        print "delegate set"
        self.remote.setIRSensorEnabled_(True)
        print "ir sensor enabled"
        #self.remote.setMotionSensorEnabled_(True)
        #print "motion sensor enabled"
        self.remote.setLEDEnabled1_enabled2_enabled3_enabled4_(True, False, False, True)
        print "led's fixed up"
        
    def willStartWiimoteConnections(self):
        print "starting wiimote connection"
    def WiiRemoteDiscoveryError_(self, code):
        print "error! " + code


#here we define the custom behavior we want to fire when we get information from the wiiremote
class wii_remote_delegate_extended(WiiMote.wii_remote_delegate):
    def rawIRData_(self, irData):
        #we just grab the first point, and x,y are the first two entries in the tuple
        self.updateIR(irData[0][0], irData[0][1])
        
    def updateIR(self,x,y):
        if not ((x == 1023) and (y == 1023)):
            #being captured
            print "raw x, y:", x, y
            self.canvas.movePoint(x, y)
    
    def buttonChanged_isPressed_(self, type, isPressed):
        #print self.canvas.calibrated
        pass
       

    def setCanvas(self, canvas):
        self.canvas = canvas

        