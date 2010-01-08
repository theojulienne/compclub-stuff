# WE HAZ AN APPID/API KEY! For the yahoo/flickr APIs

# YAHOO APPID: Nb1qEWnV34FRHdLNu3dc_tohtDAtMlgXhh8iX2ew.YLGOJN0YdtNgMFypecW9XXYnjZp
# YAHOO APPID: x2Er6ifV34FaA_WCOnb4..2eZoR6I8pq2b_zXSBPhIRLm_9CjWaPAXPlLVAaQVUeCUlh
# FLICKR API KEY: 7df9bc4628d90fe2e3bb9248cb33100a
# FLICKR API SECRET: ad9e2f8d4c18fc87

import PIL.Image as Image
import glob, os

def findNumImages():
    maxNum = -1
    for imagefile in glob.glob('images/*.jpg'):
        maxNum = max([maxNum, int(os.path.basename(imagefile).split('.')[0])])
    return maxNum+1


AMOUNT_OF_IMAGES = findNumImages()
superImage = 'hannah.jpg'
resolution = 8 # The lower, the less subimages will be visible (down to 1)
pixelConversionFactor = 3  # Each pixel in super-image represents 10 pixels of a sub-image
                           # This represents the 'size

subImageDimension = resolution * pixelConversionFactor

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
    for i in range(AMOUNT_OF_IMAGES):
        if colourOffset(averageColours[i], targetColour) < smallestOffset:
            smallestOffset = colourOffset(averageColours[i], targetColour)
            bestImage = i
    return Image.open('images/%d.jpg' % bestImage)


print 'Preprocessing image database for colour information'
averageColours = []
for i in range(AMOUNT_OF_IMAGES):
    print ('%.1f' % ((i*100)/float(AMOUNT_OF_IMAGES))) + '% complete.'
    img = Image.open('images/%d.jpg' % i)
    averageColour = getAverageRegionColour(img, (0, 0, img.size[0], img.size[1]))
    averageColours.append(averageColour)
print 'Completion of image database processing.\n'


print 'Opening super-image...'
superImage = Image.open(superImage)
imageWidth, imageHeight = superImage.size
print 'Super-image opened up successfully.'


print 'Initialising mosaic canvas...'
mosaicWidth =  pixelConversionFactor * imageWidth
mosaicHeight = pixelConversionFactor * imageHeight

mosaic = Image.new('RGB', (mosaicWidth, mosaicHeight), 'White')
print 'Mosaic canvas formed with dimensions %dx%d\n' % (mosaicWidth, mosaicHeight)

print 'Beginning formation of mosaic...'
for y in range(0, imageHeight-resolution, resolution):
    print ('%.1f' % ((y*100)/float(imageHeight))) + '% complete.'

    for x in range(0, imageWidth-resolution, resolution):
        regionColour = getAverageRegionColour(superImage, (x, y, x+resolution, y+resolution))
        subImage = getMostSimilarImage(regionColour)
        
        subImage = subImage.resize((subImageDimension, subImageDimension))

        mosaic.paste(subImage, (x/resolution*subImageDimension, y/resolution*subImageDimension, x/resolution*subImageDimension+subImageDimension, y/resolution*subImageDimension+subImageDimension))

print 'Mosaic formation is complete. Rendering process initialising...'
mosaic.save('mosaic.jpg')

print 'Rendering complete! See result in mosaic.jpg'