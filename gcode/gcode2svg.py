import svg
BLOCK_DEPTH = 5.0 # the depth of the physical block

class GCode2SVG:
    def __init__(self, input, outputObject=None):
        self.image = svg.SVG()
        self.gcode = input
        if outputObject == None:
            outputObject = open('image.svg', 'w')
        self.outputObject = outputObject
    
    def _createImage(self):
        currentCoords = (0.0, 0.0)
        currentDepth = 0.0
        
        for line in self.gcode:
            path = svg.Path()
            path.moveTo(*currentCoords)
            
            
            # parse each word in each block separately
            for word in line.strip().split():
                if word[0] == 'Z':
                    currentDepth = float(word[1:])
                elif word[0] == 'X':
                    currentCoords = (float(word[1:]), currentCoords[1])
                elif word[0] == 'Y':
                    currentCoords = (currentCoords[0], float(word[1:]))
            
            # if the depth is above the block, make the path transparent
            # else, choose a colour based on depth and draw the line
            #if currentDepth >= BLOCK_DEPTH:
                #path.moveTo(*tuple(currentCoords))
            if currentDepth < BLOCK_DEPTH:
                path.setColour(self._getColour(currentDepth))
                path.lineTo(*currentCoords)
            self.image.addPath(path)
    
    def _getColour(self, depth):
        '''convert the tool depth into a colour
           darker colours are lower in the model, 
           while lighter colours are higher'''
        return int(round((depth/BLOCK_DEPTH)*255))
    
    def renderImage(self):
        self._createImage()
        self.outputObject.write(self.image.getXML())
        self.outputObject.close()

obj = GCode2SVG(open('image.gcode', 'r'))
obj.renderImage()
