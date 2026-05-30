import requests
import pandas as pd
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Demand & Sales Forecaster",
    layout="wide"
)

st.title("📊 Store Demand & Units Sold Prediction Dashboard")

FASTAPI_URL = "http://localhost:8000/predict"

PRODUCT_CATEGORY_MAP = {
    "P0001": ["Electronics", "Groceries", "Toys"],
    "P0002": ["Clothing", "Toys", "Groceries", "Electronics"],
    "P0003": ["Clothing", "Groceries", "Electronics", "Furniture", "Toys"],
    "P0004": ["Electronics", "Groceries"],
    "P0005": ["Groceries", "Electronics", "Toys", "Clothing"],
    "P0006": ["Toys", "Clothing", "Groceries"],
    "P0007": ["Groceries", "Toys"],
    "P0008": ["Electronics", "Groceries", "Clothing", "Furniture"],
    "P0009": ["Clothing", "Groceries"],
    "P0010": ["Furniture", "Groceries"],
    "P0011": ["Furniture", "Groceries", "Electronics", "Clothing"],
    "P0012": ["Groceries", "Electronics", "Furniture"],
    "P0013": ["Toys", "Groceries"],
    "P0014": ["Groceries", "Electronics", "Furniture"],
    "P0015": ["Toys", "Clothing", "Groceries", "Furniture"],
    "P0016": ["Groceries", "Clothing", "Electronics", "Furniture", "Toys"],
    "P0017": ["Toys", "Furniture", "Clothing"],
    "P0018": ["Groceries", "Clothing", "Furniture"],
    "P0019": ["Furniture", "Clothing", "Groceries"],
    "P0020": ["Furniture", "Clothing", "Toys"],
}

st.sidebar.header("🛠️ Input Features")

store_id = st.sidebar.selectbox(
    "Store ID",
    ["S001", "S002", "S003", "S004", "S005"]
)

product_id = st.sidebar.selectbox(
    "Product ID",
    list(PRODUCT_CATEGORY_MAP.keys())
)

allowed_categories = PRODUCT_CATEGORY_MAP[product_id]

category = st.sidebar.selectbox(
    "Category",
    allowed_categories
)

# Numerical Features
inventory_level = st.sidebar.number_input(
    "Inventory Level",
    min_value=0,
    max_value=10000,
    value=100
)

units_ordered = st.sidebar.number_input(
    "Units Ordered",
    min_value=0,
    value=50
)

price = st.sidebar.number_input(
    "Price",
    min_value=0.0,
    value=19.99,
    step=0.01
)

discount = st.sidebar.slider(
    "Discount (%)",
    min_value=0,
    max_value=100,
    value=0
)

weather_condition = st.sidebar.selectbox(
    "Weather Condition",
    ["Cloudy", "Sunny", "Rainy", "Snowy"]
)

