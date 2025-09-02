import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px

st.set_page_config(page_title="Excel Sor Megjelenítő", layout="centered")
st.title("Excel sor megjelenítő")

# Ellenőrizzük, hogy a fájl létezik-e
if not os.path.exists("data.xlsx"):
    st.error("A data.xlsx fájl nem található a repo-ban!")
    st.stop()

# Excel beolvasása
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

    # GIF animáció a "szimuláció fut" érzéshez
    st.image("loading.gif")
    time.sleep(1.5)  # rövid szünet, hogy látszódjon a GIF

    st.subheader(f"A(z) {st.session_state.row_number}. sor adatai:")

    # Csak a 7 bemeneti paraméter
    input_columns = ["param1","param2","param3","param4","param5","param6","param7"]
    st.write("**Bemeneti paraméterek:**")
    st.dataframe(selected_row[input_columns])

    # 3 géphasználati érték grafikonon
    usage_columns = ["machine1_usage","machine2_usage","machine3_usage"]
    st.write("**Géphasználat:**")
    usage_fig = px.bar(
        x=usage_columns,
        y=[selected_row[col] for col in usage_columns],
        labels={"x":"Gép","y":"Használat (%)"}
    )
    st.plotly_chart(usage_fig)

    # Profit kiemelése
    st.metric(label="Profit (EUR)", value=selected_row["profit"])

    # Új sor gomb
    if st.button("Új sor"):
        st.session_state.show_row = False
        st.session_state.row_number = None
