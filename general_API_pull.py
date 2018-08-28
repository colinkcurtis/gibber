###General API Access Package
###

## import packages or modules

import configparser, json, mysql.connector, pandas as pd, requests, sqlalchemy, re, numpy as np
from collections import defaultdict

## the following are variables gathering data from the config file and creating various inputs to the class to follow, API_pull_data

# this value, API_setup, is returned from API_setup.py
# API_setup.py should be modified to specify the location and name
# of the config file. The config file must be customized more thoroughly
# for each different API pull, i.e. "/getcurrencies" 
# vs. "/getmarkets" from Bittrex

API_setup = configparser.ConfigParser()

# API_setup.ini should always be saved in the working directory!
API_setup.read('F:/Program Files/pyzo/api_work/API_setup.ini')

API_setup_location = API_setup['CONFIG LOCATION']['config_file_location']

# API_setup.py should be customized (and then run) for each separate 
# API query, producing the file "API_setup.ini" for N # of urls you want to query

temp_API_config = configparser.ConfigParser()

temp_API_config.read(API_setup_location)

API_config = dict(temp_API_config)

exchange = API_config['QUERY INFO']['exchange']

url_to_query = API_config['QUERY INFO']['url_to_query']

any_null_values_anywhere_in_data = 0 

any_invalid_type_values_anywhere_in_data = 0



input_column_headers =  [x[1] for x in API_config['INPUT COLUMN NAMES'].items()]

output_column_headers = [x[1] for x in API_config['OUTPUT COLUMN NAMES'].items()]

output_column_datatypes = [x[1] for x in API_config['OUTPUT COLUMN DATA TYPES'].items()]


