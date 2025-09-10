import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import hashlib
import sys, os
import threading, time


import app_modify_tables, app_modify_GitTable, app_display_results, app_display_parameters, app_email, app_final_result



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
if "confirm_finish" not in st.session_state:
    st.session_state.confirm_finish = False

#Local vagy Cloud:
try: try: github_token = st.secrets["GITHUB_TOKEN"]
except: github_token = None


# ------------------ LOGIN KEZELÉS ------------------
if not st.session_state.logged_in:
    st.image("header.png", use_container_width=True)
    st.subheader("Welcome to the Game! 🎮")
    st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal
    email = st.text_input("**Enter your e-mail address:** - *it will not be shown publicly*", placeholder="letsplayagame@gmail.com")
    nickname = st.text_input("**Enter your nickname:** - *this will be your public identifier*", placeholder="I am the winner")

    # A részletes Terms szöveg külön szakaszban
    #with st.expander("Detailed Terms and Conditions"):
    agree = st.checkbox("I agree to the Terms and Conditions")
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
    st.markdown("") #Üres sor

    # JS script hozzáadása
    st.markdown("""
    <script>
    const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.body.setAttribute('data-user-theme', theme);
    </script>
    """, unsafe_allow_html=True)


    st.markdown(github_token)
    
    if st.button("Login"):
        if email and nickname and agree:
            # Attempt login

           
            if github_token == None: #Lokális futtatás
                players = app_modify_tables.login_player(nickname, email)
            else: #Cloud futtatás
                players = app_modify_GitTable.login_player(nickname, email, "lapatinszki/simulator-app")
                


            if players is None:
                # Player already exists
                st.warning(f"The nickname '{nickname}' is already taken. Please choose another one.")
            else:
                # Login successful
                st.session_state.logged_in = True
                st.session_state.email_hash = hashlib.sha256(email.encode()).hexdigest()
                st.session_state.nickname = nickname
                
                #E-mail küldése bejenlentkezésről! -- Csak guthubos deploy esetén menjen ki az e-mail
                if github_token == None: #Lokális futtatás
                    print("Not sending e-mail in local run.")
                else:
                    app_email.send_email(email, st.session_state.email_hash, nickname)    
                email = "" #RESET AZONNAL!

                st.session_state.show_game_intro = True
                st.rerun()
        else:
            if email == "" or nickname == "":
                st.warning("Please enter both e-mail and nickname!")
            if not agree:
                st.warning("You must agree to the terms and conditions to proceed.")





# ------------------ JÁTÉK LEÍRÁS OLDAL -------------------
elif st.session_state.show_game_intro:
    st.image("header.png", use_container_width=True)
    st.subheader("**Game description** 📋")
    st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal
    st.markdown("""
    Welcome to the ultimate game simulation!  
    In this game, you will select parameters for your manufacturing setup,  
    and see how your choices affect the profit, machine utilization, operator efficiency, and robot performance.  
    Can you optimize your production process and maximize your results? Let's find out!
    """)
    if st.button("Let's play"):
        st.session_state.show_game_intro = False
        st.rerun()





# ------------------ VÉGEREDMÉNY FELÜLET ------------------
elif st.session_state.show_summary:
    st.image("header.png", use_container_width=True)
    st.subheader("Final result 🏆")
    st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal

    app_final_result.calculate_results(github_token)




