import scipy.optimize
#inputs
PD=9
PD_min=[2,2,2]
PD_max=[4,4,4]
c=[1,2,3]

#Processing
def economic(PD,PD_min,PD_max,c):
    B=[PD]
    A=[[1  for i in range (0,len(PD_min))]]
    print(A)
    bounds=[(0,0) for i in range (0,len(PD_min))]
    for i in range (0,len(PD_min)):
        bounds[i]=(PD_min[i],PD_max[i])
    result=scipy.optimize.linprog(c,A_eq=A,b_eq=B,bounds=bounds,method='highs')
    S = [i for i,m in enumerate(result.x) if m> 0]
    PG=max(c[i] for i,m in enumerate(result.x) if m>0)
    M = [i for i, m in enumerate(result.x) if m == 0]
    return PG,result.x,S,M

# OUTPUT
print(economic(PD,PD_min, PD_max, c))
