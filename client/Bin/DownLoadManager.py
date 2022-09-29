import requests
import shutil
class DManager :
     def __init__(self,m_url):
         self.tempDir = 'temp'
         self.url = m_url
     def downloadFile(self,filename):
         try:
            response = requests.get(self.url + '/getfile' + '?filename=' + filename, stream=True)
         except:
            print('Download File Exception') 
            return False
                      # print('saving ' + filename)
         if response.status_code == 200:
            print(self.url + '/getfile' + '&filename=' + filename)
            with open(self.tempDir +'/'+ filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print('saved ' + filename)
            return True
         else: return False
     def setUrl(self,url):
           self.url = url
     def getFileList(self):
         print(self.url + '/newdata')
         result = []
         try:
            x = requests.post(self.url +'/newdata', json = {})
            response = x.json()
         except: 
             print('newdata request went wrong')
             return result
         for filename in response['data']:
             print('downloading ' + filename)
             if self.downloadFile(filename) == True:
                 result.append(filename)
         return result

