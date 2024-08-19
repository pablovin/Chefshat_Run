import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Function to load data from a .pkl file
# @st.cache
def load_data(filepath):
    return pd.read_pickle(filepath)

# Streamlit page setup

st.write("# Explore Games tool! :game_die:")
st.write("Here you can get a summary of the agent\\`s behavior on an existing experiment. Load the .pkl dataset and this tool will generate a series of plots and metrics that can help you understand what happened in your game.")



# File uploader for user input
uploaded_file = st.file_uploader("Choose a PKL file", type="pkl")
if uploaded_file is not None:
    data = load_data(uploaded_file)
    if data.empty:
        st.write("No data found in the file.")
    else:
        st.write("Data Loaded Successfully!")

        nan_value = float("NaN") 
        data.replace("", nan_value, inplace=True)

        agent_names = data["Agent Names"].values[1].replace("[","").replace("]","").replace("'","").split(",")


        games = data['Game Number'].unique()

        #[game, player, score, maxrounds, passes, pizza]
        dataFrame = []
        index = 0
        for game in games:
            game_scores = data[(data['Game Number'] == game)]["Scores"].values[-1]  
            
            max_rounds = data[(data['Game Number'] == game)].dropna(subset="Round Number")
            max_rounds = max_rounds.groupby("Player")["Round Number"].max()

            total_pass = data[(data['Action Type'] == 'PASS') & (data['Game Number'] == game) ].groupby('Player').size()            

            for player_index in range(len(agent_names)):                 
                this_game_frame = {}
                this_game_frame["Game"] = game
                this_game_frame["Player"] = agent_names[player_index]
                this_game_frame["Score"] = game_scores[player_index]
                this_game_frame["Rounds"] = max_rounds[player_index]
                this_game_frame["Passes"] = total_pass[player_index]
                dataFrame.append(pd.DataFrame(this_game_frame, index=[index]))
                index+=1
        dataFrame = pd.concat(dataFrame)

        

        # Score Plot across all games
        st.write("# Game Score")    
        st.write("A simple score plot showing the evolution of the performance of each user during each match.")    

        st.subheader("Score Evolution")
        st.line_chart(data=dataFrame, x="Game", y="Score", x_label="Games", y_label="Scores", color="Player")
        st.subheader("Score Distribution")
        chart = alt.Chart(dataFrame).mark_boxplot(extent='min-max').encode(
            x='Player',
            y='Score'
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
        st.markdown("---")
        # Max Round Number across all games
        st.write("# Played Rounds (Pizzas)")
        st.write("The number of Rounds (or Pizzas) each player needed to finish all ingredients in their hands in each match.")    

        st.subheader("Rounds Evolution")
        st.line_chart(data=dataFrame, x="Game", y="Rounds", x_label="Games", y_label="Rounds (Pizzas) to finish all cards", color="Player")

        st.subheader("Rounds Distribution")
        chart = alt.Chart(dataFrame).mark_boxplot(extent='min-max').encode(
            x='Player',
            y='Rounds'
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        st.markdown("---")


        # Total 'PASS' actions across all games
        st.write("### Number of Passes")
        st.write("The number of `Pass` Action each player did during each match.") 

        st.subheader("Passes Evolution")
        st.line_chart(data=dataFrame, x="Game", y="Passes", x_label="Games", y_label="Number of Passes", color="Player")
        
        st.subheader("Passes Distribution")
        chart = alt.Chart(dataFrame).mark_boxplot(extent='min-max').encode(
            x='Player',
            y='Passes'
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        st.markdown("---")
        # fig, ax = plt.subplots(figsize=(10, 5))          
        # for game in games:
        #         total_pass = data[(data['Action Type'] == 'PASS') & (data['Game Number'] == game) ].groupby('Player').size()
        #         for player_index in range(len(agent_names)):
        #             player_passes[agent_names[player_index]].append(total_pass[player_index])
                

        # for player, passes in player_passes.items():
        #     ax.plot(passes, label=player, marker='o')  # Adding marker for clarity       

        # ax.set_ylabel('Number of Passes')
        # ax.set_xlabel('Matches')
        # # ax.set_xticks(range(len(next(iter(player_passes.values())))), range(1, len(next(iter(player_passes.values()))) + 1))
        # fig.legend(title="Player", loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=2)
        # fig.tight_layout()        
        # st.pyplot(fig)



        # # # Total 'PIZZA READY' actions across all games        
        # st.write("### Total 'PASS' Actions Across All Games")

        # fig, ax = plt.subplots(figsize=(10, 5))          
        # for game in games:
        #         total_pizzas = data[(data['Action Type'] == 'PIZZA_READY') & (data['Game Number'] == game) ].groupby('Player').size()
        #         print (total_pizzas)
        #         for player_index in range(len(agent_names)):
        #             pizza_ready[agent_names[player_index]].append(total_pizzas[player_index])
                

        # for player, pizzas in pizza_ready.items():
        #     ax.plot(pizzas, label=player, marker='o')  # Adding marker for clarity       

        # ax.set_ylabel('Number of Pizzas')
        # ax.set_xlabel('Games')
        # ax.set_xticks(range(len(next(iter(pizza_ready.values())))), range(1, len(next(iter(pizza_ready.values()))) + 1))
        # ax.legend(title="Player")
        # st.pyplot(fig)