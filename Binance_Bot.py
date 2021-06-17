from datetime import date
from Alerts_Data import pumpAlerts
from logging import error
import requests
import urllib3
import time
import pickle
import json
import traceback
from TgBotAPI import *
from FileIO import *
from GSheetsAPI import *
from BinanceAPI import *
from AlertService import *
from ProcessMessage import *
import Sheets_Config as sh


channelId = readFile("Tg_Ids.json")["channelId"]
kingId = readFile("Tg_Ids.json")["kingid"]
bot_secret = str(readFile("Tg_Ids.json")["bot_secret"])


def exception_to_string(excp):
    stack = traceback.extract_stack(
    )[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
    pretty = traceback.format_list(stack)
    return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)


def updateSheetAlerts():
    startTime = datetime.now()
    endTime = Null
    print("updating Sheets - ", startTime)
    getAllSheets()
    sheets = [sh.SPOT, sh.FUTURES, sh.SCALP, sh.GEM]
    for df in sheets:
        for i, row in df.iterrows():
            createAlertFromRow(row)
    endTime = datetime.now()
    td = dhms_from_seconds(date_diff_in_seconds(endTime, startTime))
    t = ""
    t = t + str(td[0]) + (" Day " if td[0] ==
                          1 else " Days ") if td[0] > 0 else t
    t = t + str(td[1]) + (" Hour " if td[1] ==
                          1 else " Hours ") if td[1] > 0 else t
    t = t + str(td[2]) + (" Minute " if td[2] ==
                          1 else " Minutes ") if td[2] > 0 else t
    t = t + str(td[3]) + (" Second " if td[3] ==
                          1 else " Seconds ") if td[3] > 0 else t
    print("updating Complete - " ,endTime , "Duration - " , t)


def main(i):
    # getAllSheets()
    # getMessage(kingId, bot_secret)
    # updateSheetAlerts()
    # createAlert("EOSUSDT",5)
    # checkAlert()
    # print(sh.SPOT)
    i = 0
    sendException = True
    while True:
        try:
            i += 1
            getAllPrices()
            if i % 200 == 1:
                pumpAlerts()
                updateSheetAlerts()
                backupAlerts()
                sendException = True
            processMessage()
            checkAlert(i-1)
        except Exception as e:
            text = ("error occurred at ", i, time.strftime(
                "%H:%M:%S", time.localtime()), exception_to_string(e))
            # print(text)
            if sendException:
                sendMessage(kingId, text, bot_secret)
                sendException = False
        time.sleep(3)


if __name__ == '__main__':
    main(0)
