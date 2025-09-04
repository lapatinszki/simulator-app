import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# --- Force light mode ---
st.markdown(
    """
    <style>
    /* Force light mode */
    :root {
        --background-color: #ffffff;
        --secondary-background-color: #ffffff;
        --primary-color: #0B142A;
        --text-color: #0B142A;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER KÉP ---
st.image("header.png", use_container_width=True)

# --- LOGIN KEZELÉS ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Welcome to the Game 🎮")
    email = st.text_input("Enter your e-mail address:")
    nickname = st.text_input("Enter your nickname:")
    if st.button("Let's play"):
        if email and nickname:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.nickname = nickname
            st.session_state.attempts = [None]*5
            st.session_state.current_tab = 0
            st.rerun()
        else:
            st.warning("Please enter both e-mail and nickname!")

else:
    st.title(f"Let's play a game, {st.session_state.nickname}! 👋")

    @st.cache_data
    def load_data():
        return pd.read_excel("data.xlsx")
    df = load_data()

    param_cols = [
        "Size of the batches",
        "Type of the shipping box",
        "Cycle time factor",
        "Number of the operators",
        "Type of the quality check",
        "Perentage of the quality check",
        "Overplus production"
    ]

    total_attempts = 5
    current_attempt_display = st.session_state.current_tab + 1
    st.markdown(f"**{total_attempts} attempts in total. You are currently at attempt {current_attempt_display}.**")

    # --- Tab logika ---
    tab_labels = []
    for idx in range(total_attempts):
        if st.session_state.attempts[idx] is None:
            tab_labels.append(f"Attempt {idx+1}")
        else:
            mask = (
                (df["Size of the batches"] == st.session_state.attempts[idx]["Size of the batches"]) &
                (df["Type of the shipping box"] == st.session_state.attempts[idx]["Type of the shipping box"]) &
                (df["Cycle time factor"].astype(float).round(1) == round(float(st.session_state.attempts[idx]["Cycle time factor"]), 1)) &
                (df["Number of the operators"] == st.session_state.attempts[idx]["Number of the operators"]) &
                (df["Type of the quality check"] == st.session_state.attempts[idx]["Type of the quality check"]) &
                (df["Perentage of the quality check"].astype(float).round(1) == round(float(st.session_state.attempts[idx]["Perentage of the quality check"]), 1)) &
                (df["Overplus production"] == st.session_state.attempts[idx]["Overplus production"])
            )
            if mask.sum() > 0:
                profit = df[mask].iloc[0]["Profit [EUR]"]
                profit_rounded = round(profit, 3)
                profit_str = f"{profit_rounded:>10.3f}"
                tab_labels.append(f"Attempt {idx+1} - Profit: <code>{profit_str} $</code>")
            else:
                tab_labels.append(f"Attempt {idx+1}")

    selectable_tabs = tab_labels[:st.session_state.current_tab+1]
    selected_tab = st.radio("Select attempt:", selectable_tabs, index=st.session_state.current_tab, format_func=lambda x: x)
    i = tab_labels.index(selected_tab)

    # --- Paraméterek kiválasztása ---
    if st.session_state.attempts[i] is None:
        st.subheader("Select parameters")
        selections = {}

        # 3x3 grid oszlopok
        cols = st.columns(3)

        # Paraméterek konfigurációja
        param_config = [
            ("Size of the batches", "radio"),
            ("Type of the shipping box", "radio"),
            ("Cycle time factor", "slider", (-20, 20, 10, 0)),
            ("Number of the operators", "radio"),
            ("Type of the quality check", "radio"),
            ("Perentage of the quality check", "slider", (0, 100, 20, 0)),
            ("Overplus production", "radio")
        ]

        for idx, param in enumerate(param_config):
            col = cols[idx % 3]
            with col:
                if param[1] == "slider":
                    min_val, max_val, step, default = param[2]
                    selections[param[0]] = st.slider(
                        param[0],
                        min_value=int(min_val),
                        max_value=int(max_val),
                        step=int(step),
                        value=int(default),
                        key=param[0]
                    )
                elif param[1] == "radio":
                    options = sorted(df[param[0]].dropna().unique())
                    selections[param[0]] = st.radio(param[0], options, index=0, key=param[0])

        if st.button("Search result"):
            st.session_state.attempts[i] = selections
            st.rerun()

    else:
        selections = st.session_state.attempts[i]

        mask = (
            (df["Size of the batches"] == selections["Size of the batches"]) &
            (df["Type of the shipping box"] == selections["Type of the shipping box"]) &
            (df["Cycle time factor"].astype(float).round(1) == round(float(selections["Cycle time factor"]), 1)) &
            (df["Number of the operators"] == selections["Number of the operators"]) &
            (df["Type of the quality check"] == selections["Type of the quality check"]) &
            (df["Perentage of the quality check"].astype(float).round(1) == round(float(selections["Perentage of the quality check"]), 1)) &
            (df["Overplus production"] == selections["Overplus production"])
        )

        if mask.sum() == 0:
            st.error("No row found for the selected parameter combination.")
        else:
            selected_row = df[mask].iloc[0]

            # Eredmény tábla
            excluded_cols = ["experiment", df.columns[0]]
            result_series = selected_row.drop(labels=excluded_cols, errors="ignore").iloc[:30]
            result_df = pd.DataFrame({"Parameter": result_series.index, "Value": result_series.values})
            param_rows = result_df[result_df["Parameter"].isin(param_cols)]
            other_rows = result_df[~result_df["Parameter"].isin(param_cols)]
            result_df = pd.concat([param_rows, other_rows], ignore_index=True)

            def highlight_params(row):
                if row["Parameter"] in param_cols:
                    return ['background-color: #1E2460', 'background-color: #1E2460']
                else:
                    return ['', '']

            styled = result_df.style.apply(highlight_params, axis=1)
            st.write("Result row (first 30 columns, parameters highlighted):")
            st.table(styled)

            # --- Grafikonok ---
            with st.spinner("Please wait..."):
                try:
                    # Machines
                    statuses = ["Waiting for MU", "Processing", "Failed", "Setting up"]
                    t100_cols = df.columns[30:34]
                    t200_cols = df.columns[34:38]
                    t800_cols = df.columns[38:42]
                    machine_data = []
                    for machine, cols in zip(["T100", "T200", "T800"], [t100_cols, t200_cols, t800_cols]):
                        total = selected_row[cols].sum()
                        for status, col in zip(statuses, cols):
                            percent = (selected_row[col]/total*100) if total>0 else 0
                            machine_data.append({"Machines": machine, "Status": status, "Ratio (%)": percent})
                    plot_df = pd.DataFrame(machine_data)
                    fig = px.bar(plot_df, x="Machines", y="Ratio (%)", color="Status", text="Ratio (%)", title="Machine utilization (%)")
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
                    fig.update_layout(yaxis=dict(ticksuffix="%"), xaxis_title="Machines")
                    st.plotly_chart(fig)

                    # Operators
                    operator_cols = {"Operator #01": df.columns[42:48], "Operator #02": df.columns[48:54], "Operator #03": df.columns[54:60]}
                    operator_data = []
                    for op_name, cols in operator_cols.items():
                        total = selected_row[cols].sum()
                        for col in cols:
                            status = col.split("-")[-1].strip()
                            percent = (selected_row[col]/total*100) if total>0 else 0
                            operator_data.append({"Operator": op_name, "Status": status, "Ratio (%)": percent})
                    op_df = pd.DataFrame(operator_data)
                    fig2 = px.bar(op_df, x="Operator", y="Ratio (%)", color="Status", text="Ratio (%)", title="Operator utilization (%)")
                    fig2.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
                    fig2.update_layout(yaxis=dict(ticksuffix="%"), xaxis_title="Operators")
                    st.plotly_chart(fig2)

                    # Robots
                    robot_cols = {"Robot #01": df.columns[60:67], "Robot #02": df.columns[67:74]}
                    robot_data = []
                    for robot_name, cols in robot_cols.items():
                        total = selected_row[cols].sum()
                        for col in cols:
                            status = col.split("-")[-1].strip()
                            percent = (selected_row[col]/total*100) if total>0 else 0
                            robot_data.append({"Robot": robot_name, "Status": status, "Ratio (%)": percent})
                    robot_df = pd.DataFrame(robot_data)
                    fig3 = px.bar(robot_df, x="Robot", y="Ratio (%)", color="Status", text="Ratio (%)", title="Robot utilization (%)")
                    fig3.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
                    fig3.update_layout(yaxis=dict(ticksuffix="%"), xaxis_title="Robots")
                    st.plotly_chart(fig3)

                except Exception as e:
                    st.error(f"An error occurred while creating the chart: {e}")

            # --- New attempt gomb ---
            if i < total_attempts-1:
                if st.button("New attempt", key=f"new_attempt_{i}"):
                    st.session_state.current_tab = i + 1
                    components.html("<script>window.scrollTo(0,0);</script>", height=0)
                    st.rerun()
