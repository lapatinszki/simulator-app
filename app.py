import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_game_intro" not in st.session_state:
    st.session_state.show_game_intro = False
if "attempts" not in st.session_state:
    st.session_state.attempts = [None]*5
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

# --- LOGIN KEZELÉS ---
if not st.session_state.logged_in:
    st.image("header.png", use_container_width=True)
    st.subheader("Welcome to the Game 🎮")
    email = st.text_input("Enter your e-mail address:")
    nickname = st.text_input("Enter your nickname:")
    if st.button("Login"):
        if email and nickname:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.nickname = nickname
            st.session_state.show_game_intro = True
            st.rerun()
        else:
            st.warning("Please enter both e-mail and nickname!")

# --- JÁTÉK LEÍRÁS OLDAL ---
elif st.session_state.show_game_intro:
    st.image("header.png", use_container_width=True)
    st.subheader("Game description 📋")
    st.markdown("""
    Welcome to the ultimate game simulation!  
    In this game, you will select parameters for your manufacturing setup,  
    and see how your choices affect the profit, machine utilization, operator efficiency, and robot performance.  
    Can you optimize your production process and maximize your results? Let's find out!
    """)
    if st.button("Let's play"):
        st.session_state.show_game_intro = False
        st.rerun()

# --- JÁTÉK FELÜLET ---
else:
    st.image("header.png", use_container_width=True)
    st.subheader(f"Let's play the game, {st.session_state.nickname}! 👋")

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

                try:
                    profit_float = float(profit)
                    profit_str = f"{profit_float:10.3f}"
                except (TypeError, ValueError):
                    profit_str = "N/A"
                    st.warning(f"Profit érték nem szám! Talált sor a DataFrame {row_index}. indexű sora.")

                tab_labels.append(f"Attempt {idx+1}     - **Profit: {profit_str} €**")

    selectable_tabs = tab_labels[:st.session_state.current_tab+1]
    selected_tab = st.radio("Select attempt:", selectable_tabs, index=st.session_state.current_tab, format_func=lambda x: x)
    i = tab_labels.index(selected_tab)

    # --- Paraméterek kiválasztása ---
    if st.session_state.attempts[i] is None:
        st.subheader("Select parameters")
        selections = {}
        cols = st.columns(3)

        # Fix értékek: label -> kulcs
        param_options = {
            "Size of the batches": {"8 pcs": 1, "24 pcs": 2, "40 pcs": 3},
            "Type of the shipping box": {"Small": 1, "Medium": 2, "Large": 3},
            "Cycle time factor": {-20: -0.2, -10: -0.1, 0: 0, 10: 0.1, 20: 0.2},
            "Number of the operators": {"1 pcs": 1, "2 pcs": 2, "3 pcs": 3},
            "Type of the quality check": {"End of the line": 1, "All machine": 2},
            "Percentage of the quality check": {0: 0, 20: 0.2, 40: 0.4, 60: 0.6, 80: 0.8, 100: 1},
            "Overshooting": {0: 0, 10: 0.1, 20: 0.2, 30: 0.3}
        }

        selections = {}
        for idx, col_name in enumerate(param_cols):
            col = cols[idx % 3]
            with col:
                label = f"{col_name}:"
                
                if col_name in ["Cycle time factor", "Percentage of the quality check", "Overshooting"]:
                    # Slider float típusú
                    keys = sorted(param_options[col_name].keys())
                    min_val = float(keys[0])
                    max_val = float(keys[-1])
                    if len(keys) > 1:
                        step_val = float(keys[1] - keys[0])
                    else:
                        step_val = 1.0
                    default_val = float(keys[len(keys)//2])
                    selections[col_name] = st.slider(
                        label,
                        min_value=min_val,
                        max_value=max_val,
                        step=step_val,
                        value=default_val,
                        format="%g"
                    )
                    # Kereséshez a kulcsérték
                    selections[col_name] = param_options[col_name][int(selections[col_name])]
                else:
                    options = list(param_options[col_name].keys())
                    selected_label = st.radio(label, options, index=0)
                    selections[col_name] = param_options[col_name][selected_label]
                
                # Elválasztó a widget alatt
                st.markdown("<hr style='border:1px solid #eee; margin:10px 0'>", unsafe_allow_html=True)



        if st.button("Run the simulation!"):
            st.session_state.attempts[i] = selections
            st.rerun()

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

            # Profit olvasás biztonságosan
            profit = selected_row.get("Profit", None)
            if profit is not None:
                profit_rounded = round(profit, 3)
                profit_str = f"{profit_rounded:>10.3f}"
            else:
                profit_str = "N/A"
                st.warning(f"Profit érték nem található. A megtalált sor a DataFrame {row_index}. indexű sora.")

            # ---------------- Kódok jelentés és mértékegység ----------------
            code_meanings = {
                "Size of the batches": {1: 8, 2: 24, 3: 40},
                "Type of the shipping box": {1: "Small", 2: "Medium", 3: "Large"},
                "Cycle time factor": {1: 1, 2: 2, 3: 3},
                "Type of the quality check": {1: "End of the line", 2: "All machine"},
                "Percentage of the quality check": {0: 0, 0.2: 20, 0.4: 40, 0.6: 60, 0.8: 80, 1: 100},
                "Overshooting": {0: 0, 0.1: 10, 0.2: 20, 0.3: 30},
                "Reached the required amount": {99: "No", 1: "Yes"}
                # A többi paraméternél nincs kód, értékét használjuk
            }

            units = {
                "Size of the batches": "[pcs]",
                "Type of the shipping box": "",
                "Cycle time factor": "[%]",
                "Number of the operators": "[operator(s)]",
                "Type of the quality check": "",
                "Percentage of the quality check": "[%]",
                "Overshooting": "[%]",
                "Elapsed time": "",
                "Used rods": "[pcs]",
                "Used raw bases": "[pcs]",
                "Used pins": "[pcs]",
                "Outcome - All": "[pcs]",
                "Outcome - OK": "[pcs]",
                "Outcome - NOK": "[pcs]",
                "Used retail boxes": "[pcs]",
                "Used shipper boxes": "[pcs]",
                "Used pallets": "[pcs]",
                "Reached the required amount": "",
                "Difference from the required - OK": "[pcs]",
                "Difference from the required - All": "[pcs]",
                "Used electricity - T100": "[kW]",
                "Used electricity - T200": "[kW]",
                "Used electricity - T800": "[kW]",
                "Income": "[€]",
                "Outgo": "[€]",
                "Profit": "[€]"
            }

            # Profit oszlop index
            profit_index = df.columns.get_loc("Profit")
            cols_to_show = list(df.columns[:profit_index + 1])  # Profit is benne

            # Táblázat készítése biztonságosan
            values_with_units = []
            for col in cols_to_show:
                if col == "Profit":
                    values_with_units.append(f"{profit_str} {units.get(col,'')}")
                else:
                    # Ha van jelentés a kódhoz, azt használjuk, különben a raw értéket
                    if col in code_meanings:
                        value = code_meanings[col].get(selected_row[col], selected_row[col])
                    else:
                        value = selected_row[col]
                    values_with_units.append(f"{value} {units.get(col,'')}")

            result_df = pd.DataFrame({
                "Parameter": cols_to_show,
                "Value": values_with_units
            })

            # ---------------- Csoportosított megjelenítés ----------------
            groups = {
                "Finances 💸": [
                    "Income", "Outgo", "Profit"
                ],
                "Input parameters ➡️": [
                    "Size of the batches", "Type of the shipping box", "Cycle time factor",
                    "Number of the operators", "Type of the quality check",
                    "Percentage of the quality check", "Overshooting"
                ],
                "Shipping details 🚚": [
                    "Elapsed time", "Outcome - All", "Outcome - OK", "Outcome - NOK",
                    "Reached the required amount", "Difference from the required - OK",
                    "Difference from the required - All"
                ],
                "Used raw and packing materials 📦": [
                    "Used rods", "Used raw bases", "Used pins", "Used retail boxes",
                    "Used shipper boxes", "Used pallets"
                ],
                "Energy consumption ⚡": [
                    "Used electricity - T100", "Used electricity - T200", "Used electricity - T800"
                ]
            }

            st.subheader("Results by groups")

            for group_name, cols in groups.items():
                expanded_state = True if group_name == "Finances 💸" else False

                with st.expander(group_name, expanded=expanded_state):
                    display_data = []
                    for col in cols:
                        if col not in df.columns:
                            continue

                        # Az érték mértékegységgel, Profit 2 tizedesjeggyel
                        if col == "Profit":
                            profit_float = float(profit_str)
                            value = f"{profit_float:.2f} {units.get(col,'')}"
                        else:
                            if col in code_meanings:
                                val = code_meanings[col].get(selected_row[col], selected_row[col])
                            else:
                                val = selected_row[col]
                            value = f"{val} {units.get(col,'')}"

                        display_data.append({
                            "Parameter": col,
                            "Value": value
                        })

                    if display_data:
                        group_df = pd.DataFrame(display_data)

                        def highlight_profit(row):
                            styles = [''] * len(row)
                            for i, param in enumerate(group_df['Parameter']):
                                if param == 'Profit':
                                    try:
                                        val = float(profit_str)
                                        color = 'green' if val > 0 else 'red'
                                    except:
                                        color = 'black'
                                    styles[i] = f'color: {color}; font-weight: bold'
                            return styles

                        styled_df = group_df.style.apply(highlight_profit, axis=0)
                        st.dataframe(styled_df, use_container_width=True, hide_index=True)



                    else:
                        st.info("Nincs adat ebben a csoportban.")








            # ---------------- Itt jönnek a grafikonok ----------------
            # ---------------- Itt jönnek a grafikonok ----------------
            with st.expander("Utilization charts - machines, operators, robots 📊", expanded=False):
                import plotly.express as px

                def create_bar_chart(selected_row, prefix_list, entity_name):
                    """
                    Készít egy bar chart-ot az adott entitás státuszairól.
                    prefix_list: list of prefixes, pl. ["Machine T100 -", "Machine T200 -"]
                    entity_name: x tengely felirat
                    """
                    data = []
                    for prefix in prefix_list:
                        # Az összes oszlop, ami ezzel a prefix-szel kezdődik
                        cols = [c for c in df.columns if c.startswith(prefix)]
                        if not cols:
                            continue
                        total = selected_row[cols].sum()
                        # Státuszok és arányok
                        for col in cols:
                            status = col.split("-")[-1].strip()
                            percent = (selected_row[col] / total * 100) if total > 0 else 0
                            entity_full_name = prefix.replace(" -", "").strip()  # pl. Machine T100
                            data.append({entity_name: entity_full_name, "Status": status, "Ratio (%)": percent})
                    plot_df = pd.DataFrame(data)
                    
                    fig = px.bar(
                        plot_df,
                        x=entity_name,
                        y="Ratio (%)",
                        color="Status",
                        text="Ratio (%)",
                        title=f"{entity_name} utilization (%)"
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
                    fig.update_layout(yaxis=dict(ticksuffix="%"))
                    st.plotly_chart(fig)

                # Gépek
                machine_prefixes = ["Machine T100 -", "Machine T200 -", "Machine T800 -"]
                create_bar_chart(selected_row, machine_prefixes, "Machines")

                # Operátorok (WP)
                wp_prefixes = ["Operator 01 -", "Operator 02 -", "Operator 03 -"]
                create_bar_chart(selected_row, wp_prefixes, "Operator(s)")

                # Robotok
                robot_prefixes = ["Robot 01 -", "Robot 02 -"]
                create_bar_chart(selected_row, robot_prefixes, "Robot(s)")




            # ---------------------------------------------------------------------
            # ---------------------------------------------------------------------
            # --- New attempt gomb ---
            if i < total_attempts - 1:  # Ha még nem az utolsó attempt
                if st.button("New attempt", key=f"new_attempt_{i}"):
                    st.session_state.current_tab = i + 1  # Következő attempt
                    # Scroll vissza a tetejére
                    components.html("<script>window.scrollTo(0,0);</script>", height=0)
                    st.rerun()  # Újrarender

