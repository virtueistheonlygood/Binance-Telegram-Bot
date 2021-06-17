import requests

PRICES = dict()

def getAllPrices():
    global PRICES
    url = "https://www.binance.com/api/v3/ticker/price"
    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    response = requests.get(url)
    json = response.json()
    for data in json:
        PRICES[data['symbol']] = float(data['price'])
    return PRICES


def getPrice(coin):
    return (PRICES[coin])


def getPeakPrice(coin, startTime):
    url = f"https://www.binance.com/api/v3/klines?symbol={coin}&interval=1h&startTime={startTime}"
    response = requests.get(url)
    data = response.json()
    max = -1.0
    for i in data:
        if float(i[2]) > max:
            max = float(i[2])
    return max
