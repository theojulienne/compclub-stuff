from svg import * 
from random import randint

class Picture(object):

	def __init__(self):
		self.svg = SVG()

	def randomWalk(self,x,y,steps):

		minY, maxY = (-100, 100)
		minX, maxX = (0, 150)

		points = []

		for i in range(steps):
			x += randint(minX, maxX)
			y += randint(minY, maxY)

			points.append( (x,y) )

		return points

	def drawVine(self,x,y,steps): 
		points = self.randomWalk(x,y,steps)  
		
		vine = Path()
		vine.setStyle("stroke", "rgb(0,150,0)")
		vine.moveTo(x,y)
		
		for coord in points:
			coordX, coordY = coord
			vine.lineTo(coordX, coordY)

		self.svg.addPath(vine)
		


	def writeSVGFile(self, filename):
		xml = self.svg.getXML()
		f = open(filename, 'w')
		f.write(xml)
		f.close()


picture = Picture()

picture.drawVine(x,y,steps)
 
picture.writeSVGFile("../images/vine.svg")

