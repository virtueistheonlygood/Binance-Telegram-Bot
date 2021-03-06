from datetime import date
import Alerts_Data as ad
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
    t = readableDateDiff(endTime,startTime)
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
    startTime = 0.0
    endTime = 0.0
    while True:
        try:
            i += 1
            getAllPrices()
            if i % 300 == 1:
                ad.pumpAlerts()
                updateSheetAlerts()
                backupAlerts()
                sendException = True
            if ad.isAlertsNeedDump():
                ad.dumpAlerts()
            processMessage()
            if(i==1):
                startTime = datetime.now()
                print("Initial Check starting at ", startTime)
            checkAlert(i-1)
            if(i==1):
                endTime = datetime.now()
                print("Intial check finished at ",endTime," Duration : ",readableDateDiff(endTime,startTime))
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
