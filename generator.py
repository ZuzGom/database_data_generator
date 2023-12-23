import random
t=[i+1 for i in range(40)]
random.shuffle(t)

f=open("e3",'r')
# foo=open("foo",'r')

def number(s):
    o=''
    for x in s.split(' '):
        o+=x
    return o[:12]
ot=''
s=[100,90,100,90,120,80,90,110,90,90]
for i in range(879):
    line=f.readline().split(',')
    ot+="({},'{}',{},{}),\n".format(line[0][1:],line[1],line[2],line[3][:-1])
f.close()
f=open("e3",'w')
f.write(ot)
f.close()

# output="INSERT INTO SubjectCourseSylabus \nVALUES\n"
# for i in range(40):
#     line=f.readline().split(',')
#     # print(line)
#     output+="({},'{}',{},{},{},{}{},'{}'),\n".format(i+1,line[1],t[i],line[2],line[3],line[3][0],2*float(line[3][2:]),line[4][:-1])
# output=output[:-2]+";"
# print(output)