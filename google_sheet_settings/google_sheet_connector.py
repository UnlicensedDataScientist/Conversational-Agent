import pandas as pd
from google.oauth2 import service_account
import gspread
import numpy as np

from core.settings import settings

# def main(dict_res):
#     return dict_res

def read_google_sheet(url, gid):

   
    # url = url_id_sheet.split('...')[0]
    # gid = url_id_sheet.split('...')[1]
    # Authorize
    gc = authorize_google()
    

    # Open url file
    gsheets = gc.open_by_url(url)

    # Get values from link
    if gid:
        # sheet_data = gsheets.worksheet(sheet_name).get_all_values()
        worksheet = get_sheet_by_gid(gsheets, gid)
    else:
        worksheet = gsheets.get_worksheet(0)

    sheet_data = worksheet.get_all_values()
    # Convert to DataFrame all data
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

    if df.shape[0] == 0:
        return "Google Sheet empty"

    # Replace empty cells with "NaN value"
    df.replace(to_replace="", value="", inplace=True)

    # Replace empty cells with "NaN value"
    df.replace(to_replace="NA", value="", inplace=True)

    # response = {"df": df.to_dict(orient='records'), "worksheet":worksheet}
    # response = {"worksheet":worksheet}
    if gc:
        del gc      

    return df, worksheet
    

def authorize_google():
    # Set scopes and credentials
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    try:
        creds = service_account.Credentials.from_service_account_info(settings.google_cloud_credentials, scopes=scopes)
    except Exception as error_msg:
        creds = service_account.Credentials.from_service_account_info(settings.google_cloud_credentials, scopes=scopes)

    return gspread.authorize(creds)

def get_sheet_by_gid(gsheets, gid):
    # Iterate through all sheets in the spreadsheet
    for sheet in gsheets.worksheets():
        if str(sheet.id) == str(gid):
            return sheet
    raise ValueError(f"No sheet found with gid: {gid}")