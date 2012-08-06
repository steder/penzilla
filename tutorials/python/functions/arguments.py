# Simplest Arguments
def multiprint(n, txt):
    i = 0
    while i < n:
        print txt

# This throws an error
multiprint()

# Default Values
def multiprint(n=5, txt=""):
    i = 0
    while i < n:
        print txt
        
# This works just fine
multiprint()

# Labels
def multiprint(n=5, txt=""):
    i = 0
    while i < n:
        print txt

# I want to call multiprint, but I'm happy with
# n = 5, so I don't want to reassign it.
# I can use the labels to set "txt" without having to set n.
multiprint(txt="Hello World!")

# You can mix default and required variables
# Notice there is a default on list, but since it is
# defined in the middle of the list, you can't do this:
# fold_right( lambda x y: x + y, 0 )

# No, you need to specify lst as well, even though you
# may be happy with the default value.
# fold_right( lambda x y: x + y, [], 0 )
def fold_right(fun, lst=None, base):
    lst = lst if lst is not None else []
    if not lst:
        return base
    else:
        return fun(lst[0], fold_right(fun, lst[1:], base))

# Now, let's say I want to just define fun and base, and not list.
# I could do this:
fold_right(fun=lambda x, y: x + y, base=0) #Look 'ma, no list!

# This makes sense if you have a large argument list (5, 10, + variables),
# some default and some required.  You can easily specify just the
# variables necessary to run the function and leave the defaults alone.  
