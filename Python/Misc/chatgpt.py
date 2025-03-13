import psycopg2
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def get_schema():
    cursor.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = cursor.fetchall()

    schema_list.delete(0, tk.END)  # Clear the listbox

    for schema in schemas:
        schema_list.insert(tk.END, schema[0])

def get_table():
    selected_schema = schema_list.get(tk.ACTIVE)
    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{selected_schema}' ORDER BY 1;")
    tables = cursor.fetchall()

    table_list.delete(0, tk.END)  # Clear the listbox

    for table in tables:
        table_list.insert(tk.END, table[0])

def get_source_columns():
    selected_table = table_list.get(tk.ACTIVE)
    if selected_table:
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}' ORDER BY ordinal_position;")
        columns = cursor.fetchall()

        # Clear previous options
        source_column_menu['menu'].delete(0, 'end')
        
        for column in columns:
            source_column_menu['menu'].add_command(label=column[0], command=lambda col=column[0]: source_column_var.set(col))

def get_dest_columns():
    global dest_df
    dest_df = pd.DataFrame(columns=["Column_1", "Column_2", "Column_3", "Column_4", "Column_5"])

    # Get the column names from the destination DataFrame
    columns = dest_df.columns.tolist()

    # Clear previous options
    dest_column_menu['menu'].delete(0, 'end')

    for column in columns:
        dest_column_menu['menu'].add_command(label=column, command=lambda col=column: dest_column_var.set(col))

def get_query():
    selected_schema = schema_list.get(tk.ACTIVE)
    selected_table = table_list.get(tk.ACTIVE)
    query = f"SELECT * FROM \"{selected_schema}\".\"{selected_table}\""

    try:
        cursor.execute(query)
        query_results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data=query_results, columns=column_names)
        return df
    except psycopg2.ProgrammingError:
        database_connection.rollback()
        messagebox.showerror("Error", "Invalid Query")

def migrate_data():
    source_df = get_query()
    dest_table = table_list.get(tk.ACTIVE)
    
    # Get the selected source column
    selected_source_column = source_column_var.get()
    
    # Get the selected destination column
    selected_dest_column = dest_column_var.get()

    if not source_df.empty and dest_table and selected_source_column and selected_dest_column:
        try:
            # Write data to the destination table
            source_df[[selected_source_column]].to_sql(dest_table, con=database_connection, if_exists='replace', index=False, schema=selected_schema)
            messagebox.showinfo("Success", "Data migrated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please select a source table, and both a source and destination column.")

        
def exit_app():
    root.destroy()

# GUI Setup
var = None
root = tk.Tk()
root.title("Database Migration Tool")

# Database Connection
db_username = "postgres"
db_password = "admin"
db_host = "localhost"
db_port = "5432"
database_name = "postgres"
database_connection = psycopg2.connect(database=database_name, user=db_username, password=db_password, host=db_host, port=db_port)
cursor = database_connection.cursor()

# Widgets
schema_frame = tk.Frame(root)
schema_label = tk.Label(schema_frame, text="Select Schema:")
schema_list = tk.Listbox(schema_frame)
schema_scroll = tk.Scrollbar(schema_frame, orient=tk.VERTICAL, command=schema_list.yview)
schema_list.config(yscrollcommand=schema_scroll.set)
get_schema_button = tk.Button(schema_frame, text="Get Schemas", command=get_schema)

table_frame = tk.Frame(root)
table_label = tk.Label(table_frame, text="Select Table:")
table_list = tk.Listbox(table_frame)
table_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table_list.yview)
table_list.config(yscrollcommand=table_scroll.set)
get_table_button = tk.Button(table_frame, text="Get Tables", command=get_table)

source_column_frame = tk.Frame(root)
source_column_label = tk.Label(source_column_frame, text="Select Source Column:")
source_column_var = tk.StringVar()
source_column_menu = tk.OptionMenu(source_column_frame, source_column_var, "")
get_source_columns_button = tk.Button(source_column_frame, text="Get Source Columns", command=get_source_columns)

dest_column_frame = tk.Frame(root)
dest_column_label = tk.Label(dest_column_frame, text="Select Destination Column:")
dest_column_var = tk.StringVar()
dest_column_menu = tk.OptionMenu(dest_column_frame, dest_column_var, "")
get_dest_columns_button = tk.Button(dest_column_frame, text="Get Destination Columns", command=get_dest_columns)

map_button = tk.Button(root, text="Map Columns", command=get_source_columns)
migrate_button = tk.Button(root, text="Migrate Data", command=migrate_data)
exit_button = tk.Button(root, text="Exit", command=exit_app)

# Layout
schema_frame.grid(row=0, column=0, padx=10, pady=10)
schema_label.grid(row=0, column=0, sticky="w")
schema_list.grid(row=1, column=0, sticky="nsew")
schema_scroll.grid(row=1, column=1, sticky="ns")
get_schema_button.grid(row=2, column=0, pady=(5, 0))

table_frame.grid(row=0, column=1, padx=10, pady=10)
table_label.grid(row=0, column=0, sticky="w")
table_list.grid(row=1, column=0, sticky="nsew")
table_scroll.grid(row=1, column=1, sticky="ns")
get_table_button.grid(row=2, column=0, pady=(5, 0))

source_column_frame.grid(row=0, column=2, padx=10, pady=10)
source_column_label.grid(row=0, column=0, sticky="w")
source_column_menu.grid(row=1, column=0, columnspan=2, pady=(5, 0))
get_source_columns_button.grid(row=2, column=0, columnspan=2, pady=(5, 0))

dest_column_frame.grid(row=0, column=3, padx=10, pady=10)
dest_column_label.grid(row=0, column=0, sticky="w")
dest_column_menu.grid(row=1, column=0, columnspan=2, pady=(5, 0))
get_dest_columns_button.grid(row=2, column=0, columnspan=2, pady=(5, 0))

map_button.grid(row=1, column=2, pady=(5, 0))
migrate_button.grid(row=1, column=3, pady=(5, 0))
exit_button.grid(row=2, column=0, columnspan=4, pady=(5, 0))

root.mainloop()
