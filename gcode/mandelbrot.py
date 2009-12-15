import gcode

IMG_WIDTH  = 1000
IMG_HEIGHT = 1000
IMG_DEPTH  = 5.0
BOTTOM_LEFT = (-2, -1.0)
TOP_RIGHT   = ( 0.5,  1.0)
MAX_ITERATIONS = 256

def mandelbrot(px, py):
    count = 0
    widthRatio = px/float(IMG_WIDTH)
    heightRatio = py/float(IMG_HEIGHT)
    px = BOTTOM_LEFT[0] + widthRatio * (TOP_RIGHT[0]-BOTTOM_LEFT[0])
    py = BOTTOM_LEFT[1] + heightRatio * (TOP_RIGHT[1]-BOTTOM_LEFT[1])
    x, y = 0, 0
    
    while (x**2+y**2)**0.5 < 2 and count < MAX_ITERATIONS:
        x, y = (x**2 - y**2 + px), (2*x*y + py)
        count += 1
        
    depth = ((count - 1) / 255.0)*5
    return depth

def createMandelbrotGCode(gcode):
    previousDepth = IMG_DEPTH + 1
    
    for y in range(IMG_HEIGHT):
        for x in range(IMG_WIDTH):
            currentDepth = mandelbrot(x, y)

            if currentDepth > previousDepth: # if currentdepth higher than prevdepth
                gcode.cutAbsolute(z=currentDepth) # then first rise, then move
                
            gcode.cutAbsolute(x=float(x), y=float(y))
            
            if currentDepth < previousDepth: # currentdepth lower than prevdepth
                gcode.cutAbsolute(z=currentDepth) # then move first, then sink
            
            previousDepth = currentDepth
        gcode.moveAbsolute(x=0, y=y)

def main():
    o = gcode.simpleGenerator(open('output.txt', 'w'))
    createMandelbrotGCode(o)

main()