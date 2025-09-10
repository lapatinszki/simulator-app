import streamlit.components.v1 as components
import streamlit as st


def scroll_to_top():
    st.markdown(
    """
    <script>
    setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 1000);
    </script>
    """,
    unsafe_allow_html=True
)
