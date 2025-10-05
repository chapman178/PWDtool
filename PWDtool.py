import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import ttk

# Create Tkinter environement

root = tk.Tk()
root.geometry('600x625')

#
#define variables
#

Lane1_EN = tk.BooleanVar() 
Lane2_EN = tk.BooleanVar()
Lane3_EN = tk.BooleanVar()
Lane4_EN = tk.BooleanVar()
Lane1_EN.set(True)
Lane2_EN.set(True)
Lane3_EN.set(True)
Lane4_EN.set(True)

ShowEliminated_EN = tk.BooleanVar()
ShowEliminated_EN.set(True)

Lane1_Car = tk.IntVar() 
Lane2_Car = tk.IntVar()
Lane3_Car = tk.IntVar()
Lane4_Car = tk.IntVar()
Lane1_Car.set(int(0))
Lane2_Car.set(int(0))
Lane3_Car.set(int(0))
Lane4_Car.set(int(0))

Car_number = tk.IntVar()
Car_number.set(int(0))

Lane1_Car_str = tk.StringVar() 
Lane2_Car_str = tk.StringVar()
Lane3_Car_str = tk.StringVar()
Lane4_Car_str = tk.StringVar()

Loss1_EN = tk.BooleanVar() 
Loss2_EN = tk.BooleanVar()
Loss3_EN = tk.BooleanVar()
Loss4_EN = tk.BooleanVar()
Loss1_EN.set(False)
Loss2_EN.set(False)
Loss3_EN.set(False)
Loss4_EN.set(False)

global df
global df_select

#
# Define functions 
#

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
    df['L1'] = 0
    df['L2'] = 0
    df['L3'] = 0
    df['L4'] = 0
    df['Races'] = 0
    df_select = df
    load_lb_Racers()


def load_lb_Racers():
    global df_select
    try : 
        A = df_select
    except:
        A = []
    print(A)
    if not(ShowEliminated_EN.get()):
        print( "in here" )
        A = A[A['Losses']<3]
    lb_Racers.delete(*lb_Racers.get_children())
    for index, racer_row in A.iterrows():
        lb_Racers.insert("",'end', values=(racer_row['Number'], racer_row['Losses'], racer_row['Type'], racer_row['Name'], racer_row['Races'], racer_row['L1'], racer_row['L2'], racer_row['L3'], racer_row['L4']))

def load_racers():
    global df_select
    try : 
        A_select = df_select
    except:
        A_select = []
        print('no cars selected, line 82')
        return

    # activate all cars with losses less then 3
    A_active = A_select[A_select['Losses']<3]
    # if number of active cars is less than number of active lanes adjust number of lanes.
    rws, cols = A_active.shape
    if rws <=1:
        print('There is a winner,  add more cars')
        return
    number_of_active_lanes = Lane1_EN.get() + Lane2_EN.get() + Lane3_EN.get() + Lane4_EN.get()
    if number_of_active_lanes > rws:
        Lane4_EN.set(False)
        number_of_active_lanes = Lane1_EN.get() + Lane2_EN.get() + Lane3_EN.get() + Lane4_EN.get()
        if number_of_active_lanes > rws:
            Lane1_EN.set(False)
            number_of_active_lanes = Lane1_EN.get() + Lane2_EN.get() + Lane3_EN.get() + Lane4_EN.get()

    number_of_lanes = sum([Lane1_EN.get(), Lane2_EN.get(), Lane3_EN.get(), Lane4_EN.get()])
    Cars_to_race = get_cars_to_race(A_active, number_of_lanes)
    Cars_to_race_laned = assign_lanes(Cars_to_race, [Lane1_EN.get(), Lane2_EN.get(), Lane3_EN.get(), Lane4_EN.get()] )
    print(Cars_to_race_laned)
    i = 0
    if Lane1_EN.get():
        lb_Racer1.delete(tk.END)
        Lane1_Car_local = Cars_to_race_laned.iloc[i]['Number']
        Lane1_Car.set(int(Lane1_Car_local))
        Lane1_Car_str.set(str(Lane1_Car_local))
        i+=1
    else :
        Lane1_Car_str.set(str(''))
    if Lane2_EN.get():
        lb_Racer2.delete(tk.END)
        Lane2_Car_local = Cars_to_race_laned.iloc[i]['Number']
        Lane2_Car.set(int(Lane2_Car_local))
        Lane2_Car_str.set(str(Lane2_Car_local))
        i+=1
    else :
        Lane2_Car_str.set(str(''))
    if Lane3_EN.get():
        lb_Racer3.delete(tk.END)
        Lane3_Car_local = Cars_to_race_laned.iloc[i]['Number']
        Lane3_Car.set(int(Lane3_Car_local))
        Lane3_Car_str.set(str(Lane3_Car_local))
        i+=1
    else :
        Lane3_Car_str.set(str(''))
    if Lane4_EN.get():
        lb_Racer4.delete(tk.END)
        Lane4_Car_local = Cars_to_race_laned.iloc[i]['Number']
        Lane4_Car.set(int(Lane4_Car_local))
        Lane4_Car_str.set(str(Lane4_Car_local))
        i+=1
    else :
        Lane4_Car_str.set(str(''))
    
