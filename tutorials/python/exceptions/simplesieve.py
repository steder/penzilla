#simplesieve.py
import Numeric

def sieve( n ):
	# Let's start at array index 1 instead of 0
	array = Numeric.zeros(n+1)
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
	n = int(input)
	primes = sieve( n )
	print "There are %d primes between 1 and %d.  They are:" % (len(primes),n)
	print primes
	return
	
if __name__=="__main__":
	main()
