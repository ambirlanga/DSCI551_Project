#!/usr/bin/env python
# coding: utf-8

# CREDITS
# Created by: Ariel Martinez (1-330), (370-555)
# Mention to: Kenneth (330-370) 

# Lines (330-370) correspond to PART of the VISUAL widgets of the inital Admin window, no actual implementation with Database is done in these lines.

import tkinter as tk
from tkinter import ttk
from Manager import *
from tkinter import messagebox
import sv_ttk
import requests
import sys
import webbrowser
import json

#Creates Table for the UI to show
def table(dics,t):
    vals = []
    for dic in dics:
        for k, v in dic.items():   
            dic = {}
            dic["ID"] = k
            dic["Name"] = v["Name"]
            dic["Location"] = v["Location"]
            dic["Type"] = v["Type of food"]
            dic["Stars"] = v["Score"]["Stars"]
            dic["Likes"] = v["Score"]["Likes"]
            dic["Dislikes"] = v["Score"]["Dislikes"]
            dic["NumScores"] = v["Score"]["Num of score"]
            vals.append(dic)
    t.delete(*t.get_children())
    for row in vals:
        t.insert("", "end", values=(row["ID"], row["Name"], row["Location"], row["Type"], row["Stars"], row["Likes"], row["Dislikes"], row["NumScores"]))

#Loads data for the ShowAll database option
def update_table(t): 
    urls = ["https://asi1-99476-default-rtdb.firebaseio.com/restaurants.json", "https://asi1b-5445c-default-rtdb.firebaseio.com/restaurants.json"]
    lis = []
    for url in urls:
        test = requests.get(url).json()
        lis.append(test)
    table(lis,t)

#Filters data by key value and action (equalTo/startAt/endAt)
def filter_table(r,t): 
    filter = tk.Toplevel(r)

    titStr= "Select filter"
    filter.title(titStr)
    filter.iconbitmap("5235253.ico")

    filter.geometry("300x350")
    r.eval(f'tk::PlaceWindow {str(filter)} center')
    filter.resizable(False, False)

    #Widgets
    labelNew = ttk.Label(filter,text="New Restaurant", justify='center',font='Helvetica 12 bold')
    labelNew.pack(pady=(15,0))

    fil = ttk.Combobox(filter, state="readonly", values=["Name", "Location", "Type of food", "Stars", "Likes", "Dislikes", "Num of score"])
    fil.current(0)
    fil.pack(padx=5, pady=10)

    equal = ttk.Label(filter,text="equalTo (Disables startAt/endAt):")
    equal.pack(fill=tk.X, padx=5, pady=10)
    equal = tk.Entry(filter,width=45)
    equal.pack()

    start = ttk.Label(filter,text="startAt:")
    start.pack(fill=tk.X, padx=5, pady=(25,5))
    start = tk.Entry(filter,width=45)
    start.pack()

    end = ttk.Label(filter,text="endAt:")
    end.pack(fill=tk.X, padx=5, pady=(25,5))
    end = tk.Entry(filter,width=45)
    end.pack()

    #first = ttk.Label(filter,text="limitToFirst ('-' for LimitToLast):")
    #first.pack(fill=tk.X, padx=5, pady=(25,5))
    #first = tk.Entry(filter,width=45)
    #first.pack()

    buttons = ttk.Frame(filter)
    buttons.pack(pady =(25,0))
    button1= tk.Button(buttons, text= "Filter Current Selection", height=1, justify='center')
    button1.pack(side = "left")
    button2= tk.Button(buttons, text= "Filter Database",  height=1, justify='center')
    button2.pack()

    #Gets necesary instances from firebase
    def full_click(event):
        fil2= fil.get()
        if fil2 in ["Location", "Name", "Type of food"]:
            s = ".json?orderBy=" + f'"{fil2}"'
        else:
            s = ".json?orderBy=" + '"Score/' +f'{fil2}"'
        eq = equal.get()
        if eq == "":
            if start.get() != "":
                if fil2 in ["Location", "Name", "Type of food"]:
                    s+= "&startAt=" + f'"{start.get()}"'
                else:
                    s+= "&startAt=" + start.get()
            if end.get() != "":
                if fil2 in ["Location", "Name", "Type of food"]:
                    s+= "&endAt=" + f'"{end.get()}"'
                else:
                    s+= "&endAt=" + end.get()
        else:
            if fil2 in ["Location", "Name", "Type of food"]:
                s+= "&equalTo=" + f'"{eq}"'
            else:
                s+= "&equalTo=" + eq
        #lm = first.get()
        #if lm == "":
        if fil.get() == 'Name' and eq != "":
            res, ans = filter_restaurant(True,eq,s)
        else:
            res, ans = filter_restaurant(False,None,s)

        if ans == 200:
            table(res,t)
        else:
            messagebox.showerror('Data Error', 'Invalid values where used')

    #Filters the data CURRENTLY showing in the UI, it does NOT interact with firebase
    def current_click(event):
        fil2= fil.get()
        ind = ["ID", "Name", "Location", "Type of food", "Stars", "Likes", "Dislikes", "Num of score"].index(fil2)
        eq = equal.get()
        if eq != "":
            if fil2 not in ["Location", "Name", "Type of food"]:
                if eq == '': eq = 0
                eq = float(eq)
            for row in t.get_children():
                item = t.item(row)['values'][ind]
                if fil2 == "Stars": item = float(item)
                if item != eq:
                    t.delete(row)
        elif end.get != '' or start.get() != '':
            st = start.get()
            en = end.get()
            if fil2 not in ["Location", "Name", "Type of food"]:
                if en == '': en =float('inf')
                if st == '': en =float('-inf')
                en = float(en)
                st = float(st)
            for row in t.get_children():
                item = t.item(row)['values'][ind]
                if fil2 == "Stars": item = float(item)
                if en == '':
                    if item < st:
                        t.delete(row)
                elif st == '':
                    if item > en:
                        t.delete(row)
                else:
                    if item < st or item > en:
                        t.delete(row)

    #Bindings
    button2.bind("<Button-1>", full_click)
    button1.bind("<Button-1>", current_click)


