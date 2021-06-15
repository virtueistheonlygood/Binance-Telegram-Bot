from GSheetsAPI import *
from AlertService import *
from TgBotAPI import *
from FileIO import *
import Sheets_Config as sh
from Binance_Bot import updateSheetAlerts


kingId = readFile("Tg_Ids.json")["kingid"]
bot_secret = str(readFile("Tg_Ids.json")["bot_secret"])


def processMessage():
    message = getMessage(kingId, bot_secret)
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


def createNewCall(message):
    return "Invalid Format"

# Format : SPOT_1


def createSheetCall(message):
    updateSheetAlerts()
    text = ""
    if "SPOT_" in message:
        row = sh.SPOT.loc[sh.SPOT["CODE"] == message].iloc[0]
        text = generateCall_SPOT(row)
    elif "FUTURES_" in message:
        row = sh.FUTURES.loc[sh.FUTURES["CODE"] == message].iloc[0]
        text = generateCall_FUTURES(row)
    elif "GEM_" in message:
        row = sh.GEM.loc[sh.GEM["CODE"] == message].iloc[0]
        text = generateCall_GEM(row)
    elif "SCALP_" in message:
        row = sh.SCALP.loc[sh.SCALP["CODE"] == message].iloc[0]
        text = generateCall_SCALP(row)
    return text


# Format : ALERT EOSUSDT 5.16


def createAlertFromMessage(message):
    data = message.split(" ")
    if not len(data) == 3:
        return "Invalid Format"
    coin = data[1]
    price = data[2]
    createAlert(coin, float(price))
    return f"Alert Created {coin} at {price}."


#Format : DISABLE/ENABLE (ALERT) CODE (TYPE)

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
    text += f"\nEntry - {row['ENTRY']}\n"

    text += f"\nShort Term Targets" if not row['STTP1'] == "" else ""
    text += f"\nTP1 - {row['STTP1']}" if not row['STTP1'] == "" else ""
    text += f"\nTP2 - {row['STTP2']}" if not row['STTP2'] == "" else ""
    text += f"\nTP3 - {row['STTP3']}\n" if not row['STTP3'] == "" else "\n"

    text += f"\nMid Term Targets" if not row['MTTP1'] == "" else ""
    text += f"\nTP1 - {row['MTTP1']}" if not row['MTTP1'] == "" else ""
    text += f"\nTP2 - {row['MTTP2']}" if not row['MTTP2'] == "" else ""
    text += f"\nTP3 - {row['MTTP3']}\n" if not row['MTTP3'] == "" else "\n"

    text += f"\nLong Term Targets" if not row['LTTP1'] == "" else ""
    text += f"\nTP1 - {row['LTTP1']}" if not row['LTTP1'] == "" else ""
    text += f"\nTP2 - {row['LTTP2']}" if not row['LTTP2'] == "" else ""
    text += f"\nTP3 - {row['LTTP3']}\n" if not row['LTTP3'] == "" else "\n"

    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_FUTURES(row):
    text = f"#{row['CODE']}"
    text += f"\nPair: {row['PAIR']} (x10)"
    text += f"\nEntry - {row['ENTRY']}\n"

    text += f"\nExit"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}" if not row['TP3'] == "" else ""
    text += f"\nTP4 - {row['TP4']}" if not row['TP4'] == "" else ""
    text += f"\nTP5 - {row['TP5']}" if not row['TP5'] == "" else ""
    text += f"\nTP6 - {row['TP6']}" if not row['TP6'] == "" else ""
    text += f"\nTP7 - {row['TP7']}\n" if not row['TP7'] == "" else "\n"

    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_GEM(row):
    text = f"#{row['CODE']}"
    text += f"\nPair: {row['PAIR']}"
    text += f"\nEntry - {row['ENTRY']}\n"

    text += f"\nTargets"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}\n" if not row['TP3'] == "" else "\n"

    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text


def generateCall_SCALP(row):
    text = f"#{row['CODE']}"
    text += f"\nPair: {row['PAIR']} (x10)"
    text += f"\nEntry - {row['ENTRY']}\n"

    text += f"\nExit"
    text += f"\nTP1 - {row['TP1']}" if not row['TP1'] == "" else ""
    text += f"\nTP2 - {row['TP2']}" if not row['TP2'] == "" else ""
    text += f"\nTP3 - {row['TP3']}\n" if not row['TP3'] == "" else "\n"

    text += f"\nSL: {row['SL']}" if not row['SL'] == "" else "SL - $0.0"

    # print(text)
    return text
