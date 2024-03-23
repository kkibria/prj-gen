# importing the "tarfile" module 
import tarfile 

# open file 
file = tarfile.open('dist\prj_gen-0.1.0.tar.gz') 

# extracting file 
file.extractall('./tar')
# for x in file.getmembers():
#     print(x.name)
file.close() 