#Creates new instance
def create_record(r, t):

    create = tk.Toplevel(r)

    titStr= "Create New"
    create.title(titStr)
    create.iconbitmap("5235253.ico")

    create.geometry("300x350")
    r.eval(f'tk::PlaceWindow {str(create)} center')
    create.resizable(False, False)

    #Widgets
    labelNew = ttk.Label(create,text="New Restaurant", justify='center',font='Helvetica 12 bold')
    labelNew.pack(pady=(15,0))

    labelName = ttk.Label(create,text="Name:")
    labelName.pack(fill=tk.X, padx=5, pady=10)
    labelName = tk.Entry(create,width=45)
    labelName.pack()

    labelLoc = ttk.Label(create,text="Location:")
    labelLoc.pack(fill=tk.X, padx=5, pady=(25,5))
    labelLoc = tk.Entry(create,width=45)
    labelLoc.pack()

    labelType = ttk.Label(create,text="Type of food:")
    labelType.pack(fill=tk.X, padx=5, pady=(25,5))
    labelType = tk.Entry(create,width=45)
    labelType.pack()

    buttonA = tk.Button(create, text="Accept",height=1, width = 15)
    buttonA.pack(padx=5, pady=(40,0))

    #Post in firebase + update UI WITHOUT using GET
    def handle_click(event):
        res, ide = add_restaurant(labelName.get(), labelType.get(), labelLoc.get())
        if res == 200:
            t.insert("", "end", values=(ide, labelName.get(), labelLoc.get(), labelType.get(), 0.0, 0, 0, 0))
        create.destroy()

    #Bindings
    buttonA.bind("<Button-1>", handle_click)


