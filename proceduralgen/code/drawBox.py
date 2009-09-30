from svg import * 

class Picture(object):

	def __init__(self):
		self.svg = SVG()

	def drawBox(self, x, y, width, height, colour, isFilled):
		
		box = Path()

		if isFilled:
			box.setStyle("fill", colour)
		
		box.setStyle("stroke", colour)
		box.moveTo(x,y)
		box.lineTo(x,y+height)
		box.lineTo(x+width,y+height)
		box.lineTo(x+width,y)
		box.lineTo(x,y)

		self.svg.addPath(box)

	def drawCheckerBoardRow(self, x, y, squareSize, sideLength):
		for squareNum in range(sideLength):
			self.drawBox(x+squareSize*2*squareNum, y, squareSize, squareSize, "black", True)

	def drawCheckerBoard(self, x, y, squareSize, sideLength):


		borderSize = sideLength*squareSize
		self.drawBox(x,y,borderSize,borderSize,"black",False)

		sideLength /= 2


		for row in range(sideLength):
			self.drawCheckerBoardRow(x, y+squareSize*2*row, squareSize, sideLength)

		x += squareSize
		y += squareSize

		for row in range(sideLength):
			self.drawCheckerBoardRow(x, y+squareSize*2*row, squareSize, sideLength)


	def writeSVGFile(self, filename):
		xml = self.svg.getXML()
		f = open(filename, 'w')
		f.write(xml)
		f.close()


picture = Picture()

picture.drawCheckerBoard(10,10, 50, 8)
 
picture.writeSVGFile("../images/box.svg")

