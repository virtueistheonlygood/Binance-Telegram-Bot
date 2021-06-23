from ast import parse
from GSheetsAPI import *
from AlertService import *
from TgBotAPI import *
from FileIO import *
import Sheets_Config as sh
from Binance_Bot import updateSheetAlerts


kingId = readFile("Tg_Ids.json")["kingid"]
bot_secret = str(readFile("Tg_Ids.json")["bot_secret"])


def processMessage(message = "Default",mode=0):
    message = message if mode == 1 else getMessage(kingId, bot_secret)
    if "Error" in message:
        raise Exception(message)
    message = message.upper()
    text = ""
    if "NO MESSAGES" in message:
        return
    if "NEW" in message:
        text = createNewCall(message)
    elif "DISABLE" in message:
        text = disableAlertFromMessage(message)
    elif "ENABLE" in message:
        text = enableAlertFromMessage(message)
    elif "ALERT" in message:
        text = createAlertFromMessage(message)
    elif "SPOT_" in message or "FUTURES_" in message or "SCALP_" in message or "GEM_" in message:
        text = createSheetCall(message)

    sendMessage(kingId, text, bot_secret)


# Format : NEW SPOT {COIN} {ENTRY PRICE} ({LEV})


def createNewCall(message):
    message = message + " 1"
    call,typ,coin,price,lev = message.split(" ")[:5]
    print(call,typ,coin,price,lev)
    if "GEM" in typ:
        code = addRowGem(coin,float(price))
        processMessage(code,1)
    if "SPOT" in typ:
        code = addRowSpot(coin,float(price))
        processMessage(code,1)
    if "FUTURES" in typ:
        code = addRowFutures(coin,float(price),lev)
        processMessage(code,1)
    if "SCALP" in typ:
        code = addRowScalp(coin,float(price),lev)
        processMessage(code,1)

# Format : {CODE}


def createSheetCall(message):
    data = message.split(" ")
    if not len(data) == 1:
        return "Invalid Format"
    text = ""
    if "SPOT_" in message:
        refreshSpot()
        row = sh.SPOT.loc[sh.SPOT["CODE"] == message].iloc[0]
        createAlertFromRow(row)
        text = generateCall_SPOT(row)
    elif "FUTURES_" in message:
        refreshFutures()
        row = sh.FUTURES.loc[sh.FUTURES["CODE"] == message].iloc[0]
        createAlertFromRow(row)
        text = generateCall_FUTURES(row)
    elif "GEM_" in message:
        refreshGem()
        row = sh.GEM.loc[sh.GEM["CODE"] == message].iloc[0]
        createAlertFromRow(row)
        text = generateCall_GEM(row)
    elif "SCALP_" in message:
        refreshScalp()
        row = sh.SCALP.loc[sh.SCALP["CODE"] == message].iloc[0]
        createAlertFromRow(row)
        text = generateCall_SCALP(row)
    return text


# Format : ALERT {COIN} {PRICE}


def createAlertFromMessage(message):
    data = message.split(" ")
    if not len(data) == 3:
        return "Invalid Format"
    coin = data[1]
    price = data[2]
    createAlert(coin, float(price))
    return f"Alert Created {coin} at {price}."


#Format : DISABLE/ENABLE (ALERT) {CODE} ({TYPE})

def disableAlertFromMessage(message):
    message = message.split(" ")
    message.remove("ALERT") if "ALERT" in message else message
    if len(message) < 2:
        return "Invalid Format"
    if "SPOT_" in message[1] or "FUTURES_" in message[1] or "SCALP_" in message[1] or "GEM_" in message[1]:
        if len(message) == 3:
            disableAlert(message[1], message[2])
            return f"Disabled Alert {message[1]} - {message[2]}"
        else:
            disableAlert(message[1])
            return f"Disabled Alert {message[1]}"
    else:
        return "Invalid Format"


def enableAlertFromMessage(message):
    message = message.split(" ")
    message.remove("ALERT") if "ALERT" in message else message
    if len(message) < 2:
        return "Invalid Format"
    if "SPOT_" in message[1] or "FUTURES_" in message[1] or "SCALP_" in message[1] or "GEM_" in message[1]:
        if len(message) == 3:
            enableAlert(message[1], message[2])
            return f"Enabled Alert {message[1]} - {message[2]}"
        else:
            enableAlert(message[1])
            return f"Enabled Alert {message[1]}"
    else:
        return "Invalid Format"


