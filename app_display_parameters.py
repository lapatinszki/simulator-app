import streamlit as st

# ---------------- Paraméterek kiválasztása ÉS Értékei ----------------
param_options = {
    "Size of the batches": {"8 pcs": 1, "24 pcs": 2, "40 pcs": 3},
    "Type of the shipping box": {"Small": 1, "Medium": 2, "Large": 3},
    "Cycle time factor": {-20: -0.2, -10: -0.1, 0: 0, 10: 0.1, 20: 0.2},
    "Number of the operators": {"1 pcs": 1, "2 pcs": 2, "3 pcs": 3},
    "Type of the quality check": {"End of the line": 1, "All machine": 2},
    "Percentage of the quality check": {0: 0, 20: 0.2, 40: 0.4, 60: 0.6, 80: 0.8, 100: 1},
    "Overshooting": {0: 0, 10: 0.1, 20: 0.2, 30: 0.3}
}

def display_inputs(param_cols):
    cols = st.columns(3)
    # Fix értékek: label -> kulcs

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
    return selections