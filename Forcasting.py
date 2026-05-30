import streamlit as st


dashboard_page = st.Page("plot.py", title="Dashboard", icon="📊")
prediction_page = st.Page("app.py", title="Run Predictions", icon="📊")
pg = st.navigation([prediction_page,dashboard_page])
st.set_page_config(page_title="Data App", layout="wide")

pg.run()