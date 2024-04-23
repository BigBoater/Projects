from dotenv import load_dotenv
import platform
import requests 
import json
import os 
import sys

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
            *getPermissionCheck\n\
            getFolder\n\
            createPermission\n\
            deletePermissions"

print(functions)

####~~~~~~~~~Login~~~~~~~~~####
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

####~~~~~~~~~Lookup Object~~~~~~~~~####
def getFolder ():    
    #Variables
    global fl_jsonResponse
    queryObject = input("Request type? (location, type, tag) ")
    lValue = input("Lookup value: ")

    #URL
    fl_url = url+f"/public/core/v3/objects?q={queryObject}=='{lValue}'"
    fl_response = requests.get(fl_url, headers=headers)
    fl_jsonResponse = fl_response.json()
    print(json.dumps(fl_jsonResponse, indent=4))

####~~~~~~~~~Lookup All Object Type~~~~~~~~~####
def getAllObjectType ():    
    #Variables
    global fl_dict
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
    print(message)
    lValue = input("Lookup value: ")
    ####URL
    fl_url = url+f"/public/core/v3/objects?q={queryObject}=='{lValue}'"
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
    print(functions)

####~~~~~~~~~Lookup Object~~~~~~~~~####
def getObjectCompare ():    
    #Variables
    global fl_jsonResponse #for testing
    global fl_dict
    global fl_output
    queryObject = "type"
    message = "Lookvalues\n\
          MTT = Mapping task\n\
          TASKFLOW\n\
          PROJECT\n\
          FOLDER\n\
          DTEMPLATE = Mapping\n\
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
          VISIOTEMPLATE"
    print(message)
    lValue = input("Lookup value: ")
    prefix_value = input("Object prefix value: ")

    ####URL
    fl_url = url+f"/public/core/v3/objects?q={queryObject}=='{lValue}'"
    fl_response = requests.get(fl_url, headers=headers)
    fl_jsonResponse = fl_response.json()
    fl_value = []
    fl_value2 = []
    
    #Pull all objects into list
    for element in fl_jsonResponse['objects']:
        fl_value.append(element['path'].split('/')[-1])
        
    #Getting IDS
    for element2 in fl_jsonResponse['objects']:
        fl_value2.append(element2['id'])
        
    #Combine Object Name and Values
    fl_dict = {}
    fl_dict = dict(map(lambda i,j : (i,j) , fl_value,fl_value2))
    
    #Compare perfix value to object list RETURN only
    fl_output = []
    for element3 in fl_dict.keys():
        if element3[:len(prefix_value)].upper() != prefix_value.upper():
            fl_output.append(element3)
        else:
            continue
    print(json.dumps(fl_jsonResponse, indent=4))
    with open(save_path + "ObjectCompare.json", "w") as outfile:
        json.dump(fl_output, outfile, indent=4)
    print("ObjectCompare.json output to Document folder")
    print(functions)

####~~~~~~~~~Lookup Permissions~~~~~~~~~####
def getPermissions ():
    #Variables
    global pl_jsonResponse
    pLookup = input("Object ID: 7blX5A6W4opf6QHR0HjykD")
    
    #URL    
    pl_url = url+f"/public/core/v3/objects/{pLookup}/permissions"
    pl_response = requests.get(pl_url, headers=headers)
    pl_jsonResponse = pl_response.json()
    print(json.dumps(pl_jsonResponse, indent=4))
    print(functions)