class API_pull_data:
    
  def __init__ (self, exchange, url_to_query, input_column_headers, output_column_headers):
    
    self.exchange = exchange
    
    self.url_to_query = url_to_query
    
    self.input_column_headers = input_column_headers
    
    self.output_column_headers = output_column_headers
    
    # self.any_null_values_anywhere_in_data = any_null_values_anywhere_in_data
    # 
    # self.any_invalid_type_values_anywhere_in_data = any_invalid_type_values_anywhere_in_data


  def API_request(self):
      
    raw_API_data = requests.get(self.url_to_query)
    json_API_data = raw_API_data.json()
    
    print('###')
    print()  
    print('Hello, you have begun an API query.')
    print()
    print('Data has been requested from',self.exchange,'@url',self.url_to_query)
    print()
    print('###')
    print()

    if raw_API_data.status_code != 200:
              
      print('oopsies...your query has failed or been rejected with the following status_code:', raw_API_data.status_code)
      print()
        
    else:
              
      print('k.jpeg')
      print()
      
      print('API query to %s was succesful, the raw data has been retrieved, status code: %s' % (self.url_to_query, raw_API_data.status_code))
      print()
        
      # print(json_API_data)
      APIPullData = pd.DataFrame(json_API_data['result'], columns = input_column_headers)
      
      # The column names will most likely need to be adjusted manually for each API request, this is just a starter example
      APIPullData.columns = output_column_headers
        
      print('Column header names were changed from the original, %s, to %s.' % (input_column_headers, output_column_headers))
      print()
      print('The data types for those columns, respectively: %s' % (output_column_datatypes))
      print()
      print('###')
      print()
      
      return APIPullData





  def coin_parameter_check(self, unverified_data):
    
    # a few useful arrays and variables to have on hINTEand for the current method
    
    i = 0
    
    coin_parameter_values_list = list()
    location_nonetype_values = []
    all_nonetype_values = []
    unexpected_value_locations = []
    unexpected_value_type =[]
    
    number_of_columns = len(unverified_data.columns)
    
    temp = number_of_columns
    
    column_length = len(unverified_data)
    
    null = type(None)
    
    any_null_values_anywhere_in_data = 0
    
    any_invalid_type_values_anywhere_in_data = 0
    
    
    
    # we will now check each column(i) for any abberrant data types
    while i < number_of_columns:
      
      # select out the column we want to look over for type-errors
      
      coin_parameter_values_list = unverified_data.loc[: , unverified_data.columns[i]]

      values_list_length = len(coin_parameter_values_list)
      
      

      
      if output_column_datatypes[i] == 'str':
        expected_type = type('string')
        
      elif output_column_datatypes[i] == 'bool':
        expected_type = type(np.bool_(1))
        
      elif output_column_datatypes[i] == 'float':
        expected_type = type(np.float64(1.23))

      elif output_column_datatypes[i] == 'int':
        expected_type = type(np.int64(123))
      
      else:
        print ('Missing data-type value in API_column.ini for at least one column')  


      empty_element_present = 0
      
      invalid_data_present = 0
      
      
      questionable_type_entries = list()
      
      null_entries = list()
      
      
      for x in range(values_list_length):
        
        parameter_value_type = type(coin_parameter_values_list[x])
        
        # print(parameter_value_type)
        # 
        # print(expected_type)
        
        if parameter_value_type == expected_type:
          
          continue
        
        else:
         
          if parameter_value_type is null:
            
            empty_element_present = 1
            
            any_null_values_anywhere_in_data = 1
            
            null_entries.append(str(x))
            
          else:
              
            invalid_data_present = 1
            
            questionable_type_entries.append(str(x))
            
      
      #print(questionable_type_entries)
      
            
      if empty_element_present and invalid_data_present == 0:
          
        any_null_values_anywhere_in_data = 0
    
        any_invalid_type_values_anywhere_in_data = 0
          
        print('Data in column %s is of expected type, %s' % (unverified_data.columns[i], str(output_column_datatypes[i])))
        print()
  
      elif empty_element_present == 1 and invalid_data_present == 0:
        
        any_null_values_anywhere_in_data = 0
        
        any_invalid_type_values_anywhere_in_data = 0
          
        # print('At least one row in column %s is null/empty' % (unverified_data.columns[i]))
        # print()
        # 
        # print('In the %s column, rows containing null/empty values: %s' % (unverified_data.columns[i], ', '.join(null_entries)))
        # print()

      elif empty_element_present == 0 and invalid_data_present == 1:
        
        any_null_values_anywhere_in_data = 1
        
        any_invalid_type_values_anywhere_in_data = 1
        
        # print('At least one row in column %s is not of type %s' % (unverified_data.columns[i], str(output_column_datatypes[i])))
        # print()
        # 
        # print('In the %s column, rows containing questionable-type values: %s' % (unverified_data.columns[i], ', '.join(questionable_type_entries)))
        # print()
        
      else:
        
        any_null_values_anywhere_in_data = 1
        
        any_invalid_type_values_anywhere_in_data = 1
        
        print('At least one row in column %s is not of type %s' % (unverified_data.columns[i], str(output_column_datatypes[i])))
        print()
        
        # print('In the %s column, rows containing null/empty values: %s' % (unverified_data.columns[i], ', '.join(null_entries)))
        # print()
        # 
        # print('In the %s column, rows containing questionable-type values: %s'  % (unverified_data.columns[i], ', '.join(questionable_type_entries)))
        # print()
        
        
        
        # if i < (temp-1):
        #   
        #   print()
        #   print('Next column...')
        #   print()
        # 
        # else:
        #   pass
      
      i+=1
      
      print("ok")
    return any_null_values_anywhere_in_data, any_invalid_type_values_anywhere_in_data



  def output(self, any_null_values_anywhere_in_data, any_invalid_type_values_anywhere_in_data):

    #LEAST PERMISSIVE CASE: NO UNEXPECTED DATA ACCEPTED FOR PASSING TO DATABASE
    if all(API_config['ACCEPTABLE OUTPUT SETTINGS']) == 'False' and (any_null_values_anywhere_in_data + any_invalid_type_values_anywhere_in_data) != 0:
    
      print('Config File dictates that unacceptable data types (null OR unexpected type) shall not be added to the database')  
      
    #PERMISSIVE CASE 1: INVALID-TYPE DATA ACCEPTED AND PASSED TO DATABASE but null is not
    elif API_config['ACCEPTABLE OUTPUT SETTINGS']['null_values_acceptable'] == 'False' and any_null_values_anywhere_in_data == 1:
    
      print('Config File dictates that unacceptable data (null) shall not be added to the database')
    
    
    #PERMISSIVE CASE: null DATA ACCEPTED AND PASSED TO DATABASE but invalid-type is not
    elif API_config['ACCEPTABLE OUTPUT SETTINGS']['unexpected_value_types_acceptable'] == 'False' and any_invalid_type_values_anywhere_in_data == 1:
    
      print('Config File dictates that unacceptable data types (unexpected type) shall not be added to the database')
    
    
    #COMPLETELY PERMISSIVE CASE: ALL DATA ACCEPTED AND PASSED TO DATABASE
    else:
      
      print()
      print('Data will be output to the Database...')
      print()
      
      
      if API_config['DATA OUTPUT TYPES']['output_to_csv'] == 'True':
        
        the_data_we_need.to_csv(API_config['CSV OUTPUT DETAILS']['csv_output_path'])
        
        print('The data has been output to path %s in %s format.' % (API_config['CSV OUTPUT DETAILS']['csv_output_path'], API_config['CSV OUTPUT DETAILS']['csv_format']))
        print()
        
      else:
        print('Data will not be output to CSV, see config file if this was unintended')
        print()
        pass
       
          
      if API_config['DATA OUTPUT TYPES']['output_to_sql'] == 'True':
        
        the_data_we_need.to_csv(API_config['SQL OUTPUT DETAILS']['sql_output_path'])
        
        print('The data has been output to path %s in %s format.' % (API_config['SQL OUTPUT DETAILS']['sql_output_path'], API_config['SQL OUTPUT DETAILS']['sql_format']))
        print()
        
      else:
        print('Data will not be output to SQL, see config file if this was unintended')
        print()
        pass
        
      
      if API_config['DATA OUTPUT TYPES']['output_to_json'] == 'True':
        
        the_data_we_need.to_csv(API_config['JSON OUTPUT DETAILS']['json_output_path'])
        
        print('The data has been output to path %s in %s format.' % (API_config['JSON OUTPUT DETAILS']['json_output_path'], API_config['JSON OUTPUT DETAILS']['json_format']))
        print()
        
      else:
        print('Data will not be output to JSON, see config file if this was unintended')
        print()
        pass

