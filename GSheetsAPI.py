from os import W_OK
from pyasn1.type.univ import Null
from pygsheets.cell import Cell
from pygsheets.custom_types import WorkSheetProperty
from pygsheets.spreadsheet import Spreadsheet
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

def __writeSheetDf(SHEET,data,num):
    wk1 = (sht.worksheet_by_title(SHEET))
    # wk1 = Worksheet(sht,sht.worksheet_by_title(SHEET).jsonSheet)
    wk1.insert_rows(num+2,values = [*data.values()], inherit = True)
    row1 = wk1.get_row(1)
    rown = wk1.get_row(num+3,returnas='cells')
    for i in rown:
        if("TP" in row1[i.col-1] or "SL" in row1[i.col-1]):
            i.color = (1,1,1,0)

def getAllSheets():
    
    refreshSpot()
    refreshFutures()
    refreshGem()
    refreshScalp()

def refreshSpot():
    sh.SPOT = __getSheetDf(spot)
    
def refreshFutures():
    sh.FUTURES = __getSheetDf(futures)

def refreshGem():
    sh.GEM = __getSheetDf(gem)

def refreshScalp():
    sh.SCALP = __getSheetDf(scalp)


def writeGem(row,rownum):
    __writeSheetDf(gem,row,rownum)
    
def writeSpot(row,rownum):
    __writeSheetDf(spot,row,rownum)
    
def writeFutures(row,rownum):
    __writeSheetDf(futures,row,rownum)
    
def writeScalp(row,rownum):
    __writeSheetDf(scalp,row,rownum)