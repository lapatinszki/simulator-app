import streamlit as st

# ---------------- Paraméterek  ----------------
param_cols = {
    "Size of the batches": "Batch size",
    "Type of the shipping box": "Shipping box size",
    "Cycle time factor": "Machine - Cycle time fact. [%]",
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
    "Size of the batches": 1,
    "Type of the shipping box": 1,
    "Cycle time factor": 0.0,
    "Number of the operators": 1,
    "Type of the quality check": 1,
    "Percentage of the quality check": 0.0,
    "Overshooting": 0.0
}

# ---------------- Tooltip szövegek ----------------
import streamlit as st

# Tooltip szövegek HTML formázással
info_texts = {
    "Size of the batches": "<i>Small ⟶ faster start, but more changeovers<br>Large ⟶ fewer changeovers, but slower start</i>",
    "Type of the shipping box": "<i>Small ⟶ lower price, more boxes, more pallets<br></i><i>Large ⟶ higher price, fewer boxes, fewer pallets</i>",
    "Cycle time factor": "<i>Faster ⟶ higher output, but lower availability, more rejects, demands higher energy, and more operator<br></i><i>Slower ⟶ lower output, but higher availability, fewer rejects, demands lower energy, and fewer operator</i>",
    "Number of the operators": "<i>Fewer operators ⟶ lower cost, but higher downtime risk<br></i><i>More operators ⟶ higher cost, but smoother production flow</i>",
    "Type of the quality check": "<i>At each station ⟶ demands more operator, but fewer rejects<br></i><i>End-of-line ⟶ demands fewer operator, but more rejects</i>",
    "Percentage of the quality check": "<i>Low percentage ⟶ demands fewer operator, but more outgoing rejects<br></i><i>High percentage ⟶ demands more operator, but less or none outgoing rejects</i>",
    "Overshooting": "Planned overproduction for reject compensation."
}

# CSS a tooltiphez
st.markdown("""
<style>
.tooltip-wrapper {
  display: inline-block;
  position: relative;
  margin-left: 2px;
}

.tooltip-icon {
  display: inline-block;
  background-color: #17a2b8;
  color: white;
  font-family: Arial, sans-serif;
  width: 16px;
  height: 16px;
  line-height: 16px;
  font-size: 12px;
  border-radius: 50%;
  text-align: center;
  cursor: pointer;
}

.tooltip-text {
  visibility: hidden;
  width: 350px;
  background-color: #333;
  color: #fff;
  text-align: left;
  padding: 4px 4px;
  border-radius: 6px;
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  line-height: 1.4;
  z-index: 1;
}

.tooltip-wrapper:focus .tooltip-text {
  visibility: visible;
}
</style>
""", unsafe_allow_html=True)


# ---------------- Fő függvény a bemenetekhez ----------------
def display_inputs(attempt_idx):
    n_cols = 3
    cols = st.columns(n_cols)
    st.session_state.setdefault("selections", {})

    # Biztonság: ha még nincs session_state back_to_info_values vagy attempts
    st.session_state.setdefault("back_to_info_values", {})
    st.session_state.setdefault("attempts", [{}])

    # Jelenlegi attempt index ellenőrzése
    if not isinstance(attempt_idx, int):
        attempt_idx = 0

    param_list = list(param_cols.items())
    n_rows = (len(param_list) + n_cols - 1) // n_cols  # hány sor kell

    for i, (col_name, label) in enumerate(param_list):
        col_idx = i // n_rows
        col = cols[col_idx]

        # Tooltip szöveg
        tooltip_text = info_texts.get(col_name, "")

        # Előző attempt értéke
        if st.session_state.back_to_info_values.get(col_name) is not None:
            prev_val = st.session_state.back_to_info_values[col_name]
        elif attempt_idx > 0 and st.session_state.attempts[attempt_idx - 1] is not None:
            prev_val = st.session_state.attempts[attempt_idx - 1][col_name]
        else:
            prev_val = default_values.get(col_name, None) if default_values else None

        with col:
            if col_name in ["Cycle time factor", "Percentage of the quality check", "Overshooting"]:
                options_dict = param_options[col_name]
                keys = sorted(options_dict.keys())
                min_val = keys[0]
                max_val = keys[-1]
                step_val = keys[1] - keys[0] if len(keys) > 1 else 1

                if prev_val is not None:
                    key_for_slider = next((k for k,v in options_dict.items() if v == prev_val), min_val)
                else:
                    key_for_slider = min_val

                # Paraméter név + tooltip közvetlenül a slider fölé
                st.markdown(f"""
                <div style='margin:0; padding:0';">
                    <div style='margin:0; padding:0'>{label}:
                    <span class="tooltip-wrapper" tabindex="0">
                        <span class="tooltip-icon">i</span>
                        <span class="tooltip-text">{tooltip_text}</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
                selected_label = st.slider(
                    "",  # üres label
                    min_value=min_val,
                    max_value=max_val,
                    step=step_val,
                    value=key_for_slider,
                    format="%g"
                )
                st.session_state.selections[col_name] = options_dict[selected_label]

            else:
                options = list(param_options[col_name].keys())
                if prev_val is not None:
                    try:
                        index = options.index(next(k for k,v in param_options[col_name].items() if v == prev_val))
                    except StopIteration:
                        index = 0
                else:
                    index = 0

                # Paraméter név + tooltip közvetlenül a radio box fölé
                st.markdown(f"""
                    <div style='margin:0; padding:0';">
                        <div style='margin:0; padding:0'>{label}:
                        <span class="tooltip-wrapper" tabindex="0">
                            <span class="tooltip-icon">i</span>
                            <span class="tooltip-text">{tooltip_text}</span>
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                selected_label = st.radio(
                    "",  # üres label
                    options,
                    index=index,
                    horizontal=False
                )
                st.session_state.selections[col_name] = param_options[col_name][selected_label]

            # Vízszintes vonal elválasztónak
            st.markdown("<hr style='border:1px solid rgba(241, 89, 34, 0.3); margin:0px 0'>", unsafe_allow_html=True)

    return st.session_state.selections
