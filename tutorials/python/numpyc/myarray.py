import _myarray

def identity( array ):
    """
    identity_of_array = identity( array )

    This method simply returns the array unchanged.
    """
    return _myarray.identity( array )

def create_array( n ):
    """
    >>> newArray = create_array( 7 )
    >>> print newArray
    array([0, 1, 2, 3, 4, 5, 6],'i')

    This method simply creates a new array and initializes it's values
    to 0 -> N-1.
    """

if __name__=="__main__":
    import Numeric
    A = Numeric.zeros((5,5),Numeric.Int32)
    print identity( A )
