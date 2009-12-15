import math
import random
import os

class Path:
	def __init__(self):
		self.style = {}
		#self.style['fill'] = 'none'
		self.style['stroke'] = 'black'
		#self.style['stroke-linecap'] = 'round'
		#self.style['stroke-width'] = 1
		self.d = ''
		self.width = 0
		self.height = 0
    
	def setColour(self, colour):
		self.style['stroke'] = '#' + ('%02x' % int(hex(colour), 16))*3

	def upsize(self, x, y):
		if(x > self.width): self.width = x
		if(y > self.height): self.height = y 
		
	def setStyle(self, style, value):
		self.style[style] = value
				
	def moveTo(self, x, y):
		self.upsize(x, y)
		self.d += 'M %f,%f ' % (x, y)
		
	def lineTo(self, x, y):
		self.upsize(x, y)
		self.d += 'L %f,%f ' % (x, y)
		
	def curveTo(self, x1, y1, x2, y2, x, y):
		self.upsize(x1, y1)
		self.upsize(x2, y2)
		self.upsize(x, y)
		self.d += 'C %f,%f %f,%f %f,%f ' % (x1, y1, x2, y2, x, y)
		
	def getBounds(self):
		return (self.width, self.height)
		
	def getXML(self):
		xmlStr = '<path d="' + self.d + '" '
		for (k, v) in self.style.iteritems():
			xmlStr += k + '="'+ str(v) + '" '
		xmlStr += '/>\n'
		
		return xmlStr
	
class SVG:
	def __init__(self):
		self.paths = []
		self.width = 0
		self.height = 0

	def upsize(self, x, y):
		if(x > self.width): self.width = x
		if(y > self.height): self.height = y	
	
	def addPath(self, path):
		self.upsize(*path.getBounds())
		self.paths.append(path)
		
	def getXML(self):
		xmlStr = """<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
		<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
		    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
		<svg xmlns="http://www.w3.org/2000/svg"
		     xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" """
		xmlStr += 'width="%d" height="%d">\n' % (self.width, self.height)
		
		for path in self.paths:
			xmlStr += path.getXML()
		
		xmlStr += '</svg>\n'
		
		return xmlStr
