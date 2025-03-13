import psycopg2 #library for Postgres
import pandas as pd #library for all the dataframe stuff
import sys #used to break the function with stronger error handling
import time #used for sleep functions. Bandaid to call out errors
import tkinter as tk #user interface
from tkinter import messagebox

'''

Project Notes:
LookUps: TODO, USER INTERACTION

Current State:
Working functions: map_column, select_column, query, get_schema, get_tables, get_query, start_query
0.) start_query: is the rough draft of this program
1.) map_column: uses select_column function to prompt the user to select two columns and move the data over
2.) select_column: is used by map_column and is the function the users to select the column
3.) query: executes the query the user has provided or been prompted to provide to return the data from the chosen table to a dataframe
4.) get_schema: will prompt the user to select from a list of schemas to choose from to aid in making a query
5.) get_table: will prompt the user to select from a list of tables to choose from to aid in making a query
6.) get_query: is a free field where a savy user can by pass get_tables/get_schema to supply their own query

Future State:
Create a way to merge two columns together
Create a way to add in functions to a column
???Data Cleanup or just SALSIFY it?
Implement via and actual user interface (tkinter? or something Web? Django?)
Draw more attention to errors (pop ups?)

Critical Bugs:
Make a catch for worng y/n input - works.... but dropping the query_results and fatally crashing the application    

Minor Bugs:
Make a catch to pick up wrong selection for schema
Make a catch to pick up wrong selection for table


'''

'''
TODO: Feed the exit straight to the tables function
Catches for non-schemas
'''

##Program Skeleton

def get_schema(cursor):
    global query
    #A script to allow the user to select the schema where the table migration is #User Interaction
    cursor.execute("select schema_name from information_schema.schemata;")
    schemas = cursor.fetchall()
    
    #Provides a list of avaliable schemas
    print("Avaliable Schemas: \n")
    for schema in schemas:
        listbox.insert(tk.END, schmea)
        print(*schema)

    sschema = input("\nPlease select a schema: ")

    getTable = input("Get table? (y/n) :")
    
    if getTable.upper() == "Y":
        schema = sschema
        query = get_table(cursor, schema)
    elif getTable.upper() == "N":
        pass
    else:
        print("\nNO PROPER SELECTION MADE!\n")
        time.sleep(10)
        get_schema(cursor)
    #Passes back to root script on exit with selected schema
    return query


'''
TODO:Feed the exit straight to the map columns function
Get more catches for non-valid tables
Incorporated to tkinter.... or at least trying too
'''
def get_table(cursor, schema):
    global query
    #A script to allow the user to select the table that is to be migrated #User Interaction
    if schema == None:
        cursor.execute("select table_name from information_schema.tables order by 1;")
    else:
        try:
            cursor.execute(f"select table_name from information_schema.tables where table_schema = '{schema}' order by 1;")
        except psycopg2.ProgrammingError:
            database_connection.rollback()
            print("Bad Query")
            #get_table(cursor, schema)
            print(schema)
        
    tables = cursor.fetchall()

    #Provides a list of tables
    print("Avaliable Tables: \n")
    for table in tables:
        print(*table)
    stable = input("\nPlease select a table: ")
    query = f"select * from {schema}.{stable}"
    #Passes back to root script on exit with selected table
    return query
    

'''
TODO switch this out for an automated process using the Schema and Table selected functions
Catch for bad queries
'''
def get_query(cursor, query):
    #A script to return query results
    try:
        cursor.execute(query)
        query_results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data = query_results, columns = column_names)
        return df
    #Needed for rollback or table will lock up!!!
    except psycopg2.ProgrammingError:
        database_connection.rollback()
        return print("Bad Query")
        time.sleep(10)