## Calling the code above, which ultimately must be scripted...
#the inputs, manually defined above, are then packaged into a single device which we 
#are then able to call when we create the object

bittrex_getcurrencies_API_config = [exchange, url_to_query, input_column_headers, output_column_headers, output_column_datatypes] 

#instantiate the object
the_data_object = API_pull_data(bittrex_getcurrencies_API_config[0], bittrex_getcurrencies_API_config[1], bittrex_getcurrencies_API_config[2], bittrex_getcurrencies_API_config[3])

#create the request for data and format it with our method for the object
the_data_we_need = the_data_object.API_request()


error_check = the_data_object.coin_parameter_check(unverified_data = the_data_we_need)

output_fcn = the_data_object.output(any_null_values_anywhere_in_data = error_check[0], any_invalid_type_values_anywhere_in_data = error_check[1])






# 
# 
# else:
#   
#   print('Config File dictates that unacceptable data types (null OR unexpected type) shall not be added to the database')


 ##   elif API_config['ACCEPTABLE OUTPUT SETTINGS']['null_values_acceptable']) == True and API_config['ACCEPTABLE OUTPUT SETTINGS']['null_values_acceptable']) == False:
  # 
  #   print('This data may contain invalid-type entries')
  #   
  #   if API_config['DATA OUTPUT TYPES']['output_to_csv'] == True:
  #   
  #     the_data_we_need.to_csv(API_config['CSV OUTPUT DETAILS']['csv_output_path'])
  #     
  #     print('The data has been output to path %s in %s format.' % (API_config['CSV OUTPUT DETAILS']['csv_output_path'], API_config['CSV OUTPUT DETAILS']['csv_format']))
  #   
  #   else:
  #     
  #     pass
  #   
  #   if API_config['DATA OUTPUT TYPES']['output_to_sql'] == True:
  #     
  #     the_data_we_need.to_csv(API_config['SQL OUTPUT DETAILS']['sql_output_path'])
  #     
  #     print('The data has been output to path %s in %s format.' % (API_config['SQL OUTPUT DETAILS']['sql_output_path'], API_config['SQL OUTPUT DETAILS']['sql_format']))
  #   
  #   else:
  #     
  #     pass
  #   
  #   if API_config['DATA OUTPUT TYPES']['output_to_json'] == True:
  #     
  #     the_data_we_need.to_csv(API_config['JSON OUTPUT DETAILS']['json_output_path'])
  #     
  #     print('The data has been output to path %s in %s format.' % (API_config['JSON OUTPUT DETAILS']['json_output_path'], API_config['JSON OUTPUT DETAILS']['json_format']))
  #   
  #   else:
  #     
  #     pass


  

