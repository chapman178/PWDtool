import tkinter as tk
import pandas as pd
from tkinter import filedialog

root = tk.Tk()
root.geometry('1000x1000')

#define variables
Lane1_EN = tk.IntVar() 
Lane2_EN = tk.IntVar()
Lane3_EN = tk.IntVar()
Lane4_EN = tk.IntVar()

#initialize lane variable
Lane1_EN.set(1)
Lane2_EN.set(1)
Lane3_EN.set(1)
Lane4_EN.set(1)

Names = tk.IntVar() 
Numbers = tk.IntVar()
Types = tk.IntVar()

global df

def load_data():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.csv")])
    if not filepath:
        return
    df = pd.read_csv('.//InputData.csv')

def line_up_cars_clicked():
    global df
    print("button clicked")
    print(df)
    print(Lane1_EN.get())

def select_race_group(event):
    global df
    print("button clicked")
    print(df)
    print(Lane1_EN.get())




#create places for components
menubar = tk.Menu(root)
frame_lane1 = tk.Frame(root)
frame_lane2 = tk.Frame(root)
frame_lane3 = tk.Frame(root)
frame_lane4 = tk.Frame(root)
frame_cntrl = tk.Frame(root)
frame_race_group = tk.Frame(root)


#Create menu bar
file = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label = 'Load Data', command = lambda:load_data())

#create checkboxes
btn1 = tk.Checkbutton(frame_lane1, text = ' Lane 1 ', variable = Lane1_EN, onvalue=1, offvalue=0, height=1,width=5)
btn1.pack(side=tk.LEFT)
btn2 = tk.Checkbutton(frame_lane2, text = ' Lane 2 ', variable = Lane2_EN, onvalue=1, offvalue=0, height=1,width=5)
btn2.pack(side=tk.LEFT)
btn3 = tk.Checkbutton(frame_lane3, text = ' Lane 3 ', variable = Lane3_EN, onvalue=1, offvalue=0, height=1,width=5)
btn3.pack(side=tk.LEFT)
btn4 = tk.Checkbutton(frame_lane4, text = ' Lane 4 ', variable = Lane4_EN, onvalue=1, offvalue=0, height=1,width=5)
btn4.pack(side=tk.LEFT)

#create button
button_line_up = tk.Button(frame_cntrl, text=' line up cars ', command= line_up_cars_clicked)
button_line_up.pack(side=tk.LEFT)

button_race = tk.Button(frame_cntrl, text=' cars raced ', command= line_up_cars_clicked)
button_race.pack(side=tk.LEFT)

# Create list box
pack_names = ('Overall', 'Pack', 'Arrow', 'Webelo', 'Bear', 'Wolf', 'Tiger', 'Lion', 'Open')
pack_var = tk.Variable(value=pack_names)
listbox = tk.Listbox(frame_race_group, height = 10, width = 10, bg='gray', activestyle = 'dotbox', font='Helvetica', 
    fg='yellow',listvariable=pack_var ,selectmode=tk.SINGLE)
listbox.bind('<<ListboxSelect>>', select_race_group)
listbox.pack(side=tk.LEFT)


txt_edit = tk.Text(frame_race_group)
txt_edit.pack(side=tk.LEFT)

root.config(menu = menubar)
frame_lane1.pack()
frame_lane2.pack()
frame_lane3.pack()
frame_lane4.pack()
frame_cntrl.pack()
frame_race_group.pack()

root.mainloop()