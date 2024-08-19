import streamlit as st

# Assuming the ChefsHatEnv and ChefsHatRoomServer are imported correctly
from ChefsHatGym.gameRooms.chefs_hat_room_server import ChefsHatRoomServer
from ChefsHatGym.env import ChefsHatEnv
import threading

from opponents_list import agents_list, spectators_list, not_show_parameters
import time
import inspect
from utils import temp_directory

from typing import get_origin, get_args, Literal



def create_opponent_input_fields(i, suffix, opponent_class):
    init_signature = inspect.signature(opponent_class.__init__)
    
    for param_name, param in init_signature.parameters.items():
        if param_name != 'self' and param_name not in not_show_parameters:
            param_type = param.annotation            
            if param_type == bool:
                add_opponents[f"{suffix}_{i+1}"]["params"][param_name] = st.selectbox(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    options=[False, True],
                    key=f"{suffix}_{i+1}_{param_name}"
                )
            elif param_type == float:
                add_opponents[f"{suffix}_{i+1}"]["params"][param_name] = st.slider(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    min_value=0.0,
                    max_value=1.0,
                    step =0.1,
                    value=float(param.default) if param.default != inspect.Parameter.empty else 0.5,
                    key=f"{suffix}_{i+1}_{param_name}"
                )
            elif get_origin(param_type) is Literal:
                literal_options = get_args(param_type)
                add_opponents[f"{suffix}_{i+1}"]["params"][param_name] = st.selectbox(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    options=literal_options,
                    index=literal_options.index(param.default) if param.default in literal_options else 0,
                    key=f"{suffix}_{i+1}_{param_name}"
                )
            else:
                add_opponents[f"{suffix}_{i+1}"]["params"][param_name] = st.text_input(
                    f"{param_name} (required)" if param.default == inspect.Parameter.empty else f"{param_name} (default: {param.default})",
                    value=param.default if param.default != inspect.Parameter.empty else "",
                    key=f"{suffix}_{i+1}_{param_name}"
                )

def join_spectators(spectators, log_directory, room_url, room_port):
    # print (f"opponents: {opponents}")
    try:
        for key, opponent_info in spectators.items():
            spectator_class = opponent_info['class']
            spectator_params = opponent_info['params']
            spectator_params["name"] = opponent_info["name"]
            spectator_params["log_directory"] = log_directory
            spectator_params["verbose_log"] = True                    
            spectator_params["verbose_console"] = False                    
            # Create an instance of the class with the given parameters

            # print (f"Creating this player: {opponent_info['name']}")
            # print (f" --- Params: {opponent_params}")
            spectator_instance = spectator_class(**spectator_params)
            # print (f" --- Instance: {opponent_instance}")

            spectator_instance.joinGame(room_pass=room_pass, room_url=room_url, room_port=int(room_port))
            # print (f" --- Added to the game room: {room_url}:room_port - pass: {room_pass}")
            
    except Exception as e:
        raise e
    
def join_players(opponents, log_directory, room_url, room_port):
    # print (f"opponents: {opponents}")
    try:
        for key, opponent_info in opponents.items():
            opponent_class = opponent_info['class']
            opponent_params = opponent_info['params']
            opponent_params["name"] = opponent_info["name"]
            opponent_params["log_directory"] = log_directory
            opponent_params["verbose_log"] = True                    
            opponent_params["verbose_console"] = False      

            # Create an instance of the class with the given parameters

            # print (f"Creating this player: {opponent_info['name']}")
            # print (f" --- Params: {opponent_params}")
            opponent_instance = opponent_class(**opponent_params)
            # print (f" --- Instance: {opponent_instance}")

            opponent_instance.joinGame(room_pass=room_pass, room_url=room_url, room_port=int(room_port))
            # print (f" --- Added to the game room: {room_url}:room_port - pass: {room_pass}")
            
    except Exception as e:
        raise e

def start_room_thread(room):       
    room.start_room()


# st.title("Create New ChefsHat Room")

st.write("# New Room tool! :black_joker: ")
st.write("Here you can create a new Chef`\\s Hat room, populate it with different Players and Spectators and start your experiments! And everything without a line of code :D")
st.write("All the rooms you create here will be run as a server, meaning you can connect to them also from another computer. Imagine the possibilities ;)")

