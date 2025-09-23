import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import hashlib
import sys, os
import time

from concurrent.futures import ThreadPoolExecutor
from streamlit_scroll_to_top import scroll_to_here
import app_modify_tables, app_modify_GitTable, app_display_results, app_display_parameters, app_email, app_final_result, app_game_description




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



# Inicializálás, ha még nem létezik
if "back_to_info_values" not in st.session_state:
    st.session_state.back_to_info_values = {}
if "selections" not in st.session_state:
    st.session_state.selections = {}
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False
if 'scroll_to_top_Delay' not in st.session_state:
    st.session_state.scroll_to_top_Delay = False

   

def scroll():
    st.session_state.scroll_to_top = True

def scroll_Delay():
    st.session_state.scroll_to_top_Delay = True




#Local vagy Cloud:
try: github_token = st.secrets["GITHUB_TOKEN"]
except: github_token = None

# ------------------ GÖRGETÉS: KEZELÉS ------------------
if st.session_state.scroll_to_top:
    scroll_to_here(0, key="top")  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling
    time.sleep(0.2)
    st.rerun() 

elif st.session_state.scroll_to_top_Delay:
    scroll_to_here(0, key="top")  # Scroll to the top of the page
    st.session_state.scroll_to_top_Delay = False  # Reset the state after scrolling
    time.sleep(0.8)
    st.rerun() 



# ------------------ LOGIN KEZELÉS ------------------
elif not st.session_state.logged_in:


    st.image("header.png", use_container_width=True)
    st.subheader("Welcome to the Game! 🎮")
    
    st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
    email = st.text_input("**Enter your e-mail address:** - *it will not be shown publicly*", placeholder="letsplayagame@gmail.com")
    nickname = st.text_input("**Enter your nickname:** - *this will be your public identifier*", placeholder="I am the winner")

    # A részletes Terms szöveg külön szakaszban
    #with st.expander("Detailed Terms and Conditions"):
    agree = st.checkbox("I agree to the Terms and Conditions")
    st.markdown(
        """
        <div style='font-size:12px; line-height:1.4; text-align: justify; text-justify: inter-word;'>
        I hereby consent to the processing of my personal data (nickname, email address) by IDM-Systems Zrt., (hereinafter: Data Controller) for the purpose of receiving newsletters with information about the company’s products, services, promotions, and events. <br><br>

        I confirm that I have read and understood <a href="https://www.idm-systems.hu" target="_blank">IDM-Systems Zrt’s Privacy Notice</a> - for website visitors - and acknowledge that I may withdraw my consent at any time, without giving any reason, by clicking the "Unsubscribe" in the newsletter or by sending an email to privacy@idm-systems.hu.  
        </div>
        """,
        unsafe_allow_html=True
    )
    #st.markdown("") #Üres sor

    # JS script hozzáadása
    st.markdown("""
    <script>
    const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.body.setAttribute('data-user-theme', theme);
    </script>
    """, unsafe_allow_html=True)




    if st.button("Login"):

        #Checkolja e-mailt!
        email_valid = False
        if email != "":
            email_valid = app_email.is_valid_email(email)


        # Attempt login
        if email_valid and nickname and agree:
            
            #Változók mentése:
            st.session_state.email_hash = hashlib.sha256(email.encode()).hexdigest()
            st.session_state.email = email
            st.session_state.nickname = nickname

            if github_token == None: #Lokális futtatás
                players = app_modify_tables.login_player(nickname, st.session_state.email_hash)
            else: #Cloud futtatás
                players = app_modify_GitTable.login_player(nickname, st.session_state.email_hash, "lapatinszki/simulator-app")
                


            if players is None:
                # Player already exists
                st.warning(f"The nickname '{nickname}' is already taken. Please choose another one.")
            else:
                # Login successful
                st.session_state.logged_in = True
            
                #E-mail küldése bejenlentkezésről! -- Csak guthubos deploy esetén menjen ki az e-mail
                if github_token == None: #Lokális futtatás
                    print("Not sending e-mail in local run.")
                else:
                    app_email.send_email(email, st.session_state.email_hash, nickname)

                st.session_state.show_game_intro = True
                scroll_Delay()
                st.rerun()
        else:
            if email == "":
                st.warning("Please enter your e-mail!")
            else:
                if email_valid == False:
                    st.warning("Please enter a valid e-mail!")
            if nickname == "":               
                st.warning("Please enter your nickname!")              
            if not agree:
                st.warning("You must agree to the terms and conditions to proceed.")





