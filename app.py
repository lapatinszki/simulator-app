import streamlit as st
from parameter_box import ParameterBox

st.set_page_config(page_title="Paraméterek", layout="centered")
st.title("📋 Paraméterek kiválasztása")

parameters = [
    {"name": "Hőmérséklet", "options": ["Alacsony", "Közepes", "Magas"], "emoji": "🌡️", "mode": "radio"},
    {"name": "Sebesség", "options": ["Lassú", "Normál", "Gyors"], "emoji": "🏎️", "mode": "slider"},
    {"name": "Nyomás", "options": ["Alacsony", "Közepes", "Magas", "Nagyon magas"], "emoji": "⚙️", "mode": "radio"},
    {"name": "Szín", "options": ["Piros", "Zöld"], "emoji": "🎨", "mode": "radio"},
]

selections = []
for param in parameters:
    box = ParameterBox(param["name"], param["options"], param["emoji"], param["mode"])
    selections.append(box.render())

if st.button("✅ Mentés"):
    st.success("Mentve!")
    for i, sel in enumerate(selections):
        st.write(f"- {parameters[i]['name']}: {sel}")
