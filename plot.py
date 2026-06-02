import streamlit as st

st.set_page_config(
    page_title="Sales & Demand Forecast Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales & Demand Forecast Dashboard")
st.sidebar.markdown(
    """
    Analyze model performance for **Demand Forecasting** and **Units Sold Prediction**.
    Review actual vs predicted values of last 6 months > '2023-06-01', error distributions, and model evaluation metrics.
    """
)

# METRICS
st.subheader("🎯 Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="RMSE",
        value="19.28"
    )

with col2:
    st.metric(
        label="R² Score",
        value="0.812"
    )

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Demand Forecast",
        "📦 Units Sold Forecast",
        "⚠️ Error Analysis"
    ]
)

with tab1:

    st.subheader("Demand Forecast Results")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "plot/Actual Demand.png",
            caption="Actual Demand",
            use_container_width=True
        )

    with col2:
        st.image(
            "plot/Predicted Demand.png",
            caption="Predicted Demand",
            use_container_width=True
        )

    st.image(
        "plot/Actual vs Predicted Demand.png",
        caption="Actual vs Predicted Demand",
        use_container_width=True
    )

with tab2:

    st.subheader("Units Sold Forecast Results")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "plot/Actual Units Sold.png",
            caption="Actual Units Sold",
            use_container_width=True
        )

    with col2:
        st.image(
            "plot/Predicted Units Sold.png",
            caption="Predicted Units Sold",
            use_container_width=True
        )

    st.image(
        "plot/Actual vs Predicted Units Sold.png",
        caption="Actual vs Predicted Units Sold",
        use_container_width=True
    )

with tab3:

    st.subheader("Error Analysis by Category")

    cols = st.columns(2)

    images = [
        "plot/1.png",
        "plot/2.png",
        "plot/3.png",
        "plot/4.png",
        "plot/5.png",
        "plot/6.png",
        "plot/7.png",
        "plot/8.png",
        "plot/9.png",
        "plot/10.png",
    ]

    for idx, img in enumerate(images):
        with cols[idx % 2]:
            st.image(
                img,
                caption=f"Category Error Analysis {idx+1}",
                use_container_width=True
            )

with st.expander("📋 Model Summary"):

    st.markdown("""
    ### Model Metrics

    - **RMSE:** 19.28
    - **R² Score:** 0.812

    ### Interpretation

    - The XGB model explains approximately **81.2%** of the variance.
    - Prediction accuracy is strong for a retail demand forecasting problem.
    - Error analysis helps identify categories where forecasting can be improved.
    """)