st.subheader("First, let`s start setting up the room information:")
# Room Information
col1, col2 = st.columns(2)
with col1:
    room_name = st.text_input("Room Name", value="", help="Name of the room. No special characters allowed. Room Names must be unique.")
    room_url = st.text_input("Room URL", value="localhost")

with col2:
    room_pass = st.text_input("Room Password", type="password", value="")
    room_port = st.text_input("Room Port", value="10000")

st.markdown("---")
# Game settings
st.subheader("Second, set some basic game settings:")
col1, col2, col3 = st.columns(3)

with col1:
    stop_criteria = st.number_input("Stop Criteria", value=1)
with col2:
    game_type = st.selectbox("Game Type", options=["MATCHES", "POINTS"], index=0)    
with col3:
    max_rounds = st.number_input("Max Rounds (-1 for no max rounds)", value=-1)

st.markdown("---")
st.subheader("Third, select if you want to run any Player locally:")
st.write("Running a player localy means that the Player will run from this machine, and be automatically added to the game. Remember, a **game needs 4 players**. If you do not add all four Players locally, they need to connect to the **room remotely**.")
st.sidebar.subheader("Need Help?")
st.sidebar.write("You have no idea what all these parameters are? Check our [Room Page](https://chefshatgym.readthedocs.io/en/latest/04_rooms.html).")
st.sidebar.write("Need more information about the Player types? Check the [Player\\`s Club](https://github.com/pablovin/ChefsHatPlayersClub)")
st.sidebar.write("What are Spectators? Check the [Spectator Page](https://chefshatgym.readthedocs.io/en/latest/07_spectators.html)")

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

            create_opponent_input_fields(i, "opponent", opponent_class)
        else:
            add_opponents.pop(f"opponent_{i+1}", None)

        
st.markdown("---")
st.subheader("Finnaly, Add some Spectators if you need them:")
st.write("Spectators are optional, and you can run a game without any of them. You can always connect Spectators remotely at any time.")
columns = st.columns(4)

# Iterate over the four opponent slots
opponents_parameters = {}
add_spectators = {}

for i in range(4):
    with columns[i]:
        add_spectator = st.checkbox(f"Run Spectator {i + 1} Local")
        if add_spectator:
            
            add_spectators[f"spectator_{i+1}"] = {}

            add_spectators[f"spectator_{i+1}"]["type"] = st.selectbox(f"spectator_ {i + 1} Type", options=list(spectators_list.keys()))                      
            add_spectators[f"spectator_{i+1}"]["name"] = st.text_input(f"spectator_ {i + 1} Name", value=f"{add_spectators[f'spectator_{i+1}']['type']}_{i+1}")                                    
                        
            add_spectators[f"spectator_{i+1}"]["params"] = {}

            spectator_type = add_spectators[f"spectator_{i+1}"]["type"]
            spectator_class = spectators_list[spectator_type]['class']

            add_spectators[f"spectator_{i+1}"]["class"] = spectator_class

            create_opponent_input_fields(i, "spectator", spectator_class)
        else:
            add_spectators.pop(f"spectator_{i+1}", None)




st.markdown("---")
# Submit buttons
st.subheader("Now you are ready to create your room!")
col1, col2, col3 = st.columns(3)
with col2:
    button_create_room = st.button("**Create Room**")

if button_create_room:
    if room_name:                
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
                    log_directory=temp_directory,
                    timeout_player_response=120,
                    timeout_player_subscribers=120
                )                
          
            
                # st.session_state["rooms"][room_name] = room

                room_thread = threading.Thread(
                    target=start_room_thread,
                    args=[room]
                    )
                
                room_thread.start()

                time.sleep(5)
                if len(add_spectators) > 0:                
                    log_directory = room.get_log_directory()
                    spectators_thread = threading.Thread(
                        target=join_spectators,
                        args=(add_spectators, log_directory, room_url, room_port)
                            )                
                    spectators_thread.start()
                
                if len(add_opponents) > 0:                
                    log_directory = room.get_log_directory()
                    players_thread = threading.Thread(
                        target=join_players,
                        args=(add_opponents, log_directory, room_url, room_port)
                            )
                    
                    players_thread.start()


                # Store the thread in session state if you want to keep track of it
                # st.session_state[f"{room_name}_thread"] = room_thread

                st.success(f"Room '{room_name}' created! Check the Online Rooms tool!")
            except Exception as e:
                raise e

    else:
        st.error("Room name is required!")