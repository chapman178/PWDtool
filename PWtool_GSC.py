import streamlit as st
import pandas as pd
from github import Github, Auth
import io


st.markdown("""
    <style>
    /* 1. Reduce the gap between columns */
    [data-testid="column"] {
        width: min-content !important;
        flex-basis: auto !important;
        min-width: 0px !important;
    }
    
    /* 2. Shrink the gap between elements (checkboxes/inputs) */
    [data-testid="stVerticalBlock"] > div {
        gap: 0.2rem !important;
    }

    /* 3. Remove padding from the main container */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* 4. Force Checkboxes to occupy almost zero extra width */
    [data-testid="stCheckbox"] {
        width: fit-content !important;
    }
    [data-testid="stCheckbox"] > label {
        width: fit-content !important;
        margin-right: -15px !important; /* Pulls the next element closer */
    }
    </style>
    """, unsafe_allow_html=True)

# Set up the page
st.set_page_config(page_title="PWD Tool", layout="wide")
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
        st.rerun()

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

if "Ln1_EN" not in st.session_state:
    st.session_state.Ln1_EN = True
if "Ln2_EN" not in st.session_state:
    st.session_state.Ln2_EN = True
if "L3_EN" not in st.session_state:
    st.session_state.Ln3_EN = True
if "Ln4_EN" not in st.session_state:
    st.session_state.Ln4_EN = True

if "Loss_L1" not in st.session_state:
    st.session_state.Loss_L1 = False
if "Loss_L2" not in st.session_state:
    st.session_state.Loss_L2 = False
if "Loss_L3" not in st.session_state:
    st.session_state.Loss_L3 = False
if "Loss_L4" not in st.session_state:
    st.session_state.Loss_L4 = False

# def load_racers(df, ChosenDen):
#     if ChosenDen == 'All':
#         den_df = df
#     else:
#         den_df = df[df['Den']==ChosenDen]
#     active_df = den_df[den_df['Losses'] < 3]

#     # if number of active cars is less than number of active lanes adjust number of lanes
#     rws, cols = active_df.shape
#     if rws <=1:
#         st.write('There is a winner, add more cars!')
#         return
#     number_of_active_lanes = st.session_state.L1_EN + st.session_state.L2_EN + st.session_state.L3_EN + st.session_state.L4_EN
#     print(number_of_active_lanes)

# Initial Load
df, file_sha = load_github_data()

st.subheader(" Lanes ")
lane_btn1, lane_btn2, lane_bogus = st.columns([1,1,4], gap = 'xxsmall' ,vertical_alignment = 'center')
with lane_btn1:
    if st.button ("SetLanes"):
        # load_racers()
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L1_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L2_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L3_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L4_car = str(random_id)
with lane_btn2:
    if st.button ("RaceDone"):

        race_results = [
        (st.session_state.L1_car, st.session_state.Loss_L1),
            (st.session_state.L2_car, st.session_state.Loss_L2),
            (st.session_state.L3_car, st.session_state.Loss_L3),
            (st.session_state.L4_car, st.session_state.Loss_L4)
        ]

        for car_id, is_loss in race_results:
            if car_id == "000":
                continue
            matching_rows = df[df["ID"].astype(str) == str(car_id)].index

            if not matching_rows.empty:
                idx = matching_rows[0]
                # Always increment 'Races' count
                df.at[idx, "Races"] += 1
                # Only increment 'Losses' if the checkbox was checked
                if is_loss:
                    df.at[idx, "Losses"] += 1

        random_id = df["ID"].sample().iloc[0]
        st.session_state.L1_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L2_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L3_car = str(random_id)
        random_id = df["ID"].sample().iloc[0]
        st.session_state.L4_car = str(random_id)
        save_to_github(df)



lca1, lcb1, lcc1 = st.columns([1,5,1], gap = 'xxsmall' ,vertical_alignment = 'center')
with lca1:
    st.checkbox ("L1_EN", key = "Ln1_EN")
with lcb1:
    st.text_input( "Lane 1", key="L1_car", label_visibility='collapsed', disabled=False)
with lcc1:
    st.checkbox ("Ln1_loss", key='Loss_L1')

lca2, lcb2, lcc2 = st.columns([1,5,1], gap = 'small' ,vertical_alignment = 'center')
with lca2:
    st.checkbox ("L2_EN", key = "Ln2_EN")
with lcb2:
    st.text_input( "Lane 2", key="L2_car", label_visibility='collapsed', disabled=False)  
with lcc2:
    st.checkbox ("Ln2_loss", key='Loss_L2') 

lca3, lcb3, lcc3 = st.columns([1,5,1], gap = 'small' ,vertical_alignment = 'center')
with lca3:
    st.checkbox ("L3_EN", key = "Ln3_EN")
with lcb3:
    st.text_input( "Lane 3", key="L3_car", label_visibility='collapsed', disabled=False)
with lcc3:
    st.checkbox ("Ln3_loss", key='Loss_L3')

lca4, lcb4, lcc4 = st.columns([1,5,1], gap = 'small' ,vertical_alignment = 'center')
with lca4:
    st.checkbox ("L4_EN", key = "Ln4_EN")
with lcb4:
    st.text_input( "Lane 4", key="L4_car", label_visibility='collapsed', disabled=False)
with lcc4:
    st.checkbox ("Ln4_loss", key='Loss_L4')


print(st.session_state.ChosenDen)

st.divider()

# 3. Display the Data
st.subheader("Cars to race")
dd1, dd2 = st.columns(2)

with dd1:
    unique_vals = ['All', 'Lion', 'Tiger', 'Wolf', 'Bear', 'Webelo', 'Arrow', 'Open']
    selected_val = st.selectbox(f"Select Den", options=unique_vals, key="ChosenDen")
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

st.dataframe(display_df, width='stretch', hide_index=True)

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
    target_cols = data_cols # This uses the list of real column names
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

with btn2:
    if st.button("➖ Decrease", use_container_width=True):
        for idx in target_indices:
            for col in target_cols:
                new_val = pd.to_numeric(df.at[idx, col]) -1
                df.at[idx, col] = max(0, new_val)
        save_to_github(df)

with btn3:
    if st.button("Reset", use_container_width=True):
        for idx in target_indices:
            for col in target_cols:
                df.at[idx, col] = 0
        save_to_github(df)

st.divider()
st.subheader("🛠️ Add/Remove Racers")

tab1, tab2 = st.tabs(["➕ Add New", "🗑️ Remove"])
Dens = ['Lion', 'Tiger', 'Wolf', 'Bear', 'Webelo', 'Arrow', 'Open']

with tab1:
    with st.form("add_form", clear_on_submit=True):
        new_id = st.text_input("New ID")
        new_name = st.text_input("Name")
        new_cat = st.selectbox("Den", Dens)
        
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