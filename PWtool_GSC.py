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

# Initial Load
df, file_sha = load_github_data()



st.subheader(" Lanes ")

enable_L1 = st.checkbox ("Lane1_EN", value= True)
enable_L2 = st.checkbox ("Lane2_EN", value= True)
enable_L3 = st.checkbox ("Lane3_EN", value= True)
enable_L4 = st.checkbox ("Lane4_EN", value= True)

st.divider()
# 3. Display the Data
st.subheader("Current Data (from GitHub)")
st.dataframe(df, width='stretch', hide_index=True)



# 4. Update Logic
st.subheader("Update Values")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_id = st.selectbox("Select ID to Update", df["ID"].unique())

# Find the row and current value
current_row_index = df[df["ID"] == selected_id].index[0]
current_val = df.at[current_row_index, "L1"]

st.write(f"Current Value for ID {selected_id}: **{current_val}**")

# Helper function to push to GitHub
def save_to_github(updated_df):
    with st.spinner("Pushing changes to GitHub..."):
        auth = Auth.Token(TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        csv_content = updated_df.to_csv(index=False)
        repo.update_file(
            path=FILE_PATH,
            message=f"Updated ID {selected_id} via Streamlit App",
            content=csv_content,
            sha=file_sha
        )
        st.cache_data.clear() # Reset cache to see new data
        st.success("GitHub Updated!")

with col2:
    if st.button("➕ Increase"):
        df.at[current_row_index, "L1"] = current_val + 1
        save_to_github(df)
        st.rerun()

with col3:
    if st.button("➖ Decrease"):
        df.at[current_row_index, "L1"] = current_val - 1
        save_to_github(df)
        st.rerun()