def get_cars_to_race(A_active, NL):
    number_of_lanes = NL
    # select racers with minimun number of races
    print(A_active['Races'].min() )
    print(A_active )
    A_next_racers = A_active[A_active['Races'] == A_active['Races'].min()] 
    N_rws, N_cols = A_next_racers.shape
    if N_rws >= number_of_lanes :
        Cars_to_race = A_next_racers.sample(number_of_lanes)
    else :
        Cars_to_race = A_next_racers
        Additional_racers = A_active[A_active['Races'] > A_active['Races'].min()]
        Additional_cars = Additional_racers.sample(number_of_lanes - N_rws)
        Cars_to_race = pd.concat([Cars_to_race, Additional_cars], ignore_index=True)
    return Cars_to_race

def assign_lanes(Cars_to_Race, NL_EN):
    Cars_hat = Cars_to_Race
    Cars_to_race_laned = Cars_to_Race.iloc[0:0]
    if NL_EN[0]:
        Cars_hat = Cars_hat.sort_values(by='L1', ascending=True)
        Cars_to_race_laned = pd.concat([Cars_to_race_laned, Cars_hat.head(1)], ignore_index=True) 
        Cars_hat.drop(index=Cars_hat.index[0], inplace=True)
    if NL_EN[1]:
        Cars_hat = Cars_hat.sort_values(by='L2', ascending=True)
        Cars_to_race_laned = pd.concat([Cars_to_race_laned, Cars_hat.head(1)], ignore_index=True) 
        Cars_hat.drop(index=Cars_hat.index[0], inplace=True)
    if NL_EN[2]:
        Cars_hat = Cars_hat.sort_values(by='L3', ascending=True)
        Cars_to_race_laned = pd.concat([Cars_to_race_laned, Cars_hat.head(1)], ignore_index=True) 
        Cars_hat.drop(index=Cars_hat.index[0], inplace=True)
    if NL_EN[3]:
        Cars_hat = Cars_hat.sort_values(by='L4', ascending=True)
        Cars_to_race_laned = pd.concat([Cars_to_race_laned, Cars_hat.head(1)], ignore_index=True)
        Cars_hat.drop(index=Cars_hat.index[0], inplace=True)
    return Cars_to_race_laned 

def select_race_group_lb(event):
    select_race_group()

def select_race_group():
    global df
    global df_select
    type_selected = listbox.get(listbox.curselection())
    if (type_selected=='Overall'):
        df_select = df
    elif (type_selected == 'Pack') :
        df_select = df.loc[df['Type']!='Open']
    else :
        df_select = df.loc[df['Type']==type_selected]
    # print(df_select)
    load_lb_Racers()

