#simplesieve.py
import traceback
try:
	import Numeric
except ImportError:
	print "Sorry, you don't have the Numeric module installed, and this"
	print "script relies on it.  Please install or reconfigure Numeric"
	print "and try again."

def sieve( n ):
	# Let's start at array index 1 instead of 0
	try:
		array = Numeric.zeros(n+1)
	except ValueError:
		traceback.print_exc()
		return []
		
	for i in xrange(1,n+1):
		array[i] = i
	
	done = False
	prime = array[2] # The number, as well as the index.
	while( prime < n ):
		# Index 2 corresponds to the number 2 for this indexing scheme
		index = prime
		index += prime
		# Mark multiples of prime
		while( index <= n ):
			array[index]=-1
			index += prime
		# Get a new prime
		prime+=1
		while( prime < n ):
			if (array[prime]==-1):
				prime+=1
			elif (prime < n ):
				break
		#print prime,n,array

	# Grab all the primes
	primes = []
	for i in xrange(1,n+1):
		if( array[i] != -1):
			primes.append(array[i])
			
	return primes

def main():
	print "This program computes the number of primes between 1 and n\nusing the Sieve of Erastothenes."
	input = raw_input("Enter (n):")
	
	try:
		n = int(input)
	except ValueError:
		print "You entered:",input
		print "Please enter a positive integer next time."
		return
		
	primes = sieve( n )
	print "There are %d primes between 1 and %d.  They are:" % (len(primes),n)
	print primes
	return
	
if __name__=="__main__":
	try:
		main()
	except:
		print "An unhandled exception occured, here's the traceback!"
		traceback.print_exc()
