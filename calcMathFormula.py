#! /usr/bin/env python

import sys
import StringIO
from math import *
import numpy as np

################################################################################
################################################################################
"""
The script:
i.  peforms mathematical operations between columns of an input data file. 
ii. prints out the calculated values with the reference column values. The 
    default reference column is 1st column. 

-- To change the reference column use: -rc column_id
-- To restrict the operation for a range of values of reference column:
   -set lower_limit upper_limit  
-- To calculate the cumulative sum use: -csum
"""
################################################################################

################################################################################
"""  reading command line arguments """
################################################################################
rcolumn  = 0     # reference column
drange   = [0.0, 1.0]
Setlimit = False
Csum     = False # cumulative sum 
carg     = 1

if len(sys.argv)<2:
    sys.stderr.write("Usage: formula e.g. '(y0+y1*y2**3)/log(y3)',  filename(s) ")
    print
    sys.exit()
    
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-rc":
            carg += 1
            rcolumn = int(sys.argv[carg])
            print "# reference column ", rcolumn
            carg += 1
        
        if word == "-set":
            Setlimit = True 
            drange = [float(sys.argv[carg+1]), float(sys.argv[carg+2])]
            carg += 3
            print "# range: ", drange
            
        if word == "-csum":
            Csum = True
            carg += 1


get_formula = sys.argv[carg]
print "#", get_formula 
carg += 1


################################################################################
"""  evaluate the formula """
################################################################################
def evaluateFormula(data, columns, formula):

    cum_sum = 0 

    for l in range(len(data)):

        if data[l][rcolumn] >= drange[0] and data[l][rcolumn] <= drange[1]:
            cformula = '' # constructinag the formula including data columns
            s = 0
            c = 0
            while  s < len(formula):
                if formula[s] == 'y':
                    cformula += str(data[l][columns[c]])
                    c += 1 
                else:
                    cformula += formula[s]
                    
                s += 1
                    
            if l==0:
                sys.stderr.write('# check the operation for 1st row: '+str(cformula)+'\n')
    
            val = eval(cformula)  # evaluate the formula from the string

            if Csum: # compute cumulative sum 
                cum_sum += val
                print data[l][rcolumn], val, cum_sum
            else:
                print data[l][rcolumn], val


################################################################################
"""  extract the formula from the formula-argument """
################################################################################
y_index    = []
wy_formula = []

i=0
while i < len(get_formula):

    if get_formula[i] == 'y':
        c = 1
        j = i+1
        intstr = ''
        while j < len(get_formula):
            istr =  get_formula[j]
            if ord(istr) > 47 and ord(istr) < 58: # ASCII values between 0 to 9
                intstr += istr
                c += 1
            else:
                break
                
            j += 1

        i += c
        y_index.append(int(intstr))
        wy_formula.append('y')

    else:
        wy_formula.append(get_formula[i])
        i += 1


################################################################################
"""  reading input files """ 
################################################################################
for filename in sys.argv[carg:]:

    f = open(filename)
    data = f.readlines()
    f.close()

    List = []
    for j in range(0, len(data)):
        if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = np.fromstring(data[j],sep=" ")
            List.append(tmp)

    sys.stderr.write('# import '+filename+'\n')
    l = np.array(List)
    No_rows = len(l)
    No_columns = len(l[0])
    sys.stderr.write('# nb. of rows and columns: '+str(No_rows)+' '+str(No_columns)+'\n')
    
    if Setlimit == False:
        drange[0] = l[0][rcolumn] 
        drange[1] = l[No_rows-1][rcolumn] 

    if drange[0] > drange[1]:
        rval      =  drange[1]
        drange[1] = drange[0]
        drange[0] = rval

    evaluateFormula(l,y_index,wy_formula)