def generateCall_SPOT(row):
    text = f"#{row['CODE']}"
    text += f"\nPair: {row['PAIR']}"
    text += f"\nEntry - {row['ENTRY']}"

    text += f"\n"
    text += f"\nShort Term Targets" if not row['STTP1'] == "" else ""
    text += f"\nTP1 - {row['STTP1']}" if not row['STTP1'] == "" else ""
    text += f"\nTP2 - {row['STTP2']}" if not row['STTP2'] == "" else ""
    text += f"\nTP3 - {row['STTP3']}" if not row['STTP3'] == "" else ""

    text += f"\n"
    text += f"\nMid Term Targets" if not row['MTTP1'] == "" else ""
    text += f"\nTP1 - {row['MTTP1']}" if not row['MTTP1'] == "" else ""
    text += f"\nTP2 - {row['MTTP2']}" if not row['MTTP2'] == "" else ""
    text += f"\nTP3 - {row['MTTP3']}" if not row['MTTP3'] == "" else ""

    text += f"\n"
    text += f"\nLong Term Targets" if not row['LTTP1'] == "" else ""
    text += f"\nTP1 - {row['LTTP1']}" if not row['LTTP1'] == "" else ""
    text += f"\nTP2 - {row['LTTP2']}" if not row['LTTP2'] == "" else ""
    text += f"\nTP3 - {row['LTTP3']}" if not row['LTTP3'] == "" else ""
    
    text += f"\n"
    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_FUTURES(row):
    text = f"#{row['CODE']}"
    text += f"\nLong" if int(row['LEV']) > 0 else f"\nShort"
    text += f"\nPair: {row['PAIR']} (x{abs(int(row['LEV']))})"
    text += f"\nEntry - {row['ENTRY']}"
    
    text += f"\n"
    text += f"\nExit"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}" if not row['TP3'] == "" else ""
    text += f"\nTP4 - {row['TP4']}" if not row['TP4'] == "" else ""
    text += f"\nTP5 - {row['TP5']}" if not row['TP5'] == "" else ""
    text += f"\nTP6 - {row['TP6']}" if not row['TP6'] == "" else ""
    text += f"\nTP7 - {row['TP7']}" if not row['TP7'] == "" else ""

    text += f"\n"
    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_GEM(row):
    text = f"#{row['CODE']}"
    text += f"\nPair: {row['PAIR']}"
    text += f"\nEntry - {row['ENTRY']}"

    text += f"\n"
    text += f"\nTargets"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}" if not row['TP3'] == "" else ""

    text += f"\n"
    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_SCALP(row):
    text = f"#{row['CODE']}"
    text += f"\nLong" if int(row['LEV']) > 0 else f"\nShort"
    text += f"\nPair: {row['PAIR']} (x{abs(int(row['LEV']))})"
    text += f"\nEntry - {row['ENTRY']}"

    text += f"\n"
    text += f"\nExit"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}" if not row['TP3'] == "" else ""
    text += f"\nTP4 - {row['TP4']}" if not row['TP4'] == "" else ""

    text += f"\n"
    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def addRowGem(coin,price):
    refreshGem()
    row = [i for temp,i in sh.GEM.iterrows() if ("GEM" in i['CODE'])][-1]
    row = row.copy()
    row = row.to_dict()
    row['CODE'] = "GEM_" + str(int(row['CODE'].split("_")[1])+1)
    row['PAIR'] = ("$" + coin.split("USDT")[0]+"/USDT" if "USDT" in coin else coin.split("BTC")[0] + "/BTC")
    row['SYMBOL'] = coin
    row['ENTRY'] = "${:.3f}".format(price)
    
    row['TP1'] = "${:.3f}".format(price*2)
    row['TP2'] = "${:.3f}".format(price*3)
    row['TP3'] = "${:.3f}".format(price*4)
    
    row['SL'] = "${:.3f}".format(price*0.3)
    row['PEAK'] = ""
    row['CMP'] = ""
    
    row[[i for i in row.keys() if "PNL" in i or "Loading" in i][0]] = ""
    row[[i for i in row.keys() if "PEAK -" in i or "Loading" in i][0]] = ""
    
    row['TIME'] = ""
    row['Days'] = ""
    row['Hours'] = ""
    row['Minutes'] = ""
    
    row['POSTED'] = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    row['NOW'] = "=NOW()"
    writeGem(row)
    return row['CODE']
    
    
