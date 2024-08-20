import streamlit as st
from utils import script_directory
import os


def main():
    st.set_page_config(
        page_title="Chef`s Hat Run",
        page_icon="👋",
    )

    st.sidebar.success("Select one of the tools from the menu on the left.")

    st.image(
        f"{os.path.join(script_directory,'ChefsHatRun.png')}",
        caption="Serving Chef`s Hat Games to Everyone!",
    )

    st.write("# Welcome to Chef`s Hat Run! 👋")

    st.markdown(
        """
        Chef\\`s Hat Run is a tool to create, run and manage Chef\\`s Hat Rooms and experiments.
        You can use it to run full agent-based simulations, collect and analyse their data without the need to code anything.
        Also, you can use it to create and server Chef`s Hat Server rooms that allow other players to connect to the game.
        
        **👈 Select one of the tools on the sidebar** and have fun!
        ### Available tools
        - **Create New Room**: Use this tool to create your very own Chef\\`s Hat Room! Add Players and Spectators to run locally, and start your experiments!
        - **Online Rooms**: Use this tool to follow up the rooms that you created with the Create New Room tool. See a live representation of the game`s status and a summary of the game log.
        - **Explore Games**: Use this tool to read and explore existing games from a .pkl Dataset. It can create explorative plots, and give you some insights about the experiment.
        - **Competitive Metrics**: Use this tool to generate a set of the competitive metrics defined by Laura Triglia here: https://github.com/lauratriglia/MetricsChefsHat .
        
        ### Need more information about Chef`s Hat Environment?
        - Check all all about the Chef`s Hat Run: https://github.com/pablovin/Chefshat_Run        
        - Also the Chef`s Hat Gym page for an overview of the simulator: https://github.com/pablovin/ChefsHatGYM 
        - And of course, the Chef`s Hat Players Club has all the information about the artificial Players: https://github.com/pablovin/ChefsHatPlayersClub             
    """
    )


if __name__ == "__main__":
    # wide_space_default()
    main()
