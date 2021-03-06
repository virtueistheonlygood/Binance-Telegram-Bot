from pyasn1.type.univ import Null
import requests

PRICES = dict()
PREMIUMPRICES = dict()

def getAllPrices():
    global PRICES
    global PREMIUMPRICES
    url = "https://www.binance.com/api/v3/ticker/price"
    premiumurl = "https://www.binance.com/fapi/v1/ticker/price"
    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    response = requests.get(url)
    json = response.json()
    for data in json:
        PRICES[data['symbol']] = float(data['price'])
    
    response = requests.get(premiumurl)
    json = response.json()
    for data in json:
        PREMIUMPRICES[data['symbol']] = float(data['price'])
        
    return PRICES


def getPrice(coin,code=0):
    if code == 0:
        return (PRICES[coin])
    elif (not code == 0) and "FUTURES" in code or "SCALP" in code:
        return (PREMIUMPRICES[coin]) 
    else:   
        return (PRICES[coin])


def getPeakPrice(coin, startTime,code,cmp=1):
    if code == 0:
        url = f"https://www.binance.com/api/v3/klines?symbol={coin}&interval=1h&startTime={startTime}"
    elif "FUTURES" in code or "SCALP" in code:
        url = f"https://www.binance.com/fapi/v1/klines?symbol={coin}&interval=1h&startTime={startTime}"
    else:
        url = f"https://www.binance.com/api/v3/klines?symbol={coin}&interval=1h&startTime={startTime}"
    response = requests.get(url)
    data = response.json()
    max = -1.0
    min = 100000000.00 if not len(data) == 0 else -1
    for i in data:
        if float(i[2]) > max:
            max = float(i[2])
        if float(i[3]) < min:
            min = float(i[3])
    return max if cmp>0 else min
