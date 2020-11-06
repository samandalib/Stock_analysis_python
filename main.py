# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:03:20 2020

@author: hesam
"""

import finnhub
from helpers import *

# start_date = input("Enter the start date in mm/dd/yyyy format: ")
# end_date = input("Enter the end date in mm/dd/yyyy format: ")

start_date = "01/01/2010"
end_date = "01/01/2020"
start_date, end_date = date_convertor(start_date), date_convertor(end_date)


print(start_date, end_date)
# Setup client
finnhub_client = finnhub.Client(api_key="bui229f48v6rfhsb6s50")

# Stock candles
res = finnhub_client.stock_candles('AAPL', 'D', start_date, end_date)
#print(res)

#Convert to Pandas Dataframe
import pandas as pd
print(pd.DataFrame(res))




