import streamlit as st
import pandas as pd

st.title("Excel sor megjelenítő")

# Excel betöltése (repo-ból)
df = pd.read_excel("data.xlsx")

# Session state a gombok kezeléséhez
if "show_row" not in st.session_state:
    st.session_state.show_row = False
if "row_number" not in st.session_state:
    st.session_state.row_number = None

# Ha még nem nyomták meg a "Mutasd" gombot
if not st.session_state.show_row:
    row_number = st.number_input(
        "Add meg a sor számát (1-től {}-ig)".format(len(df)),
        min_value=1,
        max_value=len(df),
        value=1,
        step=1
    )

    if st.button("Mutasd"):
        st.session_state.show_row = True
        st.session_state.row_number = row_number

# Ha a "Mutasd" gombot megnyomták
if st.session_state.show_row:
    selected_row = df.iloc[st.session_state.row_number - 1]
    st.write(f"A(z) {st.session_state.row_number}. sor adatai:")
    st.dataframe(selected_row)

    if st.button("Új sor"):
        st.session_state.show_row = False
        st.session_state.row_number = None
