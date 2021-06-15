import pandas as pd
import pygsheets
import Sheets_Config as sh


def getSheet(SHEET):
    gc = pygsheets.authorize()
    sht = gc.open('Crypto')
    wk1 = sht.worksheet_by_title(SHEET)
    df = pd.DataFrame(wk1.get_all_records())
    return df
    # print(df.iloc[0, 0])


def getAllSheets():

    gc = pygsheets.authorize()
    sht = gc.open('Crypto')
    # sh.SPOT = pd.DataFrame(sht.worksheet_by_title('SPOT'))
    # sh.FUTURES = pd.DataFrame(sht.worksheet_by_title('FUTURES'))
    # sh.SCALP = pd.DataFrame(sht.worksheet_by_title('SCALP'))
    # sh.GEM = pd.DataFrame(sht.worksheet_by_title('GEM'))
    sh.SPOT = getSheet('SPOT')
    sh.FUTURES = getSheet('FUTURES')
    sh.SCALP = getSheet('SCALP')
    sh.GEM = getSheet('GEM')
    # print(sh.SPOT)s
    # return [SPOT, FUTURES, SCALP, GEM]
