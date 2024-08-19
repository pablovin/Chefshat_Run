from ChefsHatGym.agents.agent_random import AgentRandon
from ChefsHatPlayersClub.agents.classic.dql import AgentDQL
from ChefsHatPlayersClub.agents.classic.ppo import AgentPPO
from ChefsHatPlayersClub.agents.karma_camaleon_club.airl import AgentAIRL
from ChefsHatPlayersClub.agents.karma_camaleon_club.airl import AgentAIRL
from ChefsHatPlayersClub.agents.chefs_cup_v1.team_yves.aiacimp import AIACIMP
from ChefsHatPlayersClub.agents.chefs_cup_v1.team_yves.ainsa import AINSA
from ChefsHatPlayersClub.agents.chefs_cup_v1.team_yves.allin import ALLIN
from ChefsHatPlayersClub.agents.chefs_cup_v1.team_yves.amyg4 import AMYG4
from ChefsHatPlayersClub.agents.chefs_cup_v2.bloom.Bloom import Bloom
from ChefsHatPlayersClub.agents.chefs_cup_v2.larger_value.larger_value import AgentLargerValue
from ChefsHatPlayersClub.agents.chefs_cup_v2.ppo_v2.ppo_v2 import AgentPPOV2

from ChefsHatGym.agents.spectator_logger import SpectatorLogger


not_show_parameters = ["name", "saveFolder", "this_agent_folder", "verbose_console","verbose_log", "logDirectory", "log_directory", "loadNetwork", "demonstrations"]


agents_list = {
    'Random': {      
        'class': AgentRandon  
    },
    'DQL': {        
        'class': AgentDQL  
    },
    'PPO': {        
        'class': AgentPPO 
        } 
    ,
    'Imitation Learning': {        
        'class': AgentAIRL  
    },
    'AIACIMP': {        
        'class': AIACIMP  
    },
    'AINSA': {        
        'class': AINSA  
    },    
    'ALLIN': {        
        'class': ALLIN  
    },    
    'AMYG4': {        
        'class': AMYG4  
    },    
    'Bloom': {        
        'class': Bloom  
    },    
    'Larger Value': {        
        'class': AgentLargerValue  
    },    
    'PPO V2': {        
        'class': AgentPPOV2  
    }
    
    
}
spectators_list = {
    'Logger': {      
        'class': SpectatorLogger  
    }
    
}