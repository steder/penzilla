# Let's get the average and our grades:
us = {"Sammy":0,"summy":0,"spoonman":0}
homework_ave = 0
total = 0
files = ["hw0grades.txt"]

students = 0

# Get the Data
for file in files:
    infile = open(file,"r")
    while infile:
        line = infile.readline()
        for person in us:
            if line.find(person) >= 0 and len(line.split()[0])==len(person):
                us[person] = float( line.split()[1] )
        s = line.split()
        n = len(s)
        if n == 0:
            break
        try:
            total += float( s[ n-1 ] )
        except:
            pass
        students += 1

# Compute the Average
print total, students
homework_ave = total / ( students * (1.0) )

# Assume the average is C
# Define grade ranges:
c = homework_ave 
cmax = c + homework_ave * .05
cmin = c - homework_ave * .05
bmax = cmax + homework_ave * .1
bmin = cmax
amin = bmax
amax = cmin
dmin = cmin - homework_ave * .1
emax = dmin
# Print out some STATS:
print "The AVERAGE for this homework:", homework_ave
print "The A range:", ">="+str(amin)
print "The B range:", bmax,"-", bmin
print "The C range:", cmax,"-", cmin
print "The D range:", dmax,"-", dmin
print "The E range:", "<"+str(emax)

# Assign grades to us:
for person in us:
    if us[person] >= amin:
        print person,"(",us[person],")","probably got an A on this assignment."
    elif bmax > us[person] >= bmin:
        print person,"(",us[person],")","probably got a B on this assignment."
    elif cmax > us[person] >= cmin:
        print person,"(",us[person],")","probably got a C on this assignment."
    elif dmax > us[person] >= dmin:
        print person,"(",us[person],")","probably got a D on this assignment."
    else:
        print person,"(",us[person],")","probably got a E on this assignment."
        
