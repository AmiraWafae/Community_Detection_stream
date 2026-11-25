import pandas as pd

SRC = "/home/leticia/Documents/Uni/M2/DataMining/reduced_merged_steam_data.csv"        # your big attributes file
OUT = "/home/leticia/Documents/Uni/M2/DataMining/reduced_ds.csv"





CHUNK = 100_000

DROP = [
    "name",                            # duplicate of game_name
    "minimum_system_requirement",      # heavy text, no social meaning
    "recommend_system_requirement",
    "long_description",                # heavy text repeated per review
    "short_description",               # genre already describes the game
    "link",                            # URL only
    "number_of_english_reviews",       # redundant game-level count
    "date",                            # no year, little value
]

first = True
for chunk in pd.read_csv(SRC, encoding="utf-8-sig", chunksize=CHUNK, low_memory=False):
    chunk = chunk.drop(columns=DROP, errors="ignore")

    # Clean "1,090" style numbers
    for c in ["helpful", "funny"]:
        chunk[c] = pd.to_numeric(chunk[c].astype(str).str.replace(",", ""),
                                 errors="coerce").fillna(0).astype(int)

    # Replace review text by a light numeric feature, then drop the text
    chunk["review_len"] = chunk["review"].fillna("").astype(str).str.len()
    chunk = chunk.drop(columns="review")

    chunk.to_csv(OUT, mode="w" if first else "a", header=first, index=False)
    first = False

print("Saved", OUT)
#resulting in : 375784 rows
