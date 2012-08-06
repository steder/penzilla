# map.py
def map( fun, list ):
    nlist = []
    for item in list:
        nlist.append( fun( item ) )
    return nlist

def rmap ( fun, list ):
    if list == []:
        return []
    else:
        return [fun( list[0] )] + rmap( fun, list[1:] )

def increment(x):
    return x+1
