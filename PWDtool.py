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

#initialize variables 
Lane1_EN.set(True)
Lane2_EN.set(True)
Lane3_EN.set(True)
Lane4_EN.set(True)

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
frame_lane1 = tk.Frame(root)
frame_lane2 = tk.Frame(root)
frame_lane3 = tk.Frame(root)
frame_lane4 = tk.Frame(root)
frame_cntrl = tk.Frame(root)
frameData = tk.Frame(root)
menubar = tk.Menu(root)

#Create menu bar
file_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label = 'Load Data', command = lambda:load_data())
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label ='File', menu = file_menu)

# Create GUI

#create checkboxes
ck_lane1 = tk.Checkbutton(frame_lane1, text = 'Lane 1', variable = Lane1_EN, onvalue=1, offvalue=0, height=1,width=5)
ck_lane1.pack(side=tk.LEFT)


ch_lane2 = tk.Checkbutton(frame_lane2, text = 'Lane 2', variable = Lane2_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane2.pack(side=tk.LEFT)


ch_lane3 = tk.Checkbutton(frame_lane3, text = 'Lane 3', variable = Lane3_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane3.pack(side=tk.LEFT)


ch_lane4 = tk.Checkbutton(frame_lane4, text = 'Lane 4', variable = Lane4_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane4.pack(side=tk.LEFT)




# Create racer consideration label
lb_Racers = tk.Listbox(frameData, height = 10, width = 40, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow')

# Create a Scrollbar
scrollbar = tk.Scrollbar(frameData, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady= 10)

# Link the Scrollbar to the Listbox
lb_Racers.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lb_Racers.yview)
# pack racer consideration label
lb_Racers.pack()

#create button load racers
btn_LoadRacers = tk.Button(frame_cntrl, text='Load Racers', command= load_racers)
btn_LoadRacers.pack()

#create button
button = tk.Button(frame, text='hello', command= button_clicked)
button.pack()

txt_edit = tk.Text(frame)


def select_race_group(event):
    global df
    print("button clicked")
    print(listbox.get(listbox.curselection()))
    print(Lane1_EN.get())

# Create list box
pack_names = ('Overall', 'Pack', 'Arrow', 'Webelo', 'Bear', 'Wolf', 'Tiger', 'Lion', 'Open')
pack_var = tk.Variable(value=pack_names)
listbox = tk.Listbox(frameData, height = 10, width = 10, bg='gray', activestyle = 'dotbox', font='Helvetica', 
    fg='yellow',listvariable=pack_var ,selectmode=tk.SINGLE)
listbox.bind('<<ListboxSelect>>', select_race_group)
listbox.pack(side=tk.RIGHT)


# lb_Number.pack(side=tk.LEFT)
# lb_Type.pack(side=tk.LEFT)
# lb_Losses.pack(side=tk.LEFT)
# txt_edit.pack()
frame_lane1.pack()
frame_lane2.pack()
frame_lane3.pack()
frame_lane4.pack()
frameData.pack()
frame_cntrl.pack()


root.config(menu = menubar)
root.mainloop()