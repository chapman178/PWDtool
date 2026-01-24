import streamlit as st
import pandas as pd
from github import Github, Auth
import io

# Set up the page
st.set_page_config(page_title="PWD Tool", layout="centered")

st.title("Pinewood Derby, Pack 159")

# 1. Configuration from Secrets
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_NAME = st.secrets["REPO_NAME"]
    FILE_PATH = "InputData.csv" # The name of your file in the repo
except KeyError:
    st.error("Please set GITHUB_TOKEN and REPO_NAME in your secrets.toml")
    st.stop()

# 2. GitHub Connection Logic
@st.cache_data(ttl=5) # Cache for 10 seconds to keep it snappy
def load_github_data():
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(REPO_NAME)
    contents = repo.get_contents(FILE_PATH)
    # Decode content and read into pandas
    df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
    return df, contents.sha

# Helper function to push to GitHub
def save_to_github(updated_df, commit_message="Data updated via App"):
    with st.spinner("Pushing changes to GitHub..."):
        auth = Auth.Token(TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        csv_content = updated_df.to_csv(index=False)
        repo.update_file(
            path=FILE_PATH,
            message=commit_message,
            content=csv_content,
            sha=file_sha
        )
        st.cache_data.clear() # Reset cache to see new data
        st.success("GitHub Updated!")
        # st.rerun()

if "ChosenDen" not in st.session_state:
    st.session_state.ChosenDen = "All"

if "L1_car" not in st.session_state:
    st.session_state.L1_car = "000"
if "L2_car" not in st.session_state:
    st.session_state.L2_car = "000"
if "L3_car" not in st.session_state:
    st.session_state.L3_car = "000"
if "L4_car" not in st.session_state:
    st.session_state.L4_car = "000"

if "L1_EN" not in st.session_state:
    st.session_state.L1_EN = True
if "L2_EN" not in st.session_state:
    st.session_state.L2_EN = True
if "L3_EN" not in st.session_state:
    st.session_state.L3_EN = True
if "L4_EN" not in st.session_state:
    st.session_state.L4_EN = True

if "Loss_L1" not in st.session_state:
    st.session_state.Loss_L1 = False
if "Loss_L2" not in st.session_state:
    st.session_state.Loss_L2 = False
if "Loss_L3" not in st.session_state:
    st.session_state.Loss_L3 = False
if "Loss_L4" not in st.session_state:
    st.session_state.Loss_L4 = False

if "Den4add" not in st.session_state:
    st.session_state.Den4add = "Lion"


def load_racers(df):
    # 1. Filter data
    if st.session_state.ChosenDen == 'All':
        den_df = df
    else:
        den_df = df[df['Den'] == st.session_state.ChosenDen]
    
    active_df = den_df[den_df['Losses'] < 3].copy()
    num_cars_available = len(active_df)

    if num_cars_available <= 1:
        st.error('There is a winner, add more cars!')
        return
    
    # 2. Adjust active lanes based on car count
    lane_keys = ["L1_EN", "L2_EN", "L3_EN", "L4_EN"]
    current_checked_lanes = sum([st.session_state[k] for k in lane_keys])
    
    if current_checked_lanes > num_cars_available:
        for key in reversed(lane_keys):
            if st.session_state[key]:
                st.session_state[key] = False
                current_checked_lanes -= 1
            if current_checked_lanes <= num_cars_available:
                break

    # 3. Select the pool of cars for this heat
    # First, get cars with the absolute minimum number of total races
    min_races = active_df['Races'].min()
    pool_df = active_df[active_df['Races'] == min_races]
    
    if len(pool_df) >= current_checked_lanes:
        cars_to_race_df = pool_df.sample(current_checked_lanes)
    else:
        # If not enough "minimum race" cars, grab others and sample to fill the gap
        others_df = active_df[active_df['Races'] > min_races]
        fill_needed = current_checked_lanes - len(pool_df)
        fill_df = others_df.sample(fill_needed)
        cars_to_race_df = pd.concat([pool_df, fill_df], ignore_index=True)

    # 4. Assign to lanes (Prioritizing car with fewest runs in THAT specific lane)
    # We use a temporary list to track who is already assigned
    for lane_num in range(1, 5):
        en_key = f"L{lane_num}_EN"
        car_key = f"L{lane_num}_car"
        lane_col = f"L{lane_num}" # Assumes columns L1, L2, L3, L4 exist in your CSV
        
        if st.session_state[en_key] and not cars_to_race_df.empty:
            # Sort the remaining pool by who has used THIS lane the least
            cars_to_race_df = cars_to_race_df.sort_values(by=lane_col, ascending=True)
            
            # Pick the top car
            picked_car = cars_to_race_df.iloc[0]
            st.session_state[car_key] = str(picked_car["ID"])
            
            # Remove them from the pool for the next lane assignment in this heat
            cars_to_race_df = cars_to_race_df.iloc[1:]
        else:
            st.session_state[car_key] = "000"

def finish_race(df): 
    race_results = [
        (st.session_state.L1_car, st.session_state.Loss_L1, "L1", "L1_Loss"),
        (st.session_state.L2_car, st.session_state.Loss_L2, "L2", "L2_Loss"),
        (st.session_state.L3_car, st.session_state.Loss_L3, "L3", "L3_Loss"),
        (st.session_state.L4_car, st.session_state.Loss_L4, "L4", "L4_Loss")
    ]

    for car_id, is_loss, lane_col, lane_loss in race_results:
        if car_id == "000":
            continue
        matching_rows = df[df["ID"].astype(str) == str(car_id)].index

        if not matching_rows.empty:
            idx = matching_rows[0]
            # Always increment 'Races' count
            df.at[idx, "Races"] += 1
            # 2. Increment the specific lane (L1, L2, L3, or L4)
            df.at[idx, lane_col] += 1
            # Only increment 'Losses' if the checkbox was checked
            if is_loss:
                df.at[idx, "Losses"] += 1
                df.at[idx, lane_loss] += 1

    st.session_state.Loss_L1 = False
    st.session_state.Loss_L2 = False
    st.session_state.Loss_L3 = False
    st.session_state.Loss_L4 = False 
    return df

def handle_finish_race_logic(current_df):
    updated_df = finish_race(current_df)
    save_to_github(updated_df)
    load_racers(updated_df)



# Initial Load
df, file_sha = load_github_data()

for col in ["Losses", "Races", 
            "L1", "L2", "L3", "L4",
            "L1_Loss", "L2_Loss", "L3_Loss", "L4_Loss"]:
    if col not in df.columns:
        df[col] = 0

st.subheader(" Lanes ")
st.checkbox ("Lane1 active", key = "L1_EN")
st.checkbox ("Lane2 active", key = "L2_EN")
st.checkbox ("Lane3 active", key = "L3_EN")
st.checkbox ("Lane4 active", key = "L4_EN")

lane_btn1, lane_btn2 = st.columns([1,1], gap = 'xxsmall' ,vertical_alignment = 'center')
with lane_btn1:
    st.button ("SetLanes", on_click=load_racers, args=(df,))

with lane_btn2:
    st.button("FinishRace", on_click=handle_finish_race_logic, args=(df,))
    # if st.button ("FinishRace"):
    #     df = finish_race(df)
    #     save_to_github(df)
    #     load_racers(df)
        

st.text_input( "Lane 1", key="L1_car", label_visibility='collapsed', disabled=False)
st.text_input( "Lane 2", key="L2_car", label_visibility='collapsed', disabled=False)
st.text_input( "Lane 3", key="L3_car", label_visibility='collapsed', disabled=False)
st.text_input( "Lane 4", key="L4_car", label_visibility='collapsed', disabled=False)

st.checkbox ("Lane1 loss", key='Loss_L1')
st.checkbox ("Lane2 loss", key='Loss_L2')
st.checkbox ("Lane3 loss", key='Loss_L3')
st.checkbox ("Lane4 loss", key='Loss_L4')

st.divider()

# 3. Display the Data
st.subheader("Cars to race")
dd1, dd2 = st.columns(2)

with dd1:
    unique_vals = ['All', 'Lion', 'Tiger', 'Wolf', 'Bear', 'Webelo', 'Arrow', 'Open']
    
    # Calculate the index of the currently selected Den
    if st.session_state.ChosenDen in unique_vals:
        current_index = unique_vals.index(st.session_state.ChosenDen)
    else:
        current_index = 0

    selected_val = st.radio(
        "Select Den:",
        options=unique_vals,
        horizontal=True,
        index=current_index, # This keeps it "sticky"
        key="ChosenDen"
    )
    
    # selected_val = st.selectbox(f"Select Den", options=unique_vals, key="ChosenDen")
with dd2:
    enable_view_lost = st.checkbox ("View Eliminated", value= False)

if selected_val == 'All':
    den_df = df
else:
    den_df = df[df['Den']==selected_val]

if enable_view_lost:
    display_df = den_df
else:
    display_df = den_df[den_df['Losses'] < 3]

visible_columns = ["ID", "Name", "Den", "Races", "Losses", "L1", "L2", "L3", "L4"]
st.dataframe(display_df, column_order=visible_columns, width='stretch', hide_index=True)

st.divider()
# 4. Update Logic
st.subheader("Manual Adjust")

data_cols = [col for col in df.columns if col not in ["ID", "Name", "Den"]]
updateable_columns = ["All"] + data_cols

col_id, col_header = st.columns(2)

with col_id:
    id_options = ['All'] + list(display_df["ID"].unique())
    selected_id = st.selectbox("Select ID", id_options)

with col_header:
    selected_col = st.selectbox("Select Column", updateable_columns)

# --- LOGIC TO DEFINE TARGETS ---

# Identify target rows
if selected_id == 'All':
    target_indices = display_df.index.tolist()
else:
    target_indices = [df[df["ID"] == selected_id].index[0]]

# Identify target columns
if selected_col == 'All':
    target_cols = [c for c in df.columns if c in ["L1", "L2", "L3", "L4", "Races", "Losses"]]
else:
    target_cols = [selected_col]

# --- LOGIC TO DEFINE DISPLAY VALUE ---

if selected_id == 'All' or selected_col == 'All':
    current_val_display = "N/A (Bulk Update)"
else:
    current_val_display = df.at[target_indices[0], selected_col]

# Display string
st.write(f"Modifying **{selected_col}** for **{selected_id}**. Current: **{current_val_display}**")

# Action buttons 

btn1, btn2, btn3 = st.columns(3)

with btn1:
    if st.button("➕ Increase", use_container_width=True):
        for idx in target_indices:
            for col in target_cols:
                df.at[idx, col] += 1
        save_to_github(df)
        st.rerun()

with btn2:
    if st.button("➖ Decrease", use_container_width=True):
        for idx in target_indices:
            for col in target_cols:
                new_val = pd.to_numeric(df.at[idx, col]) -1
                df.at[idx, col] = max(0, new_val)
        save_to_github(df)
        st.rerun()

with btn3:
    if st.button("Reset", use_container_width=True):
        for idx in target_indices:
            for col in target_cols:
                df.at[idx, col] = 0
        save_to_github(df)
        st.rerun()

st.divider()
st.subheader("🛠️ Add/Remove Racers")

tab1, tab2 = st.tabs(["➕ Add New", "🗑️ Remove"])
Dens = ['Lion', 'Tiger', 'Wolf', 'Bear', 'Webelo', 'Arrow', 'Open']

with tab1:
    with st.form("add_form", clear_on_submit=True):
        new_id = st.text_input("New ID")
        new_name = st.text_input("Name")

        if st.session_state.Den4add in Dens:
            current_den_index = Dens.index(st.session_state.Den4add)
        else:
            current_den_index = 0
    
        new_cat = st.radio("Den", 
                options=Dens, 
                horizontal=True,
                index=current_den_index, 
                key="Den4add")
        
        # You can add default values for your L1, L2 fields here
        if st.form_submit_button("Add to List"):
            if new_id and new_id not in df["ID"].values:
                # Create the new row
                new_row = pd.DataFrame([{
                    "ID": new_id, 
                    "Name": new_name, 
                    "Den": new_cat,
                    "Losses": 0, 
                    "Races": 0,
                    "L1": 0,
                    "L2": 0,
                    "L3": 0,
                    "L4": 0
                }])

                # Combine and save
                updated_df = pd.concat([df, new_row], ignore_index=True)
                save_to_github(updated_df)
                st.rerun()
            else:
                st.error("ID is either empty or already exists!")

with tab2:
    id_to_delete = st.selectbox("Select ID to Delete", df["ID"].unique(), index=None, placeholder="Choose an ID...")
    
    # Red button for deletion to warn the user
    if st.button("🔥 Permanently Delete Row", type="primary"):
        if id_to_delete:
            updated_df = df[df["ID"] != id_to_delete]
            save_to_github(updated_df)
        else:
            st.warning("Please select an ID first.")

st.divider()
st.subheader(" Lane Stats ")
target_cols = [c for c in df.columns if c in ["L1_Loss", "L2_Loss", "L3_Loss", "L4_Loss"]]
# Calculate the sums for all cars currently in the dataframe
l1_total = df["L1_Loss"].sum()
l2_total = df["L2_Loss"].sum()
l3_total = df["L3_Loss"].sum()
l4_total = df["L4_Loss"].sum()

# Display them in 4 nice columns
m1, m2, m3, m4 = st.columns(4)
m1.metric("Lane 1", f"{l1_total} ❌")
m2.metric("Lane 2", f"{l2_total} ❌")
m3.metric("Lane 3", f"{l3_total} ❌")
m4.metric("Lane 4", f"{l4_total} ❌")

if st.button("Clear All Lane Loss Totals", type="primary", use_container_width=True):
    # 1. Targeted columns to reset
    loss_cols = ["L1_Loss", "L2_Loss", "L3_Loss", "L4_Loss"]
    
    # 2. Update every row in the dataframe to 0 for these columns
    df[loss_cols] = 0
    
    # 3. Save the blanked-out data to GitHub
    save_to_github(df, commit_message="Reset all lane loss statistics")
    
    st.warning("All lane loss columns have been reset to zero.")
    st.rerun()
    
