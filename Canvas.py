#
#  Canvas.py
#  enjapen
#
#  Created by Ian Johnson on 2/24/08.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#
from Foundation import *
from AppKit import *
import time
import threading
from perspective import Perspective

class Canvas(NSView):
    point = objc.ivar('point') 
    perspective = Perspective()
    calibrated = False
    mouseMode = False
    
    
    def awakeFromNib(self):
        self.center = (50.0, 50.0)
        self.radius = 10.0
        self.color = NSColor.redColor()
        #self.perspective.setdst((0.0,0.0),(400,0.0),(0.0,400),(400,400))
        self.perspective.setdst((0.0,400),(400,400),(0.0,0.0),(400,0.0))
        
        #preperation for allowing mouse control
        from Quartz import CoreGraphics
        self.CG = CG = CoreGraphics
        #displayWidth = CG.CGMainDisplayID
        displayWidth = CG.CGDisplayPixelsWide(CG.CGMainDisplayID())
        displayHeight = CG.CGDisplayPixelsHigh(CG.CGMainDisplayID())
        print displayWidth, displayHeight
        dp = Perspective()
        dp.setdst((0,0),(displayWidth,0),(0,displayHeight),(displayWidth,displayHeight))
        self.display_perspective = dp
        
        #callibrate the wiimote to our perspectives
        self.calib = Calibratinator()
        self.calib.perspective = self.perspective
        self.calib.display_perspective = self.display_perspective
        self.calib.calibrated = self.calibrated
        
        
        
    def drawRect_(self, rect):
        NSColor.whiteColor().set()
        NSRectFill(self.bounds())
        origin = (self.center[0]-self.radius, self.center[1]-self.radius)
        size = (2 * self.radius, 2 * self.radius)
        dotRect = (origin, size)
        self.color.set()
        NSBezierPath.bezierPathWithOvalInRect_(dotRect).fill()
        
    def movePoint(self, x, y):
        #print (x, y)
        self.calib.irFound = True
        self.calib.irPoint = (x, y)
        #print "movepoint calib:", self.calibrated
        if self.calib.calibrated:
            print "gogo gadget point!"
            xw, yw = self.perspective.warp(x,y)
            print xw, yw
            self.center = (xw, yw)
            self.setNeedsDisplay_(True)
            if(self.mouseMode):
                CG = self.CG
                #calculate perspective for display (it is top left oriented)
                xd, yd = self.display_perspective.warp(x,y)
                print "display coords: ", xd, yd
                event = CG.CGEventCreateMouseEvent(None, CG.kCGEventMouseMoved, (xd,yd), CG.kCGMouseButtonLeft)
                CG.CGEventSetType(event, CG.kCGEventMouseMoved)
                CG.CGEventPost(CG.kCGHIDEventTap, event)
        
    def stopCalibrating(self):
        self.calib.calibrating = False
        
    def calibrate(self):
        self.calib.calibrate()
   
        
class Calibratinator(threading.Thread):
    #we need to enter a state of meditation to calibrate our canvas
    calibrating = False
    #we will use this to wait on an ir point
    irFound = False
    irPoint = (0,0)
    #the 4 cornders of the canvas
    corners = [(0,0),(0,0),(0,0),(0,0)]
    calibrated = False
    perspective = None
    
    def __init__(self):
        threading.Thread.__init__(self)
    
    def calibrate(self):
        self.start()
        
    def run(self):
        #wait on irdata, set corner
        self.irFound = False
        self.irPoint = (0,0)
        self.calibrating = True
        print "calibrating"
        while(not self.irFound and self.calibrating):
            time.sleep(1)
            print "1"
        self.irFound = False
        self.corners[0] = self.irPoint
        print "corner 0", self.corners[0]
        
        while(not self.irFound and self.calibrating):
            time.sleep(1)
        self.irFound = False
        self.corners[1] = self.irPoint
        print "corner 1", self.corners[1]
        
        while(not self.irFound and self.calibrating):
            time.sleep(1)
        self.irFound = False
        self.corners[2] = self.irPoint
        print "corner 2", self.corners[2]
        
        while(not self.irFound and self.calibrating):
            time.sleep(1)
        self.irFound = False
        self.corners[3] = self.irPoint
        print "corner 3", self.corners[3]
        
        self.perspective.setsrc(self.corners[0],
                                self.corners[1],
                                self.corners[2],
                                self.corners[3])
        self.display_perspective.setsrc(self.corners[0],
                                self.corners[1],
                                self.corners[2],
                                self.corners[3])
        self.calibrated = True
        print "calibed", self.calibrated
        self.calibrating = False
        
        print "done calibrating"
        
        
    
        
        