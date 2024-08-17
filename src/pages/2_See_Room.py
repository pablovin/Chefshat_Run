import streamlit as st
import os
import time
import re

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

# Ensure that 'rooms' exists in session state
if "rooms" not in st.session_state:
    st.session_state["rooms"] = {}

# Sidebar: List all room names
st.sidebar.title("Select a Room")
room_names = [room.get_room_name() for room in st.session_state["rooms"].values()]

# Display the list of rooms in the sidebar
selected_room_name = st.sidebar.selectbox("Rooms", room_names)

if selected_room_name:
    room = next(room for room in st.session_state["rooms"].values() if room.get_room_name() == selected_room_name)
    
    # Get the log directory for the selected room
    log_directory = room.get_log_directory()
    game_log_file = os.path.join(log_directory, "Log", "Log.log")    
    
    # Main area: Display room and game activity
    st.title(f"Room: {selected_room_name}")
    st.write(f"Summary information from this room!")

    st.subheader(f"Logs saved here: {log_directory}")

    # Header information
    stop_criteria = None
    max_rounds = None
    match_number = None
    players = []
    scores = []

    st.markdown("---")
    st.subheader("Current Game Setting")

    # Placeholder for header information
    col1, col2 = st.columns(2)
    with col1:
        stop_criteria_placeholder = st.empty()
    with col2:
        max_rounds_placeholder = st.empty()    

    st.markdown("---")
    st.subheader("Current Game Status")
    match_number_placeholder = st.empty()
    
    cols = st.columns(4)  
    player_names = []
    player_scores= []

    for i in range(4):
        with cols[i]:            
            
            player_names.append(st.empty())
            player_scores.append(st.empty())
        
    st.markdown("---")
    st.subheader("Game Log")           
    game_activity = st.empty()
    

    # players_placeholder = st.empty()
    
    # # Columns for Room Activity and Game Activity
    # col1, col2 = st.columns(2)

    # # Placeholder to update the content dynamically
    # with col1:
    #     st.subheader("Room Activity")
    #     room_activity = st.empty()
    
    # with col2:
    #     st.subheader("Game Activity")
    #     game_activity = st.empty()

    # Continuously update logs
    while True:
        # Read game activity log
        if os.path.exists(game_log_file):
            with open(game_log_file, "r") as f:
                game_log_content = f.read()
                
                # st.markdown("---")
                # st.subheader("Game Setting")
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
                
                # st.markdown("---")
                # st.subheader("Game Status")
                # Extract Players
                

                print (f"Players: {players}")                      
                                                                   

                print (f"Scores: {scores}")     
                if players and scores:

                    player_data = []
                    for i, player_name in enumerate(players):
                        player_data.append({
                            "Player Position": i,
                            "Player Name": player_name,
                            "Player Score": scores[i] if i < len(scores) else 0
                        })


                    cols = st.columns(len(scores))         
                # Display players and scores
                                    
                    for i, player in enumerate(player_data):
                        player_names[i].text(f"Player {i + 1}: \n{player['Player Name']} ")
                        player_scores[i].text(f"Score: {player['Player Score']}")
                            

                # Update Room and Game Activity areas
                # room_activity.text_area("Room Log", game_log_content, height=400)
                game_activity.text_area("Game Log", game_log_content[-1000:], height=400)

                # Check if the game is over
                if "INFO     Game Over!" in game_log_content:
                    st.success("Game Over! Stopping updates.")
                    break
        
        # Wait for 3 second before updating again
        time.sleep(1)