def addRowSpot(coin,price):
    refreshSpot()
    row = [i for temp,i in sh.SPOT.iterrows() if ("SPOT" in i['CODE'])][-1]
    row = row.copy()
    row = row.to_dict()
    row['CODE'] = "SPOT_" + str(int(row['CODE'].split("_")[1])+1)
    row['PAIR'] = ("$" + coin.split("USDT")[0]+"/USDT" if "USDT" in coin else coin.split("BTC")[0] + "/BTC")
    row['SYMBOL'] = coin
    row['ENTRY'] = "${:.3f}".format(price)
    
    row['STTP1'] = "${:.3f}".format(price*1.1)
    row['STTP2'] = "${:.3f}".format(price*1.2)
    row['STTP3'] = "${:.3f}".format(price*1.3)
    row['MTTP1'] = "${:.3f}".format(price*1.5)
    row['MTTP2'] = "${:.3f}".format(price*1.7)
    row['MTTP3'] = "${:.3f}".format(price*1.9)
    row['LTTP1'] = "${:.3f}".format(price*2)
    row['LTTP2'] = "${:.3f}".format(price*2.5)
    row['LTTP3'] = "${:.3f}".format(price*3)
    
    row['SL'] = "${:.3f}".format(price*0.85)
    row['PEAK'] = ""
    row['CMP'] = ""
    
    row[[i for i in row.keys() if "PNL" in i or "Loading" in i][0]] = ""
    row[[i for i in row.keys() if "PEAK -" in i or "Loading" in i][0]] = ""
    
    row['TIME'] = ""
    row['Days'] = ""
    row['Hours'] = ""
    row['Minutes'] = ""
    
    row['POSTED'] = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    row['NOW'] = "=NOW()"
    writeSpot(row)
    return row['CODE']
    
    
def addRowFutures(coin,price,lev):
    refreshFutures()
    row = [i for temp,i in sh.FUTURES.iterrows() if ("FUTURES" in i['CODE'])][-1]
    row = row.copy()
    row = row.to_dict()
    row['CODE'] = "FUTURES_" + str(int(row['CODE'].split("_")[1])+1)
    row['PAIR'] = ("$" + coin.split("USDT")[0]+"/USDT" if "USDT" in coin else coin.split("BTC")[0] + "/BTC")
    row['SYMBOL'] = coin
    row['ENTRY'] = "${:.3f}".format(price)
    row['LEV'] = int(lev)
    
    row['TP1'] = "${:.3f}".format(price*1.01)
    row['TP2'] = "${:.3f}".format(price*1.03)
    row['TP3'] = "${:.3f}".format(price*1.05)
    row['TP4'] = "${:.3f}".format(price*1.07)
    row['TP5'] = "${:.3f}".format(price*1.1)
    row['TP6'] = "${:.3f}".format(price*1.2)
    row['TP7'] = "${:.3f}".format(price*1.3)
    
    row['SL'] = "${:.3f}".format(price*0.9)
    row['PEAK'] = ""
    row['CMP'] = ""
    
    row[[i for i in row.keys() if "PNL" in i or "Loading" in i][0]] = ""
    row[[i for i in row.keys() if "PEAK -" in i or "Loading" in i][0]] = ""
    
    row['TIME'] = ""
    row['Days'] = ""
    row['Hours'] = ""
    row['Minutes'] = ""
    
    row['POSTED'] = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    row['NOW'] = "=NOW()"
    writeFutures(row)
    return row['CODE']
    
    
def addRowScalp(coin,price,lev):
    refreshScalp()
    row = [i for temp,i in sh.SCALP.iterrows() if ("SCALP" in i['CODE'])][-1]
    row = row.copy()
    row = row.to_dict()
    row['CODE'] = "SCALP_" + str(int(row['CODE'].split("_")[1])+1)
    row['PAIR'] = ("$" + coin.split("USDT")[0]+"/USDT" if "USDT" in coin else coin.split("BTC")[0] + "/BTC")
    row['SYMBOL'] = coin
    row['ENTRY'] = "${:.3f}".format(price)
    row['LEV'] = lev
    
    row['TP1'] = "${:.3f}".format(price*1.01)
    row['TP2'] = "${:.3f}".format(price*1.03)
    row['TP3'] = "${:.3f}".format(price*1.05)
    row['TP4'] = "${:.3f}".format(price*1.1)
    
    row['SL'] ="${:.3f}".format( price*0.5)
    row['PEAK'] = ""
    row['CMP'] = ""
    
    row[[i for i in row.keys() if "PNL" in i or "Loading" in i][0]] = ""
    row[[i for i in row.keys() if "PEAK -" in i or "Loading" in i][0]] = ""
    
    row['TIME'] = ""
    row['Days'] = ""
    row['Hours'] = ""
    row['Minutes'] = ""
    
    row['POSTED'] = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    row['NOW'] = "=NOW()"
    writeScalp(row)
    return row['CODE']
    