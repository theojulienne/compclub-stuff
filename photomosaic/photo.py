import PIL.Image as Image

AMOUNT_OF_IMAGES = 44
INFINITY = float('inf')

def getAverageColour(image):
    tr = tg = tb = 0
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
  #  print targetColour
    for i in range(AMOUNT_OF_IMAGES):
        if colourOffset(averageColours[i], targetColour) < smallestOffset:
            smallestOffset = colourOffset(averageColours[i], targetColour)
            bestImage = i
    return Image.open('images/%d.jpeg' % (bestImage+1))


averageColours = []
for i in range(AMOUNT_OF_IMAGES):
    averageColours.append(getAverageColour(Image.open('images/%d.jpeg' % (i+1))))

subImageSize = 30


width = 400
height = 300


target = Image.open('truck.jpg')
mosaic = Image.new('RGB', (subImageSize*width,subImageSize*height), 'White')


for y in range(height):
    print "row" + str(y) + " " + str((y*100)/height) + "%"
    for x in range(width):
        targetColour = target.getpixel((x, y))
        bestMatch = getMostSimilarImage(targetColour)
        
        region = bestMatch.copy()
        mosaic.paste(region, (x*30, y*30, x*30+30, y*30+30))

mosaic.save('mosaic.jpeg')

#print getAverageColour(im)