def complete_race():
    global df
    if Lane1_EN.get():
        print('lane1 - complete')
        index = df.index[df['Number']==Lane1_Car.get()]
        df.loc[index, 'Races'] +=1 
        df.loc[index, 'L1'] +=1 
        if Loss1_EN.get():
            df.loc[index, 'Losses']+=1
    if Lane2_EN.get():
        print('lane1 - complete')
        index = df.index[df['Number']==Lane2_Car.get()]
        df.loc[index, 'Races'] +=1 
        df.loc[index, 'L2'] +=1 
        if Loss2_EN.get():
            df.loc[index, 'Losses']+=1
    if Lane3_EN.get():
        print('lane1 - complete')
        index = df.index[df['Number']==Lane3_Car.get()]
        df.loc[index, 'Races'] +=1 
        df.loc[index, 'L3'] +=1 
        if Loss3_EN.get():
            df.loc[index, 'Losses']+=1
    if Lane4_EN.get():
        print('lane1 - complete')
        index = df.index[df['Number']==Lane4_Car.get()]
        df.loc[index, 'Races'] +=1 
        df.loc[index, 'L4'] +=1 
        if Loss4_EN.get():
            df.loc[index, 'Losses']+=1
    # print('Updated racers')
    # print(df)
    uncheck_Losses()
    select_race_group()
    load_racers()
    return

def uncheck_Losses():
    Loss1_EN.set(False)
    Loss2_EN.set(False)
    Loss3_EN.set(False)
    Loss4_EN.set(False)

def reset_races():
    df.loc[df['Races']!=0, 'Races'] = 0
    df.loc[df['L1']!=0, 'L1'] = 0
    df.loc[df['L2']!=0, 'L2'] = 0
    df.loc[df['L3']!=0, 'L3'] = 0
    df.loc[df['L4']!=0, 'L4'] = 0
    select_race_group()

def reset_losses():
    df.loc[df['Losses']<3, 'Losses'] = 0
    select_race_group()

def loss_up():
    df.loc[df['Number']==Car_number.get(), 'Losses'] +=1
    select_race_group()
    return

def loss_dwn():
    df.loc[df['Number']==Car_number.get(), 'Losses'] -=1
    select_race_group()
    return

def race_up():
    df.loc[df['Number']==Car_number.get(), 'Races'] +=1
    select_race_group()
    return

def race_dwn():
    df.loc[df['Number']==Car_number.get(), 'Races'] -=1
    select_race_group()
    return

def L1_up():
    df.loc[df['Number']==Car_number.get(), 'L1'] +=1
    select_race_group()
    return

def L1_dwn():
    df.loc[df['Number']==Car_number.get(), 'L1'] -=1
    select_race_group()
    return

def L2_up():
    df.loc[df['Number']==Car_number.get(), 'L2'] +=1
    select_race_group()
    return

def L2_dwn():
    df.loc[df['Number']==Car_number.get(), 'L2'] -=1
    select_race_group()
    return

def L3_up():
    df.loc[df['Number']==Car_number.get(), 'L3'] +=1
    select_race_group()
    return

def L3_dwn():
    df.loc[df['Number']==Car_number.get(), 'L3'] -=1
    select_race_group()
    return

def L4_up():
    df.loc[df['Number']==Car_number.get(), 'L4'] +=1
    select_race_group()
    return

def L4_dwn():
    df.loc[df['Number']==Car_number.get(), 'L2'] -=1
    select_race_group()
    return

def move_den():
    print('Move Den')
    type_selected = listbox.get(listbox.curselection())
    df.loc[df['Number']==Car_number.get(), 'Type'] = type_selected
    select_race_group()
    return

#
#    DEVELOP GUI
#
#create places for components

