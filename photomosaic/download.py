# Sourced from
# http://jesolem.blogspot.com/2009/02/using-python-to-download-images-from.html
# With major changes by Goldy

from PIL import Image
import flickr
import urllib, urlparse
import os, sys, glob
import photo

def findNumImages():
    maxNum = -1
    for imagefile in glob.glob('images/*.jpg'):
        maxNum = max([maxNum, int(os.path.basename(imagefile).split('.')[0])])
    return maxNum+1
        

def main(tag, amount):
    f = flickr.photos_search(tags=tag)

    for n, k in enumerate(f, start=findNextImageNumber()):
        url = k.getURL(size='Small', urlType='source')
        image = urllib.URLopener()
        filename = urlparse.urlparse(url).path
        image.retrieve(url, 'images/' + str(n) + '.jpg')
        print 'Downloading image %d:' % n, url
        
        if n >= amount-1:
            break



def resize(size):
    for imagefile in glob.glob('images/*.jpg'):
        im = Image.open(imagefile)
        im.thumbnail((1000, size[1]), Image.ANTIALIAS)
        im = im.crop((0, 0, size[0], size[1]))
        im.save(imagefile)
  


if __name__ == '__main__':
    main(' '.join(sys.argv[1:-1]), int(sys.argv[-1]))
    resize((100, 100))