# ------------------ JÁTÉK LEÍRÁS OLDAL -------------------
elif st.session_state.show_game_intro:
    st.image("header.png", use_container_width=True)
    app_game_description.game_info()
    if st.button("Let's play"):               
        st.session_state.show_game_intro = False
        scroll_Delay()
        st.rerun()
    


# ------------------ VÉGEREDMÉNY FELÜLET ------------------
elif st.session_state.show_summary:
    app_final_result.calculate_results(github_token, st.session_state.nickname, st.session_state.email)




# ------------------ JÁTÉK FELÜLET ------------------
else:
    st.image("header.png", use_container_width=True)
    st.subheader(f"Let's play the game, {st.session_state.nickname}! 🎮")
    st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal

    if st.button("Back to description"):
        st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek
        st.session_state.show_game_intro = True
        scroll()
        st.rerun()
    
    st.markdown("<hr style='border:1px solid rgba(241, 89, 34, 0.3); margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal


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
                profit_str = f"{profit_float:10.2f}"


                tab_labels.append(f"Attempt {idx+1}     - **Profit: {profit_str} €**")

    selectable_tabs = tab_labels[:st.session_state.current_tab+1]
    selected_tab = st.radio("Select attempt:", selectable_tabs, index=st.session_state.current_tab, format_func=lambda x: x)
    i = tab_labels.index(selected_tab)




    # ------------------------ Paraméterek kiválasztása ------------------------
    if st.session_state.attempts[i] is None:
        st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
        st.subheader("Select input parameters")
        attempt_idx = st.session_state.current_tab
        selections = app_display_parameters.display_inputs(attempt_idx)
        #st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek

        # ------------------------ Szimuláció FUTTATÁSA ------------------------
        # ------------------------ Szimuláció FUTTATÁSA ------------------------
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
                nickname = st.session_state.get("nickname")
                email_hash = st.session_state.get("email_hash")

                # --- 1. Háttérfüggvény: paraméterekkel dolgozik, NEM session_state-tel ---
                def update_tables(nickname, email_hash, profit_value, github_token):
                    if github_token is None:  # Lokális futtatás
                        app_modify_tables.update_player_attempt(nickname, email_hash, profit_value)
                        app_modify_tables.update_leaderboard(nickname, profit_value)
                    else:  # Cloud futtatás
                        app_modify_GitTable.update_player_attempt(nickname, email_hash, profit_value, "lapatinszki/simulator-app")
                        app_modify_GitTable.update_leaderboard(nickname, profit_value, "lapatinszki/simulator-app")


                # --- 2. Háttérszál indítása ---
                executor = ThreadPoolExecutor(max_workers=1)
                future = executor.submit(update_tables, nickname, email_hash, profit_value, github_token)

                # --- 3. GIF lejátszása ---
                start_time = time.time()
                app_display_results.play_the_GIF()  # elindítja a gifet

                # minimum 5 másodperc + a háttérszál végéig
                gif_min_duration = 5
                while True:
                    elapsed = time.time() - start_time
                    if elapsed >= gif_min_duration and future.done():
                        break
                    time.sleep(0.1)  # rövid szünet, hogy ne pörögjön a CPU fölöslegesen

                # --- 4. Várjuk meg a háttér futás végét ---
                result = future.result()


                # --- Attempt mentése Profit-tal együtt ---
                selections_with_profit = selections.copy()
                selections_with_profit["Profit"] = profit_value
                st.session_state.attempts[i] = selections_with_profit

                scroll()
                st.rerun()


    # ------------------------ Eredmények megjelenítése ------------------------
    else:
        selections = st.session_state.attempts[i]
        st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek

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
            st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
            if i == st.session_state.current_tab:
                # New attempt gomb
                if i < total_attempts - 1 and st.session_state.attempts[i+1] is None:
                    if st.button("Next round! Let’s do this! 🔄", key=f"new_attempt_{i}"):
                        scroll_Delay()
                        st.session_state.current_tab = i + 1  
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
                        scroll_Delay()
                        st.session_state.show_summary = True
                        st.session_state.confirm_finish = False
                        st.rerun()
                    if st.button("❌ No, I'll keep playing!", key=f"confirm_no_{i}"):
                        st.session_state.confirm_finish = False
                        st.rerun()
            







