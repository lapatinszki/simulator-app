import pandas as pd
import io
import time
from github import Github
from github import GithubException
import streamlit as st

# -------------------------------------------------------------------------------------------
# GitHub CSV helper
# -------------------------------------------------------------------------------------------
def load_csv_from_github(repo_name, file_path):
    #Betölti a CSV-t GitHub repo-ból DataFrame-be.
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo(repo_name)
    try:
        contents = repo.get_contents(file_path)
        csv_str = contents.decoded_content.decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_str))
        df.columns = df.columns.str.strip()
        return df, contents.sha
    except Exception:
        # Ha nincs fájl, üres DataFrame-et adunk
        return pd.DataFrame(), None


def save_csv_to_github(df, repo_name, file_path, sha=None, commit_message="Update CSV"):
    #Mentés GitHub repo-ba commit-tal.
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo(repo_name)

    while True:
        try:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue()
            if sha:
                repo.update_file(file_path, commit_message, csv_content, sha)
            else:
                repo.create_file(file_path, commit_message, csv_content)
            break


        except GithubException as e:
            if e.status == 409:
                time.sleep(2)

                # Új fájl és SHA lekérése
                contents = repo.get_contents(file_path)
                csv_str = contents.decoded_content.decode("utf-8")
                latest_df = pd.read_csv(io.StringIO(csv_str))
                latest_df.columns = latest_df.columns.str.strip()

                # Az új df-hez hozzá kell fűzni a régi df különbségeit
                # (például merge, append, concat – attól függ, mit tároltok benne)
                #df = pd.concat([latest_df, df]).drop_duplicates().reset_index(drop=True)
                sha = contents.sha
                continue
            else:
                raise ## Más hiba van, Nem próbálkozik tovább!
            






# -------------------------------------------------------------------------------------------
# Játékos login
# -------------------------------------------------------------------------------------------
def login_player(nickname, email_code, repo_name, players_file="table_Players.csv"):
    players, sha = load_csv_from_github(repo_name, players_file)

    # Ha üres, inicializáljuk
    if players.empty:
        players = pd.DataFrame(columns=["Nickname", "E-mail_code"] + [f"Attempt_{i+1}" for i in range(5)])

    # Ellenőrzés, hogy létezik-e a játékos
    if nickname in players["Nickname"].values:
        return None
    else:
        new_row = {col: "" for col in players.columns}
        new_row["Nickname"] = nickname
        if "E-mail_code" in players.columns:
            new_row["E-mail_code"] = email_code
        players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)

    save_csv_to_github(players, repo_name, players_file, sha, commit_message=f"Add player {nickname}")
    return players


# -------------------------------------------------------------------------------------------
# Játékos próbálkozás frissítése
# -------------------------------------------------------------------------------------------
def update_player_attempt(nickname, email_code, profit, repo_name, players_file="table_Players.csv"):
    players, sha = load_csv_from_github(repo_name, players_file)

    player_index = players.index[players["Nickname"] == nickname].tolist()
    if not player_index:
        raise ValueError(f"Player with nickname '{nickname}' not found in table. Did you login first?")
    idx = player_index[0]

    if "E-mail_code" in players.columns:
        players.loc[idx, "E-mail_code"] = email_code

    attempt_cols = [col for col in players.columns if col.startswith("Attempt_")]
    updated = False
    for col in attempt_cols:
        if pd.isna(players.loc[idx, col]) or players.loc[idx, col] == "":
            players.loc[idx, col] = profit
            updated = True
            break
    if not updated:
        raise ValueError(f"No empty Attempt columns left for player '{nickname}'.")

    save_csv_to_github(players, repo_name, players_file, sha, commit_message=f"Update {nickname} attempt")
    return players


# -------------------------------------------------------------------------------------------
# Leaderboard frissítése
# -------------------------------------------------------------------------------------------
def update_leaderboard(nickname, profit, repo_name, leaderboard_file="table_Leaderboard.csv"):
    lb_df, sha = load_csv_from_github(repo_name, leaderboard_file)

    if lb_df.empty:
        lb_df = pd.DataFrame(columns=["Nickname", "Profit"])

    if nickname in lb_df["Nickname"].values:
        current_profit = lb_df.loc[lb_df["Nickname"] == nickname, "Profit"].values[0]
        if profit > current_profit:
            lb_df.loc[lb_df["Nickname"] == nickname, "Profit"] = profit
    else:
        new_row = pd.DataFrame([{"Nickname": nickname, "Profit": profit}])
        lb_df = pd.concat([lb_df, new_row], ignore_index=True)

    lb_df = lb_df.sort_values(by="Profit", ascending=False).reset_index(drop=True)
    save_csv_to_github(lb_df, repo_name, leaderboard_file, sha, commit_message=f"Update leaderboard for {nickname}")


# -------------------------------------------------------------------------------------------
# Profit helyezés lekérdezése
# -------------------------------------------------------------------------------------------
def get_rank_for_profit(profit, repo_name, leaderboard_file="table_Leaderboard.csv"):
    lb_df, _ = load_csv_from_github(repo_name, leaderboard_file)
    if lb_df.empty:
        return 1
    lb_df = lb_df.sort_values(by="Profit", ascending=False).reset_index(drop=True)
    rank = (lb_df["Profit"] > profit).sum() + 1
    return rank



