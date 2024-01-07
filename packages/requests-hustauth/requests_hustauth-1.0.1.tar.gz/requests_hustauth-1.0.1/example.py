import requests
from requests_hustauth import HustAuth

session = requests.Session()
hust_auth = HustAuth('USERID','PASSWORD')

resp = session.get('http://m.hust.edu.cn/wechat/apps_center.jsp',auth=hust_auth)
print(resp.text)
