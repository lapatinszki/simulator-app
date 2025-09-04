import streamlit as st

class ParameterBox:
    def __init__(self, name, options, emoji="🔧", mode="radio"):
        self.name = name
        self.options = options
        self.emoji = emoji
        self.mode = mode  # "radio" vagy "slider"

    def render(self):
        # Fejléc (sötétkék, középre igazítva, félkövér)
        st.markdown(
            f"""
            <div style="
                background-color: #003366;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                margin-bottom: 0px;
            ">
                {self.emoji} {self.name}
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = None

        if self.mode == "radio":
            # CSS: radio gombok vízszintesen, egyenletes elosztással
            st.markdown(
                """
                <style>
                div[data-testid="stRadio"] > label {
                    flex: 1;
                    text-align: center;
                    font-weight: 500;
                }
                div[data-testid="stRadio"] {
                    display: flex !important;
                    justify-content: space-evenly !important;
                    gap: 10px;
                    margin-top: 6px;
                    margin-bottom: 20px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            selected = st.radio(
                label="",
                options=self.options,
                horizontal=True,
                key=self.name
            )

        elif self.mode == "slider":
            # Slider megjelenítés
            selected = st.slider(
                label="",
                min_value=0,
                max_value=len(self.options) - 1,
                value=len(self.options) // 2,
                format="%s",
                key=self.name
            )
            selected = self.options[selected]  # indexből érték

            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

        return selected
