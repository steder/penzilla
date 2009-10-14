# myexception.py

import exceptions
class Expletive(exceptions.Exception):
	def __init__(self):
		return
		
	def __str__(self):
		print "","An Expletive occured!"
	
def main():
	raise Expletive
	
if __name__=="__main__":
	try:
		main()
	except ImportError:
		print "Unable to import something..."
	except Exception, e:
		raise e
