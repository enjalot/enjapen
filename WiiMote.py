#
#  WiiMote.py
#  enjapen
#
#  Created by Ian Johnson on 2/17/08.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#
import objc


def loadbundle(nm, fn): 
    objc.loadBundle(nm, globals(), bundle_path = objc.pathForFramework(fn)) 
loadbundle('WiiRemote', u'/Library/Frameworks/WiiRemote.framework') 
#loadbundle('WiiRemote', u'WiiRemote.framework') 

IRData = objc.createStructType("IRData", "iii", ["x", "y", "s"])

WiiRemoteDiscoveryDelegate = objc.informal_protocol(
    "WiiRemoteDiscoveryDelegate",
    [
        objc.selector(None,
            selector="willStartWiimoteConnections",signature="v@:",isRequired=0),
        objc.selector(None,
            selector="WiiRemoteDiscovered:",signature="v@:@",isRequired=0),
        objc.selector(None, 
            selector="WiiRemoteDiscoveryError:",signature="v@:i",isRequired=0)
    ])

WiiRemoteDelegate = objc.informal_protocol(
    "WiiRemoteDelegate",
    [
        objc.selector(None, 
            selector="irPointMovedX:Y:",
            signature="v@:ff", isRequired=False),
        objc.selector(None, selector="rawIRData:", 
            signature="v@:n^[4{IRData=iii}]", 
            isRequired=False),
        objc.selector(None,
            selector="buttonChanged:isPressed:", 
            signature="v@:SS", isRequired=False),
        objc.selector(None,
            selector="accelerationChanged:accX:accY:accZ:",
            signature="v@:SSSS", isRequired=False),
        objc.selector(None,
            selector="joyStickChanged:tiltX:tiltY:",
            signature="v@:SSS", isRequired=False),
        objc.selector(None,
            selector="analogButtonChanged:amount:", 
            signature="v@:SS", isRequired=False),
        objc.selector(None, 
            selector="batteryLevelChanged:",
            signature="v@:d", isRequired=False),
        objc.selector(None, 
            selector="wiiRemoteDisconnected:",
            signature="v@:@", isRequired=False),
    ])


#We provide this delegate to be overriden by the Application using this library
class wii_remote_delegate(NSObject):
    def irPointMovedX_Y_(self, px, py):
        #print 'irPointMovedX:Y:', px, py
        pass
        
    def rawIRData_(self, irData):
        #print 'rawIRData: ' , irData
        pass
    
    def buttonChanged_isPressed_(self, type, isPressed):
        #print 'buttonChanged:isPressed:', type, isPressed
        pass

    def accelerationChanged_accX_accY_accZ_(self, type, accX, accY, accZ):
        #print 'accelerationChanged:accX:accY:accZ:', type, accX, accY, accZ
        pass

    def joyStickChanged_tiltX_tiltY_wiiRemote_(self, type, tiltX, tiltY):
        #print 'joyStickChanged:tiltX:tiltY:'
        pass

    def analogButtonChanged_amount_wiiRemote_(self, type, press):
        #print 'analogButtonChanged:amount:'
        pass

    def batterLevelChanged_(self, level):
        #print 'batteryLevelChanged:', level
        pass

    def wiiRemoteDisconnected_(self, device):
        #print 'wiiRemoteDisconnected:'
        pass

