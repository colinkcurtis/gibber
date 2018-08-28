#
# 
####  API Access - Bittrex public getcurrencies
import pandas as pd, numpy as np, requests, json, os, sqlalchemy, mysql.connector, timeit, re

## pull the data from the API access

data = requests.get("https://bittrex.com/api/v1.1/public/getcurrencies")

jsondata = data.json()

# if it doesn't work, say oops; if it works, k
if data.status_code != 200:
  print()
  print('oopsies...', data.status_code)
  print()
    
else:
    
  print()
  print('k.jpeg')
  print()

# we will be using pandas.DataFrame to mySQL, so we convert to this type

BittrexGetCurrenciesDataFrame = pd.DataFrame(jsondata['result'], columns=['CurrencyLong', 'Currency', 'CoinType', 'TxFee', 'MinConfirmation','IsActive','BaseAddress'])

# rename the columns for intelligibility
BittrexGetCurrenciesDataFrame.columns = ['BittrexCurrencyFullName', 'BittrexCurrencyShortName', 'BittrexCoinType', 'BittrexTransactionFee', 'BittrexMinForConfirmation', 'BittrexCoinIsActive','BittrexCoinBaseAddress']

print(BittrexGetCurrenciesDataFrame)

## Data Quality Check and Bad Data Replacement v0.1

# Before we add a new batch of data to our database, it is worthwhile
# to quickly check for problems within the batch
# For now, any problem spot will be replaced with "BAD CHAR INPUT" and a flag
# will be thrown to the users. 
# ALSO - in order to make comparisons using the same models across
# multiple data sets originating from multiple data sources, there
# must be a "data homogenization" process, for which we can call this the 
# 'beta' version, 'Data Quality Check and Bad Data Replacement v0.1'

# define bad characters for Currency Full Name (using RegEx) and produce a list where a 
#'True' value  indicates the presence of a so-called 'bad character'
BadCurrencyFullNameCharacters = '[^\w\s\.\-\'\/]'

BittrexCurrencyFullNameValidityList = BittrexGetCurrenciesDataFrame.BittrexCurrencyFullName.str.contains(BadCurrencyFullNameCharacters)



# define bad characters for Currency Short Name (using RegEx) and produce a list where a 'True value
# indicates the presence of a so-called 'bad character'
BadCurrencyShortNameCharacters = '[^\w]'

BittrexCurrencyShortNameValidityList = BittrexGetCurrenciesDataFrame.BittrexCurrencyShortName.str.contains(BadCurrencyShortNameCharacters)

# define bad characters for Coin Type (using RegEx) and produce a list where a 'True value
# indicates the presence of a so-called 'bad character'
BadCoinTypeCharacters = '[^\w\_]'

BittrexCoinTypeValidityList = BittrexGetCurrenciesDataFrame.BittrexCoinType.str.contains(BadCoinTypeCharacters)

# 
# #
# #
# #
# 
# # define bad characters for Transaction Fee (using RegEx) and produce a list where a 'True value
# # indicates the presence of a so-called 'bad character'
BadTransactionFeeCharacters = '[^\d\.]'

BittrexTransactionFeeValidityList = BittrexGetCurrenciesDataFrame.BittrexTransactionFee.str.contains(BadTransactionFeeCharacters)

# 
# 
# 
# 
# 
# # define bad characters for Min # For Confirmation (using RegEx) and produce a list where a 'True value
# # indicates the presence of a so-called 'bad character'
# MinForConfirmationCharacters = '[^\d\.]'
# # 
# BittrexMinForConfirmationValidityList = BittrexGetCurrenciesDataFrame.BittrexMinForConfirmation.str.contains(MinForConfirmationCharacters)

# 
# 
# 
# 
# 
# # define bad characters for Coin Is Active (using RegEx) and produce a list where a 'True value
# # indicates the presence of a so-called 'bad character'
# CoinIsActiveCharacters = '[^\w]'
# # 
# BittrexCoinIsActiveValidityList = BittrexGetCurrenciesDataFrame.BittrexCoinIsActive.str.contains(CoinIsActiveCharacters)
# 
# 
# 
# 
# 
# 
# 
# # define bad characters for CoinBaseAddress (using RegEx) and produce a list where a 'True value
# # indicates the presence of a so-called 'bad character'
# BadCoinBaseAddressCharacters = '[^\w]'
# 
# BittrexCoinBaseAddressValidityList = BittrexGetCurrenciesDataFrame.BittrexCoinBaseAddress.str.contains(BadCoinBaseAddressCharacters)
# 


