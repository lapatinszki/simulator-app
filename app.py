import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import hashlib

import app_modify_talbes
import app_display_results
import app_display_parameters


# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_game_intro" not in st.session_state:
    st.session_state.show_game_intro = False
if "attempts" not in st.session_state:
    st.session_state.attempts = [None]*5
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

# --- LOGIN KEZELÉS ---
if not st.session_state.logged_in:
    st.image("header.png", use_container_width=True)
    st.subheader("Welcome to the Game! 🎮")
    email = st.text_input("Enter your e-mail address:", placeholder="It will not be shown publicly.")
    nickname = st.text_input("Enter your nickname:", placeholder="This will be your public identifier.")

    # A részletes Terms szöveg külön szakaszban
    #with st.expander("Detailed Terms and Conditions"):
    st.markdown(
        """
        <div style='font-size:12px; line-height:1.4;'>
        I hereby consent to IDM Systems Zrt. using my personal data (email address, nickname) 
        in connection with the "Let's play a game" for the duration of the online game 
        10.01.2025 – 10.02.2025.  
        I understand that I may withdraw my consent at any time by contacting [*] via email.
        </div>
        """,
        unsafe_allow_html=True
    )

    agree = st.checkbox(" I agree to the Terms and Conditions")
    
    
    if st.button("Login"):
            if email and nickname and agree:
                # Attempt login
                players = app_modify_talbes.login_player(nickname, email)

                if players is None:
                    # Player already exists
                    st.warning(f"The nickname '{nickname}' is already taken. Please choose another one.")
                else:
                    # Login successful
                    st.session_state.logged_in = True
                    st.session_state.email = hashlib.sha256(email.encode()).hexdigest()
                    st.session_state.nickname = nickname
                    st.session_state.show_game_intro = True

                    st.success(f"Welcome, {nickname}!")
                    st.rerun()
            else:
                if email == "" or nickname == "":
                    st.warning("Please enter both e-mail and nickname!")
                if not agree:
                    st.warning("You must agree to the terms and conditions to proceed.")

# --- JÁTÉK LEÍRÁS OLDAL ---
elif st.session_state.show_game_intro:
    st.image("header.png", use_container_width=True)
    st.subheader("**Game description** 📋")
    st.markdown("""
    Welcome to the ultimate game simulation!  
    In this game, you will select parameters for your manufacturing setup,  
    and see how your choices affect the profit, machine utilization, operator efficiency, and robot performance.  
    Can you optimize your production process and maximize your results? Let's find out!
    """)
    if st.button("Let's play"):
        st.session_state.show_game_intro = False
        st.rerun()

# --- VÉGEREDMÉNY FELÜLET ---
elif st.session_state.show_summary:
    st.image("header.png", use_container_width=True)
    st.subheader("Final Results 🏆")

    # Maximum profit a játékos összes attempt-jából
    attempts = [a for a in st.session_state.attempts if a is not None]
    if attempts:
        profits = [a["Profit"] for a in attempts]
        max_profit = max(profits)

        rank = app_modify_talbes.get_rank_for_profit(max_profit)
        st.success(f"Your best profit: **{max_profit:.2f} €**")
        st.info(f"Your best attempt placed you at rank **#{rank}** on the current leaderboard.")

    else:
        st.warning("No attempts recorded.")

    st.markdown("⚠️ You cannot go back to the game!")

