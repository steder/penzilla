# lamba-map.py
# Remember our "map" function from a little earlier?
import map
list = xrange(0,2,100)

# Let's redefine increment as a lambda function.
increment = lambda x: x + 1

# This looks like how you would normally do it.
map.map( increment, list )

# Or, we're do lazy for that "=" statement above :~)
# That and increment is so simple...
map.map( lambda x: x + 1, list )

# Where lambda won't work:
# Lambda's cannot contain statements.  So although the following
# code is almost valid Ocaml, it is _not_ valid Python.  :~)
lmap = ( lambda f, lst:
    if lst == []:
        return []
    else:
        return [ f( lst[0] ) ] + lmap( f lst[1:] ) )
