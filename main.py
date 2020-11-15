# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:03:20 2020

@author: hesam 
"""
import os
import json
import pandas as pd
import helpers as h

companies = h.get_companies_info()

# with open('data_sets\\companies_records.json','r') as fhandle:
#     companies_records = json.load(fhandle)

companies_records = h.refine_companies_records()
#companies = [key for key in companies_records]

user_input= input("Enter the symbol of the company or type HELP: ").upper()
  
    
if user_input == "HELP":
    #print(companies)
    data = pd.DataFrame.from_dict(companies, orient = 'index')
    pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', 5)
    print("list of companies: \n", data)
    
else:
    if user_input in companies:
        company_data = companies_records[user_input.upper()]
        #print(companies_records[user_input.upper()])
        print(company_data)
        print("Working on it ...")
        
        #data_frame= pd.DataFrame()
        rows = [company_data[i].dates for i in range(len(company_data))]
        columns = [c for c in companies ][1:]
        
        # for company in companies_records:

 
def get_compared_datapoints(company_data):
        #let's compare data for the company with it's corrosponding data point in other companies
        data_points = []
        dict_of_dates = {}
        
        for i in company_data:
            date = i.dates
            change = i.change
            percent = i.percent
            
            lc=[]
            
            for symbol in companies_records:
                company_to_compare = companies_records[symbol]
                
                for k in company_to_compare:
                    date_k = k.dates
                    change_k = k.change
                    percent_k = k.percent
                    
                    #set color of the comparison result
                    if date == date_k:
                        if (change*change_k)<=0:
                            same_change = False #show in Red color
                        else:
                            same_change = True #show in Green color
                    
                        # Set Color Opacity
                        try:
                            relational_opacity = abs(percent_k/percent)
                            if relational_opacity >=1:
                                relational_opacity = 1
                            
                        except:
                        
                            relational_opacity = 0
                       
                        data_point = (same_change, relational_opacity)                        
                        data_points.append(data_point)
                    
                        company_date_dict = {symbol:data_point}

                        lc.append(company_date_dict)

            dict_of_dates[date] = lc
            
        results = dict_of_dates
        
        #merge separate dictionaries that are created in the last step
        for date in results:
            merged_dict={}
            for d in results[date]:
                merged_dict.update(d) 
            results[date] = merged_dict
        
        return results
    
result = get_compared_datapoints(company_data)

dataframe=pd.DataFrame.from_dict(result)
_dataframe = pd.DataFrame.transpose(dataframe)


                        