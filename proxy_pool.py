"""
# Project: proxies pool
# Author: Eddie
# Date:  06/07/2023
"""
import requests
import re


"""
import requests

proxyip = "http://storm-stst123_area-FR:123123@proxy.stormip.cn:1000"
url = "http://myip.ipip.net"
proxies={
    'http':proxyip,
    'https':proxyip,
}
data = requests.get(url=url,proxies=proxies)
print(data.text)
"""
# Clear the proxy_text
proxy_text = 'proxy_text.txt'

with open(proxy_text, 'w') as file:
    file.write('')


def proxy_generation(number):
    for i in range(number):
        ###########
        proxyip = "http://storm-stst123:123123@eu.stormip.cn:1000"
        url = "http://myip.ipip.net"
        proxies = {
            'http': proxyip,
            'https': proxyip,
        }
        print(proxies)
        with open(proxy_text, 'a') as file:
            file.write(proxyip)
            file.write('\n')

        print("Data saved to", proxy_text)

# Change the number to decide the number of proxies generated
proxy_generation(5)

# API way to generate proxy
# proxy_url = 'https://api.stormproxies.cn/web_v1/ip/get-ip-v3?app_key=64318690cd8b0c33d643b078d3974ebf&pt=9&num=20&ep=&cc=FR&state=&city=&life=30&protocol=1&format=txt&lb=%5Cr%5Cn'
# proxy_text = 'proxy_text.txt'
#
# response = requests.get(proxy_url)
#
# if response.status_code == 200:
#     data = response.text.strip().split('\n')
#     proxy_list = [f'http://{ip}' for ip in data]
#
#     with open(proxy_text, 'w') as file:
#         file.write('\n'.join(proxy_list))
#
#     print("Data saved to", proxy_text)
# else:
#     print("Failed to fetch data from the website.")