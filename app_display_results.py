import streamlit as st
import pandas as pd
import time
import base64

# ---------------- Paraméterek központi definíciója ----------------
parameters = {
    "Income":                         {"label": "Revenue",                  "unit": "[€]",          "group": "Finances 💸"},
    "Outgo":                          {"label": "Expense",                  "unit": "[€]",          "group": "Finances 💸"},
    "Profit":                         {"label": "Profit",                   "unit": "[€]",          "group": "Finances 💸"},

    "Size of the batches":            {"label": "Size of the batches",                  "unit": "[pcs]",        "group": "Input parameters ⚙️", "codes": {1: 8, 2: 24, 3: 40}},
    "Type of the shipping box":       {"label": "Size of the shipping box",             "unit": "",             "group": "Input parameters ⚙️", "codes": {1: "Small", 2: "Medium", 3: "Large"}},
    "Cycle time factor":              {"label": "Machines - cycle time factor",         "unit": "[%]",          "group": "Input parameters ⚙️", "codes": {-0.2: -20.00, -0.1: -10.00, 0: 0.00, 0.1: 10.00, 0.2: 20.00}},
    "Number of the operators":        {"label": "Number of the operators",              "unit": "[operator]",   "group": "Input parameters ⚙️"},
    "Type of the quality check":      {"label": "Type of the quality check",            "unit": "",             "group": "Input parameters ⚙️", "codes": {1: "End of the line", 2: "All machine"}},
    "Percentage of the quality check":{"label": "Percentage of the quality check",      "unit": "[%]",          "group": "Input parameters ⚙️", "codes": {0: 0.00, 0.2: 20.00, 0.4: 40.00, 0.6: 60.00, 0.8: 80.00, 1: 100.00}},
    "Overshooting":                   {"label": "Percentage of the overshooting",       "unit": "[%]",          "group": "Input parameters ⚙️", "codes": {0: 0.00, 0.1: 10.00, 0.2: 20.00, 0.3: 30.00}},
    
    "Elapsed time":                         {"label": "Elapsed time",               "unit": "",             "group": "Shipping details 🚚"},
    "Outcome - All":                        {"label": "Outcome (All)",              "unit": "[pcs]",        "group": "Shipping details 🚚"},
    "Outcome - OK":                         {"label": "Outcome (OK)",               "unit": "[pcs]",        "group": "Shipping details 🚚"},
    "Outcome - NOK":                        {"label": "Outcome (NOK)",              "unit": "[pcs]",        "group": "Shipping details 🚚"},
    "Reached the required amount":          {"label": "Reached the 1000 pieces",    "unit": "",             "group": "Shipping details 🚚", "codes": {99: "No", 1: "Yes"}},
    "Difference from the required - OK":    {"label": "Diff. from required (OK)",   "unit": "[pcs]",        "group": "Shipping details 🚚"},
    "Difference from the required - All":   {"label": "Diff. from required (All)",  "unit": "[pcs]",        "group": "Shipping details 🚚"},
    
    "Used rods":                      {"label": "Used rods",               "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    "Used raw bases":                 {"label": "Used raw bases",          "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    "Used pins":                      {"label": "Used pins",               "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    "Used retail boxes":              {"label": "Used retail boxes",       "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    "Used shipper boxes":             {"label": "Used shipper boxes",      "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    "Used pallets":                   {"label": "Used pallets",            "unit": "[pcs]",        "group": "Used raw and packing materials 📦"},
    
    "Used electricity - T100":        {"label": "Used electricity T100",        "unit": "[kW]",         "group": "Energy consumption ⚡"},
    "Used electricity - T200":        {"label": "Used electricity T200",        "unit": "[kW]",         "group": "Energy consumption ⚡"},
    "Used electricity - T800":        {"label": "Used electricity T800",        "unit": "[kW]",         "group": "Energy consumption ⚡"},
}


# ---------------- Segédfüggvény: érték feldolgozás ----------------
def format_value(col, raw_val):
    param = parameters.get(col, {})
    unit = param.get("unit", "")
    codes = param.get("codes", {})

    val = codes.get(raw_val, raw_val)
    return f"{val} {unit}".strip()

#------------------------  0. GIF lejátszása -------------------------------
def play_the_GIF():
    # Betöltjük a GIF-et base64-be
    with open("loading.gif", "rb") as f:
        data = f.read()
        data_url = base64.b64encode(data).decode()

    # Placeholder a teljes overlay-hez
    overlay_placeholder = st.empty()
    # HTML overlay a placeholder-ben
    overlay_html = f"""
    <div style="
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: rgba(12, 23, 45, 0.95);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    ">
        <img src="data:image/gif;base64,{data_url}" style="width:600px;">
    </div>
    """
    overlay_placeholder.markdown(overlay_html, unsafe_allow_html=True)

    # Hosszú folyamat szimulálása
    time.sleep(5)  # ide jön a tényleges betöltés / számítás

    # Eltüntetés a .empty() metódussal
    overlay_placeholder.empty()





#------------------------  1. TÁBLÁZATOK megjelenítése  -------------------------------
def display_tables(selected_row, df):
    st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
    st.subheader("**Result by groups**")

    # Csoportok kigyűjtése a parameters alapján
    groups = {}
    for col, meta in parameters.items():
        grp = meta.get("group", "Other")
        groups.setdefault(grp, []).append(col)

    for group_name, cols in groups.items():
        expanded_state = True if group_name == "Finances 💸" else False

        with st.expander(group_name, expanded=expanded_state):
            display_data = []
            for col in cols:
                if col not in df.columns:
                    continue

                label = parameters[col]["label"]
                value = format_value(col, selected_row[col])

                display_data.append({"Parameter": label, "Value": value})

            if display_data:
                group_df = pd.DataFrame(display_data)

                # Profit sor színezése
                def highlight_profit(row):
                    styles = [''] * len(row)
                    if row["Parameter"] == "Profit":
                        val_str = st.session_state.profit_str = f"{round(selected_row.get("Profit", None), 3):>10.3f}"
                        try:
                            val = float(val_str)
                            color = "green" if val > 0 else "red"
                        except:
                            color = "black"
                        styles[1] = f"color: {color}; font-weight: bold"
                    return styles

                styled_df = group_df.style.apply(highlight_profit, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.info("Nincs adat ebben a csoportban.")



#------------------------  3. GRAFIKONOK megjelenítése  -------------------------------
def display_charts(selected_row, df):
    with st.expander("Utilization charts 📊", expanded=False):
        import plotly.express as px

        def create_bar_chart(selected_row, prefix_list, entity_name):
            data = []
            for prefix in prefix_list:
                cols = [c for c in df.columns if c.startswith(prefix)]
                if not cols:
                    continue
                total = selected_row[cols].sum()
                for col in cols:
                    status = col.split("-")[-1].strip()
                    percent = (selected_row[col] / total * 100) if total > 0 else 0
                    entity_full_name = prefix.replace(" -", "").strip()
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

        # Operátorok
        wp_prefixes = ["Operator 01 -", "Operator 02 -", "Operator 03 -"]
        create_bar_chart(selected_row, wp_prefixes, "Operator(s)")

        # Robotok
        robot_prefixes = ["Robot 01 -", "Robot 02 -"]
        create_bar_chart(selected_row, robot_prefixes, "Robot(s)")