####~~~~~~~~~Lookup Permissions~~~~~~~~~####
def getPermissionCheck ():
    #Variables
    global pcv_jsonResponse
    global pc_dict
    global pcv_output
    global value_output
    global value_output2
    pcv_output = []
    message = "Lookvalues\n\
          MTT = Mapping task\n\
          TASKFLOW\n\
          PROJECT\n\
          FOLDER\n\
          DTEMPLATE = Mapping\n\
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
          VISIOTEMPLATE"
    print(message)
    #Input
    pc_Value = input("Lookup value: ")
    pc_Group = input("Group Name to check permissions: ") #not implemented array.index("value")
    pc_Var = input("Manual Entry (Y/N) ")

    #Manual Entry Path
    if pc_Var.upper() == "Y":
        pc_id = input("Object ID: (Ex: 7h4bge4CzsXkNYpkNDusIh ) ")

        #URL
        pc_url = url+f'/public/core/v3/objects/{pc_id}/permissions'
        pc_response = requests.get(pc_url, headers=headers)
        pc_jsonResponse = pc_response.json()
        pc_value = json.dumps(pc_jsonResponse, indent = 4)

        #Print Value from API
        print(pc_id)
        print(pc_value)
        
        #Print out values to documents
        with open(save_path + "PermissionChecks.json", "w") as outfile:
            outfile.write(pc_value)
        print("Permission Details output to PermissionChecks.json in Documents")
        print(functions)
    
    #Full Lookup or Folder
    elif pc_Var.upper() == "N":
        pc_Qloc = input("Check specific folder (Y/N) ")

        #Specific Location
        if pc_Qloc.upper() == "Y":
            pc_loc = input("Folder location: ")
            
            #Get all objects for pc_Value selection
            pc_url = url+f"/public/core/v3/objects?q=type=={pc_Value} and location=='{pc_loc}'"
            pc_response = requests.get(pc_url, headers=headers)
    
            #Beginning of ID list gathering
            pc_jsonResponse = pc_response.json()
    
            #Setting up lists
            pc_keys = []
            pc_values = []
    
            #Pull all objects of type into list
            for element in pc_jsonResponse['objects']:
                pc_keys.append(element['path'].split('/')[-1])
        
            #Getting IDS
            for element2 in pc_jsonResponse['objects']:
                pc_values.append(element2['id'])
        
            #Combine Object Name and Values
            pc_dict = {}
            pc_dict = dict(map(lambda i,j : (i,j) , pc_keys,pc_values))

            #Write IDs to file
            with open(save_path + "objects.json", "w") as outfile:
                json.dump(pc_dict, outfile, indent = 4)
            print("Objects found output to objects.json in Documents")                

            #Getting Ids
            pc_ids = pc_dict.values()
            value_output = []
            value_output1 = []
            
            #Using Pulled Values to retrieve Permission Check
            for pc_id in pc_ids:
                pcv_url = url+f'/public/core/v3/objects/{pc_id}/permissions'
                pcv_URLresponse = requests.get(pcv_url, headers=headers)
                pcv_jsonResponse = pcv_URLresponse.json()
            #Permission Group Check
                for pcvalue in pcv_jsonResponse:
                    value_output.append(pcvalue['principal']['name'].upper())
                if pc_Group.upper() in value_output:
                    print(f"{pc_id} has the Group")
                    value_output = []
                else:
                    pcv_output.append(pc_id)
                    print(f"{pc_id} does NOT have the Group")
                    value_output = []
                #print(pcv_output)

            #Print out values to documents
            with open(save_path + "PermissionChecks.json", "w") as outfile:
                json.dump(pcv_output, outfile, indent = 4)
            print("Permission Details output to PermissionChecks.json in Documents")
            print(functions)
            
        #Pulling all of pc_Value
        elif pc_Qloc.upper() == "N":            
            #Get all objects for pc_Value selection
            pc_url = url+f"/public/core/v3/objects?q=type=={pc_Value}"
            pc_response = requests.get(pc_url, headers=headers)
    
            #Beginning of ID list gathering
            pc_jsonResponse = pc_response.json()
    
            #Setting up lists
            pc_keys = []
            pc_values = []
    
            #Pull all objects of type into list
            for element in pc_jsonResponse['objects']:
                pc_keys.append(element['path'].split('/')[-1])
        
            #Getting IDS
            for element2 in pc_jsonResponse['objects']:
                pc_values.append(element2['id'])
        
            #Combine Object Name and Values
            pc_dict = {}
            pc_dict = dict(map(lambda i,j : (i,j) , pc_keys,pc_values))

            #Write IDs to file
            with open(save_path + "objects.json", "w") as outfile:
                json.dump(pc_dict, outfile, indent = 4)
            print("Objects found output to objects.json in Documents")                

            #Getting Ids
            pc_ids = pc_dict.values()
            value_output = []
            value_output1 = []
            #Using Pulled Values to retrieve Permission Check
            for pc_id in pc_ids:
                pcv_url = url+f'/public/core/v3/objects/{pc_id}/permissions'
                pcv_URLresponse = requests.get(pcv_url, headers=headers)
                pcv_jsonResponse = pcv_URLresponse.json()

            #Permission Group Check
                for pcvalue in pcv_jsonResponse:
                    value_output.append(pcvalue['principal']['name'].upper())
                if pc_Group.upper() in value_output:
                    print(f"{pc_id} has the Group")
                    value_output = []
                else:
                    pcv_output.append(pc_id)
                    print(f"{pc_id} does NOT have the Group")
                    value_output = []
                #print(pcv_output)

            #Print out values to documents
            with open(save_path + "PermissionChecks.json", "w") as outfile:
                json.dump(pcv_output, outfile, indent = 4)
            print("Permission Details output to PermissionChecks.json in Documents")

        else:
            "Exiting without selection"
            exit()

    elif pc_var.upper() == "EXIT":
        exit()
    else:
        print("Value of 'N' or 'Y' only, 'exit' to exit")
        getPermissionCheck()
    print(functions)

