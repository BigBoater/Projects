import os
import csv
import json
import requests

#Needed Variables
csv_file =  "/Users/jmodisett/Documents/Structure/CSV/testNoQuotes.csv" #input("Location of CSV file with File name: ")
output_dir = "/Users/jmodisett/Documents/Structure/Output" #input("Location of where to output CSV files: ")
print(f'Current Direcrtory: {csv_file} \nCurrent Output Dirctory: {output_dir}')
#Working
print('\ncsv_to_json')
print('login')
print('rdsDelete\n')

####~~~~~~~~~Login~~~~~~~~~####
def login():
    global token
    global headers
    global headersV2
    #Login
    username = 'jmodisett@ieast.informatica.com' #input("Username: ")
    psswd= 'Number01!' #input("Password: ")
    #Login Parameters
    params = json.dumps({
    'username' : f'{username}',
    'password' : f'{psswd}'
    })
    headers = {
    'content-type' : 'application/json',
    'accept' : 'application/json'
    }
    #Url for Login
    url = 'https://dm-us.informaticacloud.com/saas'
    url = url+'/public/core/v3/login'
    response = requests.post(url, data=params, headers=headers)
    jsonResponse = response.json()
    
    #Get Token
    token = jsonResponse['userInfo'].get('sessionId')
    
    #Updating Headers with Token for futrue functions
    headers = {
    'content-type' : 'application/json',
    'accept' : 'application/json',
    'IDS-SESSION-ID' : f"{token}"
    }

    headersV2 = {
    'content-type' : 'application/json',
    'accept' : 'application/json',
    'icSessionId' : f"{token}"
    }

    #Note: v3 token appears to work for both v3 and v2
    print(f"Token: {token}")
    print(f"Status: {response.status_code}")

####~~~~~~~~~File to Jsons~~~~~~~~~####
def write_json(values, output_dir, file_index):
    json_data = {"Codes": values}
    file_name = os.path.join(output_dir, f"file_{file_index}.json")
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
        json_file.write('\n')  # Add a newline at the end for clarity

def csv_to_json(csv_file, output_dir):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        values = []
        file_index = 1

        for row in reader:
            values.append(row[0])
            if len(values) == 50:
                write_json(values, output_dir, file_index)
                values = []
                file_index += 1

        # Write the remaining values if any
        if values:
            write_json(values, output_dir, file_index)

####~~~~~~~~~API Delete Codes~~~~~~~~~####
def rdsDelete():
    #User Input
    codelist = '649c5418e77ce071b1352c1b' #input("Codelist ID: ")

    #Files
    files = os.listdir(output_dir)
    file = []
    for f in files:
        if f[-4:] == "json":
            file.append(f)
    
    #Urls
    pod = 'na1-mdm'
    cloud_provider = 'dm-us'
    rdsUrl = f'rdm-service/external/v1/codelists/{codelist}/codevalues'
    fullRdsUrl = f'https://{pod}.{cloud_provider}.informaticacloud.com/{rdsUrl}'

    #API iterative
    for f in file:
        f1 = open(f'{output_dir}/{f}')
        jsonData = json.load(f1)
        jsonData = json.dumps(jsonData)
        #json.dump(
        print(fullRdsUrl)
        print(jsonData)
        print(headers)
        
        response = requests.delete(fullRdsUrl, data=jsonData, headers=headers)
        jsonResponse = response.json()
        print(f"Status: {response}")
