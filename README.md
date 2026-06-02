# Demand Forecasting

A machine learning project for forecasting **Demand** and **Units Sold** using retail store data. The project uses a **Multi-Output Regression** approach with `sklearn.multioutput.RegressorChain` and includes data preprocessing, feature engineering, model selection, hyperparameter tuning, visualization, and deployment with FastAPI and Streamlit.

## Dataset

Dataset: Demand Forecasting Dataset
(https://www.kaggle.com/datasets/raminhuseyn/demand-forecasting-dataset)

## Project Workflow

### `test1.ipynb`

* Data preprocessing
* Feature engineering
* Save processed data as `preprocess.csv`

### `model_selection.ipynb`

Model comparison between:

* XGBoost Regressor
* LightGBM Regressor

**Result:** XGBoost achieved the best performance and was selected as the final model.

### `test2.ipynb`

Evaluated the impact of PCA on model performance.

**Result:** PCA was not used in the final pipeline because the R² score dropped from **77% to 52%**.

### `test3.ipynb`

* Hyperparameter tuning using Optuna
* Training the XGBoost model
* Saving the trained model, ColumnTransformer, and Imputer

Final Performance:

* RMSE: **18.04**
* R² Score: **0.834**

### `plot.ipynb`

* Plots actual vs predicted values for Demand and Units Sold
* Visualizes the last 6 months of predictions
* Saves plots in the `plot` folder
* Analyzes prediction errors across different features

### `plot.py`

Streamlit application for viewing prediction and error analysis plots.

### `api.py`

FastAPI backend that serves prediction requests.

### `app.py`

Streamlit frontend that:

* Predicts Demand and Units Sold
* Calculates estimated revenue
* Displays inventory levels
* Communicates with the FastAPI backend

### `forecasting.py`

Main Streamlit dashboard that combines:

* Prediction interface (`app.py`)
* Visualization dashboard (`plot.py`)

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* LightGBM
* Optuna
* FastAPI
* Streamlit
* Matplotlib

## Features

* Demand forecasting
* Units sold prediction
* Multi-output regression using `RegressorChain`
* Automated hyperparameter tuning with Optuna
* Revenue estimation
* Inventory monitoring
* Prediction error analysis
* Interactive Streamlit dashboard
* FastAPI deployment

## Results

The final XGBoost model achieved:

| Metric   | Score |
| -------- | ----- |
| RMSE     | 18.04 |
| R² Score | 0.834 |

The model provides accurate forecasts for both **Demand** and **Units Sold**, helping with inventory planning and sales analysis.
