from dotenv import load_dotenv
import platform
import requests 
import json
import os 
import sys
from tkinter import *
from tkinter.ttk import *

####~~~~~~~~~Section for USERNAME/PASSWORD parameter file~~~~~~~~~####
find_env = platform.system()

if find_env.upper() == 'DARWIN':
    # This will be the path for Mac
    save_path = '/Users/Shared/' #Where files are saved on Mac
    dotenv_path = '/Users/Shared/temp.env' #Where env variables are stored
    load_dotenv(dotenv_path)
else:
    # This will be the path for Windows
    #Setting User for Directory
    user = os.getenv('USERNAME')
    save_path = f'C:/Users/{user}/Documents/' #Location on windows where files are saved
    dotenv_path = f'C:/Users/{user}/Documents/temp.env'
    load_dotenv(dotenv_path)

#Setting Username/Password/POD info from .env file
username = os.environ.get("P_USERNAME")
psswd= os.environ.get("P_PASSWORD")
pod= os.environ.get("P_POD")
cloud_provider= os.environ.get("P_CLOUD_PROVIDER")

#input('Pod: (IE na1) ')
url = 'https://'+pod+'.'+cloud_provider+'.informaticacloud.com/saas'
url_v2 = 'https://'+pod+'.'+cloud_provider+'.informaticacloud.com/ma/api/v2/user/login'

#Demo
functions = "Current working functions:\n\
            *login\n\
            *getAllObjectType\n\
            *getObjectCompare\n\
            *getListPermissions\n\
            *getMappingDetails\n\
            *getPermissions\n\
            -getPermissionCheck (Currently Draft)\n\
            getFolder\n\
            createPermission\n\
            deletePermissions"

print(functions)

####~~~~~~~~~Login w/ GUI~~~~~~~~~####
def login():
    global token
    global headers
    global headersV2
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
    'infa-session-id' : f"{token}"
    }

    headersV2 = {
    'content-type' : 'application/json',
    'accept' : 'application/json',
    'icSessionId' : f"{token}"
    }

    #Note: v3 token appears to work for both v3 and v2
    print(f"Token: {token}")
    print(f"Status: {response.status_code}")

    login_window = Toplevel(window)
    login_window.title("Login Information")

    tokendisplay = Label(login_window, text=f"Token: {token}")
    tokendisplay.pack()

    statusdisplay = Label(login_window, text=f"Status: {response.status_code}")
    statusdisplay.pack()

####~~~~~~~~~All Object Type Screen Info~~~~~~~~~####





####~~~~~~~~~Lookup All Object Type~~~~~~~~~####
def getAllObjectType ():    
    #Variables
    global fl_dict
    global lValue1
    
    queryObject = "type"
    message = "Lookvalues\n\
          DTEMPLATE = Mapping\n\
          MTT = Mapping task\n\
          DSS = Synchronization task\n\
          DMASK = Masking task\n\
          DRS = Replication task\n\
          DMAPPLET = Mapplet created in Data Integration\n\
          MAPPLET = PowerCenter mapplet\n\
          BSERVICE = Business service definition\n\
          HSCHEMA = Hierarchical schema\n\
          PCS = PowerCenter task\n\
          FWCONFIG = Fixed width configuration\n\
          CUSTOMSOURCE = Saved query\n\
          MI_TASK = Mass ingestion task\n\
          WORKFLOW = Linear taskflow\n\
          VISIOTEMPLATE\n\
          TASKFLOW\n\
          PROJECT\n\
          FOLDER"
    
    #Screen Information
    getAOT_window = Tk()
    getAOT_window.geometry("500x500")
    getAOT_window.title("Get Object Types")
    lValue = StringVar()
    lValue = lValue.get()

    #Entry Variable Boxes
    message_Label = Label(getAOT_window, text=message)
    message_Label.grid(row=1, column=1)

    lValue = StringVar()
    lValue_Label = Label(getAOT_window, text= "Look up value: ")
    lValue_Label.grid(row=2, column=1)
    lValue_Entry = Entry(getAOT_window, textvariable = lValue, font=('calibre',10,'normal'))
    lValue_Entry.grid(row=2, column=2)

    runAOT_button = Button(getAOT_window, text="Run", command=AllObjectType)
    runAOT_button.grid(row=3,column=2)
    lValue1= StringVar()
    lValue.trace("w", mywarWritten)

def mywarWritten(*args):
    lValue1 = lValue.get()

def AllObjectType():
    queryObject = 'type'
    fl_url = url + f"/public/core/v3/objects?q={queryObject}=='{lValue1}'"
    fl_response = requests.get(fl_url, headers=headers)
    fl_jsonResponse = fl_response.json()

    #Setting up lists
    fl_keys = []
    fl_values = []
    
    #Pull all objects of type into list
    for element in fl_jsonResponse['objects']:
        fl_keys.append(element['path'].split('/')[-1])
        
    #Getting IDS
    for element2 in fl_jsonResponse['objects']:
        fl_values.append(element2['id'])

    #Combine Object Name and Values
    fl_dict = {}
    fl_dict = dict(map(lambda i,j : (i,j) , fl_keys,fl_values))

    #Compare perfix value to object list RETURN only
    print(json.dumps(fl_dict, indent=4))
    
    #Write Dictionary File to be used in other Scripts
    with open(save_path + "objects.json", "w") as outfile:
        json.dump(fl_dict, outfile, indent=4)
    print("Results output to Document folder in objects.json")

####~~~~~~~~~ The Playground ~~~~~~~~~####

def test():
    test_window = Toplevel(window)
    test_window.title("TEST")

    testValue = "as92kfna9su3nfa"
    displaylogin = Label(test_window, text=f"Login Value: {testValue}")
    displaylogin.pack()

####~~~~~~~~~ Screen Information ~~~~~~~~~####
window = Tk()
window.title("Informatica API")
window.configure(width=500, height=300)
#frm = Tk.frame(window)
window.configure(bg='lightskyblue')

#Built into the Login Function
login_button = Button(window, text="Login", command=login)
login_button.pack()

#Open to a second window to input variables
getAllObjectType_button = Button(window, text="Get All Object of a Type", command=getAllObjectType)
getAllObjectType_button.pack()

                                 
#getObjectCompare_button = Button(window, text="Compare Object Format"
#getObjectCompare_button.pack()

                                 
#getListPermissions_button = Button(window, text="Get List of Permissions"
#getMappingDetails_button = Button(window, text="Get Mapping Details"
#getPermissions_button = Button(window, text="Get Permissions Details"
#getPermissionCheck_button = Button(window, text="Check Permission"
#getFolder_button = Button(window, text="Find a Folder"
#createPermission_button = Button(window, text="Create Permissions"
#deletePermissions_button = Button(window, text="Delete Permissions"
test_button = Button(window, text="Test", command=test)
test_button.pack()


#Exit Button
exit_button = Button(window, text="Exit", command=window.destroy)
exit_button.pack()
#exit_button.pack(side=BOTTOM)
#exit_button.pack(side=RIGHT)

window.mainloop()