# ------------------ JÁTÉK FELÜLET ------------------
else:

    st.image("header.png", use_container_width=True)
    st.subheader(f"Let's play the game, {st.session_state.nickname}! 🎮")
    st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal

    @st.cache_data
    def load_data():
        return pd.read_csv("simulation_results.csv", encoding="cp1252", header=0)
    df = load_data()

    #Paraméterek indexel importálás:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.append(repo_root)
    from app_display_parameters import param_cols

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




    # ------------------------ Paraméterek kiválasztása ------------------------
    if st.session_state.attempts[i] is None:
        st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal
        st.subheader("Select input parameters")
        attempt_idx = st.session_state.current_tab
        selections = app_display_parameters.display_inputs(attempt_idx)


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


                # --- 0. Funkció az adatfeltöltéshez ---
                def update_tables():
                    if github_token is None:  # Lokális futtatás
                        app_modify_tables.update_player_attempt(st.session_state.nickname, st.session_state.email_hash, profit_value)
                        app_modify_tables.update_leaderboard(st.session_state.nickname, profit_value)
                    else: #Cload futtatás
                        app_modify_GitTable.update_player_attempt(st.session_state.nickname, st.session_state.email_hash, profit_value, "lapatinszki/simulator-app")
                        app_modify_GitTable.update_leaderboard(st.session_state.nickname, profit_value, "lapatinszki/simulator-app")



                # --- 2. Háttérszál indítása ---
                thread = threading.Thread(target=update_tables)
                thread.start()

                # --- 3. GIF lejátszása ---
                gif_duration = 5  # minimum idő másodpercben
                start_time = time.time()
                app_display_results.play_the_GIF()  # elindítja a GIF-et

                # --- 4. Várakozás: legalább gif_duration, majd a szál befejezése ---
                thread.join(timeout=gif_duration)  # várakozás maximum gif_duration-ig
                elapsed = time.time() - start_time

                # Ha a GIF-nek még futnia kell a minimum ideig
                if elapsed < gif_duration:
                    time.sleep(gif_duration - elapsed)

                # Ha a háttérszál még fut, várunk rá
                thread.join()




                # #GIF lejátszása:
                # app_display_results.play_the_GIF()

                # # --- Player attempt frissítése ---
                # if github_token == None: #Lokális futtatás
                #     app_modify_tables.update_player_attempt(st.session_state.nickname, st.session_state.email_hash, profit_value)
                #     app_modify_tables.update_leaderboard(st.session_state.nickname, profit_value)
                # else:
                #     app_modify_GitTable.update_player_attempt(st.session_state.nickname, st.session_state.email_hash, profit_value, "lapatinszki/simulator-app")
                #     app_modify_GitTable.update_leaderboard(st.session_state.nickname, profit_value, "lapatinszki/simulator-app")


                # --- Attempt mentése Profit-tal együtt ---
                selections_with_profit = selections.copy()
                selections_with_profit["Profit"] = profit_value
                st.session_state.attempts[i] = selections_with_profit

                st.rerun()

    # ------------------------ Eredmények megjelenítése ------------------------
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
            

            #Eredmények:
            app_display_results.display_tables(selected_row, df)
            app_display_results.display_charts(selected_row, df)





            # ---------------------------------------------------------------------
            # ---------------------------------------------------------------------
            # Csak akkor jelenjen meg a "New attempt" gomb és a "View results" gomb,
            # ha az aktuális attemptnél vagyunk
            st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True) #Vízszintes vonal
            if i == st.session_state.current_tab:
                # New attempt gomb
                if i < total_attempts - 1 and st.session_state.attempts[i+1] is None:
                    if st.button("Next round! Let’s do this! 🔄", key=f"new_attempt_{i}"):
                        st.session_state.current_tab = i + 1
                        components.html("<script>window.scrollTo(0,0);</script>", height=0)
                        st.rerun()

                # Csak akkor kell megerősítés, ha nem az utolsó attempt
                is_last_attempt = (i == total_attempts - 1)

                # Finish the game gomb
                if st.button("Finish the game 🏁", key=f"view_results_{i}"):
                    if is_last_attempt:
                        st.session_state.show_summary = True
                        st.rerun()
                    else:
                        st.session_state.confirm_finish = True
                        st.rerun()

                # Ha megerősítést kérünk
                if st.session_state.confirm_finish:
                    st.warning("⚠️ Are you sure you want to finish the game? You won’t be able to go back after this!")

                    if st.button("✅ Yes, I’m ready for my results!", key=f"confirm_yes_{i}"):
                        st.session_state.show_summary = True
                        st.session_state.confirm_finish = False
                        st.rerun()
                    if st.button("❌ No, I'll keep palying!", key=f"confirm_no_{i}"):
                        st.session_state.confirm_finish = False
                        st.rerun()
            


