#!/usr/bin/python
"""
Sorts Dotted Decimal IP Addresses

xxx.yyy.zzz.www
"""
import cgi, cgitb
cgitb.enable()
# Useful for a little error checking
import string

class IP:
    def __init__(self, address_string=None):
        self.a,self.b,self.c,self.d = -1,-1,-1,-1
        if address_string!=None:
            self.set(address_string)

    def set( self, address ):                
        quads = address.split(".")
        try:
            self.a = int(quads[0])
            self.b = int(quads[1])
            self.c = int(quads[2])
            self.d = int(quads[3])
        except ValueError:
            self.a,self.b,self.c,self.d=-1,-1,-1,-1

    def __cmp__(self, addr2):
        if self.greaterthen(addr2):
            return 1
        elif self.equalto(addr2):
            return 0
        else:
            return -1

    def greaterthen( self,  addr2 ):
        if self.a > addr2.a:
            return 1
        elif self.a == addr2.a and self.b > addr2.b:
            return 1
        elif self.b == addr2.b and self.c > addr2.c:
            return 1
        elif self.c == addr2.c and self.d > addr2.d:
            return 1
        else:
            return 0

    def equalto( self, addr2 ):
        if self.a == addr2.a and \
               self.b == addr2.b and \
               self.c == addr2.c and \
               self.d == addr2.d:
            return 1
        else:
            return 0

    def __str__( self ):
        string = str(self.a) + "."
        string += str(self.b) + "."
        string += str(self.c) + "."
        string += str(self.d)
        return string
    
    def __hash__( self ):
        num = self.a * 1000
        num += self.b * 100
        num += self.c * 10
        num += self.d
        return int(num)

    def __repr__( self ):
        string = str(self.a) + "."
        string += str(self.b) + "."
        string += str(self.c) + "."
        string += str(self.d)
        return string

if __name__=="__main__":
    print "Content-Type: text/html"
    print # Blank Line
    
    file_numbers = [1,2,3,4,5,6,7,8]
    filenames = []
    for each in file_numbers:
        filenames.append("../hits"+str(each)+".txt")
    
    
                
    print "<html>"
    print "<HEAD>"
    print "<TITLE>"
    print "IP Stats"
    print "</TITLE>"
    print "<body>"
    print "<H1>IP Stats</H1>"

    for filename in filenames:
        # 1). Read in the file
        file = open(filename,"r")
        lines = file.readlines()
        # 2). Get the IP's
        addresses = {}
        
        for line in lines:
            if ( string.strip( line, string.whitespace )=='' ):
                continue
            temp = IP( line )
            if temp in addresses.keys():
                addresses[temp] += 1
            else:
                addresses[temp] = 1
                
        # 2). Sort the IP's
        keys = addresses.keys()
        keys.sort()

        # 3). Print a Table of Sorted Ip's
        print "<H2>","IP's in file:",filename,"</h2>"
        print "<table>"
        for key in keys:
            print "<tr>"
            print "<td>",key,"</td><td>", addresses[key],"</td>"
            print "</tr>"
        print "</table>"

    print "</body>"
    print "</html>"
    

