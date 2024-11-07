import copy
import fractions 

# Takes a matrix(list of lists) and performs the row operation r1 -> r1*xr1 'op' r2*yr2
# Example: taboper([[1,2,3],[4,5,6],[7,8,9]],1,2,3,4,"+") (Row 1 -> Row 1*3 + Row 2*4)
# Returns: [[13, 14, 15], [4, 5, 6], [7, 8, 9]]
def taboper(l,r1,r2,xr1,yr2,op):
    r1=r1-1
    r2=r2-1
    l1=copy.deepcopy(l)
    if op=="*":
        for pos,i in enumerate(l1[r1]):
            l1[r1][pos] = l1[r1][pos] * xr1
            if type(l1[r1][pos])==fractions.Fraction:
                l1[r1][pos]=l1[r1][pos].numerator
        return l1
    if op=="/":
        for pos,i in enumerate(l1[r1]):
            if l1[r1][pos] % xr1 == 0:
                l1[r1][pos] = l1[r1][pos] // xr1
            else:
                l1[r1][pos] = fractions.Fraction(l1[r1][pos],xr1)
        return l1
    newr1=[]
    newr2=[]
    for i in l1[r1]:
        newr1.append(i*xr1)
    for i in l1[r2]:
        newr2.append(i*yr2)
    if op=="+":
        for pos,i in enumerate(l1[r1]):
            if type(newr1[pos])==int and type(newr2[pos])==int:
                l1[r1][pos]=newr1[pos]+newr2[pos]
            else:
                l1[r1][pos]=fractions.Fraction(newr1[pos]+newr2[pos])
                if l1[r1][pos].denominator == 1:
                    l1[r1][pos]=l1[r1][pos].numerator
                if l1[r1][pos].numerator == 0:
                    l1[r1][pos]=0
        return l1
    else:
        for pos,i in enumerate(l1[r1]):
            if type(newr1[pos])==int and type(newr2[pos])==int:
                l1[r1][pos]=newr1[pos]-newr2[pos]
            else:
                l1[r1][pos]=fractions.Fraction(newr1[pos]-newr2[pos])
                if l1[r1][pos].denominator == 1:
                    l1[r1][pos]=l1[r1][pos].numerator
                if l1[r1][pos].numerator == 0:
                    l1[r1][pos]=0
        return l1

# Takes a matrix(list of lists) and returns the matrix after reducing around a pivot found using Danzig's method
def pivot(l):
    max = 0
    er=0
    for pos in range(0,len(l[0])-1):
            if l[0][pos]>=max:
                max = l[0][pos]
                er = pos
    print("Entering variable: x"+str(er+1))
    if max == 0:
        return l
    col=[]
    column=0
    for i in range(0,len(l)):
        col.append(l[i][er])
    min = 100000
    for i in range(1,len(col)):
        if col[i] != 0:
            if (l[i][-1]/col[i]) < min and (l[i][-1]/col[i]) >= 0:
                min = l[i][-1]/col[i]
                column = i
    if min == 100000:
        return l

    l2=copy.deepcopy(l)
    low=l2[column][er]
    for k in range(0,len(l2[column])):
        if low == 0:
            break
        if l2[column][k]%low == 0: 
            l2[column][k] = l2[column][k]//low
        else:
            l2[column][k] = fractions.Fraction(l2[column][k],low)
    for i in range(0,len(l2)):
        value=l2[i][er]
        for pos in range(0,len(l2[i])):
            if i!=column:
                l2[i][pos] = l2[i][pos] - value*l2[column][pos]
    return l2

# Just takes a string and returns a list of numbers inc fractions
# Format the string like this: "1 2 3/4 5 6 7/8"
def commarize(n):
    for i in n:
        if i==" ":
            n=n.replace(i,",")
    n=n.split(",")
    for pos,i in enumerate(n):
        if "/" not in i:
            n[pos]=int(i)
        else:
            n[pos]=fractions.Fraction(int(i.split("/")[0]),int(i.split("/")[1]))
    return n

# Pretty prints a matrix(list of lists) row by row.
# Also prints the cost row. Input the cost row as a string: "-z,x1,x2...,RHS"
def prettyprint(cr,l):
    cr=cr.split(",")
    print(cr,end="\n")
    l2=copy.deepcopy(l)
    for pos,i in enumerate(l2):
            for posi,j in enumerate(i):
                if len(str(j))==1:
                    l2[pos][posi] = " " + str(l2[pos][posi])
                else:
                    l2[pos][posi] = str(l2[pos][posi])
            print(i,end="\n")

# Generates latex code given the cost row(-z,x1,x2...,RHS) and a matrix(list of lists). 
# Format of cost row as a string: "-z,x1,x2...,RHS"
def generator(cr,l):
    cr=cr.split(",")
    for i in range(len(cr)):
        if i!=len(cr)-1:
            if len(cr[i])!=2 or cr[i][-1].isdigit()==False:
                print(cr[i],end=" & ")
            else:
                print("$"+cr[i][0]+"_"+cr[i][-1]+"$",end=" & ")
        else:
            print(cr[i],end=" \\\ [0.85mm] \\hline \n")
    for i in l:
        for posi,j in enumerate(i):
                if type(j) == int and posi == len(i)-1:
                    print(j,end=" \\\ [0.85mm] \\hline \n")
                elif type(j) != int and posi == len(i)-1:
                    if j.denominator == 1:
                        print(j.numerator,end=" \\\ [0.85mm] \\hline \n")
                    elif j.numerator == 0:
                        print(0,end=" \\\ [0.85mm] \\hline \n")
                    else:
                        print("$\\frac{"+str(j.numerator)+"}{"+str(j.denominator)+"}$",end=" \\\ [0.85mm] \\hline \n")
                elif type(j) == int:
                    print(j,end=" & ")
                else:
                    if j.denominator == 1:
                        print(j.numerator,end=" & ")
                    elif j.numerator == 0:
                        print(0,end=" & ")
                    else:
                        print("$\\frac{"+str(j.numerator)+"}{"+str(j.denominator)+"}$",end=" & ")

# Takes a cost row(-z,x1,x2...,RHS) and a matrix(list of lists) and performs the simplex method on it.
# Prints the tableaus in latex code.
def completedsimplex(cr,l):
    lists = []
    l2=copy.deepcopy(l)
    l2=pivot(l2)
    while l2 != l:
        lists.append(l2)
        l=copy.deepcopy(l2)
        l2=pivot(l2)
    ls = cr.split(",")
    lines = "|"
    for l in range(0,len(ls)):
        lines = lines + "l|"
    for pos,i in enumerate(lists):
        print("\\textbf{Tableau "+str(pos)+"} \[0.85mm]\n")
        print("\\begin{tabular}{"+lines+"}\n")
        print("\\hline\n")
        generator(cr,i)
        print("\\end{tabular}\n")