#Modifies an instance
def modify_record(r, t, jval):

    modify = tk.Toplevel(r)

    titStr= "Modify ID: " + str(jval[0])
    modify.title(titStr)
    modify.iconbitmap("5235253.ico")

    modify.geometry("300x350")
    r.eval(f'tk::PlaceWindow {str(modify)} center')
    modify.resizable(False, False)

    #Widgets
    labelNew = ttk.Label(modify,text="Modify Current Values", justify='center',font='Helvetica 12 bold')
    labelNew.pack(pady=(15,0))

    labelName = ttk.Label(modify,text=f"Name: \n(Current: {jval[1]})")
    labelName.pack(fill=tk.X, padx=5, pady=10)
    labelName = tk.Entry(modify,width=45)
    labelName.pack()

    labelLoc = ttk.Label(modify,text=f"Location: \n(Current: {jval[2]})")
    labelLoc.pack(fill=tk.X, padx=5, pady=(25,5))
    labelLoc = tk.Entry(modify,width=45)
    labelLoc.pack()

    labelType = ttk.Label(modify,text=f"Type of food: \n(Current: {jval[3]})")
    labelType.pack(fill=tk.X, padx=5, pady=(25,5))
    labelType = tk.Entry(modify,width=45)
    labelType.pack()

    buttonA = tk.Button(modify, text="Accept",height=1, width = 15)
    buttonA.pack(padx=5, pady=(40,0))

    #Patch (or DELETE/POST if new hash) in firebase + update UI WITHOUT using GET
    def handle_click(event):
        ln = labelName.get()
        if ln == "":
            ln = jval[1]
        lt = labelType.get()
        if lt == "":
            lt = jval[3]
        ll = labelLoc.get()
        if ll == "":
            ll = jval[2]
        res, ide = modify_restaurant(jval[0], ln, lt, ll, jval[1], jval[4], jval[5], jval[6], jval[7])
        if res == 200:
            for row in t.get_children():
                item = t.item(row)['values'][0]
                if item == jval[0]:
                    t.delete(row)
            t.insert("", "end", values=(ide, ln, ll, lt, jval[4], jval[5], jval[6], jval[7]))
        modify.destroy()

    #Bindings
    buttonA.bind("<Button-1>", handle_click)


# Delete existing record
def delete_record(r, t, jval):
    delete = tk.Toplevel(r)

    titStr= "Delete ID: " + str(jval[0])
    delete.title(titStr)
    delete.iconbitmap("5235253.ico")

    delete.geometry("400x200")
    r.eval(f'tk::PlaceWindow {str(delete)} center')
    delete.resizable(False, False)

    labelNew = ttk.Label(delete,text="Are you sure you want to delete:", justify='center',font='Helvetica 12 bold')
    labelNew.pack(pady=(15,0))

    labelName = ttk.Label(delete,text=f"{jval[0]})", justify='center')
    labelName.pack(pady=(15,0))



    button_border = tk.Frame(delete, highlightbackground = "blue",  
                         highlightthickness = 2, bd=0) 


    buttonA = tk.Button(button_border, text="Yes",height=1, width = 15)
    buttonA.pack()
    button_border.pack(side="left", padx=(50,0), pady=(40,0))

    buttonB = tk.Button(delete, text="No",height=1, width = 15)
    buttonB.pack(side="right", padx=(0,50), pady=(40,0))


    # Regret
    def handle_no(event):
        delete.destroy()

    # DELETE in firebase + update UI WITHOUT using GET
    def handle_yes(event):
        res = delete_restaurant(jval[0], jval[1])
        if res == 200:
            for row in t.get_children():
                item = t.item(row)['values'][0]
                if item == jval[0]:
                    t.delete(row)
        delete.destroy()

    #Bindings
    buttonA.bind("<Button-1>", handle_yes)
    buttonB.bind("<Button-1>", handle_no)


