import Alerts_Data as ad
from os import read
from TgBotAPI import *
from FileIO import *
from GSheetsAPI import *
from BinanceAPI import *
from datetime import datetime
import math
import pandas as pd
import Sheets_Config as sh

channelId = readFile("Tg_Ids.json")["channelId"]
bot_secret = str(readFile("Tg_Ids.json")["bot_secret"])


def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)

def readableDateDiff(dt2,dt1,dhms=[1,1,1,1]):
    seconds = date_diff_in_seconds(dt2,dt1)
    td = dhms_from_seconds(seconds)
    t = ""
    t = t + str(td[0]) + (" Day " if td[0] ==
                          1 else " Days ") if td[0] > 0 and dhms[0] else t
    t = t + str(td[1]) + (" Hour " if td[1] ==
                          1 else " Hours ") if td[1] > 0 and dhms[1] else t
    t = t + str(td[2]) + (" Minute " if td[2] ==
                          1 else " Minutes ") if td[2] > 0 and dhms[2] else t
    t = t + str(td[3]) + (" Second " if td[3] ==
                          1 else " Seconds ") if td[3] > 0 and dhms[3] else t
    return t

def write_alert(coin, alert):
    alerts = ad.ALERTS
    flag = True
    if not alerts.__contains__(coin):
        alerts[coin] = []
    else:
        for al in alerts[coin]:
            if al['code'] == alert['code'] and al['type'] == alert['type']:
                if float(al['price']) == float(alert['price']):
                    return
                elif al['code'] == 0:
                    flag = True
                else:
                    alerts[coin][alerts[coin].index(al)] = alert
                    flag = False
                    break
    # print(alerts)
    if flag:
        alerts[coin].append(alert)

    ad.ALERTS = alerts


def checkAlert(mode=1):
    alerts = ad.ALERTS
    prices = getAllPrices()
    flag = False
    for coin in alerts:
        for alert in alerts[coin]:
            if alert['isActive']:
                if mode == 0:
                    print("initial check - "+coin+" "+alert['type'])
                    peakPrice = getPeakPrice(
                        coin, math.floor(alert['createdAt']))
                    if alert['price']*alert['compare'] <= peakPrice*alert['compare'] and not alert['type'] == "SL":
                        if triggerAlert(alert):
                            alert['isActive'] = False
                            alert['triggeredAt'] = float(
                                datetime.now().timestamp())
                            flag = True
                else:
                    if alert['price']*alert['compare'] <= prices[coin]*alert['compare']:
                        if triggerAlert(alert):
                            alert['isActive'] = False
                            alert['triggeredAt'] = math.floor(
                                datetime.now().timestamp()*1000)
                            flag = True
    if flag:
        ad.ALERTS = alerts


