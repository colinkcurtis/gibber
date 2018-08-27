# The config module for general_api_pull.py


from configparser import ConfigParser
from collections import OrderedDict

# 'config' is defined below for short-hand purposes in this file

setup = configparser.ConfigParser()

setup['CONFIG LOCATION'] = {

'config_file_location' : 'F:/Program Files/pyzo/api_work/API_config.ini'

}












path = 'F:/Program Files/pyzo/api_work/API_setup.ini'
with open(path, 'w') as configfile: setup.write(configfile)