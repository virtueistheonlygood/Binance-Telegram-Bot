from pyasn1.type.univ import Null
from pygsheets.worksheet import Worksheet
from FileIO import readFile
import pandas as pd
import pygsheets
import Sheets_Config as sh


fileName = readFile("sheets.json")["fileName"]
spot = readFile("sheets.json")["spotSheet"]
gem = readFile("sheets.json")["gemSheet"]
futures = readFile("sheets.json")["futuresSheet"]
scalp = readFile("sheets.json")["scalpSheet"]

gc = pygsheets.authorize()
sht = gc.open(fileName)

wkSpot = pygsheets.Worksheet;
wkFutures = pygsheets.Worksheet;
wkGem = pygsheets.Worksheet;
wkScalp = pygsheets.Worksheet;

def __getSheetDf(SHEET):
    wk1 = sht.worksheet_by_title(SHEET)
    df = pd.DataFrame(wk1.get_all_records())
    return df
    # print(df.iloc[0, 0])

def __writeSheetDf(SHEET,data,num):
    wk1 = (sht.worksheet_by_title(SHEET))
    wk1.insert_rows(num+1,values = [*data.values()], inherit = True)

def getAllSheets():
    
    refreshSpot()
    refreshFutures()
    refreshGem()
    refreshScalp()
    # sh.SPOT = pd.DataFrame(sht.worksheet_by_title('SPOT'))
    # sh.FUTURES = pd.DataFrame(sht.worksheet_by_title('FUTURES'))
    # sh.SCALP = pd.DataFrame(sht.worksheet_by_title('SCALP'))
    # sh.GEM = pd.DataFrame(sht.worksheet_by_title('GEM'))
    # sh.SPOT = getSheetDf(spot)
    # sh.FUTURES = getSheetDf(futures)
    # sh.SCALP = getSheetDf(scalp)
    # sh.GEM = getSheetDf(gem)
    # print(sh.SPOT)s
    # return [SPOT, FUTURES, SCALP, GEM]

def refreshSpot():
    sh.SPOT = __getSheetDf(spot)
    
def refreshFutures():
    sh.FUTURES = __getSheetDf(futures)

def refreshGem():
    sh.GEM = __getSheetDf(gem)

def refreshScalp():
    sh.SCALP = __getSheetDf(scalp)


def writeGem(row):
    __writeSheetDf(gem,row,sh.GEM.shape[0])
    
def writeSpot(row):
    __writeSheetDf(spot,row,sh.SPOT.shape[0])
    
def writeFutures(row):
    __writeSheetDf(futures,row,sh.FUTURES.shape[0])
    
def writeScalp(row):
    __writeSheetDf(scalp,row,sh.SCALP.shape[0])