####~~~~~~~~~Creating Permissions~~~~~~~~~####
def createPermission():
    url = 'https://'+pod+'.'+'dm-us.informaticacloud.com/saas'
    
    #Variable for Group
    cp_id = input("Object ID for permissions: ")
    userGroup = input("Group or User permission request? ").upper()
    entity = input(f"{userGroup} for access: ").lower()

    #Access Prompts in Params
    read = input("Access to read permission: (t/f) " )
    if read.upper() == "F":
        read = False
    else:
        read = True
    update = input("Access to update permission: (t/f) ")
    if update.upper() == "F":
        update = False
    else:
        update = True
    delete = input("Access to delete permission: (t/f) ")
    if delete.upper() == "F":
        delete = False
    else:
        delete = True
    execute = input("Access to execute permission: (t/f) ")
    if execute.upper() == "F":
        execute = False
    else:
       execute = True
    change = input("Access to change permission: (t/f) ")
    if change.upper() == "F":
        change = False
    else:
        change = True
    
    #Params
    params = json.dumps({
        "principal" : {
            "type" : f'{userGroup}',
            "name" : f'{entity}'
            },
        "permissions" : {
            "read" : read,
            "update" : update,
            "delete" : delete,
            "execute" : execute,
            "changePermission" : change
            }
        })

    #URL
    cp_url = url+f"/public/core/v3/objects/{cp_id}/permissions"
    cp_response = requests.post(cp_url, data=params, headers=headers)
    cp_jsonResponse = cp_response.json()
    print(json.dumps(cp_jsonResponse, indent=4))
    print(functions)

####~~~~~~~~~Delete All Permissions~~~~~~~~~####
def deletePermissions():    
    #Variables
    global dp_jsonResponse
    dPermissions = input("Object ID: ")
    
    #URL
    dp_url = url+f"/public/core/v3/objects/{dPermissions}/permissions"
    dp_response = requests.get(dp_url, headers=headers)
    dp_jsonResponse = dp_response.json()
    print(json.dumps(dp_jsonResponse, indent=4))
    print(functions)
    
####~~~~~~~~~Get List of Object Persmissions~~~~~~~~~####
def getListPermissions():
    #Load list of Objects
    global pl_values
    global lp_data
    o_list = open(save_path + "objects.json")
    data = json.load(o_list)
    
    #Setting Just IDs
    lp_data = []
    pl_values = []
    for element in data.values():
        pl_values.append(element)
        
    #URL
    for value in pl_values:
        lp_url = url+f"/public/core/v3/objects/{value}/permissions"
        lp_response = requests.get(lp_url, headers=headers)
        if lp_response.json() != []:
            print(lp_response.json())
            lp_data.append(lp_response.json())
        else:
            print(f"No Permissions assigned to {value}")
            continue
    print(functions)

