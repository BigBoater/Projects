import tkinter as tk

def show_selected():
    selected_value = var.get()
    print("Selected value:", selected_value)

root = tk.Tk()

var = tk.StringVar()

radio_button1 = tk.Radiobutton(root, text="Option 1", variable=var, value="Option 1")
radio_button2 = tk.Radiobutton(root, text="Option 2", variable=var, value="Option 2")
radio_button3 = tk.Radiobutton(root, text="Option 3", variable=var, value="Option 3")

var.set("Option 1")  # Set a default selection

button = tk.Button(root, text="Show Selected", command=show_selected)

radio_button1.pack()
radio_button2.pack()
radio_button3.pack()
button.pack()
