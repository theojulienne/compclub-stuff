from svg import * 
import random


class Picture(object):

	def __init__(self):
		self.svg = SVG()


	def drawDebugBox(self, x, y, c):
		self.drawBox(x,y,3,3,c,True)

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



	def drawCrescent(self, start, cp1, cp2, end, cp3, cp4):
		crescent = Path()
		
		(x,y) = start
		crescent.moveTo(x,y)

		(x1,y1) = cp1
		(x2,y2) = cp2
		(x,y) = end
		
		self.drawDebugBox(x1,y1, "red") 
		self.drawDebugBox(x2,y2, "blue")
		self.drawDebugBox(x,y, "black")  
		crescent.curveTo(x1, y1, x2, y2, x, y)

		(x1,y1) = cp3
		(x2,y2) = cp4
		(x,y) = start
		self.drawDebugBox(x1,y1, "green") 
		self.drawDebugBox(x2,y2, "magenta")
		self.drawDebugBox(x,y, "cyan") 
		crescent.curveTo(x1, y1, x2, y2, x, y)

		self.svg.addPath(crescent)	


	def drawParamCrescent(self, x, y, a, b, c, d, e, f, g):
		start = (x,y)
		cp1   = (x+f, y+ (a*d)) 
		cp2   = (x+f+(a*b), y+(a*d))  
		end   = (x+a, y)
		cp3   = (x+g+(a*c), y+a*e) 
		cp4   = (x+g, y+a*e) 
		self.drawCrescent(start, cp1, cp2, end, cp3, cp4)

	def drawRandCrescent(self, x, y):
		minA = 50
		maxA = 100

		a = random.randint(minA, maxA)

		maxB = 1.0
		minB = 0.5

		b = random.uniform(minB, maxB)

		maxC = b
		minC = 0.4

		c = random.uniform(minC, maxC)

		maxD = 1.0
		minD = 0.4

		d = random.uniform(minD, maxD)
		
		maxE = d
		minE = 0.1
		
		e = random.uniform(minE, maxE) 

		g =  ((a-a*e))/2.0 
		
		f = ((a-a*b))/2.0

		self.drawParamCrescent(x, y, a, b, c, d, e, f, g)


	def writeSVGFile(self, filename):
		xml = self.svg.getXML()
		f = open(filename, 'w')
		f.write(xml)
		f.close()


picture = Picture()

for i in range(100):
	x = random.randint(100,700)
	y = random.randint(100,500)
	picture.drawRandCrescent(x,y)
#picture.drawCheckerBoard(170,80, 50, 8)
 
picture.writeSVGFile("../images/box.svg")

