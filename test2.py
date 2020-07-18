import subprocess
import os ,json


from framework.CulturalAPI import CulturalAPI
#
# cmd='"D:\Program Files (x86)\python3\python3.exe" E:\小雁塔\program+pycaffe20190701\文物测试\Cultural_db/run.py'
#
# subprocess.Popen(cmd, shell=True)
dic = {
    "filename": 'wwcese.xlsx',
    "Test_Version":'v1.0_201812181345' ,
    "Test_Batch":'20200619_1',
}
data=(CulturalAPI().download_excle(dic))
print(json.loads(data))
# /
# # download(filename, Test_Version, Test_Batch)