frame = tk.Frame(root)
frame_lane1 = tk.Frame(root)
frame_lane2 = tk.Frame(root)
frame_lane3 = tk.Frame(root)
frame_lane4 = tk.Frame(root)
frame_cntrl = tk.Frame(root)
frame_cntrl_chk = tk.Frame(root)
frameData = tk.Frame(root)
frameManual = tk.Frame(root)
frameMBut1 = tk.Frame(root)
frameMBut2 = tk.Frame(root)
frameMBut3 = tk.Frame(root)
frameMBut4 = tk.Frame(root)
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
lb_Racer1 = tk.Listbox(frame_lane1, height = 1, width = 3, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow', listvariable=Lane1_Car_str)
lb_Racer1.pack(side=tk.LEFT)
ck_loss1 = tk.Checkbutton(frame_lane1, text = 'Loss', variable = Loss1_EN, onvalue=1, offvalue=0, height=1,width=5)
ck_loss1.pack(side=tk.LEFT)

ch_lane2 = tk.Checkbutton(frame_lane2, text = 'Lane 2', variable = Lane2_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane2.pack(side=tk.LEFT)
lb_Racer2 = tk.Listbox(frame_lane2, height = 1, width = 3, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow', listvariable=Lane2_Car_str)
lb_Racer2.pack(side=tk.LEFT)
ch_loss2 = tk.Checkbutton(frame_lane2, text = 'Loss', variable = Loss2_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_loss2.pack(side=tk.LEFT)

ch_lane3 = tk.Checkbutton(frame_lane3, text = 'Lane 3', variable = Lane3_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane3.pack(side=tk.LEFT)
lb_Racer3 = tk.Listbox(frame_lane3, height = 1, width = 3, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow', listvariable=Lane3_Car_str)
lb_Racer3.pack(side=tk.LEFT)
ch_loss3 = tk.Checkbutton(frame_lane3, text = 'Loss', variable = Loss3_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_loss3.pack(side=tk.LEFT)

ch_lane4 = tk.Checkbutton(frame_lane4, text = 'Lane 4', variable = Lane4_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_lane4.pack(side=tk.LEFT)
lb_Racer4 = tk.Listbox(frame_lane4, height = 1, width = 3, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow', listvariable=Lane4_Car_str)
lb_Racer4.pack(side=tk.LEFT)
ch_loss4 = tk.Checkbutton(frame_lane4, text = 'Loss', variable = Loss4_EN, onvalue=1, offvalue=0, height=1,width=5)
ch_loss4.pack(side=tk.LEFT)

#create button load racers
btn_LoadRacers = tk.Button(frame_cntrl, text='Load Racers', command= load_racers)
btn_LoadRacers.pack(side = tk.LEFT)

#create race complete button
btn_CmpltRace = tk.Button(frame_cntrl, text='Complete Race', command= complete_race)
btn_CmpltRace.pack(side = tk.LEFT)

#create race reset races button
btn_ResetRaces = tk.Button(frame_cntrl, text='Reset Races', command= reset_races)
btn_ResetRaces.pack(side = tk.LEFT)

#create race reset losses button
btn_ResetRaces = tk.Button(frame_cntrl, text='Reset Losses', command= reset_losses)
btn_ResetRaces.pack(side = tk.LEFT)

ch_ShowEliminated = tk.Checkbutton(frame_cntrl_chk, text = 'show_eliminated', variable = ShowEliminated_EN, command = select_race_group , onvalue=1, offvalue=0, height=1,width=15)
ch_ShowEliminated.pack(side=tk.RIGHT)

#create entry for manual car adjusting
ent_name = tk.Entry(frameManual,textvariable = Car_number, font=('calibre',10,'normal'), width=10)
ent_name.pack(side = tk.LEFT)

#create change loss + button
btn_LossUp = tk.Button(frameMBut1, text='Loss +', command= loss_up)
btn_LossUp.pack(side = tk.LEFT)

#create change loss - button
btn_LossDwn = tk.Button(frameMBut1, text='Loss -', command= loss_dwn)
btn_LossDwn.pack(side = tk.LEFT)

#create change race + button
btn_RaceUp = tk.Button(frameMBut1, text='Race +', command= race_up)
btn_RaceUp.pack(side = tk.LEFT)

#create change race - button
btn_RaceDwn = tk.Button(frameMBut1, text='Race -', command= race_dwn)
btn_RaceDwn.pack(side = tk.LEFT)

#create change L1 + button
btn_L1up = tk.Button(frameMBut2, text='L1 +', command= L1_up)
btn_L1up.pack(side = tk.LEFT)

#create change L1 - button
btn_L1dwn = tk.Button(frameMBut2, text='L1 -', command= L1_dwn)
btn_L1dwn.pack(side = tk.LEFT)

#create change L2 + button
btn_L2up = tk.Button(frameMBut2, text='L2 +', command= L2_up)
btn_L2up.pack(side = tk.LEFT)

#create change L2 - button
btn_L2dwn = tk.Button(frameMBut2, text='L2 -', command= L2_dwn)
btn_L2dwn.pack(side = tk.LEFT)

#create change L3 + button
btn_L3up = tk.Button(frameMBut3, text='L3 +', command= L3_up)
btn_L3up.pack(side = tk.LEFT)

#create change L3 - button
btn_L3dwn = tk.Button(frameMBut3, text='L3 -', command= L3_dwn)
btn_L3dwn.pack(side = tk.LEFT)

#create change L4 + button
btn_L4up = tk.Button(frameMBut3, text='L4 +', command= L4_up)
btn_L4up.pack(side = tk.LEFT)

#create change L4 - button
btn_L4dwn = tk.Button(frameMBut3, text='L4 -', command= L4_dwn)
btn_L4dwn.pack(side = tk.LEFT)

#create move den button
btn_MvDen = tk.Button(frameMBut4, text='Move Den', command= move_den)
btn_MvDen.pack(side = tk.LEFT)

# Create list box with catagoires
pack_names = ('Overall', 'Pack', 'Arrow', 'Webelo', 'Bear', 'Wolf', 'Tiger', 'Lion', 'Open')
pack_var = tk.Variable(value=pack_names)
listbox = tk.Listbox(frameData, height = 10, width = 10, bg='gray', activestyle = 'dotbox', font='Helvetica', 
    fg='yellow',listvariable=pack_var ,selectmode=tk.SINGLE, exportselection=False)
listbox.bind('<<ListboxSelect>>', select_race_group_lb)
listbox.pack(side=tk.LEFT)

# Create racer consideration label
# lb_Racers = tk.Listbox(frameData, height = 10, width = 40, bg='gray', activestyle = 'dotbox', font='Helvetica', fg='yellow')
lb_Racers = ttk.Treeview(frameData, selectmode = 'browse', columns = ('ID', 'Losses', 'Den', 'Name','Races' ,'L1', 'L2', 'L3', 'L4'), show='headings')
lb_Racers.column("ID", width = 40, anchor ='w') 
lb_Racers.column("Losses", width = 40, anchor ='w') 
lb_Racers.column("Den", width = 90, anchor ='w') 
lb_Racers.column("Name", width = 90, anchor ='w') 
lb_Racers.column("Races", width = 50, anchor ='w') 
lb_Racers.column("L1", width = 30, anchor ='w') 
lb_Racers.column("L2", width = 30, anchor ='w') 
lb_Racers.column("L3", width = 30, anchor ='w') 
lb_Racers.column("L4", width = 30, anchor ='w') 

lb_Racers.heading("ID", text ="ID") 
lb_Racers.heading("Losses", text ="Loss")
lb_Racers.heading("Den", text ="Den")
lb_Racers.heading("Name", text ="Name")
lb_Racers.heading("Races", text ="Races")
lb_Racers.heading("L1", text ="L1")
lb_Racers.heading("L2", text ="L2")
lb_Racers.heading("L3", text ="L3")
lb_Racers.heading("L4", text ="L4")

# Create a Scrollbar
scrollbar = tk.Scrollbar(frameData, orient=tk.VERTICAL, command=lb_Racers.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady= 10)

# Link the Scrollbar to the Listbox
lb_Racers.config(yscrollcommand=scrollbar.set)
# pack racer consideration label
lb_Racers.pack(side=tk.LEFT, fill="both", expand=True)

# lb_Number.pack(side=tk.LEFT)
# lb_Type.pack(side=tk.LEFT)
# lb_Losses.pack(side=tk.LEFT)
# txt_edit.pack()
frame_lane1.pack()
frame_lane2.pack()
frame_lane3.pack()
frame_lane4.pack()
frame_cntrl.pack()
frame_cntrl_chk.pack()
frameData.pack()
frameManual.pack()
frameMBut1.pack()
frameMBut2.pack()
frameMBut3.pack()
frameMBut4.pack()

root.config(menu = menubar)
root.mainloop()