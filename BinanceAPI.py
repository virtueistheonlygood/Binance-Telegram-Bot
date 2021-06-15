import requests


def getAllPrices():
    url = "https://www.binance.com/api/v3/ticker/price"
    prices = dict()
    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    response = requests.get(url)
    json = response.json()
    for data in json:
        prices[data['symbol']] = float(data['price'])
    return prices


def getPrice(coin):
    url = f"https://www.binance.com/api/v3/ticker/price?symbol={coin}"
    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    response = requests.get(url)
    price = response.json()
    return (price["price"])


def getPeakPrice(coin, startTime):
    url = f"https://www.binance.com/api/v3/klines?symbol={coin}&interval=30m&startTime={startTime}"
    response = requests.get(url)
    data = response.json()
    max = -1.0
    for i in data:
        if float(i[2]) > max:
            max = float(i[2])
    return max
