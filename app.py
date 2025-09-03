import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Let's play a game!")

# --------- Cached Excel load ---------
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# Session state defaults
if "show_row" not in st.session_state:
    st.session_state.show_row = False
if "row_number" not in st.session_state:
    st.session_state.row_number = 1

def reset_app():
    st.session_state.show_row = False

# --------- Cached row processing ---------
@st.cache_data
def process_row(selected_row, columns):
    total = selected_row[columns].sum()
    data = []
    for col in columns:
        status = col.split("-")[-1].strip()
        percent = (selected_row[col] / total * 100) if total > 0 else 0
        data.append({"Status": status, "Value": selected_row[col], "Percent": percent})
    return data


# Row selection
if not st.session_state.show_row:
    with st.form("row_form"):
        row_number = st.number_input(
            "Enter the row number (1 to {}):".format(len(df)),
            min_value=1,
            max_value=len(df),
            value=st.session_state.row_number,
            step=1
        )
        submit = st.form_submit_button("Result")
        if submit:
            st.session_state.show_row = True
            st.session_state.row_number = row_number
            st.rerun()

# If a row is selected
if st.session_state.show_row:
    selected_row = df.iloc[st.session_state.row_number - 1]
    st.write(f"Data of row {st.session_state.row_number} (first 30 columns):")
    st.table(selected_row.iloc[:30])  # csak az első 30 oszlop


    with st.spinner("Please wait..."):
        try:
            # ---------------- Machines ----------------
            statuses = ["Waiting for MU", "Processing", "Failed", "Setting up"]
            t100_cols = df.columns[30:34]
            t200_cols = df.columns[34:38]
            t800_cols = df.columns[38:42]

            machine_data = []
            for machine, cols in zip(["T100", "T200", "T800"], [t100_cols, t200_cols, t800_cols]):
                total = selected_row[cols].sum()
                for status, col in zip(statuses, cols):
                    percent = (selected_row[col] / total * 100) if total > 0 else 0
                    machine_data.append({"Machines": machine, "Status": status, "Ratio (%)": percent})

            plot_df = pd.DataFrame(machine_data)
            fig = px.bar(
                plot_df,
                x="Machines",
                y="Ratio (%)",
                color="Status",
                text="Ratio (%)",
                title="Machine utilization (%)",
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
            fig.update_layout(yaxis=dict(ticksuffix="%"), xaxis_title="Machines")
            st.plotly_chart(fig)

            # ---------------- Operators ----------------
            operator_cols = {
                "Operator #01": df.columns[42:48],
                "Operator #02": df.columns[48:54],
                "Operator #03": df.columns[54:60],
            }

            operator_data = []
            for op_name, cols in operator_cols.items():
                total = selected_row[cols].sum()
                for col in cols:
                    status = col.split("-")[-1].strip()
                    percent = (selected_row[col] / total * 100) if total > 0 else 0
                    operator_data.append({"Operator": op_name, "Status": status, "Ratio (%)": percent})

            op_df = pd.DataFrame(operator_data)
            fig2 = px.bar(
                op_df,
                x="Operator",
                y="Ratio (%)",
                color="Status",
                text="Ratio (%)",
                title="Operator utilization (%)",

            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
            fig2.update_layout(yaxis=dict(ticksuffix="%"), xaxis_title="Operators")
            st.plotly_chart(fig2)

            # ---------------- Robots ----------------
            # Robot data előkészítés
            robot_cols = {
                "Robot #01": df.columns[60:67],  # 61–67
                "Robot #02": df.columns[67:74],  # 68–74
            }

            robot_data = []
            for robot_name, cols in robot_cols.items():
                total = selected_row[cols].sum()
                for col in cols:
                    status = col.split("-")[-1].strip()
                    percent = (selected_row[col] / total * 100) if total > 0 else 0
                    robot_data.append({"Robot": robot_name, "Status": status, "Ratio (%)": percent})

            robot_df = pd.DataFrame(robot_data)

            fig3 = px.bar(
                robot_df,
                x="Robot",
                y="Ratio (%)",
                color="Status",
                text="Ratio (%)",
                title="Robot utilization (%)",
            )

            fig3.update_traces(texttemplate='%{text:.1f}%', textposition="inside")
            fig3.update_layout(
                yaxis=dict(ticksuffix="%"),
                xaxis_title="Robots"
            )

            st.plotly_chart(fig3)


        except Exception as e:
            st.error(f"An error occurred while creating the chart: {e}")

    if st.button("Try again"):
        reset_app()
        st.rerun()




#py -m streamlit run app.py

#py -m streamlit run app.py --server.port 8501 --server.address 172.31.218.134