####~~~~~~~~~Mapping Detail~~~~~~~~~####
def getMappingDetails():
    #Getting IDs
    global md_dict
    global md_jsonResponse
    global md_output
    global md_ids
    md_output = []
    md_jsonResponse = []
    md_var = input('Manual Entry (Y/N): ')
    if md_var.upper() == 'N':
        #Getting all Mapping or from Location
        md_listvar = input('Pull all mappings (Y/N): ')
        if md_listvar.upper() == 'N':
            #Mapping from certain location
            md_loc = input('Location: ')
            md_url = url+f"/public/core/v3/objects?q=type=='MTT' and location=='{md_loc}'"
            md_response = requests.get(md_url, headers=headers)
            
            #Beginning of ID list gathering
            md_jsonResponse = md_response.json()
            
            ####Setting up lists
            md_keys = []
            md_values = []
            
            #Pull all objects of type into list
            for element in md_jsonResponse['objects']:
                md_keys.append(element['path'].split('/')[-1])
                
            ####Getting IDS
            for element2 in md_jsonResponse['objects']:
                md_values.append(element2['id'])
                
            ####Combine Object Name and Values
            md_dict = {}
            md_dict = dict(map(lambda i,j : (i,j) , md_keys,md_values))
            
            #Write IDs to file
            with open(save_path + "mapping.json", "w") as outfile:
                json.dump(md_dict, outfile, indent=4)
            print('mapping.json created in Documents folder')
            
            #Writes just values to variable
            md_ids = md_dict.values()
            
            #Getting Values
            for md_id in md_ids:
                md_vvs = {}
                md_url = url+f"/api/v2/mttask/{md_id}"
                md_URLresponse = requests.get(md_url, headers=headersV2)
                md_jsonResponse = md_URLresponse.json()
                
                #Variables
                md_soe = {}
                md_verbose = {}
                md_valid = {}
                try:
                    if int(md_jsonResponse['sessionProperties']['Stop on errors']) > 0:
                        md_soe = {"Stop on Error" : "Enabled"}
                    else:
                        md_soe = {"Stop on Error" : "Not Enabled"}
                except KeyError:
                    md_soe = {"Stop on Error" : "Not Enabled"}
                except ValueError:
                    md_soe = {"Stop on Error" : "Not Enabled"}
                    
                #Checking Verbose
                try:
                    if md_jsonResponse['sessionProperties']['Override tracing'] == "Verbose Data":
                        md_verbose = {"Verbose" : "Enabled"}
                    else:
                        md_verbose = {"Verbose" : "Not Enabled"}
                except KeyError:
                    md_verbose = {"Verbose" : "Not Enabled"}
                    
                #Check Validation
                try:
                    if md_jsonResponse['valid'] == "True":
                        md_valid = {"Valid" : "True"}
                    else:
                        md_valid = {"Valid" : "False"}
                except KeyError:
                    md_valid = {"Valid" : "False"}
                    
                #id
                md_pid = {"id" : f"{md_id}"}
                
                #Combine Values
                md_vvs = md_pid | md_valid | md_verbose | md_soe
                
                #Append  to master testing
                md_output.append(md_vvs)
                print(md_id)
            with open(save_path + "MappingDetails.json", "w") as outfile:
                json.dump(md_output, outfile, indent = 4)
            print("Mapping Details output to MappingDetails.json in Documents")
            print(functions)
            
        #Pull All Mappings
        else:
            md_url = url+"/public/core/v3/objects?q=type=='MTT'"
            md_response = requests.get(md_url, headers=headers)
            
            #Beginning of ID list gathering
            md_jsonResponse = md_response.json()
            
            #Setting up lists
            md_keys = []
            md_values = []
            
            #Pull all objects of type into list
            for element in md_jsonResponse['objects']:
                md_keys.append(element['path'].split('/')[-1])
                
            #Getting IDS
            for element2 in md_jsonResponse['objects']:
                md_values.append(element2['id'])
                
            #Combine Object Name and Values
            md_dict = {}
            md_dict = dict(map(lambda i,j : (i,j) , md_keys,md_values))
            
            #Write IDs to file
            with open(save_path + "mapping.json", "w") as outfile:
                json.dump(md_dict, outfile, indent=4)
            print('mapping.json created in Documents folder')
            
            #Writes just values to variable
            md_ids = md_dict.values()
            
            #Getting Values
            for md_id in md_ids:
                md_vvs = {}
                md_url = url+f"/api/v2/mttask/{md_id}"
                md_URLresponse = requests.get(md_url, headers=headersV2)
                md_jsonResponse = md_URLresponse.json()
                
                #Variables
                md_soe = {}
                md_verbose = {}
                md_valid = {}
                try:
                    if int(md_jsonResponse['sessionProperties']['Stop on errors']) > 0:
                        md_soe = {"Stop on Error" : "Enabled"}
                    else:
                        md_soe = {"Stop on Error" : "Not Enabled"}
                except KeyError:
                    md_soe = {"Stop on Error" : "Not Enabled"}
                except ValueError:
                    md_soe = {"Stop on Error" : "Not Enabled"}
                    
                #Checking Verbose
                try:
                    if md_jsonResponse['sessionProperties']['Override tracing'] == "Verbose Data":
                        md_verbose = {"Verbose" : "Enabled"}
                    else:
                        md_verbose = {"Verbose" : "Not Enabled"}
                except KeyError:
                    md_verbose = {"Verbose" : "Not Enabled"}
                    
                #Check Validation
                try:
                    if md_jsonResponse['valid'] == "True":
                        md_valid = {"Valid" : "True"}
                    else:
                        md_valid = {"Valid" : "False"}
                except KeyError:
                    md_valid = {"Valid" : "False"}
                    
                #id
                md_pid = {"id" : f"{md_id}"}
                
                #Combine Values
                md_vvs = md_pid | md_valid | md_verbose | md_soe
                
                #Append  to master testing
                md_output.append(md_vvs)
                print(md_id)
            with open(save_path + "MappingDetails.json", "w") as outfile:
                json.dump(md_output, outfile, indent = 4)
            print("Mapping Details output to MappingDetails.json in Documents")
            print(functions)
    else:
        #Manual Entry Route
        md_manid = input('ID: 03xpbNE9CPocucEoquCo8o / 0zlHGumDGujfoSaQxZZ6c6 ')
        md_url = url+f"/api/v2/mttask/{md_manid}"
        md_URLresponse = requests.get(md_url, headers=headersV2)
        md_jsonResponse = md_URLresponse.json()
        md_vvs = {}
        
        #Variables
        md_soe = {}
        md_verbose = {}
        md_valid = {}
        try:
            if int(md_jsonResponse['sessionProperties']['Stop on errors']) > 0:
                md_soe = {"Stop on Error" : "Enabled"}
            else:
                md_soe = {"Stop on Error" : "Not Enabled"}
        except KeyError:
            md_soe = {"Stop on Error" : "Not Enabled"}
        except ValueError:
            md_soe = {"Stop on Error" : "Not Enabled"}
                
        #Checking Verbose
        try:
            if md_jsonResponse['sessionProperties']['Override tracing'] == "Verbose Data":
                md_verbose = {"Verbose" : "Enabled"}
            else:
                md_verbose = {"Verbose" : "Not Enabled"}
        except KeyError:
            md_verbose = {"Verbose" : "Not Enabled"}
            
        #Check Validation
        try:
            if md_jsonResponse['valid'] == "True":
                md_valid = {"Valid" : "True"}
            else:
                md_valid = {"Valid" : "False"}
        except KeyError:
            md_valid = {"Valid" : "False"}
            
        #id
        md_pid = {"id" : f"{md_manid}"}
        
        #Combine Values
        md_vvs = md_pid | md_valid | md_verbose | md_soe
        
        #Append  to master testing
        md_output.append(md_vvs)
        print(md_manid)
        with open(save_path + "MappingDetails.json", "w") as outfile:
            json.dump(md_output, outfile, indent = 4)
        print("Mapping Details output to MappingDetails.json in Documents")
        print(functions)
