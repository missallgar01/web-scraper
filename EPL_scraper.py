import pandas as pd


log = pd.DataFrame(pd.read_csv("/kaggle/input/fantasy-premier-league-dataset-2023-2024/players.csv"))
log.sample(5)