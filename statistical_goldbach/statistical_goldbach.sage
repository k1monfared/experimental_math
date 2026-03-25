# Below I define functions that get a positive integer number n as an input and return a plot of number of the ways all first n even numbers can be decomposed as sum of two prime numbers.


# this makes a list of all the decompositions of 2,4,...,2n
def list_of_all_decompositions(m,n):
    AllDecompositions = []
    Primes = primes_first_n(floor(n/2)+1)
    max = len(Primes)
    
    for i in range(m,n):
        for j in range(max):
            for k in range(max):
                if 2*i == Primes[j] + Primes[k]:
                    AllDecompositions = AllDecompositions + [[2*i,Primes[j],Primes[k]]]
    
    return(AllDecompositions)

# this counts the number of decompositions for each i=2,4,...,2n-4
def number_of_decompositions(L,m,n):
    NumberOfDecompositions = []
    for i in range(m,n-1):
        count = 0
        j = 0
        while j < (len(L)):
            while 2 * i == L[j][0]:
                count = count + 1
                j = j + 1
            j = j+1
        NumberOfDecompositions = NumberOfDecompositions + [[2*i,count]]
    
    return(NumberOfDecompositions)

# this calls the previous two functions and draws the plot
def plot_number_of_decompositions(lower_limit, upper_limit , function_of_x): 
    
    f(x) = function_of_x   
    m = floor(lower_limit/2)
    n = ceil(upper_limit/2)
    
    L = list_of_all_decompositions(m,n+2)
    Points = number_of_decompositions(L,m,n+2)
    
    i = 0
    C = (0,0,1)
    S = 20    
    if Points[i][1] < f(Points[i][0]):
        C = (1,0,0)
    elif Points[i][1] == f(Points[i][0]):
        C = (0,1,0)
    P = plot(f(x), (x,2*m,2*n),rgbcolor=(0,0,0))

    
    for i in range( len(Points)):
        C = (0,0,1)
        if Points[i][1] < f(Points[i][0]):
            C = (1,0,0)
        elif Points[i][1] == f(Points[i][0]):
            C = (0,1,0)
        P += point(Points[i], rgbcolor = C, size = S)
        
    return(P)

###################################
# Sample input

a = (1+sqrt(5))/2
f = (x/(a*pi))^(1/a)

plot_number_of_decompositions(2, 1000 , f)
