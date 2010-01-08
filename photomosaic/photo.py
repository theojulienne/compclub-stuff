# WE HAZ AN APPID/API KEY! For the yahoo/flickr APIs

# YAHOO APPID: Nb1qEWnV34FRHdLNu3dc_tohtDAtMlgXhh8iX2ew.YLGOJN0YdtNgMFypecW9XXYnjZp
# YAHOO APPID: x2Er6ifV34FaA_WCOnb4..2eZoR6I8pq2b_zXSBPhIRLm_9CjWaPAXPlLVAaQVUeCUlh
# FLICKR API KEY: 7df9bc4628d90fe2e3bb9248cb33100a
# FLICKR API SECRET: ad9e2f8d4c18fc87

import PIL.Image as Image
import os

def getCachedColourData():
    return eval(open('colour_data.txt', 'r').read())


def databaseProcessingIsNecessary(averageColours):
    return len(averageColours) < amountOfImages


def preprocessDatabase():
    averageColours = []
    for i in range(amountOfImages):
        print ('Preprocessing %.1f' % ((i*100)/float(amountOfImages))) + '% complete.'
        img = Image.open('images/%d.jpg' % i)
        averageColour = getAverageRegionColour(img, (0, 0, img.size[0], img.size[1]))
        averageColours.append(averageColour)
        open('colour_data.txt', 'w').write(str(averageColours))
    return averageColours


def findNumImages():
    return len(filter(lambda x: '.jpg' in x.lower(), os.listdir('images')))


def getAverageRegionColour(image, (startx, starty, endx, endy)):
    tr = tg = tb = 0
    width = endx - startx
    height = endy - starty

    for y in range(starty, endy):
        for x in range(startx, endx):
            px = image.getpixel((x,y))
            tr += px[0]
            tg += px[1]
            tb += px[2]

    return tr/(width*height), tg/(width*height), tb/(width*height)


def colourOffset(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])


def getMostSimilarImage(targetColour):
    smallestOffset = float('inf')
    bestImage = None
    for i in range(amountOfImages):
        if colourOffset(averageColours[i], targetColour) < smallestOffset:
            smallestOffset = colourOffset(averageColours[i], targetColour)
            bestImage = i
    return Image.open('images/%d.jpg' % bestImage)
    
    
    

    
amountOfImages = findNumImages()
print amountOfImages
superImage = 'hannah.jpg'
resolution = 6 # The lower, the less subimages will be visible (down to 1)
pixelConversionFactor = 4  # Each pixel in super-image represents n pixels of a sub-image
                           # This represents the 'size' of the mosaic
subImageDimension = resolution * pixelConversionFactor


# Collate average colourinfo on database
averageColours = getCachedColourData()
if databaseProcessingIsNecessary(averageColours):
    print 'Detected that image database preprocessing is necessary.\nPreprocessing is commencing.'
    averageColours = preprocessDatabase()
print 'Image database colour data collated.\n'


# Open up the superimage
print 'Opening super-image...'
superImage = Image.open(superImage)
imageWidth, imageHeight = superImage.size
print 'Super-image opened up successfully.'


# Open up the mosaic canvas
print 'Initialising mosaic canvas...'
mosaicWidth =  pixelConversionFactor * imageWidth
mosaicHeight = pixelConversionFactor * imageHeight

mosaic = Image.new('RGB', (mosaicWidth, mosaicHeight), 'White')
print 'Mosaic canvas formed with dimensions %dx%d\n' % (mosaicWidth, mosaicHeight)


# Form the mosaic
print 'Beginning formation of mosaic...'
for y in range(0, imageHeight-resolution, resolution):
    print ('%.1f' % ((y*100)/float(imageHeight))) + '% complete.'

    for x in range(0, imageWidth-resolution, resolution):
        regionColour = getAverageRegionColour(superImage, (x, y, x+resolution, y+resolution))
        subImage = getMostSimilarImage(regionColour)
        
        subImage = subImage.resize((subImageDimension, subImageDimension))

        mosaic.paste(subImage, (x/resolution*subImageDimension, y/resolution*subImageDimension, x/resolution*subImageDimension+subImageDimension, y/resolution*subImageDimension+subImageDimension))


# Render the mosaic
print 'Mosaic formation is complete. Rendering process initialising...'
mosaic.save('mosaic.jpg')

print 'Rendering complete! See result in mosaic.jpg'
