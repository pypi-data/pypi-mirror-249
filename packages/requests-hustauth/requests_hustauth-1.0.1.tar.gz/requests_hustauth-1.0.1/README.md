# HustAuth

![HustPassLogo](https://pass.hust.edu.cn/cas/comm/image/logo-inside.png)

This project provides HustPass support for [Requests](https://requests.readthedocs.io/)

Variation of [HustLogin](https://github.com/MarvinTerry/HustLogin)

## Installation

```
pip install requests-hustauth
```

## Dependency

*(automatically handled by PIP)*

```
Requests
Pillow
numpy
pycryptodome
fake_useragent
```

## Usage

example.py
```python
import requests
from requests_hustauth import HustAuth

session = requests.Session()
hust_auth = HustAuth('USERID','PASSWORD')

resp = session.get('http://m.hust.edu.cn/wechat/apps_center.jsp',auth=hust_auth)
print(resp.text)
```

