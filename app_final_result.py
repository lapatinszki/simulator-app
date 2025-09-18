import app_modify_GitTable, app_modify_tables, app_email
import streamlit.components.v1 as components
import streamlit as st
import time

def calculate_results(github_token, nickname, email):
    # Maximum profit a játékos összes attempt-jából
    attempts = [a for a in st.session_state.attempts if a is not None]
    if attempts:
        profits = [a["Profit"] for a in attempts]
        max_profit = max(profits)

        if github_token == None: #Lokális futtatás
            rank = app_modify_tables.get_rank_for_profit(max_profit)
        else: #Cloud futtatás
            rank = app_modify_GitTable.get_rank_for_profit(max_profit, "lapatinszki/simulator-app")

        # --- Ordinal suffix függvény ---
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            return f"{n}{suffix}"

        rank_str = ordinal(rank)

    gap_height = 60  # itt állítod a magasságot

    html_gap = f"""
    <div style="height:{gap_height}px;"></div>
    """

    components.html(html_gap, height=gap_height)


    html_content_1 = f"""
    <style>
    .container {{
        position: relative;
        overflow: visible;
        height: auto;
        margin-bottom: 5px;
        text-align: center;
        color: white;
        padding: 8px 12px;
    }}

    @keyframes slideUp {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    .slide-up {{
        opacity: 0;
        display: block;
        width: 100%;
        animation-name: slideUp;
        animation-duration: 0.8s;
        animation-timing-function: ease-out;
        animation-fill-mode: both;
        white-space: normal;
        word-wrap: break-word;
        margin: 8px 0;
    }}

    .slide-up.delay-1 {{ animation-delay: 1.0s; }}
    .slide-up.delay-2 {{ animation-delay: 1.5s; }}
    .slide-up.delay-3 {{ animation-delay: 2.0s; }}
    .slide-up.delay-4 {{ animation-delay: 2.5s; }}

    .big-number {{ line-height: 0.9; }}
    </style>

    <div class="container">
        <div class="slide-up delay-1" style='font-size:18px; margin-bottom:5px;'>
            Your highest profit: <span style="color:#F15922; font-weight:bold;">{max_profit:.2f} €</span>
        </div>

        <div class="slide-up delay-2" style='font-size:18px; margin-bottom:15px;'>
            Your rank in the current leaderboard:
        </div>

        <div class="slide-up delay-3 big-number" style='font-size:80px; font-weight:bold; margin-bottom:15px; color:#F15922;'>
            {rank_str}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(() => {{
                confetti({{
                    particleCount: 150,
                    spread: 100,
                    origin: {{ y: 0.5 }}
                }});
            }}, 1900);
        }});
        </script>

        <div class="slide-up delay-4" style='font-size:14px; margin-top:0px;'>
            Congratulations! 🎉 You completed the game successfully.
        </div>
    </div>
    """
    components.html(html_content_1, height=200)


    html_content_2 = """
    <style>
    .container {
        position: relative;
        overflow: visible;
        height: auto;
        margin-bottom: 5px;
        text-align: center;
        color: white;
        padding: 8px 12px;
    }

    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .slide-up {
        opacity: 0;
        display: block;
        width: 100%;
        animation-name: slideUp;
        animation-duration: 0.8s;
        animation-timing-function: ease-out;
        animation-fill-mode: both;
        white-space: normal;
        word-wrap: break-word;
        margin: 8px 0;
    }

    .slide-up.delay-5 { animation-delay: 4.5s; }
    .slide-up.delay-6 { animation-delay: 5.5s; }
    </style>

    <div class="container">
        <div class="slide-up delay-5" style='font-size:18px; font-weight:bold; color:#F15922; margin-top:50px;'>
            What’s the ROI of turning 27 variables into one clear decision?
        </div>

        <div class="slide-up delay-6" style='font-size:14px; margin-top:5px; text-align: justify; text-justify: inter-word;'>
            This simulation was built in just one week, yet it already allows you to run unlimited experiments across 27 input parameters — 7 of which are highlighted here for clarity. 
            In real-world production, the number of variables is even higher, making manual testing impractical. 
            That is why advanced methods such as genetic algorithms and neural networks can be applied to optimize performance across large parameter sets. 
            The result: tangible improvements with relatively small investment, where the cost of just a single day of operations can pay back within only a few months.
        </div>
    </div>
    """

    components.html(html_content_2, height=800)





    #Email küldése eredményekről + infos cucc:
    if github_token != None: #Felhő futtatás
        app_email.send_results(email, nickname, max_profit)

    
