![Chef's Hat Run](gitImages/chefsHatLogo.png)

## Chef`s Hat Run

This repository holds the Chef`s Hat Run, an environment to simplify the runing, managing and exploration of simulations using the [ChefsHatGym]( https://github.com/pablovin/ChefsHatGYM) simulation environment.

The current version of the Chef`s Hat Run allows you too:

* Setup a server room that can be accessed remotely by any type of player.
* Run local experiments with any number of artificial Players and Spectators in a server room.
* Follow up experiments, with a live summary of the room while it is running.
* Download all logs and datasets of running experiments.
* Explore finished experiments by generating game-related statistics.

Chef`s Hat Run creates a webserver that is able to host all the experiments, allowing it to be deployed in a remote server.
All experiments results are saved in a local folder, and can be easily acessible via the Chef`s Hat Run tools.

### Instalation

Clone this repository, and create a python environment, using conda or venv, using python > 3.10. 

Install all the requirements on the "requirement.txt" file:


```python
   pip install -r requirements.txt

```

All done!

### Runing

From the repository root directory, run the Chef`s Hat Run server using:

```python
   streamlit run src\ChefsHat_Run.py

```

![Chef's Hat Run](gitImages/main_page.png)


### Chef`s Hat Run Tools

Currently, there are three tools available with Chef`s Hat Run:

## Create New Room

![Chef's Hat Run](gitImages/CreateNewRoom.gif)

This tool allows you to create new Chef`s Hat rooms, populate it with Players and Spectators and start a room server.
It is ideal to quickly run experiments without touching any code, or to setup server rooms that will be accessed by other computers.
For an in-depth understanding of our parameters when creating a room, please check the [Chef`s Hat Rooms page](https://chefshatgym.readthedocs.io/en/latest/04_rooms.html).

All the Players available at the [Chef`s Hat Players Club](https://github.com/pablovin/ChefsHatPlayersClub) are directly available to be added to your server room. Check the Player section on the Chef`s Hat Players Club website for mor information about parameters and general agent behavior.


Once your room is up and running, it will be acessible by the See Rooms tool.

## See Rooms
![Chef's Hat Run - See Rooms](gitImages/see_room.png)

The Seee Room tool allows to follow runing and finished games, checking their current status in relation to the stop criteria, and showing a small summary of the room performance.

It is ideal to check if an experiment has finished, or to verity, in real-time, the performance of remote agents playing a game in a server room.
Once the room is finished, you can download all the logs (Game and room, all players and spectators) and the game datasets for that game, for further analysis.

## Explore Games

![Chef's Hat Run - Explore Games](gitImages/explore_game.png)

The Explore Games tool uses a generated game datasets to create explorative plots that describe the behavior of the agents.
Currently, it is possible to visualize the evolution, and distribution, of the scores, number of played rounds and number of declared pizzas for each player that played a game.

All plots are interactive and can be zoomed and visualized in different angles, and can be easily downloaded as PNG or SVG files.

 

 ## Use and distribution policy

All the examples in this repository are distributed under a Non-Comercial license. If you use this environment, you have to agree with the following itens:

- To cite our associated references in any of your publication that make any use of these examples.
- To use the environment for research purpose only.
- To not provide the environment to any second parties.

## Citations

- Barros, P., Yalçın, Ö. N., Tanevska, A., & Sciutti, A. (2023). Incorporating rivalry in reinforcement learning for a competitive game. Neural Computing and Applications, 35(23), 16739-16752.

- Barros, P., & Sciutti, A. (2022). All by Myself: Learning individualized competitive behavior with a contrastive reinforcement learning optimization. Neural Networks, 150, 364-376.

- Barros, P., Yalçın, Ö. N., Tanevska, A., & Sciutti, A. (2022). Incorporating Rivalry in reinforcement learning for a competitive game. Neural Computing and Applications, 1-14.

- Barros, P., Tanevska, A., & Sciutti, A. (2021, January). Learning from learners: Adapting reinforcement learning agents to be competitive in a card game. In 2020 25th International Conference on Pattern Recognition (ICPR) (pp. 2716-2723). IEEE.

- Barros, P., Sciutti, A., Bloem, A. C., Hootsmans, I. M., Opheij, L. M., Toebosch, R. H., & Barakova, E. (2021, March). It's Food Fight! Designing the Chef's Hat Card Game for Affective-Aware HRI. In Companion of the 2021 ACM/IEEE International Conference on Human-Robot Interaction (pp. 524-528).

- Barros, P., Tanevska, A., Cruz, F., & Sciutti, A. (2020, October). Moody Learners-Explaining Competitive Behaviour of Reinforcement Learning Agents. In 2020 Joint IEEE 10th International Conference on Development and Learning and Epigenetic Robotics (ICDL-EpiRob) (pp. 1-8). IEEE.

- Barros, P., Sciutti, A., Bloem, A. C., Hootsmans, I. M., Opheij, L. M., Toebosch, R. H., & Barakova, E. (2021, March). It's food fight! Designing the chef's hat card game for affective-aware HRI. In Companion of the 2021 ACM/IEEE International Conference on Human-Robot Interaction (pp. 524-528).

## Contact

Pablo Barros - pablovin@gmail.com

- [Twitter](https://twitter.com/PBarros_br)
- [Google Scholar](https://scholar.google.com/citations?user=LU9tpkMAAAAJ)
