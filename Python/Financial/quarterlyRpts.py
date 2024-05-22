import requests

def get_income_statement(symbol, api_key):
    global data
    
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'quarterlyReports' in data:
            income_statement = data['quarterlyReports'][0]  # Assuming we want the latest quarterly data
            return income_statement
        else:
            print("No income statement data available for the symbol.")
            return None
    else:
        print("Failed to fetch data")
        return None
    
def get_pe_ratio(symbol, api_key):
    global data

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'PERatio' in data:
        return data['PERatio']
    else:
        return None    

# Variables
api_key = "WO0CMAJSK0KCEMNS"
#api_key = 'demo' ###tester key

symbol = input("Symbol: ")

'''Uncomment to run the income statement'''
#income_statement = get_income_statement(symbol, api_key)
try:
    if income_statement:
        print(f"Income Statement for {symbol}:")
        for key, value in income_statement.items():
            print(f"{key}: {value}")
    else:
        print("No income statement data available.")
except NameError:
  print("Accepting the comment and passing Get_Income_Statement function")         

'''Uncomment to run the PEration'''
try:
    pe_ratio = get_pe_ratio(symbol, api_key)

    if pe_ratio:
        print(f"The P/E ratio for {symbol} is: {pe_ratio}")
    else:
        print(f"Failed to retrieve P/E ratio for {symbol}")    

except NameError:
  print("Accepting the comment and passing PeRatio function")         
