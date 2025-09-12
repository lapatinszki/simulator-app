import streamlit as st

# ---------------- Paraméterek  ----------------
param_cols = {
    "Size of the batches": "Bactch size",
    "Type of the shipping box": "Shipping box size",
    "Cycle time factor": "Machine - Cycle time factor [%]",
    "Number of the operators": "Employee headcount",
    "Type of the quality check": "Quality check type",
    "Percentage of the quality check": "Quality check rate [%]",
    "Overshooting": "Overshooting [%]"
}

# ---------------- Paraméterek kiválasztása ÉS Értékei ----------------
param_options = {
    "Size of the batches": {"8 [pcs]": 1, "24 [pcs]": 2, "40 [pcs]": 3},
    "Type of the shipping box": {"Small - capacity: 18 [pcs]": 1, "Medium - capacity: 24 [pcs]": 2, "Large - capacity: 30 [pcs]": 3},
    "Cycle time factor": {-20: -0.2, -10: -0.1, 0: 0, 10: 0.1, 20: 0.2},
    "Number of the operators": {"1 operator": 1, "2 operators": 2, "3 operators": 3},
    "Type of the quality check": {"End of the line": 1, "All machine": 2},
    "Percentage of the quality check": {0: 0, 20: 0.2, 40: 0.4, 60: 0.6, 80: 0.8, 100: 1},
    "Overshooting": {0: 0, 10: 0.1, 20: 0.2, 30: 0.3}
}

# ---------------- Paraméterek alapja ----------------
default_values = {
    "Size of the batches": 1,                   # első lehetőség
    "Type of the shipping box": 1,              # első lehetőség
    "Cycle time factor": 0.0,                   # középső érték
    "Number of the operators": 1,               # első lehetőség
    "Type of the quality check": 1,             # első lehetőség
    "Percentage of the quality check": 0.0,     # első érték
    "Overshooting": 0.0                         # első érték
}


def display_inputs(attempt_idx):
    n_cols = 3
    cols = st.columns(n_cols)

    # Ha még nincs selections a session_state-ben, hozzuk létre egyszer
    if "selections" not in st.session_state:
        st.session_state.selections = {}

    param_list = list(param_cols.items())
    n_rows = (len(param_list) + n_cols - 1) // n_cols  # hány sor kell

    for i, (col_name, label) in enumerate(param_list):
        # Transzponált elhelyezés
        col_idx = i // n_rows
        col = cols[col_idx]

        st_label = f"{label}:"

        # Előző érték megkeresése
        if st.session_state.get("back_to_info_values", {}).get(col_name) is not None:
            prev_val = st.session_state.back_to_info_values[col_name]
        elif attempt_idx > 0 and st.session_state.get("attempts", [None])[attempt_idx - 1] is not None:
            prev_val = st.session_state.attempts[attempt_idx - 1][col_name]
        else:
            prev_val = default_values.get(col_name, None) if default_values else None

        with col:
            widget_key = f"{col_name}_{attempt_idx}"  # egyedi key minden widgethez

            if col_name in ["Cycle time factor", "Percentage of the quality check", "Overshooting"]:
                options_dict = param_options[col_name]
                keys = sorted(options_dict.keys())
                min_val = keys[0]
                max_val = keys[-1]
                step_val = keys[1] - keys[0] if len(keys) > 1 else 1

                if prev_val is not None:
                    key_for_slider = next((k for k, v in options_dict.items() if v == prev_val), min_val)
                else:
                    key_for_slider = min_val

                selected_label = st.slider(
                    st_label,
                    min_value=min_val,
                    max_value=max_val,
                    step=step_val,
                    value=key_for_slider,
                    format="%g",
                    key=widget_key
                )
                st.session_state.selections[col_name] = options_dict[selected_label]

            else:
                options = list(param_options[col_name].keys())
                if prev_val is not None:
                    try:
                        index = options.index(next(k for k, v in param_options[col_name].items() if v == prev_val))
                    except StopIteration:
                        index = 0
                else:
                    index = 0

                selected_label = st.radio(
                    st_label,
                    options,
                    index=index,
                    key=widget_key
                )
                st.session_state.selections[col_name] = param_options[col_name][selected_label]

            st.markdown("<hr style='border:1px solid rgba(241, 89, 34, 0.3); margin:0px 0'>", unsafe_allow_html=True)

    return st.session_state.selections
