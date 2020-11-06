# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:31:14 2020

@author: hesam
"""

"""
UNIX timestamp convertor functions:
    date_convertor function takes the human readable date in MM/DD/YYYY format and returns Unix
    Timestamp in integer format
    timestamp_converot function takes the UNIX timestamp format and returns human readable date in
    MM/DD/YYYY format
"""

def date_convertor(date):
    #convert the time to UNIX timestamp
    import time
    result = int(time.mktime(time.strptime(date, "%d/%m/%Y")))
    return result #Returns Integer type
    


def timestamp_convertor(timestamp):
        import datetime
        result = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
        return result #Returns String type


'''Company Symbols'''
# import requests
# r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=')
# res = r.json()
# import pandas as pd
# print(pd.DataFrame(res))