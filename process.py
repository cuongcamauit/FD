from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sqlite3



# return a list from sql statement 
def returnlist(s):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur = cur.execute(s)
    return cur.fetchall()
def settree1(list):
    for i in tree1.get_children():
        tree1.delete(i)
    for i in list:
        tree1.insert('',tk.END,values=i)
def taochuoi(a, b, c):
    s = ""
    if (a!=""):
        s = s + " A=%s" %(a)
    if (b!=""):
        if (s!=""):
            s = s + " AND B=%s" %(b)
        else:
            s = s + " B=%s" %b
    if (c!=""):
        if (s!=""):
            s = s + " AND C=%s" %(c)
        else:
            s = s + " C=%s" %(c)
    return s
# commit sql
def commitsql(s):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    try:
        cur = cur.execute(s)
        con.commit()
        settree1(returnlist("select * from R1"))
    except sqlite3.Error as e:
        messagebox.showerror("Error",e)


def item_selected(f):
    print(5)
    for selected_item in tree1.selection():
        
        # dictionary
        item = tree1.item(selected_item)
        # list
        record = item['values']
        
        A.set(record[0])
        B1.set(record[1])
        C.set(record[2])
        print(record)



def update():
    print(5)
    global s1, s2, s3
    
    s1 = A.get()
    s2 = B1.get()
    s3 = C.get()
    ap = App2(updates)
    ap.mainloop()
def insert():
    ap = App2(inserts)
    ap.mainloop()


def updates():
    s = "UPDATE R1 SET" + taochuoi(A.get(), B1.get(), C.get()) + " WHERE" + taochuoi(s1, s2, s3)
    s = s.replace("AND", ",", 2)
    print(s)
    commitsql(s)
def inserts():
    s = "INSERT INTO R1 VALUES(%s, %s, %s);" %(A.get(), B1.get(), C.get())
    commitsql(s)

def delete():
    s = "DELETE FROM R1 WHERE" + taochuoi(A.get(), B1.get(), C.get())
    commitsql(s)

class App2(tk.Toplevel):
    def __init__(self,k, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Label(self, text="A").grid(column=0, row=0)
        Entry(self, textvariable=A).grid(column=1, row=0)

        Label(self, text="B").grid(column=0, row=1)
        Entry(self, textvariable=B1).grid(column=1, row=1)

        Label(self, text="C").grid(column=0, row=2)
        Entry(self, textvariable=C).grid(column=1, row=2)

        Button(self, text="OK", width=5, command=k).grid(column=0, row=3)
        Button(self, text="Cancel", command=self.destroy).grid(column=1, row=3)




class Frame1(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        Label(self, text="R1").grid(column=0, row=0, columnspan=3)
        
        global tree1
        colums = ('#1', '#2', '#3')
        tree1 = ttk.Treeview(self, columns=colums, show='headings')
        # define heading
        tree1.heading('#1', text="A")
        tree1.heading('#2', text="B")
        tree1.heading('#3', text="C")
        tree1.grid(row=1, column=0, sticky='nsew', columnspan=3)
        
        # add a scrollbar
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree1.yview)
        tree1.config(yscroll=scrollbar.set)
        tree1.bind('<<TreeviewSelect>>', item_selected)
        scrollbar.grid(row=1, column=3, sticky='ns')

        settree1(returnlist("select * from R1"))
        Button(self, text="Insert", width=20, height=2, command=insert).grid(row=2, column=0)
        Button(self, text="Delete", width=20, height=2, command=delete).grid(row=2, column=1)
        Button(self, text="Update", width=20, height=2, command=update).grid(row=2, column=2)

        


class Frame2(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        Label(self, text="R2").grid(column=0, row=0, columnspan=3)
        global tree2
        colums = ('#1', '#2', '#3')
        tree2 = ttk.Treeview(self, columns=colums, show='headings')
        # define heading
        tree2.heading('#1', text="A")
        tree2.heading('#2', text="B")
        tree2.heading('#3', text="C")
        tree2.grid(row=1, column=0, sticky='nsew', columnspan=3)
        # add a scrollbar
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree1.yview)
        tree2.config(yscroll=scrollbar.set)
        tree2.bind('<<TreeviewSelect>>')
        Button(self, text="Insert", width=20, height=2).grid(row=2, column=0)
        Button(self, text="Delete", width=20, height=2).grid(row=2, column=1)
        Button(self, text="Update", width=20, height=2).grid(row=2, column=2)

        settree1(returnlist("select * from R1"))



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global A, B1, C, D, E, B2
        
        A = StringVar()
        B1 = StringVar()
        C = StringVar()
        D = StringVar()
        E = StringVar()
        B2 = StringVar()
        Label(self, text="FD trên nhiều quan hệ\nR1(ABC)  R2(BDC) \n A->D", font="30").grid(column=0, row=0, columnspan=2)
        Frame1(self).grid(column=0, row=1)
        Frame2(self).grid(row=1, column=1)
    
app = App()
app.mainloop()
    


