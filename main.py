#
#  main.py
#  enjapen
#
#  Created by Ian Johnson on 1/24/08.
#  Copyright __MyCompanyName__ 2008. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import enjapenAppDelegate
import Canvas

# pass control to AppKit
AppHelper.runEventLoop()


