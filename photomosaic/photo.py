# WE HAZ AN APPID/API KEY! For the yahoo/flickr APIs

# YAHOO APPID: Nb1qEWnV34FRHdLNu3dc_tohtDAtMlgXhh8iX2ew.YLGOJN0YdtNgMFypecW9XXYnjZp
# YAHOO APPID: x2Er6ifV34FaA_WCOnb4..2eZoR6I8pq2b_zXSBPhIRLm_9CjWaPAXPlLVAaQVUeCUlh
# FLICKR API KEY: 7df9bc4628d90fe2e3bb9248cb33100a
# FLICKR API SECRET: ad9e2f8d4c18fc87

import PIL.Image as Image

AMOUNT_OF_IMAGES = 100
INFINITY = float('inf')

subImageWidth = 30
subImageHeight = 30
superImage = 'failfan.jpg'



def getAverageColour(image):
    tr = tg = tb = 0
    #print image.size
    width, height = image.size

    for i in range(height):
        for j in range(width):
            px = image.getpixel((i,j))
            tr += px[0]
            tg += px[1]
            tb += px[2]
	    
    return tr/(width*height), tg/(width*height), tb/(width*height)



def colourOffset(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])



def getMostSimilarImage(targetColour):
    smallestOffset = INFINITY
    bestImage = None
    for i in range(AMOUNT_OF_IMAGES):
        if colourOffset(averageColours[i], targetColour) < smallestOffset:
            smallestOffset = colourOffset(averageColours[i], targetColour)
            bestImage = i
    return Image.open('images/%d.jpg' % bestImage)



averageColours = []
for i in range(AMOUNT_OF_IMAGES):
    print 'Average colour calculation of image', i
    averageColours.append(getAverageColour(Image.open('images/%d.jpg' % i)))

print 'Completion of average colour calculation.'

target = Image.open(superImage)

imageWidth, imageHeight = target.size

print 'Super-image opened up.'

mosaic = Image.new('RGB', (subImageWidth*imageWidth,subImageHeight*imageHeight), 'White')
print 'Mosaic image canvas formed with dimensions %d*%d' % (subImageWidth*imageWidth, subImageHeight*imageHeight)

print 'Beginning creation of mosaic...'

for y in range(imageHeight):
    print ('%.1f' % ((y*100)/float(imageHeight))) + '% complete.'
    
    for x in range(imageWidth):
        targetColour = target.getpixel((x, y))
        bestMatch = getMostSimilarImage(targetColour)
        
        subImage = bestMatch.copy()
       # print x*subImageWidth, y*subImageHeight, x*(subImageWidth+1), y*(subImageWidth+1)
        mosaic.paste(subImage, (x*subImageWidth, y*subImageHeight, x*subImageWidth+subImageWidth, y*subImageHeight+subImageWidth))

print 'Render complete! See mosaic.jpg for result.'

mosaic.save('mosaic.jpg')
