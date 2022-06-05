import json
import pandas as pd
import requests
from time import sleep

whois_key = 'key'
ip_list = ['192.168.0.1']
result = []

for ip in ip_list:
    url = f"http://whois.kisa.or.kr/openapi/whois.jsp?query={ip}&key={whois_key}&answer=json"
    response = requests.get(url)
    content = json.loads(response.content)

    isp = ''
    isp2 = ''

    if content.get('whois') and content.get('whois').get('korean'):
        korean = content.get('whois') and content.get('whois').get('korean')
        if korean and korean.get('ISP') and korean.get('ISP').get('netinfo') and \
                korean.get('ISP').get('netinfo').get('orgName'):
            isp = korean.get('ISP').get('netinfo').get('orgName')

        if korean and korean.get('user') and korean.get('user').get('netinfo') and \
                korean.get('user').get('netinfo').get('orgName'):
            isp2 = korean.get('user').get('netinfo').get('orgName')

    data = {'IP 주소': ip, '기관 명1': isp, '기관 명2': isp2}
    result.append(data)
    sleep(1)
    response.close()

df = pd.DataFrame(result)
df.to_csv('output.csv', header=True, index=True, encoding='utf-8-sig')