# Main User Interface for ADMIN
def GUI():

    root2 = tk.Tk()
    root2.title("Restaurant Database Management")

    # Create a left border frame
    border_frame = tk.Frame(root2, width=150, bg='gray16')  # You can change 'grey' to any color you prefer
    border_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Setting up the Treeview (table)
    columns = ('ID', 'Name', 'Location', 'Type', 'Stars', 'Likes', 'Dislikes', 'NumScores')
    tree2 = ttk.Treeview(root2, columns=columns, show='headings', height=20)
    tree2.heading('ID', text='ID')
    tree2.heading('Name', text='Name')
    tree2.heading('Location', text='Location')
    tree2.heading('Type', text='Type')
    tree2.heading('Stars', text='Stars')
    tree2.heading('Likes', text='Likes')
    tree2.heading('Dislikes', text='Dislikes')
    tree2.heading('NumScores', text='NumScores')

    for col in columns:
        tree2.column(col, stretch=False)

    tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,10))  # Add padding to the left of the table

    # Scrollbar for the table
    scrollbar = ttk.Scrollbar(root2, orient=tk.VERTICAL, command=tree2.yview)
    tree2.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.LEFT, fill='y')  # Changed from RIGHT to LEFT for alignment

    # Frame for the right buttons
    buttons_frame = tk.Frame(root2, width=150, bg='gray16')
    buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Buttons for Create, Modify, Delete
    create_button = tk.Button(buttons_frame, text="Create", height=2, width = 13)
    modify_button = tk.Button(buttons_frame, text="Modify", state='disabled', height=2, width = 13)  # Initially disabled
    delete_button = tk.Button(buttons_frame, text="Delete", state='disabled', height=2, width = 13, bg='red4')  # Initially disabled

    create_button.pack(pady=(100,15))
    modify_button.pack(pady=15)
    delete_button.pack(pady=15)

    # Buttos for filters and show all, Database visualization
    show_button = tk.Button(border_frame, text="Show All", height=2, width = 13) 
    filter_button = tk.Button(border_frame, text="Filter", height=2, width = 13) 
    hash_button = tk.Button(border_frame, text="Re-Hash", height=2, width = 13, bg='SpringGreen4') 

    filter_button.pack(pady=(115,15))
    show_button.pack(pady=15)
    hash_button.pack(side='bottom', pady=(0,15))
    

    def select_row(event):
        if tree2.focus():
            modify_button['state'] = 'normal'
            delete_button['state'] = 'normal'

    #Launch create
    def create_new(event):
        create_record(root2,tree2)
        modify_button['state'] = 'disabled'
        delete_button['state'] = 'disabled'

    #Launch modify
    def modify_new(event):
        if modify_button['state'] == 'normal':
            Item = tree2.focus()
            jval = tree2.item(Item)["values"]
            modify_record(root2, tree2, jval)
            modify_button['state'] = 'disabled'
            delete_button['state'] = 'disabled'

    #Launch create
    def delete_new(event):
        if delete_button['state'] == 'normal':
            Item = tree2.focus()
            jval = tree2.item(Item)["values"]
            delete_record(root2, tree2, jval)
            modify_button['state'] = 'disabled'
            delete_button['state'] = 'disabled'

    #Show all database
    def show_new(event):
        update_table(tree2)
        modify_button['state'] = 'disabled'
        delete_button['state'] = 'disabled'

    #Filter search database
    def filter_new(event):
        filter_table(root2, tree2)
        modify_button['state'] = 'disabled'
        delete_button['state'] = 'disabled'

    def rehash(event):
        if hash_button['state'] == 'normal':
            modify_button['state'] = 'disabled'
            delete_button['state'] = 'disabled'
            hash_button['state'] = 'disabled'
            children = tree2.get_children()
            for row in children:
                jval = tree2.item(row)['values']
                hash_restaurant(jval[0], jval[1], jval[3], jval[2], jval[4], jval[5], jval[6], jval[7])
            hash_button['state'] = 'normal'

    #Bindings
    tree2.bind("<ButtonRelease-1>", select_row)
    create_button.bind("<Button-1>", create_new)
    modify_button.bind("<Button-1>", modify_new)
    delete_button.bind("<Button-1>", delete_new)
    show_button.bind("<Button-1>", show_new)
    filter_button.bind("<Button-1>", filter_new)
    hash_button.bind("<Button-1>", rehash)

    sv_ttk.set_theme("dark")
    root2.iconbitmap("5235253.ico")
    root2.mainloop()





