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
# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# df = table[0]
# df.to_csv('S&P500-Info.csv')
# df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

def get_companies_info():
    with open ("data_sets\\S&P500-Info.csv","r") as f:
        companies = f.readlines()
    
    
    company_list = []
    company_dictionary = {}
    
    for line in companies:
        line_list = line.strip('\n').split(",")
        company_list.append(line_list)
        # company_dictionary[line[1]]=line[2:]
    # symbols = companies[:]
    #print (company_list)
    dictionary_guide ={}
    dictionary_guide[company_list[0][1]]=company_list[0][2:]
    
    
    print("Dictionary Guide: ",dictionary_guide)
    
    for company in company_list[0:101]:
        company_dictionary[company[1]]=company[2:]
        
    return company_dictionary

'''
Function for updating all the files in the database
'''
def update_dataset():
    import os
    import finnhub
    import pandas as pd
    # start_date = input("Enter the start date in mm/dd/yyyy format: ")
    # end_date = input("Enter the end date in mm/dd/yyyy format: ")
       
    companies = get_companies_info()
    
    start_date = "01/01/2019"
    end_date = "01/02/2019"
    start_date, end_date = date_convertor(start_date), date_convertor(end_date)
    print(start_date, end_date)
    
    os.chdir("data_sets")
    
    # Setup client
    finnhub_client = finnhub.Client(api_key ="bui229f48v6rfhsb6s50")
    
    for company in companies:
        try:
            print(company)   
            # Stock candles
            res = finnhub_client.stock_candles(company, 'D', start_date, end_date)
            #print(res)
            
            #Convert to Pandas Dataframe 
            response = pd.DataFrame(res)  
            
            #Write the CSV file out of data frame
            response_csv = response.to_csv(f"{company}.csv")
        except:
            print('no company found ...')
 
'''
Function for returning information about specific company
'''
def get_company_data(company):
    import os
    
    #os.chdir("data_sets")
    os.getcwd()
    with open (f"{company}.csv", "r") as c:
        company_data = c.readlines()
    #pd.DataFrame(company_data)
    return company_data[1:]

'''
Function for getting a dictionary for all the changes in prices in the gathered files
and calculating price changes 
'''    
def refine_companies_records():
    import os
    from classes import DeltaObject
    
    companies = get_companies_info()
    os.chdir('data_sets')
    files = os.listdir()
    companies_records = {}
    for company in companies:
        #print (True)
        if (company + '.csv') in files:
            # print('in files: ', True)
            company_data = get_company_data(company)
            
            #get close prices in a list
            close_price_list = []
            for line in company_data:
                date_price = []
                line = line.strip('\n').split(',')
                #close_price_list.append(line[1])
                date_price.append(line[1])
                date_price.append(line[6])
                close_price_list.append(date_price)
            
            #calculate the change in prices each day
            change_list = []
            
            for i in range(1,len(close_price_list)):
    
                delta_change = float(close_price_list[i][0]) - float(close_price_list[i-1][0])
                percent_change = delta_change / float(close_price_list[i-1][0])
                dates =(close_price_list[i-1][1],close_price_list[i][1])
                
                
                change_list.append(DeltaObject(delta_change,percent_change,dates))
            
            companies_records[company]= change_list
                     
    return companies_records



def export_to_json():
    import json
    records = refine_companies_records()
        
    json_data = json.dumps(records, default=lambda o: o.__dict__, indent=4)
      
    with open ('companies_records.json', 'w') as f:
                 f.write(json_data)
    