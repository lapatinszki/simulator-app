import pandas as pd

def login_player(nickname, email_code, players_file="table_Players.csv"):
    # """
    # Log in a player by Nickname and E-mail_code.
    # If the player does not exist in table_Players.csv, add a new row with empty attempts.
    # If the player exists, login is denied.
    # """
    # Load file
    players = pd.read_csv(players_file)
    players.columns = players.columns.str.strip()  # clean column names

    # Check if Nickname column exists
    if "Nickname" not in players.columns:
        raise KeyError(f"'Nickname' column not found! Columns in file: {list(players.columns)}")

    # Check if player already exists
    if nickname in players["Nickname"].values:
        # Login denied
        print(f"❌ Player '{nickname}' already exists. Login denied.")
        return None  # or raise an error if you prefer
    else:
        # Create new row
        new_row = {col: "" for col in players.columns}
        new_row["Nickname"] = nickname
        if "E-mail_code" in players.columns:
            new_row["E-mail_code"] = email_code
        players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)
        print(f"✅ New player '{nickname}' added and logged in.")

    # Save back
    players.to_csv(players_file, index=False)
    return players




def update_player_attempt(nickname, email_code, profit, players_file="table_Players.csv"):
    # """
    # Update the table_Players.csv file with the new profit result.
    # It will find the correct row by Nickname and fill the next empty Attempt_X column.
    # """
    # Load file
    players = pd.read_csv(players_file)
    players.columns = players.columns.str.strip()  # clean column names

    # Find the player row
    player_index = players.index[players["Nickname"] == nickname].tolist()
    if not player_index:
        raise ValueError(f"Player with nickname '{nickname}' not found in table. Did you login first?")
    idx = player_index[0]

    # Update email_code to keep it consistent
    if "E-mail_code" in players.columns:
        players.loc[idx, "E-mail_code"] = email_code

    # Find first empty Attempt column
    attempt_cols = [col for col in players.columns if col.startswith("Attempt_")]
    updated = False
    for col in attempt_cols:
        if pd.isna(players.loc[idx, col]) or players.loc[idx, col] == "":
            players.loc[idx, col] = profit
            updated = True
            break

    if not updated:
        raise ValueError(f"No empty Attempt columns left for player '{nickname}'.")

    # Save back
    players.to_csv(players_file, index=False)
    print(f"✅ Profit {profit} saved for {nickname}.")
    return players




def update_leaderboard(nickname, profit, leaderboard_file="table_Leaderboard.csv"):
    # """
    # Frissíti a leaderboardot az aktuális játékos profitjával.
    # - nickname: a játékos neve
    # - profit: aktuális elért profit
    # - leaderboard_file: leaderboard CSV fájl
    # """
    # --- Leaderboard betöltése ---
    try:
        lb_df = pd.read_csv(leaderboard_file, encoding="cp1252")
    except FileNotFoundError:
        lb_df = pd.DataFrame(columns=["Nickname", "Profit"])

    # Ellenőrzés, hogy a játékos már szerepel-e
    if nickname in lb_df["Nickname"].values:
        current_profit = lb_df.loc[lb_df["Nickname"] == nickname, "Profit"].values[0]
        if profit > current_profit:
            lb_df.loc[lb_df["Nickname"] == nickname, "Profit"] = profit
        # Ha kisebb vagy egyenlő, nem írunk semmit
    else:
        # Új rekord hozzáadása pd.concat-tal
        new_row = pd.DataFrame([{"Nickname": nickname, "Profit": profit}])
        lb_df = pd.concat([lb_df, new_row], ignore_index=True)

    # Rendezés Profit szerint csökkenő sorrendben
    lb_df = lb_df.sort_values(by="Profit", ascending=False)

    # Mentés CSV-be
    lb_df.to_csv(leaderboard_file, index=False, encoding="cp1252")





def get_rank_for_profit(profit, leaderboard_file="table_Leaderboard.csv"):
    #"""
    #Visszaadja, hogy a profit hányadik helyre lenne elegendő a leaderboard-ban.
    #A leaderboard csökkenő sorrendben van Profit szerint.
    #"""
    try:
        lb_df = pd.read_csv(leaderboard_file, encoding="cp1252")
    except FileNotFoundError:
        # Ha még nincs leaderboard, az első helyre kerül
        return 1

    # Rendezés csökkenő sorrendbe Profit szerint
    lb_df = lb_df.sort_values(by="Profit", ascending=False).reset_index(drop=True)

    # Hol lenne a profit?
    rank = (lb_df["Profit"] > profit).sum() + 1
    return rank