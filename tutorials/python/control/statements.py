# Continue
nlist = []
for i in xrange(0,100):
    if i == 0:
        continue
    nlist.append( 7 / i )

# Break
# How many heads can we flip in a row?
heads = 0
while 1:
    if x == 0:
        break
    else:
        x = random.rand(0,1)
        heads += 1

# Pass
# If you don't want to do anything in a case
x = 0
while 1:
    if x <= 100:
        pass
    elif x == 101:
        print "Just enough Dalmations!"
    else:
        print "Argh!  Too many Dalmations!"
        break
    x += 1
    
