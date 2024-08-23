import pandas as pd

df = pd.read_pickle("/home/pablovin/workplace/Chefshat_Run/src/temp/205000_room008/Datasets/Dataset.pkl")
# print (df)
print (f"Columnds: {df.columns}")

# print(len(df))

agent_names = df["Agent_Names"].values[0]
print (f"Agent Names: {agent_names}")
matches = df['Match'].unique()[1:]
print (f"Matches: {matches}")
# nan_value = float("NaN") 
# df.replace("", nan_value, inplace=True)

for match in matches:
    game_scores = df[(df['Match'] == match) & (df['Action_Type'] == "END_MATCH")]["Game_Score"].values[-1]
    print (f"Game: {match} - Score: {game_scores}")

    max_rounds = df[(df['Match'] == match) & (df['Action_Type'] == "DISCARD")].groupby("Source")["Round"].max()        
    print (f"Max Rounds: {max_rounds}")
    print (f"Max Rounds 0 : {max_rounds[1]}")
    
    total_pass = df[(df['Match'] == match) & (df['Action_Description'] == 'pass')].groupby('Source').size()
    print (f"Total Pass: {total_pass}")

    total_pizzas = df[(df['Match'] == match) & (df['Action_Type'] == 'DECLARE_PIZZA')].groupby('Source').size()
    print (f"Total Pizzas: {total_pizzas}")

    break

# print (f"Games: {games}")
# print (f"Agent Names: {len(agent_names)}")




