###ToDo List###
#Add in additional drop down values
#Add Calendar Picker function
#Decide on output function for file
#Additional data validation on Int Values / Reuire Fields

import tkinter as tk
from tkinter import *
import tkcalendar as ttk
from tkcalendar import *

#Drop Down Values
Consultants = [
"Consultant 1",
"Consultant 2",
"Consultant 3"
]

##ToDo add RNs
RNs = [
  "RN 1",
  "RN 2"
  "RN 3"
  ]

ApproveDeny = [
  "Approve",
  "Deny",
  "Pulled from Queue",
  "Split/Deny"
  "Void",
  "Withdrawal"
  ]

Locations = [
  "AZ",
  "CA",
  "CT",
  "NM",
  "NV",
  "UT",
  "WA"
  ]

def save_info():
  patient_info = patient.get()
  location_info = location.get()
  cdo_info = cdo.get()
  clin_consultant_info = clin_consultant.get()
  rn_sent_info = rn_sent.get()
  dos_info = dos.cget("text")
  prior_auth_info = prior_auth.get()
  approve_deny_info = approve_deny.get()
  codes_info = codes.get()
  cost_info = str(cost.get())
  mdr_decision_info = mdr_decision.get()
  savings_info = str(savings.get())
  entered_date_info = entered_date.get()
  
  #print(patient_info, location_info, cdo_info, clin_consultant_info,
  #      rn_sent_info, dos_info, prior_auth_info, approve_deny_info,
  #      codes_info, cost_info, mdr_decision_info, savings_info,
  #      entered_date_info
  #      )
 
  file = open("cdo_date.txt", "a+")
  file.write(patient_info+",")
  file.write(location_info+",")
  file.write(cdo_info+",")
  file.write(clin_consultant_info+",")
  file.write(rn_sent_info+",")
  file.write(dos_info+",")
  file.write(prior_auth_info+",")
  file.write(approve_deny_info+",")
  file.write(codes_info+",")
  file.write(cost_info+",")
  file.write(mdr_decision_info+",")
  file.write(savings_info+",")
  file.write(entered_date_info+"\n")
  file.close()
  print(" User ", patient_info, " has been registered successfully")
 
  patient_entry.delete(0, END)
  cdo_entry.delete(0, END)
  prior_auth_entry.delete(0, END)
  codes_entry.delete(0, END)
  cost_entry.delete(0, END)
  mdr_decision_entry.delete(0, END)
  savings_entry.delete(0, END)
  entered_date_entry.delete(0, END)
  
#ToDo Calendar Picker
def grabdate():
    def print_sel():
        dos.config(text=cal.get_date())
        top.destroy()
    top = tk.Toplevel(screen)

    Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(fill = 'both', padx=20, pady=20)
    Button(top, text="ok", command = print_sel, bg = 'pale green').pack(padx=10, pady=10)

#Program Display Deminsions
screen = Tk()
screen.geometry("500x900")
screen.title("SME Form")
#heading = Label(text = "SME Form", bg = "grey", fg = "black", width = "500", height = "3")
#heading.pack()


#Fields
patient_text = Label(text = "Patient Name * ",)
location_text = Label(text = "Loaction * ",)
cdo_text = Label(text = "Care Delivery Organization * ",)
clin_consultant_text = Label(text = "Clinical Consultant * ",)
rn_sent_text = Label(text = "RN Sent * ",)
dos_text = Label(text = "Date Of Service * ",)
prior_auth_text = Label(text = "Prior Authorization * ",)
approve_deny_text = Label(text = "Approval / Denial * ",)
codes_text = Label(text = "Codes * ",)
cost_text = Label(text = "Cost * ",)
mdr_decision_text = Label(text = "MDR Decision * ",)
savings_text = Label(text = "Savings * ",)
entered_date_text = Label(text = "Entered Date * ",)


#Text Field Placements
patient_text.place(x = 15, y = 15)
location_text.place(x = 15, y = 70)
cdo_text.place(x = 15, y = 125)
clin_consultant_text.place(x = 15, y = 180)
rn_sent_text.place(x = 15, y = 230)
dos_text.place(x = 15, y = 285)
prior_auth_text.place(x = 15, y = 335)
approve_deny_text.place(x = 15, y = 390)
codes_text.place(x = 15, y = 445)
cost_text.place(x = 15, y = 500)
mdr_decision_text.place(x = 15, y = 555)
savings_text.place(x = 15, y = 610)
entered_date_text.place(x = 15, y = 665)

#Declare Data Types
patient = StringVar()
location = StringVar()
location.set(Locations[0])
cdo = StringVar()
clin_consultant = StringVar()
clin_consultant.set(Consultants[0])
rn_sent = StringVar()
rn_sent.set(RNs[0])
dos = Label(screen, text = str(""))
prior_auth = StringVar()
approve_deny = StringVar()
approve_deny.set(ApproveDeny[0])
codes = StringVar()
cost = DoubleVar()
mdr_decision = StringVar()
savings = DoubleVar()
entered_date = StringVar()

#Text Variables
patient_entry = Entry(textvariable = patient, width = "30")
location_entry = OptionMenu(screen, location, *Locations)
cdo_entry = Entry(textvariable = cdo, width = "30")
clin_consultant_entry = OptionMenu(screen, clin_consultant, *Consultants)
rn_sent_entry = OptionMenu(screen, rn_sent, *RNs)
prior_auth_entry = Entry(textvariable = prior_auth, width = "30")
approve_deny_entry = OptionMenu(screen, approve_deny, *ApproveDeny)
codes_entry = Entry(textvariable = codes, width = "30")
cost_entry = Entry(textvariable = cost, width = "30")
mdr_decision_entry = Entry(textvariable = mdr_decision, width = "30")
savings_entry = Entry(textvariable = savings, width = "30")
entered_date_entry = Entry(textvariable = entered_date, width = "30")

#Text Box Placement
patient_entry.place(x = 15, y = 35)
location_entry.place(x = 15, y = 90)
cdo_entry.place(x = 15, y = 145)
clin_consultant_entry.place (x = 15, y = 200)
rn_sent_entry.place (x = 15, y = 250)
dos.place (x = 15, y = 305)
prior_auth_entry.place (x = 15, y = 360)
approve_deny_entry.place (x = 15, y = 415)
codes_entry.place (x = 15, y = 470)
cost_entry.place (x = 15, y = 525)
mdr_decision_entry.place (x = 15, y = 580)
savings_entry.place (x = 15, y = 635)
entered_date_entry.place (x = 15, y = 690)

#Button Info
register = Button(screen,text = "Register", width = "30", height = "2", command = save_info, bg = "coral")
register.place(x = 15, y = 740)

end = Button(screen,text = "End", width = "30", height = "2", command = screen.destroy, bg = "lightblue")
end.place(x = 15, y = 790)

cal = Button(screen,text = "Calendar Selection", width = "15", height = "1", command = grabdate, bg = "lightblue")
cal.place(x = 230, y = 303)

screen.mainloop()