## Time to check the data for bad (potentially harmful) characters

# If there is a bad entry in the column 'CurrencyFullName', replace with 'BAD CHAR INPUT'
# the two strings below will be used in the for loop to follow

# define a few reusable items for the following for loops
badstring =''
ReplacementString = 'BAD_CHAR_INPUT'
BittrexCoinListLength = range(len(BittrexCurrencyFullNameValidityList))

  
if np.any(BittrexCurrencyFullNameValidityList) == True:
  print('time to replace some values in CurrencyFullName column!')
    
  for w in BittrexCoinListLength: 
  
    if BittrexCurrencyFullNameValidityList[w] == True:
    
      badstring = BittrexGetCurrenciesDataFrame.BittrexCurrencyFullName[w]
 
      BittrexGetCurrenciesDataFrame.BittrexCurrencyFullName[w] =    BittrexGetCurrenciesDataFrame.BittrexCurrencyFullName[w].replace(badstring, ReplacementString)
    

    else:
      continue

else:
  print('all CurrencyFullName values OK!')
  
    
    
# just a timer for the method above, may be useful for testing alternates later
# 
# timeit1 = timeit.Timer(lambda: Q)
# 
# print('timeit for .str.contains operating on a list, x1000:')
# print(timeit1.timeit(number=1000), 'seconds')




# Check validity of BittrexCurrencyShortName



  
if np.any(BittrexCurrencyShortNameValidityList) == True:
  print('time to replace some values in CurrencyShortName column!')
    
  for w in BittrexCoinListLength: 
  
    if BittrexCurrencyShortNameValidityList[w] == True:
    
      badstring = BittrexGetCurrenciesDataFrame.BittrexCurrencyShortName[w]
 
      BittrexGetCurrenciesDataFrame.BittrexCurrencyShortName[w] =    BittrexGetCurrenciesDataFrame.BittrexCurrencyShortName[w].replace(badstring, ReplacementString)
    

    else:
      continue

else:
  print('all CurrencyShortName values OK!')
    

# Check validity of Coin Type, this could be even more specific like..
# "if in list of known coin types" etc since there are very few...


  
if np.any(BittrexCoinTypeValidityList) == True:
  print('time to replace some values in BittrexCoinType column!')
    
  for w in BittrexCoinListLength: 
  
    if BittrexCoinTypeValidityList[w] == True:
    
      badstring = BittrexGetCurrenciesDataFrame.BittrexCoinType[w]
 
      BittrexGetCurrenciesDataFrame.BittrexCoinType[w] =    BittrexGetCurrenciesDataFrame.BittrexCoinType[w].replace(badstring, ReplacementString)
    

    else:
      continue

else:
  print('all CoinType values OK!')
    
    

# Check the validity of Min

for w in BittrexCoinListLength:
 
  if BittrexCoinTypeValidityList[w] == True:
    
    print(BittrexGetCurrenciesDataFrame.BittrexCoinTypeName[w])
    
    badstring = BittrexGetCurrenciesDataFrame.BittrexCoinType[w]
 
    BittrexGetCurrenciesDataFrame.BittrexCoinType[w] =   BittrexGetCurrenciesDataFrame.BittrexCoinType[w].replace(badstring, 'BAD CHAR INPUT')
    
    print(w)
    print(BittrexGetCurrenciesDataFrame.BittrexCoinType[w])

  else:
    continue


# Check the validity of Min
    
    
for w in BittrexCoinListLength:
 
  if BittrexCoinTypeValidityList[w] == True:
    
    print(BittrexGetCurrenciesDataFrame.BittrexCoinTypeName[w])
    
    badstring = BittrexGetCurrenciesDataFrame.BittrexCoinType[w]
 
    BittrexGetCurrenciesDataFrame.BittrexCoinType[w] =   BittrexGetCurrenciesDataFrame.BittrexCoinType[w].replace(badstring, 'BAD CHAR INPUT')
    
    print(w)
    print(BittrexGetCurrenciesDataFrame.BittrexCoinType[w])

  else:
    continue
    



## Output the data to mySQL format, CSV format, or other
BittrexGetCurrenciesDataFrame.to_csv('csvtest.csv')



#engine = create_engine('mysql+mysqlconnector://[ckc1]:[Unknown?]@[host]:[port]/[schema]', echo=False)

#getCurrenciesDataFrame.to_sql(name='bittrextest', con=engine, if_exists = 'append', index=False)
