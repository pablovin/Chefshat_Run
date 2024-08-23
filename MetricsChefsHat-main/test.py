from CalculateMetrics import calculate_scores, eccentricity_df
import pandas as pd
import os

base_path = r"C:\Users\7000027512\Documents\Code\Chefshat_Run\src\temp\164220_Room_long\Datasets\Dataset.pkl"
# here with the path of your dataset

df = pd.read_pickle(base_path)
df = df.reset_index(drop=True)

for game in df["Match"].unique():
    if game == 0:
        continue
    # Filter the DataFrame for the current game
    game_df = df[(df["Match"] == game) & (df["Source"] != "SYSTEM")]
    finish_index = game_df[game_df["Player_Finished"] == True].index.min()
    game_df = game_df.loc[:finish_index]

    # Calculate the metrics Attack, Defense and Vitality for the current game
    results = calculate_scores(game_df, game)

    print(results)
