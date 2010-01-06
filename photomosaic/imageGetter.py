import urllib2, os, re, sets



def parseHTMLForImages(filehandle):
	htmlSource = filehandle.read()
	
	images = re.findall(r"https?://(?:[a-z\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg)", htmlSource)
	
	images = list(sets.Set(images)) # unify
	
	print images
	
	filehandle.close()
	return images


def downloadImages(keyword, numImagesOfEachColour):

	downloadCommand = 'wget -l1 -A jpg -U \"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.6) Gecko/20050405 Firefox/1.0 (Ubuntu package 1.0.2)\" -nd --wait=2 --random-wait --no-parent -nv '


	googleColours = ["full", "red","green","blue", "orange", "yellow", "teal", "purple", "pink", "white", "gray", "black", "brown"]

	for colour in googleColours:

		searchURL = "http://images.google.com/images?q=%s+filetype%%3Ajpg&imgtype=photo&imgcolor=%s" % (keyword, colour)
	
		print "Retrieving Images From: " + searchURL

		googleTricker = urllib2.build_opener()
		googleTricker.addheaders = [('User-agent', 'Mozilla/5.0')]
		htmlFile = googleTricker.open(searchURL)

		#htmlFile = urllib2.urlopen(searchURL)

		imageURLs = parseHTMLForImages(htmlFile)
	
	
		dirName = colour
	
		print "  - entering '%s' directory" % dirName
		if os.path.isdir(dirName):
		    os.chdir(dirName)
		else:
		    os.mkdir(dirName)
		    os.chdir(dirName)
	
		for i in range(numImagesOfEachColour):
			if i < len( imageURLs ):
				imageURL = imageURLs[i]
				print "  - downloading image %d: %s" % (i, imageURL)
				os.system(downloadCommand + imageURL + ' -O ' + str(i) + '.jpg')
	
		print "  - returning to parent directory"	
		os.chdir("..")
	
downloadImages( "dog", 3 )
