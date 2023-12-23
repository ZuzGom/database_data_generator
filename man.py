from random import randint
f=open('prodsum','r')
out=''
for _ in range(2000):
    stud,prod=f.readline().split(',')
    stud,prod=int(stud),int(prod)
    if prod<=50:
        if randint(1,3)==3:
            prod=prod%10+71
    elif prod<=70:
        if randint(1,2)==2:
            prod=prod%10+71
    out+='{},{}\n'.format(stud,prod)
o=open('prodsum_man_2','w')
o.write(out)
o.close()
f.close()
