import subprocess
import os ,json


from framework.CulturalAPI import CulturalAPI
#
# cmd='"D:\Program Files (x86)\python3\python3.exe" E:\小雁塔\program+pycaffe20190701\文物测试\Cultural_db/run.py'
#
# subprocess.Popen(cmd, shell=True)
dic = {'table_name': 'summary', 'Latest_name': 'Test_Time'}
data=(CulturalAPI().getform(dic))
print(json.loads(data))
# /
# # download(filename, Test_Version, Test_Batch)
