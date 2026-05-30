import datetime
from datetime import date
from typing import Literal
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
import uvicorn

ct = joblib.load("ColumnTransformer.pkl")
imputer = joblib.load("imputer.pkl")
model = joblib.load("xgb_model.pkl")

app = FastAPI()


class PredictionInput(BaseModel):
    store_id: Literal["S001", "S002", "S003", "S004", "S005"] = Field(
        alias="Store ID"
    )
    product_id: Literal[
        "P0001", "P0002", "P0003", "P0004", "P0005",
        "P0006", "P0007", "P0008", "P0009", "P0010",
        "P0011", "P0012", "P0013", "P0014", "P0015",
        "P0016", "P0017", "P0018", "P0019", "P0020",
    ] = Field(alias="Product ID")
    category: Literal[
        "Groceries", "Furniture", "Clothing", "Toys", "Electronics"
    ] = Field(alias="Category")

    inventory_level: int = Field(
        alias="Inventory Level", ge=0, le=1000, description="Inventory Level"
    )
    units_ordered: int = Field(alias="Units Ordered")
    price: float = Field(alias="Price", ge=0, description="Price of product")
    discount: int = Field(alias="Discount", ge=0, le=100)

    weather_condition: Literal["Cloudy", "Sunny", "Rainy", "Snowy"] = Field(
        alias="Weather Condition"
    )
    promotion: Literal[0, 1] = Field(
        alias="Promotion"
    )
    competitor_pricing: float = Field(
        alias="Competitor Pricing",
        ge=0,
        description="Price of Competitor product",
    )
    seasonality: Literal["Winter", "Spring", "Summer", "Autumn"] = Field(
        alias="Seasonality"
    )
    epidemic: int = Field(alias="Epidemic", ge=0, le=1, description="Epidemic status")
    date_input: date = Field(alias="Date")


    demand_lag1: float | None = Field(default=None, alias="demand_lag1")
    demand_lag2: float | None = Field(default=None, alias="demand_lag2")
    demand_lag3: float | None = Field(default=None, alias="demand_lag3")
    demand_lag4: float | None = Field(default=None, alias="demand_lag4")
    demand_lag5: float | None = Field(default=None, alias="demand_lag5")
    demand_lag6: float | None = Field(default=None, alias="demand_lag6")
    demand_lag7: float | None = Field(default=None, alias="demand_lag7")

    units_sold_lag1: float | None = Field(default=None, alias="Units Sold_lag1")
    units_sold_lag2: float | None = Field(default=None, alias="Units Sold_lag2")
    units_sold_lag3: float | None = Field(default=None, alias="Units Sold_lag3")
    units_sold_lag4: float | None = Field(default=None, alias="Units Sold_lag4")
    units_sold_lag5: float | None = Field(default=None, alias="Units Sold_lag5")
    units_sold_lag6: float | None = Field(default=None, alias="Units Sold_lag6")
    units_sold_lag7: float | None = Field(default=None, alias="Units Sold_lag7")

    model_config = {
        "populate_by_name": True,
    }

    @computed_field
    @property
    def Price_Premium_Index(self) -> float:
        if self.competitor_pricing == 0:
            return 0.0
        return self.price / self.competitor_pricing

    @computed_field
    @property
    def Discount_Depth(self) -> float:
        if self.price == 0:
            return 0.0
        return self.discount / self.price

    @computed_field
    @property
    def Day_of_Week(self) -> int:
        return self.date_input.weekday()

    @computed_field
    @property
    def Is_Weekend(self) -> int:
        return 1 if self.date_input.weekday() in (5, 6) else 0

    @computed_field
    @property
    def Month(self) -> int:
        return self.date_input.month

    @computed_field
    @property
    def Day_of_Month(self) -> int:
        return self.date_input.day


@app.post("/predict")
def predict(data: PredictionInput):
    input_dict = data.model_dump(by_alias=True, mode="json")

    df_features = pd.DataFrame([input_dict])

    feature_order = [
        "Date", "Store ID", "Product ID", "Category", "Inventory Level",
         "Units Ordered", "Price", "Discount", "Weather Condition",
        "Promotion", "Competitor Pricing", "Seasonality", "Epidemic",
        "Price_Premium_Index", "Discount_Depth", "Day_of_Week", "Is_Weekend",
        "Month", "Day_of_Month",
        "demand_lag1", "demand_lag2", "demand_lag3", "demand_lag4", "demand_lag5", "demand_lag6", "demand_lag7",
        "Units Sold_lag1", "Units Sold_lag2", "Units Sold_lag3", "Units Sold_lag4", "Units Sold_lag5", "Units Sold_lag6", "Units Sold_lag7"
    ]

    df_features = df_features[feature_order]

    transformed_data = ct.transform(df_features)
    imputed_data = imputer.transform(transformed_data)
    prediction = model.predict(imputed_data)

    return {"prediction Units Sold": float(prediction[0, 0]),"Prediction DEMAND": float(prediction[0, 1])
}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)