"""        
    def rawIRDataHack_(self, irarray):
        print "irarray: ", irarray
        pass
    #def rawIRDataHackX1_Y1_S1_X2_Y2_S2_X3_Y3_S3_X4_Y4_S4_(self, *posargs, **kwdargs):
        #thankfully we don't have to do this anymore, all that was needed was a n
        #objc.selector(None, 
        #    selector="rawIRDataHackX1:Y1:S1:X2:Y2:S2:X3:Y3:S3:X4:Y4:S4:",
            #signature="v@:[4{?=iii}]", isRequired=False),
        #    signature="v@:iiiiiiiiiiii", isRequired=False), 
    def rawIRDataHackX1_Y1_S1_X2_Y2_S2_X3_Y3_S3_X4_Y4_S4_(self, x1,y1,s1, x2,y2,s2, x3,y3,s3, x4,y4,s4):
        print "rawIRDataHack",x1,y1,x2,y2
        pass

    @objc.signature("v@:{IRData=iii}")
    def rawIRData0_(self, irData):
        #print "what it do? ", irData
        pass
        
    @objc.signature("v@:[4{IRData=iii}]")
    def rawIRDataASDF_(self, irData):
        print 'seriously: ' , irData
        pass
        
    #@objc.signature("v@:[4{IRData=iii}]")
    @objc.signature("v@:[4{IRData=iii}]")
    def rawIRData_(self, irData):
        #print 'rawIRData: ' , irData
        #ir = cast(irData[0], IRDATA(Structure))
        #print 'rawIRData cast?: %s' % (ir)
        pass
"""
"""
class wii_remote_discovery_delegate(NSObject):
    #WiiRemoteDiscovery Delegate functions
    #called when connecting to wiimote
    
    def willStartWiimoteConnections(self):
        print "starting wiimote connection"
        
    def WiiRemoteDiscovered_(self, remote):
        print "discovered!"
        wii = remote.retain()
        print "stored"
        #print "isButtonPressed.sig: ", self.remote.isButtonPressed_.signature
        #print "wrd: ", wrd
        #print "buttonChanged.sig: ", self.remote.buttonChanged_isPressed_.signature
        #self.remote.setDelegate_(self)
        delegate = wii_remote_delegate.new()
        wii.setDelegate_(delegate)
        #print "wrd.bc: ", remote._delegate.buttonChanged_isPressed_.signature
        #print dir(self)
        #print "self.bc.sig: ", self.accelerationChanged_accX_accY_accZ_.signature
        print "delegate set"
        wii.setIRSensorEnabled_(True)
        print "ir sensor enabled"
        #self.remote.setMotionSensorEnabled_(True)
        #print "motion sensor enabled"
        wii.setLEDEnabled1_enabled2_enabled3_enabled4_(True, False, False, True)
        print "led's fixed up"
        print "active", wii.available()
        print "battery", wii.batteryLevel()
        self.remote = wii
        #print self.remote
        #self.remote.closeConnection()
    
    def WiiRemoteDiscoveryError_(self, code):
        print "error! " + code



"""
"""
    #WiiRemote Delegate functions     
    #def wiimoteWillSendData(self):
    #    print "will send data"
        
    #def wiimoteDidSendData(self):
    #    print "sent data"

    #def irPointMovedX_Y_(self, px,py):
    def irPointMovedX_Y_(self, *posargs, **kwdargs):
        print "irz!"
        print posargs
        print kwdargs
        #print "x:", x, "y:", y
    
    #def rawIRData_(self, irData):
    def rawIRData_(self, *posargs, **kwdargs):
        print "irdata baby"
        print posargs
        print kwdargs
        #print irData
        
    #def buttonChanged_isPressed_(self, type, isPressed):
    def buttonChanged_isPressed_(self, *posargs, **kwdargs):
        print "buttonzzz!"
        print posargs
        print kwdargs
        #print type
        #print isPressed
        
    #def accelerationChanged_accX_accY_accZ_(self, type, accX, accY, accZ):
    def accelerationChanged_accX_accY_accZ_(self, *posargs, **kwdargs):
        print "acceleration changed!"
        print posargs
        print kwdargs
"""
"""
    def accelerationChanged_accX_accY_accZ_(self, type, accX, accY, accZ):
        print "hi"
    def joyStickChanged_tiltX_tiltY_(self, type, tiltX, tiltY):
        print "hi"
    def analogButtonChanged_amount_(self, type, press):
        print "hi"
    def batteryLevelChanged_(self,level):
        print "lvl", level
    def gotMiiData_at_(self, mii_data_buf, slot):
        print "hi"
       
    def wiiRemoteDisconnected_(self, device):
        print "device disconnected"
"""