def select_column(df, tries, column_count):
    #A script to prompt the user to select columns to be migrated
    #This script relies on the map_column function!!!
    print("Columns in DataFrame: ")
    #Max invalid entries before the program falls over
    max_tries = 3
    while tries <= max_tries:
        #The Fall over
        if tries == max_tries:
            sys.exit("\nToo many wrong attempts exiting. \n")
            time.sleep(10)
        else:
            #Enumerate the columns for selection
            for idx, col in enumerate(df.columns):
                print(f"{idx + 1}. {col}")
            message = "Enter the number of the column in the destination DataFrame to map: "    
            selection = input(message)
            #User Selection #User Interaction
            try:
                idx = int(selection) - 1
                if 0 <= idx < len(df.columns):
                    return df.columns[idx]
                else:
                    print("\nInvalid selection. Please enter a number within the range.\n")
                    time.sleep(10)
                    tries += 1
                    return select_column(df, tries, column_count)
            except ValueError:
                    print("\nInvalid input. Please enter a number!\n")
                    time.sleep(10)
                    tries += 1
                    return select_column(df, tries, column_count)

#TODO: currently the script only selects one column migrates and exits. Need to enumerate through all values user wants
def map_column(source_df, dest_df, tries, column_count):
    #Selecting a Source Column(s)
    dest_column_name = select_column(dest_df, tries, column_count)
    #Selecting a Destination Column(s)
    source_column_name = select_column(source_df, tries, column_count)
    #Actual Mapping piece
    if source_column_name in source_df.columns:
        if dest_column_name in dest_df.columns:
            dest_df[dest_column_name] = source_df[source_column_name]
            print(column_count)
        else:
            print(f"\nWarning: Destination column '{dest_column_name}' not found in the destination DataFrame.\n")
            time.sleep(10)
    else:
        print("Flag Error")
    return dest_df

def start_query(cursor):
    global query
    global dest_df
    global column_count
    #These standard columns should be replaced with the actual model tables when after developed...... tester values only
    #TODO: These parameters are critical for the map_column and select_column to run, but should be replaced with something more standard
    stand_columns = ["Column_1", "Column_2", "Column_3", "Column_4", "Column_5"]
    dest_df = pd.DataFrame(data= None, columns = stand_columns)
    column_count = 0
    uprompt = input("Free form a query? (y/n) ")

    if uprompt.upper() == "Y":
        query = input("Query: ")
        query_results = get_query(cursor, query)
        print(query_results)
    elif uprompt.upper() == "N":
        get_schema(cursor)
        query_results = get_query(cursor, query)
    else:
        print("\nNO PROPER SELECTION MADE!\n")
        time.sleep(10)
        start_query(cursor)
        
    source_df = query_results

    #Column Count to run the map_column for each column in the Destination table, because Destnation columns count won't change
    while column_count < len(dest_df.columns):
        column_count += 1
        map_column(source_df, dest_df, tries, column_count)
    return dest_df

##Tkinter functions
def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def on_select(event):
    global schema_value
    # Get the index of the selected item
    index = listbox.curselection()[0]
    # Get the value of the selected item
    schema_value = listbox.get(index)
    # Display the selected value
    #selected_value_label.config(text="Selected Value: " + schema_value) #testing not really needed to be shown
    print(schema_value)
    return schema_value
        

