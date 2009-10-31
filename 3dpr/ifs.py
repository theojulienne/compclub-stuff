from random import random, seed

def ifs( matrix, iterations, width, height, depth ):
        points = []

        n = iterations
        xlast = 0
        ylast = 0
        zlast = 0

        xmin = float("infinity")
        xmax = float("-infinity")
        ymin = float("infinity")
        ymax = float("-infinity")
        zmax = float("infinity")
        zmin = float("-infinity")

        ( ma, mb, mc, md, me, mf, mg, mh, mi, cx, cy, cz, probDistribution ) = matrix

        for i in range(n):


                # sample from probability distribution
                r = random();
                pSum = 0
                for pIndex in range(len(probDistribution)):
                        pSum += probDistribution[pIndex]
                        if r < pSum:
                                k = pIndex
                                break

                # select transformation to apply

                x = ma[k] * xlast + mb[k] * ylast + mc[k] * zlast + cx[k]
                y = md[k] * xlast + me[k] * ylast + mf[k] * zlast + cy[k]
                z = mg[k] * xlast + mh[k] * ylast + mi[k] * zlast + cz[k]

                xlast = x
                ylast = y
                zlast = z

                if x < xmin:
                        xmin = x
                if y < ymin:
                        ymin = y
                if x > xmax:
                        xmax = x
                if y > ymax:
                        ymax = y
                if z > zmax:
                        zmax = z
                if z < zmin:
                        zmin = z

                scale = 1
                # scale = min( width / (xmax - xmin), height / (ymax - ymin), depth / (zmax - zmin) )
                """
                xmid = (xmin + xmax)/2.0
                ymid = (ymin + ymax)/2.0
                zmid = (zmin + zmax)/2.0
                
                ix = width / 2.0 + (x - xmid) * scale
                iy = height / 2.0 + (y - ymid) * scale
                iz = depth / 2.0 + (z - zmid) * scale
                """
                points.append( list((x*scale, y*scale, z*scale)) )

        return points

w = 256
h = 256
d = 256

itern = 5000

seed(4)
def tdv(): # the 3d values
    return random()*0.4

fern = (
[0.0,0.2,-0.15,0.85],  #a 
[0.0,-0.26,0.28,0.04], #b

[tdv(),tdv(),tdv(),tdv()], # c!

[0.0,0.23,0.26,-0.04], #d
[0.16,0.22,0.24,0.85], #e

[tdv(),tdv(),tdv(),tdv()], # f!

[tdv(),tdv(),tdv(),tdv()], # g!
[tdv(),tdv(),tdv(),tdv()], # h!
[tdv(),tdv(),tdv(),tdv()], # i!

[0.0,0.0,0.0,0.0],  #cx
[0.0,1.6,0.44,1.6], #cy
[tdv(),tdv(),tdv(),tdv()],  # cz!

[0.01,0.07,0.07,0.85] # prob
)

print 'module pixels;'
print 'const static float[3][] awesomePixels = '
print ifs( fern, itern, w, h, d )
print ';'
