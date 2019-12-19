import random 
import requests
import time
from exception import *

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/`201`00101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
]

accept_languages = ['en-US,en;q=0.9', 'de;q=0.8', 'fr',
                    'it;q=0.6,vi-VN;q=0.5', 'fr-FR;q=0.3,pt;q=0.2']

def prepare_headers():
    headers = {
        'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
        'Accept-Language': accept_languages[random.randint(0, len(accept_languages) - 1)],
        'accept-encoding': 'gzip, deflate, br',
        'Accepts': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'x-requested-with': 'XMLHttpRequest',
        'x-api-source':'pc'
    }
    return headers

def send_request(request_url, params = {}, proxies = None):
    hdrs = prepare_headers()
    # proxies = ['43.247.132.52:3129', '88.118.134.214:38662',"212.56.218.90:48047","59.126.108.147:49480"]
    if proxies != None:
        result = requests.get(
            request_url, 
            headers=hdrs, 
            params=params,
            timeout=3,
            verify = False
        )
    else:
        result = requests.get(
            request_url, 
            headers=hdrs, 
            params=params,
            proxies={'http': 'http://' + random.choice(proxies)},
            timeout=3,
            verify = False
        )
    if (result.status_code == 200):
        return result
    if (result.status_code == 403):
        raise BotBlockError()
    elif (result.status_code == 404):
        raise PageNotFoundError()
    raise Exception("Error while fetching data" + str(result.status_code))
