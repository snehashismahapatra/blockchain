import datetime

x=str(datetime.datetime.now()).replace("-","").replace(" ","").replace(":","").replace(".","")
print(x)
inp=input("Enter seed (9 to 12): ")
while len(inp)<9 or len(inp)>12:
    print("improper input.....")
    inp=input("Enter seed (9 to 12): ")
st=""
for i in x:
    st=st+str(ord(i))
print(inp[:12])
for i in inp[:13]:
    st=st+str(ord(i))
if len(st)<77:
    n_space=(77-len(st))//2
    st=st+("32"*n_space)
check_st=int(st)
temp=0
while check_st not in range(20000000000000000000000000000000000000000000000000000000000000000000000000000,115792089237316195423570985008687907852837564279074904382605163141518161494337):
    if check_st<20000000000000000000000000000000000000000000000000000000000000000000000000000:
        check_st=check_st+(ord(inp[2])+ord(inp[6])+temp)
        temp=abs(temp-ord(inp[2])+ord(inp[6]))
    if check_st>115792089237316195423570985008687907852837564279074904382605163141518161494337:
        check_st=check_st-(ord(inp[2])+ord(inp[6])-temp)
        temp=abs(temp+ord(inp[2])+ord(inp[6]))
st=str(check_st)
key=hex(int(st)).replace("0x","")
print(key)
print(len(key))