promotion = st.sidebar.selectbox(
    "Promotion Active?",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

competitor_pricing = st.sidebar.number_input(
    "Competitor Pricing",
    min_value=0.0,
    value=21.50,
    step=0.01
)

seasonality = st.sidebar.selectbox(
    "Seasonality",
    ["Winter", "Spring", "Summer", "Autumn"]
)

epidemic = st.sidebar.selectbox(
    "Epidemic Status?",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

date_input = st.sidebar.date_input(
    "Target Date",
    date.today()
)

with st.sidebar.expander("⏳ Demand Lag Features (Last 7 Days)"):

    demand_lag1 = st.number_input("Demand Lag 1", value=34,step=1)
    demand_lag2 = st.number_input("Demand Lag 2", value=35,step=1)
    demand_lag3 = st.number_input("Demand Lag 3", value=36,step=1)
    demand_lag4 = st.number_input("Demand Lag 4", value=34,step=1)
    demand_lag5 = st.number_input("Demand Lag 5", value=37,step=1)
    demand_lag6 = st.number_input("Demand Lag 6", value=34,step=1)
    demand_lag7 = st.number_input("Demand Lag 7", value=35,step=1)

with st.sidebar.expander("⏳ Units Sold Lag Features (Last 7 Days)"):

    units_sold_lag1 = st.number_input("Units Sold Lag 1", value=55,step=1)
    units_sold_lag2 = st.number_input("Units Sold Lag 2", value=534,step=1)
    units_sold_lag3 = st.number_input("Units Sold Lag 3", value=354,step=1)
    units_sold_lag4 = st.number_input("Units Sold Lag 4", value=344,step=1)
    units_sold_lag5 = st.number_input("Units Sold Lag 5", value=344,step=1)
    units_sold_lag6 = st.number_input("Units Sold Lag 6", value=343,step=1)
    units_sold_lag7 = st.number_input("Units Sold Lag 7", value=334,step=1)

payload = {
    "Store ID": store_id,
    "Product ID": product_id,
    "Category": category,
    "Inventory Level": inventory_level,
    "Units Ordered": units_ordered,
    "Price": price,
    "Discount": discount,
    "Weather Condition": weather_condition,
    "Promotion": promotion,
    "Competitor Pricing": competitor_pricing,
    "Seasonality": seasonality,
    "Epidemic": epidemic,
    "Date": date_input.strftime("%Y-%m-%d"),

    "demand_lag1": demand_lag1,
    "demand_lag2": demand_lag2,
    "demand_lag3": demand_lag3,
    "demand_lag4": demand_lag4,
    "demand_lag5": demand_lag5,
    "demand_lag6": demand_lag6,
    "demand_lag7": demand_lag7,

    "Units Sold_lag1": units_sold_lag1,
    "Units Sold_lag2": units_sold_lag2,
    "Units Sold_lag3": units_sold_lag3,
    "Units Sold_lag4": units_sold_lag4,
    "Units Sold_lag5": units_sold_lag5,
    "Units Sold_lag6": units_sold_lag6,
    "Units Sold_lag7": units_sold_lag7,
}

st.subheader("📋 API Input Data")

df_display = pd.DataFrame([payload])

st.dataframe(
    df_display,
    use_container_width=True
)

if st.button(
    "🚀 Fetch Predictions from FastAPI",
    type="primary"
):

    with st.spinner("Communicating with ML Server Backend..."):

        try:
            response = requests.post(
                FASTAPI_URL,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            result = response.json()

            st.subheader("🔍 Raw API Response")
            st.json(result)

            # Extract predictions
            pred_units_sold = result.get("prediction Units Sold")
            pred_demand = result.get("Prediction DEMAND")

            if pred_units_sold is not None and pred_demand is not None:

                pred_units_sold = float(pred_units_sold)
                pred_demand = float(pred_demand)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "📦 Predicted Units Sold",
                        f"{pred_units_sold:.2f}"
                    )

                with col2:
                    st.metric(
                        "📈 Predicted Demand",
                        f"{pred_demand:.2f}"
                    )

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    shortage = pred_demand - inventory_level

                    if shortage > 0:
                        st.error(
                            f"⚠️ Need {shortage:.0f} more units in inventory"
                        )
                    else:
                        st.success(
                            f"✅ Sufficient inventory ({abs(shortage):.0f} extra units)"
                        )

                with col2:
                    discount_amount = (discount / 100) * price
                    effective_price = price - discount_amount
                    expected_revenue = effective_price * pred_units_sold

                    st.metric(
                        "💰 Expected Revenue  With Discount ",
                        f"${expected_revenue:,.2f}"
                    )

                with col3:
                    remaining_inventory = inventory_level - pred_units_sold

                    st.metric(
                        "📦 Remaining Inventory after Predictions",
                        f"{remaining_inventory:.0f}"
                    )

                summary_df = pd.DataFrame({
                    "Metric": [
                        "Inventory",
                        "Predicted Demand",
                        "Predicted Units Sold",
                        "Remaining Inventory",
                        "Expected Revenue"
                    ],
                    "Value": [
                        inventory_level,
                        round(pred_demand, 2),
                        round(pred_units_sold, 2),
                        round(remaining_inventory, 2),
                        round(expected_revenue, 2)
                    ]
                })

                st.subheader("📊 Prediction Summary")
                st.dataframe(
                    summary_df,
                    use_container_width=True
                )

            else:
                st.warning(
                    "Prediction keys not found in API response. "
                    "Check the JSON structure shown above."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Cannot connect to FastAPI.\n\n"
                "Make sure your FastAPI server is running:\n"
                "uvicorn main:app --reload"
            )

        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out after 30 seconds.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request Error: {e}")

        except ValueError as e:
            st.error(f"❌ Invalid prediction values returned by API: {e}")

        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")