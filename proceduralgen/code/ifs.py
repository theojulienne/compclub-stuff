import Image, ImageDraw

from random import random, seed

def ifs( setmatrix, colour, iterations, w, h, filename ):
	im = Image.new( "RGBA", (w,h), (255,255,255,255) )
	draw = ImageDraw.Draw(im)
	
	n = iterations
	xlast = 0
	ylast = 0
	xmin = float("infinity")
	xmax = float("-infinity")
	ymin = float("infinity")
	ymax = float("-infinity")
	
	( a, b, c, d, e, f, p ) = setmatrix
	for j in range(2):
		for i in range(n):
			r = random();
			psum = 0
			
			for pi in range(len(p)):
				psum += p[pi]
				if r < psum:
					k = pi
					break

			x = a[k] * xlast + b[k] * ylast + e[k]
			y = c[k] * xlast + d[k] * ylast + f[k]
			xlast = x
			ylast = y
			if x < xmin:
				xmin = x
			if y < ymin:
				ymin = y
			if x > xmax:
				xmax = x
			if y > ymax:
				ymax = y
			if j == 1:
				scale = min( w / (xmax - xmin), h / (ymax - ymin) )
				xmid = (xmin + xmax)/2.0
				ymid = (ymin + ymax)/2.0
				ix = w / 2.0 + (x - xmid) * scale
				iy = h / 2.0 + (y - ymid) * scale
				draw.point( (ix, h-iy), fill=colour )
				
	im.save(filename, "PNG")



w = 1200
h = 1200
itern = 1000000
green = (0,255,0,200)
red = (255,0,0,200)
blue = (0,0,255,200)

fern = (
[0.0,0.2,-0.15,0.85],
[0.0,-0.26,0.28,0.04],
[0.0,0.23,0.26,-0.04],
[0.16,0.22,0.24,0.85],
[0.0,0.0,0.0,0.0],
[0.0,1.6,0.44,1.6],
[0.01,0.07,0.07,0.85]
)

dragon = (
[0.824074, 0.088272],
[0.281428, 0.520988],
[-0.212346, -0.463889],
[0.864198, -0.377778],
[-1.882290, 0.785360],
[-0.110607, 8.095795],
[0.8, 0.2]
)

spiral = (
[ 0.787879,  -0.121212,     0.181818],
[-0.424242,   0.257576,    -0.136364],
[ 0.242424,   0.151515,     0.090909],
[ 0.859848,   0.053030,     0.181818],
[ 1.758647,  -6.721654,     6.086107],
[ 1.408065,   1.377236,     1.568035],
[ 0.90    ,   0.05    ,     0.05    ]
)

mandel = (
[0.2020, 0.1380],
[-0.8050, 0.6650],
[-0.6890, -0.5020], 
[-0.3420, -0.2220],
[-0.3730, 0.6600],
[-0.6530, -0.2770],
[0.5,0.5]
)

tree = (
[0.1950 ,   0.4620 , -0.6370 , -0.0350 , -0.0580  ],
[-0.4880,    0.4140,   0.0000,   0.0700,  -0.0700 ],
[ 0.3440,   -0.2520,   0.0000,  -0.4690,   0.4530 ],
[ 0.4430,    0.3610,   0.5010,   0.0220,  -0.1110 ],
[ 0.4431,    0.2511,   0.8562,   0.4884,   0.5976 ],
[ 0.2452,    0.5692,   0.2512,   0.5069,   0.0969 ],
[ 0.2   ,    0.2   ,   0.2   ,   0.2   ,   0.2    ]
)

snowflake = (
[0.38200,    0.11800,    0.11800,   -0.30900,   -0.30900,    0.38200], 
[0.00000,   -0.36330,    0.36330,   -0.22450,    0.22450,    0.00000], 
[0.00000,    0.36330,   -0.36330,    0.22450,   -0.22450,    0.00000], 
[0.38200,    0.11800,    0.11800,   -0.30900,   -0.30900,   -0.38200], 
[0.30900,    0.36330,    0.51870,    0.60700,    0.70160,    0.30900], 
[0.57000,    0.33060,    0.69400,    0.30900,    0.53350,    0.67700],
[0.16, 0.16, 0.16, 0.16, 0.16, 0.16]
)

maple = (
[ 0.1400,    0.4300,    0.4500,    0.4900],
[ 0.0100,    0.5200,   -0.4900,    0.0000],
[ 0.0000,   -0.4500,    0.4700,    0.0000],
[ 0.5100,    0.5000,    0.4700,    0.5100],
[-0.0800,    1.4900,   -1.6200,    0.0200],
[-1.3100,   -0.7500,   -0.7400,    1.6200],
[0.25, 0.25, 0.25, 0.25]
)


print "fern"
ifs( fern, green, itern, w, h, "fern.png" )

print "dragon"
ifs( dragon, red, itern, w, h, "dragon.png" )

print "spiral"
ifs( spiral, blue, itern, w, h, "spiral.png" )

print "mandel"
ifs( mandel, red, itern, w, h, "mandel.png" )

print "tree"
ifs( tree, green, itern, w, h, "tree.png" )

print "snowflake"
ifs( snowflake, blue, itern, w, h, "snowflake.png" )

print "maple"
ifs( maple, red, itern, w, h, "maple.png" )







