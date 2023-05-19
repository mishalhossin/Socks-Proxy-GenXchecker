import requests
import socket
import socks
import threading

# read urls from urls.txt
with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()

# function to test proxy on google.com
def test_proxy(proxy):
    ip, port = proxy.split(':')
    try:
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
        response = requests.get('https://www.google.com', timeout=10)
        if response.status_code == 200:
            with open('socks5.txt', 'a') as f:
                f.write(proxy + '\n')
    except:
        pass

# function to fetch SOCKS5 proxies from URLs
def fetch_proxies(url):
    response = requests.get(url, verify=False)
    proxies = set()
    for ip_port in response.text.split('\n'):
        proxies.add(ip_port)
    for proxy in proxies:
        threading.Thread(target=test_proxy, args=(proxy,)).start()

# read URLs from urls.txt and test proxies with 20 threads
for url in urls:
    threading.Thread(target=fetch_proxies, args=(url,)).start()
