# Let's get the average and our grades:
US = {"Sammy":0,"summy":0,"spoonman":0}
HWAVE = 0
TOTAL = 0
FILES = ["hw0grades.txt"]

STUDENTS = 0

# Get the Data
for file in FILES:
    infile = open(file,"r")
    while infile:
        line = infile.readline()
        for person in US:
            if line.find(person) >= 0 and len(line.split()[0])==len(person):
                US[person] = float( line.split()[1] )
        s = line.split()
        n = len(s)
        if n == 0:
            break
        try:
            TOTAL += float( s[ n-1 ] )
        except:
            pass
        STUDENTS += 1

# Compute the Average
print TOTAL, STUDENTS
HWAVE = TOTAL / ( STUDENTS * (1.0) )

# Assume the average is C
# Define grade ranges:
C = HWAVE 
Cmax = C + HWAVE * .05
Cmin = C - HWAVE * .05
Bmax = Cmax + HWAVE * .1
Bmin = Cmax
Amin = Bmax
Dmax = Cmin
Dmin = Cmin - HWAVE * .1
Emax = Dmin
# Print out some STATS:
print "The AVERAGE for this homework:", HWAVE
print "The A range:", ">="+str(Amin)
print "The B range:", Bmax,"-", Bmin
print "The C range:", Cmax,"-", Cmin
print "The D range:", Dmax,"-", Dmin
print "The E range:", "<"+str(Emax)

# Assign grades to US:
for person in US:
    if US[person] >= Amin:
        print person,"(",US[person],")","probably got an A on this assignment."
    elif Bmax > US[person] >= Bmin:
        print person,"(",US[person],")","probably got a B on this assignment."
    elif Cmax > US[person] >= Cmin:
        print person,"(",US[person],")","probably got a C on this assignment."
    elif Dmax > US[person] >= Dmin:
        print person,"(",US[person],")","probably got a D on this assignment."
    else:
        print person,"(",US[person],")","probably got a E on this assignment."
        
