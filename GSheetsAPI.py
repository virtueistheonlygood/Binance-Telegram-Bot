from FileIO import readFile
import pandas as pd
import pygsheets
import Sheets_Config as sh


fileName = readFile("sheets.json")["fileName"]
spot = readFile("sheets.json")["spotSheet"]
gem = readFile("sheets.json")["gemSheet"]
futures = readFile("sheets.json")["futuresSheet"]
scalp = readFile("sheets.json")["scalpSheet"]

def getSheet(SHEET):
    gc = pygsheets.authorize()
    sht = gc.open(fileName)
    wk1 = sht.worksheet_by_title(SHEET)
    df = pd.DataFrame(wk1.get_all_records())
    return df
    # print(df.iloc[0, 0])


def getAllSheets():

    gc = pygsheets.authorize()
    sht = gc.open(fileName)
    # sh.SPOT = pd.DataFrame(sht.worksheet_by_title('SPOT'))
    # sh.FUTURES = pd.DataFrame(sht.worksheet_by_title('FUTURES'))
    # sh.SCALP = pd.DataFrame(sht.worksheet_by_title('SCALP'))
    # sh.GEM = pd.DataFrame(sht.worksheet_by_title('GEM'))
    sh.SPOT = getSheet(spot)
    sh.FUTURES = getSheet(futures)
    sh.SCALP = getSheet(scalp)
    sh.GEM = getSheet(gem)
    # print(sh.SPOT)s
    # return [SPOT, FUTURES, SCALP, GEM]
