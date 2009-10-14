def createPalette( ):
    r,g,b = -1,0,256
    palette = []
    for i in xrange(0,256):
        r += 1
        b -= 1
        palette.append( (r,g,b) )
    return palette

if __name__=="__main__":
    a = createPalette()
    print a
