import streamlit as st
import os
import time
import re
import matplotlib.pyplot as plt
import zipfile
from io import BytesIO
import shutil
from utils import temp_directory
import pandas as pd
import altair as alt

plt.rcParams['font.size'] = 15

def extract_info_from_log(log_content, pattern):
    match = re.search(pattern, log_content)
    return match.group(1) if match else None

def parse_players(log_content):
    pattern = r"INFO\s+Players\s+:(\[.*?\])"
    match = re.search(pattern, log_content)
    return eval(match.group(1)) if match else []

def parse_scores(log_content, match_number):
    pattern = rf"INFO\s+Match {match_number} over! Current Score:\[(.*?)\]"
    match = re.search(pattern, log_content)
    return list(map(int, match.group(1).split(','))) if match else []

def extract_stop_criteria(log_content):
    pattern = r"INFO\s+Stop Criteria\s+:+(\d+\s+\w+)"
    match = re.search(pattern, log_content)
    return match.group(1) if match else None

def extract_last_match_number(log_content):
    match_numbers = re.findall(r"INFO\s+Match Number (\d+\.\d+) Starts!", log_content)
    return match_numbers[-1] if match_numbers else None

def parse_last_scores(log_content, match_number):
    pattern = rf"Current Score:\[(.*?)\]"
    scores_list = re.findall(pattern, log_content)
    return list(map(int, scores_list[-1].split(','))) if scores_list else []

def parse_last_players(log_content):
    player_lists = re.findall(r"INFO\s+Players\s+:(\[.*?\])", log_content)
    return eval(player_lists[-1]) if player_lists else []

def zip_directory(directory):
    """Zips the contents of the directory."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer


# Ensure that 'rooms' exists in session state
# if "rooms" not in st.session_state:
#     st.session_state["rooms"] = {}


st.write("# See Rooms tool! :globe_with_meridians:")
st.write("Here you can get a live glance on the room\\`s status, and find out when the room finished its game.")

# Sidebar: List all room names
st.sidebar.title("Select a Room")
                 # Directory where room folders are stored

# Get all folder names inside the temp/ directory
if os.path.exists(temp_directory):
    room_names = [name for name in os.listdir(temp_directory)]
else:
    room_names = []


# room_names = [room.get_room_name() for room in st.session_state["rooms"].values()]

st.sidebar.write("The list only show rooms creted with the Create New Room tool.")

# Display the list of rooms in the sidebar
selected_room_name = st.sidebar.selectbox("Available Rooms", room_names)

if selected_room_name:
    # room = next(room for room in st.session_state["rooms"].values() if room.get_room_name() == selected_room_name)
    
    

    # Get the log directory for the selected room
    log_directory = os.path.join(temp_directory,selected_room_name)        
    game_log_file = os.path.join(log_directory, "Log", "Log.log")    
    
    delete_button = st.sidebar.button("Delete Room!")
    
    if delete_button:
        st.sidebar.error("This will permantently delete all data of this room, do you want to continue?")
        st.session_state["delete_button"] = True        
    
    if "delete_button" in st.session_state and st.session_state.delete_button:
         delete_confirm = st.sidebar.button("Confirm delete")
         if delete_confirm:
            st.session_state["delete_confirm"] = True

    if "delete_confirm" in st.session_state and st.session_state.delete_confirm:
        print (f"Deleting: {log_directory}")
        shutil.rmtree(log_directory)
        st.session_state["delete_confirm"] = False
        st.session_state["delete_button"] = False
        st.rerun()



    # Main area: Display room and game activity
    st.markdown("---")
    st.header(f"Room: {selected_room_name}")
        
    st.write(f"**Room Log Directory:** {log_directory}")    
    
    col1, col2 = st.columns(2)
    with col1:
        stop_criteria_placeholder = st.empty()
    with col2:
        max_rounds_placeholder = st.empty()    

    room_status = st.empty()
    download_button_st = st.empty()


    # Header information
    stop_criteria = None
    max_rounds = None
    match_number = None
    players = []
    scores = []
  
    st.markdown("---")
    st.subheader("Current Game Status")
    match_number_placeholder = st.empty()
    
    plot_placeholder = st.empty()
        
    # Continuously update logs
    while True:
        # Read game activity log
        if os.path.exists(game_log_file):
            with open(game_log_file, "r") as f:
                game_log_content = f.read()
                
                #Extract game status

                game_dataset = os.path.join(log_directory, "Datasets", "Dataset.pkl")    
                if os.path.exists(game_dataset):
                    room_status.success("Room Status: Finished")
                    zip_file_buffer = zip_directory(log_directory)
                    basename = os.path.basename(log_directory)
                    download_button_st.download_button(label="Download Room Logs",
                                                    data=zip_file_buffer,
                                                    file_name=f"{basename}.zip",
                                                    mime="application/zip")
                else:
                    room_status.error("Room Status: Ongoing")


                # Extract Stop Criteria
                stop_criteria = stop_criteria = extract_stop_criteria(game_log_content)
                if stop_criteria:
                    stop_criteria_placeholder.text(f"Stop Criteria: {stop_criteria}")
                
                # Extract Max Rounds
                max_rounds = extract_info_from_log(game_log_content, r"INFO\s+Max Rounds\s+:+(-?\d+)")
                if max_rounds:
                    max_rounds_placeholder.text(f"Max Rounds: {max_rounds}")
                
                match_number = extract_last_match_number(game_log_content)
                if match_number:
                    match_number_placeholder.text(f"Current Match Number: {match_number}")


                scores = parse_last_scores(game_log_content, match_number)
                players = parse_last_players(game_log_content)      
                if len(scores) == len(players):
                    df = pd.DataFrame({"players":players, "scores":scores})
                    print (f"scores: {scores}")
                    print (f"players: {players}")
                    print (f"DF: {df}")
                    chart_height = len(df) * 100  # 40 pixels per player, adjust as needed

                    # Create a horizontal bar chart using Altair
                    bar_chart = alt.Chart(df).mark_bar().encode(
                        x=alt.X('scores:Q', title='Scores'),
                        y=alt.Y('players:N', sort='-x', title='Players', axis=alt.Axis(labelFontSize=10)),
                    ).properties(
                        title='Scores by Player',
                        height=chart_height  # Set the height of the chart
                    )
                    text = bar_chart.mark_text(
                        align='left',
                        baseline='middle',
                        dx=3  # Adjusts the position of the text
                    ).encode(
                        text='scores:Q'
                    )

                    final_chart = bar_chart + text
                    plot_placeholder.altair_chart(final_chart, use_container_width=True)
                                        
                    # plot_placeholder.bar_chart(data=df, x="players", y="scores")
                # Extract relevant data

                # if players and scores:
                #     # Plotting the bar graph
                #     plt.figure(figsize=(15, 4))
                #     plt.bar(players, scores)
                #     plt.xlabel('Players')
                #     plt.ylabel('Scores')
                #     plt.title('Current Scores')
                #     for i, score in enumerate(scores):
                #         plt.text(i, score + 0.5, f'{score}', ha='center', va='bottom')

                #     plt.tight_layout()
                #     plot_placeholder.pyplot(plt)  # Display the graph

                #     # Clear the plot to prevent old plots from being displayed
                #     plt.clf()


                # Check if the game is over
                if "INFO     Game Over!" in game_log_content:
                    st.success("Game Over! Stopping updates.")
                    break
        
        # Wait for 3 second before updating again
        time.sleep(1)
else:
    st.markdown('---')
    st.write("No room found!")        
    st.write("Use the Create New Room tool on the side menu to create a room.")        