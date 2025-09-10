import app_modify_GitTable, app_modify_tables
import streamlit.components.v1 as components
import streamlit as st

def calculate_results(github_token):
    # Maximum profit a játékos összes attempt-jából
    attempts = [a for a in st.session_state.attempts if a is not None]
    if attempts:
        profits = [a["Profit"] for a in attempts]
        max_profit = max(profits)

        if github_token == None: #Lokális futtatás
            rank = app_modify_tables.get_rank_for_profit(max_profit)
        else: #Cloud futtatás
            rank = app_modify_GitTable.get_rank_for_profit(max_profit, github_token, "lapatinszki/simulator-app")

        # --- Ordinal suffix függvény ---
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            return f"{n}{suffix}"

        rank_str = ordinal(rank)

        # --- HTML a megjelenítéshez ---
        html_content = f"""
            <style>
            .container {{
            position: relative;
            overflow: hidden;
            height: 250px;
            margin-bottom: 5px;
            text-align: center;
            color: white;
            }}
            @keyframes slideUp {{
            0% {{opacity: 0; transform: translateY(100%);}}
            100% {{opacity: 1; transform: translateY(0);}}
            }}
            .slide-up {{
            opacity: 0;
            animation: slideUp 1s ease-out forwards;
            }}
            .slide-up.delay-1 {{ animation-delay: 1.0s; }}
            .slide-up.delay-2 {{ animation-delay: 1.5s; }}
            .slide-up.delay-3 {{ animation-delay: 2.0s; }}
            .slide-up.delay-4 {{ animation-delay: 2.5s; }}
            </style>

            <div class="container">
            <div class="slide-up delay-1" style='font-size:18px; margin-bottom:5px;'>
            Your best profit: <span style="color:#F15922; font-weight:bold;">{max_profit:.2f} €</span>
            </div>
            <div class="slide-up delay-2" style='font-size:18px; margin-bottom:5px;'>
            Your rank in the current leaderboard:
            </div>
            <div class="slide-up delay-3" style='font-size:72px; font-weight:bold; margin-bottom:5px; color:#F15922;'>
            {rank_str}
            </div>
            <div class="slide-up delay-4" style='font-size:14px; margin-top:5px;'>
            Congratulations! You completed the game successfully. 🎉
            </div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
            <script>
            setTimeout(() => {{
            confetti({{
            particleCount: 150,
            spread: 70,
            origin: {{ y: 0.6 }}
            }});
            }}, 2000);
            </script>
            """

        components.html(html_content, height=350)
