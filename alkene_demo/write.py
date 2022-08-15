word = input('word: ')

path = './'+word+'.mol'

bit_data = bin(int.from_bytes(word.encode('utf-8'), byteorder='little', signed=False))[2:]
print(bit_data)

grand = open(path,'w',encoding='utf-8')

grand.write(' \nKingDraw2D\n\n  0  0  0     0  0              0 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS '+str(len(bit_data)+3)+' '+str(len(bit_data)+2)+' 0 0 0\nM  V30 BEGIN ATOM\n')

grand.write('M  V30 1 C 0.000000 -0.800000 0.000000 0 HCOUNT=3\n')
grand.write('M  V30 2 C -0.666666 0.390000 0.000000 0 HCOUNT=3\n')
grand.write('M  V30 3 C 0.000000 0.000000 0.000000 0 HCOUNT=1\n')

num = 4
for i in range(len(bit_data)):
    num = 4 + i
    if i < len(bit_data)-1:
        h_num = 2 - int(bit_data[i]) - int(bit_data[i+1])
        if num % 2 == 1:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-3)/3,6))+' 0.000000 0.000000 0 HCOUNT='+str(h_num)+'\n')
        else:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-3)/3,6))+' 0.390000 0.000000 0 HCOUNT='+str(h_num)+'\n')
    else:
        if num % 2 == 1:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-3)/3,6))+' 0.000000 0.000000 0 HCOUNT=3\n')
        else:grand.write('M  V30 '+str(num)+' C '+str(round(2*(num-3)/3,6))+' 0.390000 0.000000 0 HCOUNT=3\n')

grand.write('M  V30 END ATOM\nM  V30 BEGIN BOND\n')

grand.write('M  V30 1 1 2 3\n')
grand.write('M  V30 2 1 1 3\n')

dic = {'1':[],'2':[]}
num = 3
for per in bit_data:
    dic[str(1+int(per))].append(str(num)+' '+str(num+1))
    num+=1
num = 3
for data in dic['1']:
    grand.write('M  V30 '+str(num)+' 1 '+data+'\n')
    num+=1
for data in dic['2']:
    grand.write('M  V30 '+str(num)+' 2 '+data+'\n')
    num+=1

grand.write('M  V30 END BOND\nM  V30 END CTAB\nM  END')
grand.close()
