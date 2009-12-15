from svg import * 
from random import randint
from random import uniform

class Picture(object):

	def __init__(self):
		self.svg = SVG()

	def swirlyThingWalk(self,x,y,steps,stepLength,direction):
		if direction < 0:
			turn = -1
		else:
			turn = 1

		points = []
		for i in range(steps):
			x += math.cos(direction)*stepLength
			y += math.sin(direction)*stepLength
			
			direction += turn*uniform(0,math.pi/4)
			stepLength *= 0.8

			points.append((x,y))

		return points 

	def drawSwirlyThing(self,x,y,steps,stepLength,direction,col="rgb(0,80,0)"):
		points = self.swirlyThingWalk(x,y,steps,stepLength,direction)
		curvePoints = self.insertMidPoints(x,y,points)
		
		vine = Path()
		vine.setStyle("stroke", col)
		vine.moveTo(x,y)
		for i in range(1,len(curvePoints)-1,2):
			cornerX, cornerY = curvePoints[i]
			midX, midY = curvePoints[i+1]
			#vine.lineTo(cornerX, cornerY)
			vine.curveTo(cornerX, cornerY, cornerX, cornerY, midX, midY)

		self.svg.addPath(vine)


	def randomWalk(self,x,y,steps,stepLength,direction,directionMax=math.pi/4,directionMin=-math.pi/4,turnRange=math.pi/4):
		points = []
		for i in range(steps):
			x += math.cos(direction)*stepLength
			y += math.sin(direction)*stepLength
			direction += (randint(-1000,1000)/1000.0)*turnRange
                        if direction > directionMax: direction -= turnRange
                        if direction < directionMin: direction += turnRange
			points.append( (x,y) )
		return points

	def insertMidPoints (self,x,y,originalPoints) :
		newPoints = []
		for (newX,newY) in originalPoints:
			midX = (x+newX)/2.0
			midY = (y+newY)/2.0
			newPoints.append( (midX,midY) )
			newPoints.append( (newX,newY) )
			x = newX
			y = newY

		return newPoints	

	def drawVine(self,x,y,steps,size,direction):
                if size == 4:
			self.drawSwirlyThing(x,y,30,4,direction)
			return
		points = self.randomWalk(x,y,steps,2**size,direction)  
		curvePoints = self.insertMidPoints(x,y,points)		

		vine = Path()
		vine.setStyle("stroke-width", size-3)
		vine.setStyle("stroke", "rgb(0,150,0)")
		vine.moveTo(x,y)
		
		for i in range(1,len(curvePoints)-1,2):
			cornerX, cornerY = curvePoints[i]
			midX, midY = curvePoints[i+1]
			vine.curveTo(cornerX, cornerY, cornerX, cornerY, midX, midY)
			self.drawVine(midX, midY, steps/2, size-1, math.atan((midY-cornerY)/(midX-cornerX))+random.randrange(-1,2,2)*random.uniform(0.5,math.pi/4) )
			#else: self.drawSwirlyThing(x,y,30,4,direction)
		if size == 5: self.drawSwirlyThing(midX,midY,30,29,math.atan((midY-cornerY)/(midX-cornerX)),"rgb(0,50,0)")
		self.svg.addPath(vine)

	def writeSVGFile(self, filename):
		xml = self.svg.getXML()
		f = open(filename, 'w')
		f.write(xml)
		f.close()


picture = Picture()

x = 0
y = 1000
steps = 30
density = 3

for i in range(density):
	picture.drawVine(x,y+randint(-density//4,density//4),steps,7,random.uniform(-math.pi/2.0, math.pi/2.0))

picture.writeSVGFile("../images/vine.svg")
