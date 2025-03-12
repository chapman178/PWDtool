import tkinter as tk
import pandas as pd
from tkinter import filedialog

root = tk.Tk()
root.geometry('100x150')

#define variables
Lane1_EN = tk.IntVar() 
Lane2_EN = tk.IntVar()
Lane3_EN = tk.IntVar()
Lane4_EN = tk.IntVar()

Names = tk.IntVar() 
Numbers = tk.IntVar()
Types = tk.IntVar()

global df

def button_clicked():
    global df
    print("button clicked")
    print(df)
    print(Lane1_EN.get())

def load_data():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.csv")])
    if not filepath:
        return
    df = pd.read_csv('.//InputData.csv')
    
    # txt_edit.insert(df)
    print(df)


#create places for components
frame = tk.Frame(root)
menubar = tk.Menu(root)

#Create menu bar
file = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label = 'Load Data', command = lambda:load_data())

# Create GUI
listbox = tk.Listbox(frame, height = 10, width = 10, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow')
listbox.insert(1, 'One')
listbox.insert(2, 'Two')
listbox.insert(3, 'Three')
listbox.insert(4, 'Four')
listbox.insert(5, 'Four')
listbox.insert(6, 'Four')
listbox.insert(7, 'Four')
listbox.insert(8, 'Four')

#create checkboxes
btn1 = tk.Checkbutton(frame, text = 'Lane 1', variable = Lane1_EN, onvalue=1, offvalue=0, height=1,width=5)
btn1.pack(side=tk.LEFT)

#create button
button = tk.Button(frame, text='hello', command= button_clicked)

txt_edit = tk.Text(frame)



button.pack()
listbox.pack()
txt_edit.pack()

frame.pack()

root.config(menu = menubar)
root.mainloop()