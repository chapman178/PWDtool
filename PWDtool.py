import tkinter as tk
import pandas as pd
from tkinter import filedialog

# Create Tkinter environement

root = tk.Tk()
root.geometry('100x150')

#define variables

Lane1_EN = tk.BooleanVar() 
Lane2_EN = tk.BooleanVar()
Lane3_EN = tk.BooleanVar()
Lane4_EN = tk.BooleanVar()

global df
global df_select

# Define functions 

def button_clicked():
    print("button clicked")
    print(df)
    print(Lane1_EN.get())

def load_data():
    global df
    global df_select
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.csv")])
    if not filepath:
        return
    df = pd.read_csv('.//InputData.csv')
    df['Losses'] = 0
    df_select = df
    load_racers()


def load_racers():
    global df_select
    try : 
        A = df_select
    except:
        A = []
    print(A)
    lb_Racers.delete(0,'end')
    i = 1
    lb_Racers.insert(i, "    ".join(['Number', 'Losses', 'Den   ', 'Name']))
    for index, row in A.iterrows():
        lb_Racers.insert(i, "    ".join([str(row['Number']),'    ' ,str(row['Losses']),'     ' , str(row['Type']),'     ',  str(row['Name'])]))


#create places for components

frame = tk.Frame(root)
frameLower = tk.Frame(root)
menubar = tk.Menu(root)

#Create menu bar
file_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label = 'Load Data', command = lambda:load_data())
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label ='File', menu = file_menu)

# Create GUI
# Create racer consideration label
lb_Racers = tk.Listbox(frameLower, height = 10, width = 40, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow')

# Create a Scrollbar
scrollbar = tk.Scrollbar(frameLower, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady= 10)

# Link the Scrollbar to the Listbox
lb_Racers.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lb_Racers.yview)

#create checkboxes
btn1 = tk.Checkbutton(frame, text = 'Lane 1', variable = Lane1_EN, onvalue=1, offvalue=0, height=1,width=5)
btn1.pack(side=tk.LEFT)

#create button load racers
btn_LoadRacers = tk.Button(frame, text='Load Racers', command= load_racers)

#create button
button = tk.Button(frame, text='hello', command= button_clicked)

txt_edit = tk.Text(frame)



button.pack()
btn_LoadRacers.pack()
lb_Racers.pack()
# lb_Number.pack(side=tk.LEFT)
# lb_Type.pack(side=tk.LEFT)
# lb_Losses.pack(side=tk.LEFT)
# txt_edit.pack()

frame.pack()
frameLower.pack()

root.config(menu = menubar)
root.mainloop()