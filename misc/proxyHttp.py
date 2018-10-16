import random
import re
import urllib.request

proxy_list = ['39.135.11.166:8080', '111.7.130.101:8080', '120.131.9.254:1080']

handler = urllib.request.ProxyHandler({'http': random.choice(proxy_list)})
opener = urllib.request.build_opener(handler)
# The following line might be needed to avoid HTTP Error 403: Forbidden
# opener.addheaders = [
#     ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')]
urllib.request.install_opener(opener)

try:
    data = urllib.request.urlopen(
        'http://whatismyip.host').read().decode('utf-8')
    regex = r'<p class="ipaddress">(.*?)</p>'
    res = re.findall(regex, data)
except Exception as err:
    print(err)

if res:
    print('Your IPv4 address is:', res[0])