# --- JÁTÉK FELÜLET ---
else:

    st.image("header.png", use_container_width=True)
    st.subheader(f"Let's play the game, {st.session_state.nickname}! 🎮")

    @st.cache_data
    def load_data():
        return pd.read_csv("simulation_results.csv", encoding="cp1252", header=0)
    df = load_data()

    # Paraméterek
    param_cols = [
        "Size of the batches",
        "Type of the shipping box",
        "Cycle time factor",
        "Number of the operators",
        "Type of the quality check",
        "Percentage of the quality check",
        "Overshooting"
    ]

    # --- Ellenőrzés: 2-8. oszlop ---
    expected_cols = param_cols
    actual_cols = df.columns[1:8].tolist()  # CSV 2-8 oszlop
    if actual_cols != expected_cols:
        st.error(f"CSV oszlopok nem egyeznek! Talált: {actual_cols}, elvárt: {expected_cols}")

    total_attempts = 5
    current_attempt_display = st.session_state.current_tab + 1
    st.markdown(f"*You have **{total_attempts}** attempts in total. You are currently at your **{current_attempt_display}.** attempt!*")

    # --- Tab logika ---
    tab_labels = []
    for idx in range(total_attempts):
        if st.session_state.attempts[idx] is None:
            tab_labels.append(f"Attempt {idx+1}")
        else:
            # Mask létrehozása
            mask = pd.Series([True]*len(df))
            for col in param_cols:
                val = st.session_state.attempts[idx][col]
                mask &= df[col] == val
            
            if mask.sum() > 0:
                selected_row = df[mask].iloc[0]
                row_index = df[mask].index[0]

                profit = selected_row.get("Profit", None)  # vagy selected_row["Profit"]
                profit_float = float(profit)
                profit_str = f"{profit_float:10.3f}"


                tab_labels.append(f"Attempt {idx+1}     - **Profit: {profit_str} €**")

    selectable_tabs = tab_labels[:st.session_state.current_tab+1]
    selected_tab = st.radio("Select attempt:", selectable_tabs, index=st.session_state.current_tab, format_func=lambda x: x)
    i = tab_labels.index(selected_tab)




    # --- Paraméterek kiválasztása ---
    if st.session_state.attempts[i] is None:

        st.subheader("Select parameters")
        selections = app_display_parameters.display_inputs(param_cols)

        # --- Simuláció futtatása GOMB ---
        if st.button("Run the simulation!"):
            # --- Megtaláljuk a kiválasztott paramétereknek megfelelő sort ---
            mask = pd.Series([True]*len(df))
            for col_name in param_cols:
                mask &= df[col_name] == selections[col_name]

            if mask.sum() == 0:
                st.error("No row found for the selected parameter combination.")
            else:
                selected_row = df[mask].iloc[0]  # csak egy sor kell

                # --- Profit biztonságos kiolvasása ---
                profit_value = float(selected_row.get("Profit", 0.0))

                # --- Player attempt frissítése ---
                app_modify_talbes.update_player_attempt(st.session_state.nickname, st.session_state.email, profit_value)
                app_modify_talbes.update_leaderboard(st.session_state.nickname, profit_value)

                # --- Attempt mentése Profit-tal együtt ---
                selections_with_profit = selections.copy()
                selections_with_profit["Profit"] = profit_value
                st.session_state.attempts[i] = selections_with_profit

                st.rerun()

    #------- Eredmények megjelenítése ---
    else:
        selections = st.session_state.attempts[i]

        # Mask létrehozása a kiválasztott paraméterekhez
        mask = pd.Series([True]*len(df))
        for col in param_cols:
            mask &= df[col] == selections[col]

        if mask.sum() == 0:
            st.error("No row found for the selected parameter combination.")
        else:
            # Megtalált sor
            selected_row = df[mask].iloc[0]
            row_index = df[mask].index[0]  # DataFrame sor indexe
            
            app_display_results.create_tables(selected_row, row_index, df)
            app_display_results.display_tables(selected_row, df)
            app_display_results.display_charts(selected_row, df)





            # ---------------------------------------------------------------------
            # ---------------------------------------------------------------------
            # Csak akkor jelenjen meg a "New attempt" gomb és a "View results" gomb,
            # ha az aktuális attemptnél vagyunk
            if i == st.session_state.current_tab:
                cols_buttons = st.columns(2)  # Két oszlop, gombok mellé
                # New attempt gomb
                if i < total_attempts - 1 and st.session_state.attempts[i+1] is None:
                    if st.button("New attempt 🔄", key=f"new_attempt_{i}"):
                        st.session_state.current_tab = i + 1
                        components.html("<script>window.scrollTo(0,0);</script>", height=0)
                        st.rerun()
                # Finish the game gomb
                
                if st.button("Finish the game 🏁", key=f"view_results_{i}"):
                    st.session_state.show_summary = True
                    st.rerun()
                    
                st.warning("⚠️ Once you finish the game, you cannot return to attempts!")

