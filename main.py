# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:03:20 2020

@author: hesam 
"""
import os
import json
import pandas as pd
import helpers as h
import matplotlib.pyplot as plt

companies = h.get_companies_info()

# with open('data_sets\\companies_records.json','r') as fhandle:
#     companies_records = json.load(fhandle)

companies_records = h.refine_companies_records()
#companies = [key for key in companies_records]


  

def get_data():
    
    user_input= input("Enter the symbol of the company or type HELP: ").upper()  
    
    if user_input == "HELP":
        try:
            #print(companies)
            data = pd.DataFrame.from_dict(companies, orient = 'index')
            pd.set_option('display.max_rows', None)
            #pd.set_option('display.max_columns', 5)
            print("list of companies: \n", data)
            plot_graph()
        except:
            pass
        
    else:
        if user_input in companies:
            company_data = companies_records[user_input.upper()]
            #print(companies_records[user_input.upper()])
            print(company_data)
            print("Working on it ...")
            
            #rows = [company_data[i].dates for i in range(len(company_data))]
            #columns = [c for c in companies ][1:]
            
            return company_data
        

def get_compared_datapoints(company_data):
    '''
    function that takes the company data as a list of objects from the Deltaobject class and returns a nested
    dictionary in this format {time:{company_1:(Color tuple,..., company_n:(color_tuple))}}
    ''' 
    #let's compare data for the company with it's corrosponding data point in other companies
    data_points = []
    dict_of_dates = {}
    #counts = {}
    
    #for each date in the company_data get object's attributes
    for i in company_data:
        date = i.dates
        change = i.change
        percent = i.percent
        
        list_of_companies=[]
        #count = 0
        
        #for the same date, get corresponding data of the companies that you want to compare
        for symbol in companies_records:
            company_to_compare = companies_records[symbol]
            
            
            #for each existing date in company_to_compare dictionary
            for k in company_to_compare:
                
                date_k = k.dates
                change_k = k.change
                percent_k = k.percent
                
                #set color of the comparison result
                if date == date_k:
                    if (change*change_k)<=0:
                        same_change = [1,0,0]#False #show in Red color
                    else:
                        same_change = [0,1,0]#True #show in Green color
                        ##count number of times that change is the same
                        #count += 1
                        #print('count: ', count)
                
                    # Set Color Opacity
                    try:
                        relational_opacity = round(abs(percent_k/percent),2)
                        if relational_opacity >=1:
                            relational_opacity = 1
                        
                    except:
                    
                        relational_opacity = 0
                        
                    
                    #data_point = (same_change, relational_opacity)
                    same_change.append(relational_opacity)
                    data_point = tuple(same_change)
                    #print(data_point)                        
                    data_points.append(data_point)
                
                    company_date_dict = {symbol:data_point}

                    list_of_companies.append(company_date_dict)
                    #counts[k]= count
        #print('company: ', symbol, 'count: ', count, 'k', k)

        dict_of_dates[date] = list_of_companies
        
        
    results = dict_of_dates
    
    #merge separate dictionaries that are created in the last step
    for date in results:
        merged_dict={}
        for d in results[date]:
            merged_dict.update(d) 
        results[date] = merged_dict
    #returns a nested dictionary 
    #return (results , counts)
    return results 

#companies_compared = get_compared_datapoints(get_data())

def clean_dataframe(dataframe):
    try:
        dataframe.fillna(method = 'bfill')
    except:
        dataframe.fillna(0)

def plot_graph():
    """
    function to plot the graph based on the user input and the number of companies they enter
    """
    
    company_data = get_data()    
    result = get_compared_datapoints(company_data)
     
    dataframe = pd.DataFrame(result)           
    
    new_dataframe= clean_dataframe(dataframe)
    
    cols = list(new_dataframe.columns)
    
    companies = list(new_dataframe.index)

    selection = int(input("Number of companies to compare: "))
    
    x_companies = companies[:selection]
    y_date = 1
    
    colors_data = new_dataframe.values[:selection]
    
    #print(colors_data, len(colors_data))
    
    for j in range(colors_data.shape[1]):
        for i in range(selection):
            print(i,j,colors_data[i][j])
            plt.bar(x_companies[i], y_date,bottom=j, color=colors_data[i][j])
            


    new_cols = []
    i = 0
    for col in cols:
        new_cols.append('d'+str(i))
        i += 1
    
        
        
    new_dataframe.columns= new_cols
    
    plt.xticks(x_companies, rotation=90)
    plt.yticks([f for f in range(j+1)],new_cols)
    
    return new_dataframe