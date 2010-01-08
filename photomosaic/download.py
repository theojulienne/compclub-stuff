# Sourced from
# http://jesolem.blogspot.com/2009/02/using-python-to-download-images-from.html
# With major changes by Goldy

from PIL import Image
import flickr
import urllib, urlparse
import os, sys, glob


def findNumImages():
    return len(filter(lambda x: '.jpg' in x.lower(), os.listdir('images')))


def main(tag, amount):
    f = flickr.photos_search(tags=tag)
    imagesAtStart = findNumImages()
    for n, k in enumerate(f, start=imagesAtStart):
        url = k.getURL(size='Small', urlType='source')
        image = urllib.URLopener()
        filename = urlparse.urlparse(url).path
        image.retrieve(url, 'images/' + str(n) + '.jpg')
        print 'Downloading image %d:' % n, url
        
        if n-imagesAtStart >= amount-1:
            break



def resize(size):
    for imagefile in glob.glob('images/*.jpg'):
        im = Image.open(imagefile)d
        im.thumbnail((1000, size[1]), Image.ANTIALIAS)
        im = im.crop((0, 0, size[0], size[1]))
        im.save(imagefile)
  


if __name__ == '__main__':
    main(' '.join(sys.argv[1:-1]), int(sys.argv[-1]))
    resize((100, 100))