#Schema Window Option
def schmea_window():
    global schema_value
    global query
    global listbox
    # Create a new window
    schema_window = tk.Toplevel(root)
    schema_window.title("Schema Information")

    # Add content to the new window
    user_input_label = tk.Label(schema_window, text= "Please select a schema: \n") #Label
    user_input_label.pack(padx=1, pady=1) 
    listbox = tk.Listbox(schema_window, width=30, height=10) #List Value
    listbox.pack(padx=20, pady=20)

    #A script to allow the user to select the schema where the table migration is #User Interaction
    cursor.execute("select schema_name from information_schema.schemata;")
    schemas = cursor.fetchall()

    #Schema Selection Passes to Window Table Upon Selection
    def table_window(cursor, schema):
        global query
        global schema_value
        
        # Create a new window
        table_window = tk.Toplevel(root)
        table_window.title("Table Information")

        # Add content to the new window
        user_input_label = tk.Label(table_window, text= "Please select a table: \n") #Label
        user_input_label.pack(padx=1, pady=1) 
        listbox = tk.Listbox(table_window, width=30, height=10) #List Value
        listbox.pack(padx=20, pady=20)
    
        #A script to allow the user to select the table that is to be migrated #User Interaction
        try:
            cursor.execute(f"select table_name from information_schema.tables where table_schema = '{schema_value}' order by 1;")
        except psycopg2.ProgrammingError:
            database_connection.rollback()
            messagebox.showerror(title="Error!", message="Fatal Error with Schema", command= table_window.destroy())
        
        tables = cursor.fetchall()

        #Provides a list of avaliable tables
        for table in tables:
            listbox.insert(tk.END, *table)

        #Value on user select    
        listbox.bind("<<ListboxSelect>>", on_select)

        # Label to display the selected value
        selected_value_label = tk.Label(table_window, text="Selected Value: ")
        selected_value_label.pack(pady=10)

        #Schema Select Button
        table_select_button = tk.Button(table_window, text="Select?", command=lambda:[get_query(cursor, schema),table_widow.destroy()])
        table_select_button.pack(padx=20, pady=10) #Exit

        #Exit Button
        schema_exit_button = tk.Button(table_window, text="Exit", command=exit_program)
        schema_exit_button.pack(padx=20, pady=10) #Exit    
        #####
        stable = input("\nPlease select a table: ")
        query = f"select * from {schema}.{stable}"
        #Passes back to root script on exit with selected table
        return query

    #Provides a list of avaliable schemas
    for schema in schemas:
        listbox.insert(tk.END, *schema)

    #Value on user select    
    listbox.bind("<<ListboxSelect>>", on_select)
    
    # Label to display the selected value
    selected_value_label = tk.Label(schema_window, text="Selected Value: ")
    selected_value_label.pack(pady=10)

    #Schema Select Button
    schema_select_button = tk.Button(schema_window, text="Select?", command=lambda:table_window(cursor, schema_value))
    schema_select_button.pack(padx=20, pady=10) #Exit

    #Exit Button
    schema_exit_button = tk.Button(schema_window, text="Exit", command=exit_program)
    schema_exit_button.pack(padx=20, pady=10) #Exit

#Free Form Query Window Option
def freeQuery_window():
    # Create a new window
    freeQuery_window = tk.Toplevel(root)
    freeQuery_window.title("Free Form Query")

    # Add content to the new window
    label = tk.Label(freeQuery_window, text="This is a new window!")
    label.pack(padx=20, pady=20)
    
# Init
if __name__ == "__main__":
    #Only used as a exit in functions
    tries = 0
    
    #User Dependent Parameters
    #TODO: switch these back to user prompted and not hardcoded
    db_username = "postgres" #input("Username: ")
    db_password = "admin" #input("Password: ")
    db_host = "localhost" #input ("Host: ")
    db_port = "5432" #input("Port: ")
    database_name = "postgres" #input("Database Name: ")

    #Build Database URL from Param and connect
    database_connection = psycopg2.connect(database=database_name, user=db_username, password=db_password, host=db_host, port=db_port)
    cursor = database_connection.cursor()

    print("Working functions: \n get_schema\n get_table\n get_query\n select_column\n map_column\n start_query\n")

#User Interface
    # Create the main tkinter window
    root = tk.Tk()
    root.title("Initial Module")
    # Create a frame to hold the variable list

    # Create a button to run function 1
    button1 = tk.Button(root, text="Get Schema", command=schmea_window)
    button1.pack(padx=20, pady=10)

    # Create a button to run function 2
    button2 = tk.Button(root, text="Free Form Query", command=freeQuery_window)
    button2.pack(padx=20, pady=10)

    # Create a button to exit the program
    exit_button = tk.Button(root, text="Exit", command=exit_program)
    exit_button.pack(padx=20, pady=10)


    # Start the tkinter event loop
    #root.mainloop()
