import streamlit as st

# Assuming the ChefsHatEnv and ChefsHatRoomServer are imported correctly
from ChefsHatGym.gameRooms.chefs_hat_room_server import ChefsHatRoomServer
from ChefsHatGym.env import ChefsHatEnv
import os
import threading

from opponents_list import agents_list, not_show_parameters
import time
import inspect


from typing import get_origin, get_args, Literal


def create_opponent_input_fields(i, opponent_class):
    init_signature = inspect.signature(opponent_class.__init__)
    
    for param_name, param in init_signature.parameters.items():
        if param_name != 'self' and param_name not in not_show_parameters:
            param_type = param.annotation
            
            if param_type == bool:
                add_opponents[f"opponent_{i+1}"]["params"][param_name] = st.selectbox(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    options=[True, False],
                    key=f"opponent_{i+1}_{param_name}"
                )
            elif param_type == float:
                add_opponents[f"opponent_{i+1}"]["params"][param_name] = st.slider(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    min_value=0.0,
                    max_value=1.0,
                    value=param.default if param.default != inspect.Parameter.empty else 0.5,
                    key=f"opponent_{i+1}_{param_name}"
                )
            elif get_origin(param_type) is Literal:
                literal_options = get_args(param_type)
                add_opponents[f"opponent_{i+1}"]["params"][param_name] = st.selectbox(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    options=literal_options,
                    index=literal_options.index(param.default) if param.default in literal_options else 0,
                    key=f"opponent_{i+1}_{param_name}"
                )
            else:
                add_opponents[f"opponent_{i+1}"]["params"][param_name] = st.text_input(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    value=param.default if param.default != inspect.Parameter.empty else "",
                    key=f"opponent_{i+1}_{param_name}"
                )


def add_players(opponents, log_directory, room_url, room_port):
    # print (f"opponents: {opponents}")
    try:
        for key, opponent_info in opponents.items():
            opponent_class = opponent_info['class']
            opponent_params = opponent_info['params']
            opponent_params["name"] = opponent_info["name"]
            opponent_params["logDirectory"] = log_directory
            opponent_params["verbose"] = True                    
            # Create an instance of the class with the given parameters

            # print (f"Creating this player: {opponent_info['name']}")
            # print (f" --- Params: {opponent_params}")
            opponent_instance = opponent_class(**opponent_params)
            # print (f" --- Instance: {opponent_instance}")

            
            # Store the instance if needed
            # opponent_instances[key] = opponent_instance

            opponent_instance.joinGame(room_pass=room_pass, room_url=room_url, room_port=int(room_port))
            # print (f" --- Added to the game room: {room_url}:room_port - pass: {room_pass}")
            
    except Exception as e:
        raise e

def start_room_thread(room):       
    room.start_room()



script_directory = os.path.dirname(os.path.abspath(__file__))

st.title("Create New ChefsHat Room")

st.subheader("Room Information")
# Room Information
col1, col2 = st.columns(2)
with col1:
    room_name = st.text_input("Room Name", value="", help="Name of the room. No special characters allowed.")
    room_url = st.text_input("Room URL", value="localhost")

with col2:
    room_pass = st.text_input("Room Password", type="password", value="")
    room_port = st.text_input("Room Port", value="10000")

st.markdown("---")
st.subheader("Choose Opponents")
st.write("Need more information about the opponent types? Find here: https://github.com/pablovin/ChefsHatPlayersClub")
columns = st.columns(4)

# Iterate over the four opponent slots
opponents_parameters = {}
add_opponents = {}

for i in range(4):
    with columns[i]:
        add_opponent = st.checkbox(f"Run Player {i + 1} Local")
        if add_opponent:
            
            add_opponents[f"opponent_{i+1}"] = {}

            add_opponents[f"opponent_{i+1}"]["type"] = st.selectbox(f"Player {i + 1} Type", options=list(agents_list.keys()))                      
            add_opponents[f"opponent_{i+1}"]["name"] = st.text_input(f"Player {i + 1} Name", value=f"{add_opponents[f'opponent_{i+1}']['type']}_{i+1}")                                    
                        

            add_opponents[f"opponent_{i+1}"]["params"] = {}

            opponent_type = add_opponents[f"opponent_{i+1}"]["type"]
            opponent_class = agents_list[opponent_type]['class']

            add_opponents[f"opponent_{i+1}"]["class"] = opponent_class

            create_opponent_input_fields(i, opponent_class)
        else:
            add_opponents.pop(f"opponent_{i+1}", None)

        


st.markdown("---")
# Game settings
st.subheader("Game Settings")
col1, col2 = st.columns(2)
with col1:
    stop_criteria = st.number_input("Stop Criteria", value=1)
    max_rounds = st.number_input("Maximum Rounds (Choose -1 to not define a max)", value=-1)
with col2:
    game_type = st.selectbox("Game Type", options=["MATCHES", "POINTS"], index=0)    
    timeout_player_subscribers = st.number_input("Timeout Player Subscribers (seconds)", value=30)
    timeout_player_response = st.number_input("Timeout Player Response (seconds)", value=5)

st.markdown("---")
# Submit button
if st.button("Create Room"):
    if room_name:        
        if "rooms" not in st.session_state:
            st.session_state["rooms"] = {}
        
        if room_name not in st.session_state["rooms"]:            
            try:
                room  = ChefsHatRoomServer(
                    room_name=room_name,
                    room_pass=room_pass,
                    room_url=room_url,
                    room_port=int(room_port),
                    game_type=ChefsHatEnv.GAMETYPE[game_type],
                    stop_criteria=int(stop_criteria),
                    max_rounds=int(max_rounds),
                    verbose_console=False,
                    verbose_log=True,
                    game_verbose_console=False,
                    game_verbose_log=True,
                    save_dataset=True,
                    log_directory=f"{script_directory}/temp",
                    timeout_player_subscribers=int(timeout_player_subscribers),
                    timeout_player_response=int(timeout_player_response),
                )                
            except Exception as e:
                raise e
            
            st.session_state["rooms"][room_name] = room

            room_thread = threading.Thread(
                target=start_room_thread,
                args=[room]
                )
            
            room_thread.start()

            time.sleep(5)

            if len(add_opponents) > 0:                
                log_directory = room.get_log_directory()
                players_thread = threading.Thread(
                    target=add_players,
                    args=(add_opponents, log_directory, room_url, room_port)
                        )
                
                players_thread.start()


            # Store the thread in session state if you want to keep track of it
            st.session_state[f"{room_name}_thread"] = room_thread

            st.success(f"Room '{room_name}' created successfully and is running in a separate thread!")
        else:
            st.error("Room name already exists!")
    else:
        st.error("Room name is required!")