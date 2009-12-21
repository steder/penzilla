"""
This is a simple script to download all of the
comic strips off of the penny arcade site for archival.
"""

import normalDate #This file needs to be in the path, or in the same directory
import string
import os

def download_lin():
    """<evil laugh>Using this nifty date class I can easily iterate
    through the dates that conveniently fit the penny arcade naming
    convention...  </evil laugh>"""
    '''
    Just Change the year and the year on the directory in the
    path variable and you can download the entire PA comic archive.
    '''
    for year in YEARS:
        today = START[year]
        # Depending on the year PA used either Jpegs or Gifs
        # A more intelligent script could probably check to see
        # which one is available, and then download appropriately.
        # This one just bruteforce tries both types for everything.
        type = "h.jpg"
        type2 = "h.gif"
        finish = FINISH[year]
        while(today >= finish):
            list,list2 = [],[]
            list.append("%s" % today)
            list2.append("%s" % today)
            list.append(type)
            list2.append(type2)
            item = string.join(list,'')
            item2 = string.join(list2,'')
            # Notice this is the one thing that isn't crossplatform
            path = string.join(["wget -nc", year]," ")
            command, command2 = [], []
            command.append(path)
            command.append(item)
            command2.append(path)
            command2.append(item2)
            # This is crossplatform, but the command string itself
            # is not.
            os.popen(string.join(command,''))
            os.popen(string.join(command2,''))
            today = today - 1

import urllib
def download_cross_platform():
    for year in YEARS:
        print year
        today = START[year]
        # Depending on the year PA used either Jpegs or Gifs
        # A more intelligent script could probably check to see
        # which one is available, and then download appropriately.
        # This one just bruteforce tries both types for everything.
        type = "h.jpg"
        type2 = "h.gif"
        finish = FINISH[year]
        while(today >= finish):
            list,list2 = [],[]
            list.append("%s" % today)
            list2.append("%s" % today)
            list.append(type)
            list2.append(type2)
            item = string.join(list,'')
            item2 = string.join(list2,'')
            path = string.join([year,item],"")
            path2 = string.join([year,item2],"")
            print path
            urllib.urlretrieve(path, item)
            print path2
            urllib.urlretrieve(path2, item2)
            today = today - 1
            
# Useful Data values for the above functions:            
YEARS = ["http://www.penny-arcade.com/images/1998/",
         "http://www.penny-arcade.com/images/1999/",
         "http://www.penny-arcade.com/images/2000/",
         "http://www.penny-arcade.com/images/2001/",
         "http://www.penny-arcade.com/images/2002/",
         "http://www.penny-arcade.com/images/2003/"]

START = {"http://www.penny-arcade.com/images/1998/":normalDate.ND(19981231),
         "http://www.penny-arcade.com/images/1999/":normalDate.ND(19991231),
         "http://www.penny-arcade.com/images/2000/":normalDate.ND(20001231),
         "http://www.penny-arcade.com/images/2001/":normalDate.ND(20011231),
         "http://www.penny-arcade.com/images/2002/":normalDate.ND(20021231),
         "http://www.penny-arcade.com/images/2003/":normalDate.ND(20031231)}

FINISH = {"http://www.penny-arcade.com/images/1998/":normalDate.ND(19980101),
         "http://www.penny-arcade.com/images/1999/":normalDate.ND(19990101),
         "http://www.penny-arcade.com/images/2000/":normalDate.ND(20000101),
         "http://www.penny-arcade.com/images/2001/":normalDate.ND(20010101),
         "http://www.penny-arcade.com/images/2002/":normalDate.ND(20020101),
         "http://www.penny-arcade.com/images/2003/":normalDate.ND(20030101)}

if __name__=="__main__":
    download_cross_platform()
