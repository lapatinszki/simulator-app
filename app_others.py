import streamlit.components.v1 as components


def scroll_to_top():
    components.html(
    """
    <script>
    setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 1000);  // 1 másodperc múlva
    </script>
    """,
    height=0,
)