#########
#User/Admin Log in and Sign in window
#########

# Only 1 database, just 2 different paths
urls2 = ["https://user-b8599-default-rtdb.firebaseio.com/Admins.json", "https://user-b8599-default-rtdb.firebaseio.com/Users.json"]

#Window Creation
root = tk.Tk()
root.title("The Foody")
root.iconbitmap("5235253.ico")

root.geometry("300x350")
root.eval(f'tk::PlaceWindow {str(root)} center')
root.resizable(False, False)

#Widgets
Enter = ttk.Label(root,text="Enter Credentials", justify='center',font='Helvetica 12 bold')
Enter.pack(pady=(15,0))

Username = ttk.Label(root,text="Username:")
Username.pack(fill=tk.X, padx=5, pady=10)
Username = tk.Entry(root,width=45)
Username.pack()

Password = ttk.Label(root,text="Password:")
Password.pack(fill=tk.X, padx=5, pady=(25,5))
Password = tk.Entry(root,width=45)
Password.pack()

admin = tk.IntVar()
admincheck = tk.Checkbutton(root, text='Admin',variable=admin, onvalue=1, offvalue=0, selectcolor="black", anchor="w")
admincheck.pack(fill=tk.X, padx=5, pady=(15,5))
admincheck.pack()

Log = tk.Button(root, text="Log In",height=1, width = 15)
Log.pack(padx=5, pady=(40,0))

Sing = tk.Button(root, text="Sing Up",height=1, width = 10, fg='Cyan')
Sing.pack(padx=5, pady=(40,0))


#Check user and launch
def check(event):
    token = False
    if admin.get() == 1: 
        test = requests.get(urls2[0]).json()
        for k, v in test.items():  
            if str(k) == str(Username.get()):
                if str(v["Password"]) == str(Password.get()):
                    token = True
                break
        if token:
            root.destroy()
            GUI()
        else:
            messagebox.showerror('Credentials Error', 'Admin account not found')
                    
    else:
        test = requests.get(urls2[1]).json()
        for k, v in test.items():  
            if str(k) == str(Username.get()):
                if str(v["Password"]) == str(Password.get()):
                    token = True
                break
        if token:
            webbrowser.open('https://dsci551projecttesting.netlify.app/')
            sys.exit()
        else:
            messagebox.showerror('Credentials Error', 'User account not found')

#Create user
def create(event):
    if admin.get() == 1: 
        messagebox.showerror('Application Error', 'Admin account creation not allowed')
    else:
        token = False
        test = requests.get(urls2[1]).json()
        for k in test.keys():  
            if str(k) == str(Username.get()):
                token = True
        if token:
            messagebox.showerror('Credentials Error', 'Username already in use')
        else:
            dataj = {"Password": str(Password.get())}
            dataj = json.dumps(dataj)
            url = "https://user-b8599-default-rtdb.firebaseio.com/Users/" + str(Username.get()) + ".json"
            response = requests.patch(url, data=dataj)
            print(response)
            if response.status_code == 200:
                messagebox.showinfo("User Created", "New User added successfuly, you can now Log In")
            else:
                messagebox.showerror('Database Error', 'Error while creating new user')

#Bindings
Log.bind("<Button-1>", check)
Sing.bind("<Button-1>", create)

sv_ttk.set_theme("dark")
root.mainloop()


#pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/ariel/Desktop/551/AProject/v2/5235253.ico" --collect-data "sv_ttk"  "C:/Users/ariel/Desktop/551/AProject/v2/Foody.py"