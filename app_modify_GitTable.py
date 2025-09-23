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


def save_csv_to_github(df, repo_name, file_path, sha=None, commit_message="Update CSV", retry_update_func=None, retry_args=None):
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

                # Újraolvasás GitHub-ból
                contents = repo.get_contents(file_path)
                csv_str = contents.decoded_content.decode("utf-8")
                df = pd.read_csv(io.StringIO(csv_str))
                df.columns = df.columns.str.strip()
                sha = contents.sha

                # Újraalkalmazzuk a user változtatását
                if retry_update_func:
                    df = retry_update_func(df, *retry_args)

                continue
            else:
                raise
            






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

    def apply_update(players_df, nickname, email_code, profit):
        player_index = players_df.index[players_df["Nickname"] == nickname].tolist()
        if not player_index:
            raise ValueError(f"Player '{nickname}' not found.")
        idx = player_index[0]

        if "E-mail_code" in players_df.columns:
            players_df.loc[idx, "E-mail_code"] = email_code

        attempt_cols = [col for col in players_df.columns if col.startswith("Attempt_")]
        for col in attempt_cols:
            if pd.isna(players_df.loc[idx, col]) or players_df.loc[idx, col] == "":
                players_df.loc[idx, col] = profit
                return players_df
        raise ValueError(f"No empty Attempt columns left for '{nickname}'.")

    # Első próbálkozás
    players = apply_update(players, nickname, email_code, profit)

    save_csv_to_github(
        players,
        repo_name,
        players_file,
        sha,
        commit_message=f"Update {nickname} attempt",
        retry_update_func=apply_update,
        retry_args=(nickname, email_code, profit)
    )
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


