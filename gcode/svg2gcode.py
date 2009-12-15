import gcode
import re

BLOCK_DEPTH = 5.0 # the depth of the physical block

class SVG2GCode:
    def __init__(self, input, outputObject=None):
        self.svg = input
        
        if outputObject == None:
            outputObject = open('image.gcode', 'w')
        
        self.gcodeObject = gcode.SimpleGenerator(outputObject = outputObject)
        
        self._createImage()
    
    def _createImage(self):
        pattern = re.compile('d=\"M (.*?),(.*) L (.*?),(.*?)\"')
        currentCoords = (0.0, 0.0)
        currentDepth = 0.0
        
        for line in self.svg:
            print line
            nums = pattern.findall(line)
            print nums

            if nums:
#                colour = nums[0][4]
                
                nums = nums[0][:4]
                
                nums = map(float, nums)
                source = nums[:2]
                target = nums[2:4]
                
#                depth = self.getDepth(colour)
                self.gcodeObject.moveAbsolute(x=source[0], y=source[1])
                self.gcodeObject.cutAbsolute(x=target[0], y=target[1], z=BLOCK_DEPTH)
    
        self.gcodeObject.finish()

    def getDepth(self, colourKey):
        r, g, b = int(colourKey[:2], 16), int(colourKey[2:4], 16), int(colourKey[4:], 16)
        return ((r + g + b) / 48.0) * BLOCK_DEPTH
    

obj = SVG2GCode(open('image.svg', 'r'))

