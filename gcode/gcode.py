import StringIO as io
import time

class SimpleGenerator():
  def __init__(self, outputObject = None, preOptions = "", *machineOptions):
    """ setup code. preOptions is a string that will be prepended to the
    g-code output incase users want to add stuff. MachineOptions is a tuple of options"""
    if (outputObject == None):
      outputObject = io.StringIO()
    self.outputObject = outputObject

    self.parseOptions(machineOptions)

    self.xPos = 0.0
    self.yPos = 0.0
    self.zPos = 0.0
    self.lineNumber = 0
    self.feedRate = 20
    self.gCodeInit(preOptions)

  def parseOptions(self, *opts):
    pass
    # still working on this.
    #'''Parse the set of options we pass to the system.
    #feedRate=NUM # set the feedrate in mm/min
    #'''
    #for str in opts:
      #print(str)

  def gCodeInit(self, str):

    initCodes = [
        "G21" # we want units in mm
      , "G0 X0.00 Y0.00 Z0.00"# go to 0,0,0
      ]

    self.gCodeWrite("(Created by the UNSW compClub gCode generator on ", time.asctime(), ")")
    self.gCodeWrite(str)

    self.gCodeWrite("( ", time.asctime(), " )\n")

    for str in initCodes:
      self.gCodeWrite(str)

  def gCodeWrite(self, *args):
    showLineNumber = 1
    if (showLineNumber==1):
      self.outputObject.write("N%05d " % self.lineNumber)
      self.lineNumber += 10
      for arg in args:
        self.outputObject.write(arg.upper())
    else:
      self.outputObject.write("       ")
      for arg in args:
        self.outputObject.write(arg)
    self.outputObject.write("\n")

  def __str__(self):
    ''' For internal testing only. '''
    pos = self.outputObject.tell()
    self.outputObject.seek(0,0)
    result = self.outputObject.read()
    self.outputObject.seek(pos, 0)
    return result

    self.outputObject.write(arg)
    self.outputObject.write("\n")

  def writePosition(self):
    if (self.xPos <= 9.995):
      spaceX = " "
    else:
      spaceX = ""
    if (self.yPos <= 9.995):
      spaceY = " "
    else:
      spaceY = ""
    if (self.zPos <= 9.995):
      spaceZ = " "
    else:
      spaceZ = ""
    self.gCodeWrite('G0 X%s%.2f Y%s%.2f Z%s%.2f' % (spaceX, self.xPos, spaceY, self.yPos, spaceZ, self.zPos))

  def updatePositions(self, nx=None, ny=None, nz=None):
    self.xPos = (nx if nx != None else self.xPos)
    self.yPos = (ny if ny != None else self.yPos)
    self.zPos = (nz if nz != None else self.zPos)

  def moveAbsolute(self, x=None,y=None,z=None):
    '''obj.moveAbsolute(x=5.0,y=6.0,z=8.0)
       Moves the drill to the x,y,z position
       Also updates self.{xyz}Pos accordingly'''
    self.updatePositions(nx=x, ny=y, nz=z)
    #move the z axis first. The idea is to lift the bit up and out of the way first
    #also, do we want to go to z=0 or z=SOMETHING BIG
    self.gCodeWrite('G0 Z%.2f' % self.zPos)
    #then do the xy movements
    self.gCodeWrite('GO X%.2f Y%.2f' % (self.xPos, self.yPos))

  def moveRelative(self, x=None,y=None,z=None):
    '''obj.moveRelative(x=5.0, y=6.0, z=8.0)
       Moves the drill to the xPos+x,yPos+y,zPos+z position
       Also updates self.{xyz}Pos accordingly'''
    self.updatePositions(nx=x+self.xPos, ny=y+self.yPos, nz=z+self.zPos)
    #move the z axis first. The idea is to lift the bit up and out of the way first
    #also, do we want to go to z=0 or z=SOMETHING BIG
    #we want SOMETHING BIG. Z0 is the lowest the z can go.
    self.gCodeWrite('G0 Z%.2f' % self.zPos)
    #then do the xy movements
    self.gCodeWrite('G0 X%.2f Y%.2f' % (self.xPos, self.yPos))

  def cutAbsolute(self, x=None,y=None,z=None, feedRate = None):
    '''cuts to the x,y,z position
    Also updates self.{xyz}Pos accordingly. This
    will cut at feedRate or self.feedRate, with feedRate in mm/min'''
    self.updatePositions(nx=x, ny=y, nz=z)
    cutRate = (self.feedRate if feedRate == None else feedRate)
    self.gCodeWrite('G1 X%.2f Y%.2f Z%.2f F%.2f' % (self.xPos, self.yPos, self.zPos, cutRate))

  def cutRelative(self, x=None,y=None,z=None, feedRate = None):
    '''cuts to the relative x,y,z position
    Also updates self.{xyz}Pos accordingly. This
    will cut at feedRate or self.feedRate, with feedRate in mm/min'''
    self.updatePositions(nx=x+self.xPos, ny=y+self.yPos, nz=z+self.zPos)
    cutRate = (self.feedRate if feedRate == None else feedRate)
    self.gCodeWrite('G1 X%.2f Y%.2f Z%.2f F%.2f' % (self.xPos, self.yPos, self.zPos, cutRate))

  def coords(self):
    return  (self.xPos, self.yPos, self.zPos)

  def finish(self):
    self.outputObject.close()