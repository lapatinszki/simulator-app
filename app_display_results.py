import streamlit as st
import pandas as pd

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


# ---------------- Mértékegységek ----------------
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


#------------------------  1. TÁBLÁZATOK LÉTREHOZÁSA  -------------------------------
def create_tables(selected_row, row_index, df):

    # Profit olvasás biztonságosan
    profit = selected_row.get("Profit", None)
    if profit is not None:
        st.session_state.profit_rounded = round(profit, 3)
        st.session_state.profit_str = f"{st.session_state.profit_rounded:>10.3f}"

    else:
        st.session_state.profit_str = "N/A"
        st.warning(f"Profit érték nem található. A megtalált sor a DataFrame {row_index}. indexű sora.")


    # Profit oszlop index
    profit_index = df.columns.get_loc("Profit")
    cols_to_show = list(df.columns[:profit_index + 1])  # Profit is benne

    # Táblázat készítése biztonságosan
    values_with_units = []
    for col in cols_to_show:
        if col == "Profit":
            values_with_units.append(f"{st.session_state.profit_str} {units.get(col,'')}")
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
    

#------------------------  2. TÁBLÁZATOK megjelenítése  -------------------------------
def display_tables(selected_row, df):

    st.subheader(f"**Result by groups**")
    # Feltételezve, hogy profit_float az aktuális profit
    for group_name, cols in groups.items():
        expanded_state = True if group_name == "Finances 💸" else False

        with st.expander(group_name, expanded=expanded_state):
            display_data = []
            for col in cols:
                if col not in df.columns:
                    continue

                # Az érték mértékegységgel, Profit 2 tizedesjeggyel
                if col == "Profit":
                    profit_float = float(st.session_state.profit_str)
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
                                val = float(st.session_state.profit_str)
                                color = 'green' if val > 0 else 'red'
                            except:
                                color = 'black'
                            styles[i] = f'color: {color}; font-weight: bold'
                    return styles

                styled_df = group_df.style.apply(highlight_profit, axis=0)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)



            else:
                st.info("Nincs adat ebben a csoportban.")


#------------------------  3. GRAFIKONOK megjelenítése  -------------------------------
def display_charts(selected_row, df):
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
