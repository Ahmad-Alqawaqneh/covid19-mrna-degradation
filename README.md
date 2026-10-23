# COVID-19 mRNA Vaccine Degradation Prediction

Multi-output regression project from the **Tahaluf Al Emarat Machine Learning program** Kaggle competition
([competition page](https://www.kaggle.com/competitions/covid-19-mrnavaccinedegradation/overview)).
The goal is to predict the degradation rate of mRNA sequences at each base (reactivity, `deg_Mg_pH10`, `deg_pH10`, `deg_Mg_50C`, `deg_50C`) to help design more stable mRNA vaccines.

## Approach
- **Data understanding** – RNA sequence, secondary structure and predicted loop type for each base; signal-to-noise filtering.
- **Feature engineering** – per-base features from sequence, structure and loop type, neighbouring bases, label encoding.
- **Missing targets** – each target and its error column filled with a dedicated strategy.
- **Model comparison** – benchmarked **17 regressors** with the competition metric **MCRMSE** (mean column-wise RMSE), then tuned the best one.
- **Error analysis** – residual analysis and feature importance (`xgboost.plot_importance`).

## Results (MCRMSE, lower is better)

| Model | MCRMSE |
|---|---|
| **XGBoost (tuned)** | **0.367** |
| Random Forest | 0.453 |
| Gradient Boosting | 0.488 |
| LightGBM | 0.505 |
| CatBoost | 0.513 |
| HistGradientBoosting | 0.530 |
| Ridge / Bayesian Ridge | 0.612 |
| Lasso | 0.747 |

Best XGBoost parameters: `max_depth=6, learning_rate=0.1, n_estimators=1500, colsample_bytree=0.9, reg_alpha=5, reg_lambda=6, min_child_weight=2`.

## Notebooks
- `notebooks/mrna_degradation_modeling.ipynb` – preprocessing, feature engineering and 17-model comparison
- `notebooks/error_analysis.ipynb` – error analysis of the final XGBoost model
- `notebooks/eda_openvaccine.ipynb` – exploratory study of the data, adapted from [a public Kaggle notebook by Andrew Lukyanenko](https://www.kaggle.com/artgor/openvaccine-eda-feature-engineering-and-modelling)
- `dashboard/streamlit_dashboard.py` – interactive Streamlit + Plotly dashboard to explore degradation targets by sequence (`streamlit run dashboard/streamlit_dashboard.py`)
- `presentation/mrna_degradation_presentation.pptx` – team presentation

**Tech:** Python · Streamlit · Plotly · pandas · scikit-learn · XGBoost · LightGBM · CatBoost · Seaborn

> Team project during the Tahaluf Al Emarat ML internship. Data is not included; download it from the competition page.
