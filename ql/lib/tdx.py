

"""
Read data from tongdaxin output file.
1.one day data file
2.5mins data file
3.1mins data file
4.
"""
import struct

#ofile=open('/opt/ql/data/sz000001.lc5','rb')
ofile=open('/opt/ql/data/sz000001.day','rb')
buf=ofile.read()
ofile.close()
 
ifile=open('/opt/ql/data/tdx.txt','w')
num=len(buf)
print num
no=num/32
b=0
e=32
line=''
 
for i in xrange(no):
   a=struct.unpack('IIIIIfII',buf[b:e])
   line=str(a[0])+' '+str(a[1]/100.0)+' '+str(a[2]/100.0)+' '+str(a[3]/100.0)+' '+str(a[4]/100.0)+' '+str(a[5]/10.0)+' '+str(a[6])+' '+str(a[7])+' '+'\n'
   print line
   ifile.write(line)
   b=b+32
   e=e+32
ifile.close()
