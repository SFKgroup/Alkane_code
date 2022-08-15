word = input('word: ')

path = './'+word+'_烷.mol'

bit_data = bin(int.from_bytes(word.encode('utf-8'), byteorder='big', signed=False))[2:]
bit_data = len(bit_data)%4*'0' + bit_data
print(bit_data)
bit_data = bit_data + '0'

ground = '甲乙丙丁戊己庚辛壬癸'
chinese_num = '零一二三四五六七八九'
chinese = '十百千万'
name = ''
c_length = len(bit_data)+3
if c_length <= 10:name = ground[c_length-1]
else:
    for n,m in zip(str(c_length)[::-1],chinese):
        name = m + chinese_num[int(n)] + name
    name = name[1:].replace('零十零','').replace('十零','十')
    if name[:2] == '一十':name = name[1:]

name = name + '烷'
l = 3
r = len(bit_data)+1
count = 4
for p in bit_data:
    if p == '1':l+=count
    count+=1
count = 1
for p in bit_data:
    if p == '1':r+=count
    count+=1

if l >= r:
    l = ''
    count = 4
    for p in bit_data:
        if p == '1':l += str(count)+','
        count+=1
    name = l[:-1]+'-甲基-3-乙基'+name
else:
    r = ''
    count = 1
    for p in bit_data:
        if p == '1':r += str(count)+','
        count+=1
    name = l[:-1]+'-甲基-'+str(len(bit_data)+1)+'-乙基'+name

print(name,'('+str(len(bit_data)+3)+'烷)')

grand = open(path,'w',encoding='utf-8')

grand.write(' \nSFKDraw2D\n\n  0  0  0     0  0              0 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS '+str(len(bit_data)+3)+' '+str(len(bit_data)+2)+' 0 0 0\nM  V30 BEGIN ATOM\n')

grand.write('M  V30 1 C 0.000000 -0.800000 0.000000 0 HCOUNT=3\n')
grand.write('M  V30 2 C 0.666666 -1.190000 0.000000 0 HCOUNT=3\n')
grand.write('M  V30 3 C -0.666666 0.390000 0.000000 0 HCOUNT=2\n')
grand.write('M  V30 4 C -1.333333 0.000000 0.000000 0 HCOUNT=3\n')
grand.write('M  V30 5 C 0.000000 0.000000 0.000000 0 HCOUNT=1\n')

adding = []
for i in range(len(bit_data)):
    num = 6 + i
    if i < len(bit_data)-1:
        h_num = 2 - int(bit_data[i]) - int(bit_data[i+1])
        if num % 2 == 1:
            grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-5)/3,6))+' 0.000000 0.000000 0 HCOUNT='+str(h_num)+'\n')
            if bit_data[i] == '1':adding.append([num,str(round(2*(num-5)/3,6))+' -0.800000 0.000000 0 HCOUNT=3\n'])
        else:
            grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-5)/3,6))+' 0.390000 0.000000 0 HCOUNT='+str(h_num)+'\n')
            if bit_data[i] == '1':adding.append([num,str(round(2*(num-5)/3,6))+' 1.190000 0.000000 0 HCOUNT=3\n'])
    else:
        if num % 2 == 1:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-5)/3,6))+' 0.000000 0.000000 0 HCOUNT=3\n')
        else:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-5)/3,6))+' 0.390000 0.000000 0 HCOUNT=3\n')

for i in adding:
    num += 1
    grand.write('M  V30 '+str(num)+' C '+i[1])
    i.append(num)

grand.write('M  V30 END ATOM\nM  V30 BEGIN BOND\n')

grand.write('M  V30 1 1 3 4\n')
grand.write('M  V30 2 1 3 5\n')
grand.write('M  V30 3 1 1 2\n')
grand.write('M  V30 4 1 1 5\n')


num = 5
for i in range(len(bit_data)):
    grand.write('M  V30 '+str(num)+' 1 '+str(num)+' '+str(num+1)+'\n')
    num+=1

for i in adding:
    grand.write('M  V30 '+str(num)+' 1 '+str(i[0])+' '+str(i[2])+'\n')
    num+=1

grand.write('M  V30 END BOND\nM  V30 END CTAB\nM  END')
grand.close()