def triggerAlert(alert):
    print("Alert Triggered " + str(alert['code']) + " " +
          str(alert['pair']) + " at " + str(alert['price']))
    # print(SPOT)
    # print(alert)
    code = alert['code']
    type = alert['type']

    if not code == 0:
        row = sh.SPOT.loc[sh.SPOT["CODE"] == code].iloc[0] if "SPOT" in code else sh.FUTURES.loc[sh.FUTURES["CODE"] == code].iloc[0] if "FUTURES" in code else sh.GEM.loc[sh.GEM["CODE"]
                                                                                                                                                                          == code].iloc[0] if "GEM" in code else sh.SCALP.loc[sh.SCALP["CODE"] == code].iloc[0] if "SCALP" in code else 0
        if row.empty:
            return
        entry = float(row['ENTRY'][1:].replace(',', ''))
        lev = int(row['LEV'])
        profit = round(((float(row[type][1:].replace(',', '')
                               )-entry)/entry) * 100 * lev, 2)
        lev = abs(lev)
        # t = ""
        # t = t + str(row['Days']) + " Day(s) "if row['Days'] > 0 else t
        # t = t + str(row['Hours']) + " Hour(s) "if row['Hours'] > 0 else t
        # t = t + str(row['Minutes']) + " Minute(s) "if row['Minutes'] > 0 else t
    else:
        profit = ""
        lev = ""
    td = dhms_from_seconds(date_diff_in_seconds(
        datetime.now(), datetime.fromtimestamp(alert['createdAt']/1000)))
    t = readableDateDiff(datetime.now(), datetime.fromtimestamp(alert['createdAt']/1000),[1,1,1,0])
    # print()
    
    text = dict({
        'ENTRY': f"#{alert['code']} ✔️ \nFilled.",
        'STTP1': f"#{alert['code']} ✅ \n{alert['pair']} \nFirst Short Term Target hit.📈           \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'STTP2': f"#{alert['code']} ✅ \n{alert['pair']} \nShort Term Target 2 DONE. 📈             \nProfit : {profit}% (x{lev}) 💵        \nTime : {t}",
        'STTP3': f"#{alert['code']} ✅ \n{alert['pair']} \nAll Short Term Targets achieved.🎉     \nProfit : {profit}% (x{lev}) 💰        \nTime : {t}",
        'MTTP1': f"#{alert['code']} ✅ \n{alert['pair']} \nMid Term Target 1 Hit.📈                 \nProfit : {profit}% (x{lev}) 💲        \nTime : {t}",
        'MTTP2': f"#{alert['code']} ✅ \n{alert['pair']} \nSecond Mid Term Target Done. 🚀        \nProfit : {profit}% (x{lev}) 💴        \nTime : {t}",
        'MTTP3': f"#{alert['code']} ✅ \n{alert['pair']} \nAll Mid Term Targets achieved.🎉       \nProfit : {profit}% (x{lev}) 💰        \nTime : {t}",
        'LTTP1': f"#{alert['code']} ✅ \n{alert['pair']} \nLong Term Target 1 HIT.📈                \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'LTTP2': f"#{alert['code']} ✅ \n{alert['pair']} \nSecond Long Term achieved.✨           \nProfit : {profit}% (x{lev}) 💵        \nTime : {t}",
        'LTTP3': f"#{alert['code']} ✅ \n{alert['pair']} \nAll Long Term Targets achieved.🎉      \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'TP1':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 1 Achieved.📈          \nProfit : {profit}% (x{lev}) 💲🚀      \nTime : {t}",
        'TP2':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 2 Done.📈              \nProfit : {profit}% (x{lev}) 💰        \nTime : {t}",
        'TP3':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 3 Hit. 📈              \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'TP4':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 4 Reached.💰🚀      \nProfit : {profit}% (x{lev}) 💰        \nTime : {t}",
        'TP5':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 5 Accomplished.📈      \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'TP6':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 6 Achieved.✨        \nProfit : {profit}% (x{lev}) ✨        \nTime : {t}",
        'TP7':   f"#{alert['code']} ✅ \n{alert['pair']} \nTake-Profit Target 7 DONE.🎉            \nProfit : {profit}% (x{lev}) 💸        \nTime : {t}",
        'emojis': "🚀 🕔 ⏳ ⏰ 💸 💴 💰 💲 💵 ✨ 🎉 📉 📈",
        'SL':    f"#{alert['code']}🛑  \nStopLoss :(                                                \nLoss : {profit}% (x{lev}) 📉            \nTime : {t}",
        'Generic': f"{alert['pair']} Alert triggered at {alert['price']} \nTime : {t}",
    })
    sendMessage(channelId, text[type], bot_secret)

    return True


def createAlert(coin, price=0.0, type="Generic", repeat=1, df=pd.DataFrame()):

    code = 0 if df.empty else df["CODE"]
    if not df.empty and df[type] == '':
        return
    cmp = getPrice(coin)
    price = float(df[type][1:].replace(',', '')) if not code == 0 else price
    pair = ("$" + coin.split("USDT")[0]+"/USDT" if "USDT" in coin else coin.split(
        "BTC")[0] + "/BTC") if code == 0 else df["PAIR"]
    createdAt = math.floor(datetime.now().timestamp()*1000) if code == 0 else math.floor(
        datetime.strptime(df["POSTED"], '%d/%m/%Y %H:%M:%S').timestamp()*1000)
    alert = {
        'code': code,
        'price': price,
        'pair': pair,
        'isActive': True,
        'compare': 1 if float(cmp) <= float(price) else -1,
        'createdAt': createdAt,
        'triggeredAt': 0,
        'type': type,
        'repeat': repeat
    }
    write_alert(coin, alert)

def createAlertFromRow(row=pd.DataFrame()):
    if "SPOT" in row["CODE"] or "FUTURES" in row["CODE"] or "GEM" in row["CODE"] or "SCALP" in row["CODE"]:
        for key in row.keys():
            if "TP" in key or "SL" in key or "ENTRY" in key:
                createAlert(coin=row["SYMBOL"], type=key, df=row)
                # print(row)

def disableAlert(code, type="any"):
    alerts = ad.ALERTS

    for coin in alerts.keys():
        for alert in alerts[coin]:
            if alert['code'] == code:
                if type == "any":
                    alerts[coin][alerts[coin].index(alert)]['isActive'] = False
                elif alert['type'] == type:
                    alerts[coin][alerts[coin].index(alert)]['isActive'] = False

    ad.ALERTS = alerts
    return


def enableAlert(code, type="any"):
    alerts = ad.ALERTS

    for coin in alerts.keys():
        for alert in alerts[coin]:
            if alert['code'] == code:
                if type == "any":
                    alerts[coin][alerts[coin].index(alert)]['isActive'] = True
                elif alert['type'] == type:
                    alerts[coin][alerts[coin].index(alert)]['isActive'] = True

    ad.ALERTS = alerts
    return


def backupAlerts():
    alerts = readFile("alerts.json")
    writeFile(alerts, "alerts_bak.json")


def debug():
    ad.pumpAlerts()
    refreshGem()
    for i, row in sh.GEM.iterrows():
        createAlertFromRow(row=row)
# debug()