## The config module for general_api_pull.py

from configparser import ConfigParser
from collections import OrderedDict

# 'config' is defined below for short-hand purposes in this file

config = configparser.ConfigParser()


config['QUERY INFO'] = {

'exchange' : 'Bittrex', 
'url_to_query' : 'https://bittrex.com/api/v1.1/public/getcurrencies'

}


config['INPUT COLUMN NAMES'] = {

'column_input_name_1' : 'CurrencyLong',
'column_input_name_2' : 'Currency',
'column_input_name_3' : 'Coindatatype',
'column_input_name_4' : 'TxFee',
'column_input_name_5' : 'MinConfirmation',
'column_input_name_6' : 'IsActive',
'column_input_name_7' : 'BaseAddress',
'column_input_name_8' : 'Notice',

}


config['OUTPUT COLUMN NAMES'] = {

'column_output_name_1' : 'LongName',
'column_output_name_2' : 'ShortName',
'column_output_name_3' : 'Coindatatype',
'column_output_name_4' : 'TransactionFee',
'column_output_name_5' : 'MinNumberConfirmsAcceptTransaction',
'column_output_name_6' : 'CoinIsActive',
'column_output_name_7' : 'BaseAddress',
'column_output_name_8' : 'Notes',

}


config['OUTPUT COLUMN DATA TYPES'] = {

'column_output_datatype_1' : 'str',
'column_output_datatype_2' : 'str',
'column_output_datatype_3' : 'str',
'column_output_datatype_4' : 'float',
'column_output_datatype_5' : 'int',
'column_output_datatype_6' : 'bool',
'column_output_datatype_7' : 'str',
'column_output_datatype_8' : 'str'

}

config['ACCEPTABLE OUTPUT SETTINGS'] = {

'null_values_acceptable' : False,
'unexpected_value_types_acceptable' : False

}

config['DATA OUTPUT TYPES'] = {

'output_to_csv' : True,
'output_to_sql' : False,
'output_to_json' : False

}



config['CSV OUTPUT DETAILS'] = {

'csv_format' : 'CSV',

'csv_output_path' : 'csv_test.csv'

}



config['SQL OUTPUT DETAILS'] = {

'sql_format' : 'SQL',

'csv_output_path' : 'sql_test.sql'

}



config['JSON OUTPUT DETAILS'] = {

'json_format' : 'JSON',

'csv_output_path' : 'json_test.json'

}


path = 'F:/Program Files/pyzo/api_work/API_config.ini'
with open(path, 'w') as configfile: config.write(configfile)