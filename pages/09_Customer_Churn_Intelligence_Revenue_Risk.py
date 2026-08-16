import streamlit as st

st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Customer Churn Intelligence")

st.caption(
    "Customer churn, risk levels and revenue exposure based on the "
    "finalized Customer 360 analysis."
)

st.info(
    "CUSTOMER 360  →  CHURN PREDICTION  →  RISK SEGMENTATION  "
    "→  REVENUE RISK  →  RETENTION ACTION"
)

st.divider()

st.header("Churn Exposure")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", "96,096")

with col2:
    st.metric("Customers at Risk", "68,352")

with col3:
    st.metric("At-Risk Rate", "71.13%")

with col4:
    st.metric("Revenue at Risk", "₹11,261,919.01")

st.write(
    "Out of 96,096 customers, 68,352 have been identified within the "
    "at-risk group. This means that 71.13% of the customer base needs "
    "attention from a retention point of view."
)

st.write(
    "The purpose of this analysis is to help the business identify "
    "customers who may need attention before they are lost."
)

st.divider()

st.header("Revenue Risk")

rev1, rev2, rev3 = st.columns(3)

with rev1:
    st.metric(
        "Revenue at Risk",
        "₹11,261,919.01"
    )

with rev2:
    st.metric(
        "Customers at Risk",
        "68,352"
    )

with rev3:
    st.metric(
        "Average Spending",
        "₹164.76"
    )

st.warning(
    "A large customer group is currently exposed to churn risk. "
    "The revenue figure shows why customer retention is important "
    "from a business perspective."
)

st.divider()

st.header("Customer Risk Segmentation")

risk1, risk2, risk3 = st.columns(3)

with risk1:
    st.metric(
        "High Risk",
        "11,961"
    )

with risk2:
    st.metric(
        "Medium Risk",
        "5,776"
    )

with risk3:
    st.metric(
        "Low Risk",
        "1,483"
    )

st.write(
    "The risk groups help the business decide which customers should "
    "be contacted first. High Risk customers need the most immediate "
    "attention, followed by Medium Risk and Low Risk customers."
)

st.divider()

st.header("Customer Value and Churn")

value1, value2, value3 = st.columns(3)

with value1:
    st.subheader("High Value")

    st.metric(
        "Churn Rate",
        "70.45%"
    )

    st.write("Customers: 32,032")
    st.write("Revenue: ₹10,884,246.37")
    st.write("Average Spending: ₹339.79")

with value2:
    st.subheader("Medium Value")

    st.metric(
        "Churn Rate",
        "70.81%"
    )

    st.write("Customers: 32,029")
    st.write("Revenue: ₹3,523,030.40")
    st.write("Average Spending: ₹110.00")

with value3:
    st.subheader("Low Value")

    st.metric(
        "Churn Rate",
        "72.13%"
    )

    st.write("Customers: 32,034")
    st.write("Revenue: ₹1,601,595.35")
    st.write("Average Spending: ₹50.00")

st.info(
    "Churn is slightly higher among Low Value customers, while High Value "
    "customers still have a high churn rate of 70.45%. This shows why "
    "customer value and churn risk should be considered together."
)
st.divider()

st.header("Machine Learning Model Performance")

st.write(
    "Four classification models were evaluated during the completed "
    "machine learning analysis. Their performance is compared below."
)

model_data = {
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost"
    ],
    "Accuracy": [
        "66.26%",
        "65.35%",
        "66.45%",
        "77.10%"
    ],
    "Precision": [
        "82.73%",
        "82.95%",
        "81.80%",
        "77.46%"
    ],
    "Recall": [
        "66.43%",
        "64.56%",
        "67.95%",
        "95.62%"
    ],
    "F1 Score": [
        "73.69%",
        "72.61%",
        "74.23%",
        "85.59%"
    ],
    "ROC-AUC": [
        "71.96%",
        "72.05%",
        "71.35%",
        "78.15%"
    ]
}

st.dataframe(
    model_data,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("Final Model: XGBoost")

model1, model2, model3, model4, model5 = st.columns(5)

with model1:
    st.metric(
        "Accuracy",
        "77.10%"
    )

with model2:
    st.metric(
        "Precision",
        "77.46%"
    )

with model3:
    st.metric(
        "Recall",
        "95.62%"
    )

with model4:
    st.metric(
        "F1 Score",
        "85.59%"
    )

with model5:
    st.metric(
        "ROC-AUC",
        "78.15%"
    )

st.write(
    "XGBoost was selected as the final model because the main focus of "
    "this project is customer retention. In this situation, identifying "
    "as many genuinely at-risk customers as possible is important."
)

st.write(
    "With a recall of 95.62%, XGBoost detected a larger share of the "
    "customers who were actually at risk compared with the other models."
)

st.success(
    "Final model selected: XGBoost"
)

import plotly.express as px
import pandas as pd

st.divider()

st.header("Machine Learning Model Performance")

st.write(
    "Four models were tested during the completed machine learning analysis. "
    "The comparison below shows how each model performed."
)

model_df = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost"
    ],
    "Accuracy": [
        66.26,
        65.35,
        66.45,
        77.10
    ],
    "Precision": [
        82.73,
        82.95,
        81.80,
        77.46
    ],
    "Recall": [
        66.43,
        64.56,
        67.95,
        95.62
    ],
    "F1 Score": [
        73.69,
        72.61,
        74.23,
        85.59
    ],
    "ROC-AUC": [
        71.96,
        72.05,
        71.35,
        78.15
    ]
})

metric_choice = st.selectbox(
    "Select performance metric",
    [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ]
)

fig = px.bar(
    model_df,
    x="Model",
    y=metric_choice,
    text=metric_choice,
    title=f"{metric_choice} Comparison Across Models",
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    height=430,
    yaxis_title=f"{metric_choice} (%)",
    xaxis_title="Model",
    yaxis=dict(range=[0, 105]),
    margin=dict(l=20, r=20, t=70, b=20),
    font=dict(size=13)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("View complete model comparison"):

    display_df = model_df.copy()

    for column in [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ]:
        display_df[column] = (
            display_df[column].astype(str) + "%"
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.header("🏆 Final Model Selection")

st.success(
    "XGBoost was selected as the final model."
)

final_col1, final_col2, final_col3, final_col4, final_col5 = st.columns(5)

with final_col1:
    st.metric(
        "Accuracy",
        "77.10%"
    )

with final_col2:
    st.metric(
        "Precision",
        "77.46%"
    )

with final_col3:
    st.metric(
        "Recall",
        "95.62%"
    )

with final_col4:
    st.metric(
        "F1 Score",
        "85.59%"
    )

with final_col5:
    st.metric(
        "ROC-AUC",
        "78.15%"
    )

st.info(
    "The model was selected mainly because recall is important for this "
    "project. A high recall means fewer genuinely at-risk customers are "
    "missed, giving the business more opportunities to take action."
)

st.divider()

st.header("📈 What the Model Results Tell Us")

insight_a, insight_b, insight_c = st.columns(3)

with insight_a:
    st.subheader("Strong Recall")
    st.metric(
        "XGBoost Recall",
        "95.62%"
    )
    st.caption(
        "Most actual at-risk customers were identified."
    )

with insight_b:
    st.subheader("Best Overall F1")
    st.metric(
        "XGBoost F1",
        "85.59%"
    )
    st.caption(
        "Best balance between precision and recall among the tested models."
    )

with insight_c:
    st.subheader("Highest ROC-AUC")
    st.metric(
        "XGBoost ROC-AUC",
        "78.15%"
    )
    st.caption(
        "Strongest ranking performance among the evaluated models."
    )

st.divider()

st.header("Customer Churn Model Summary")

st.write(
    "The model comparison shows that XGBoost performed best overall for "
    "the project's retention-focused objective. The final Streamlit page "
    "uses the completed model results rather than retraining the models."
)

st.divider()

st.header("Churn Risk Distribution")

st.write(
    "The following view shows how customers are distributed across the "
    "finalized risk categories."
)

risk_df = pd.DataFrame({
    "Risk Segment": [
        "High Risk",
        "Medium Risk",
        "Low Risk"
    ],
    "Customers": [
        11961,
        5776,
        1483
    ]
})

risk_chart = px.bar(
    risk_df,
    x="Risk Segment",
    y="Customers",
    text="Customers",
    title="Customers by Risk Segment",
    labels={
        "Risk Segment": "Risk Segment",
        "Customers": "Number of Customers"
    }
)

risk_chart.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

risk_chart.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=70, b=20),
    yaxis=dict(
        title="Customers"
    ),
    xaxis=dict(
        title=""
    )
)

st.plotly_chart(
    risk_chart,
    use_container_width=True
)

st.divider()

st.subheader("Risk Segment Share")

risk_share = px.pie(
    risk_df,
    names="Risk Segment",
    values="Customers",
    hole=0.55,
    title="Risk Segment Distribution"
)

risk_share.update_traces(
    textposition="inside",
    textinfo="label+percent"
)

risk_share.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=70, b=20)
)

st.plotly_chart(
    risk_share,
    use_container_width=True
)

st.info(
    "High Risk customers form the most important group for immediate "
    "retention attention. Medium Risk customers can be monitored and "
    "targeted with preventive actions, while Low Risk customers can "
    "remain under regular customer engagement."
)

st.divider()

st.header("Churn Rate Across Customer Value Tiers")

tier_df = pd.DataFrame({
    "Customer Value Tier": [
        "High Value",
        "Medium Value",
        "Low Value"
    ],
    "Churn Rate": [
        70.45,
        70.81,
        72.13
    ]
})

tier_chart = px.bar(
    tier_df,
    x="Customer Value Tier",
    y="Churn Rate",
    text="Churn Rate",
    title="Churn Rate by Customer Value Tier",
    labels={
        "Customer Value Tier": "Customer Value",
        "Churn Rate": "Churn Rate (%)"
    }
)

tier_chart.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

tier_chart.update_layout(
    height=430,
    yaxis=dict(
        title="Churn Rate (%)",
        range=[0, 80]
    ),
    xaxis=dict(
        title=""
    ),
    margin=dict(l=20, r=20, t=70, b=20)
)

st.plotly_chart(
    tier_chart,
    use_container_width=True
)

st.info(
    "The churn rate remains high across all three customer value tiers. "
    "Low Value customers have the highest churn rate at 72.13%, while "
    "High Value customers have a slightly lower churn rate of 70.45%. "
    "High-value customers still deserve attention because of their "
    "higher average spending and revenue contribution."
)

st.divider()

from pathlib import Path
import pandas as pd
import streamlit as st

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "2 Notebook" / "outputs"

FEATURE_FILE = OUTPUT_DIR / "feature_importance.csv"
HIGH_CHURN_FILE = OUTPUT_DIR / "high_churn_drivers.csv"
RETENTION_FILE = OUTPUT_DIR / "retention_drivers.csv"


# Safe CSV loader
def load_csv(file_path):
    if not file_path.exists():
        st.warning(
            f"File not found: {file_path.name}"
        )
        return None

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        st.warning(
            f"Could not read {file_path.name}: {e}"
        )
        return None


# Load existing project outputs
feature_df = load_csv(FEATURE_FILE)
high_churn_df = load_csv(HIGH_CHURN_FILE)
retention_df = load_csv(RETENTION_FILE)


st.divider()

st.header("Churn Drivers")

st.write(
    "The completed analysis identified several factors that help "
    "explain customer churn. The results below are taken directly "
    "from the existing project output files."
)


# ------------------------------------------------------------
# Feature Importance
# ------------------------------------------------------------

if feature_df is not None and not feature_df.empty:

    st.subheader("Feature Importance")

    st.write(
        "These results show the importance of the features used during "
        "the completed churn modelling process."
    )

    st.dataframe(
        feature_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Feature importance results are not available."
    )


# ------------------------------------------------------------
# High Churn Drivers
# ------------------------------------------------------------

if high_churn_df is not None and not high_churn_df.empty:

    st.divider()

    st.subheader("High Churn Drivers")

    st.write(
        "The following results come from the finalized high-churn "
        "driver analysis."
    )

    st.dataframe(
        high_churn_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "High churn driver results are not available."
    )


# ------------------------------------------------------------
# Retention Drivers
# ------------------------------------------------------------

if retention_df is not None and not retention_df.empty:

    st.divider()

    st.subheader("Retention Drivers")

    st.write(
        "These results connect the churn analysis with factors that "
        "can be considered when planning customer retention."
    )

    st.dataframe(
        retention_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Retention driver results are not available."
    )


# ------------------------------------------------------------
# Business Interpretation
# ------------------------------------------------------------

st.divider()

st.header("What the Churn Drivers Tell Us")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Understanding Churn")

    st.write(
        "Churn analysis is not only about identifying customers who "
        "may leave. It is also important to understand the factors "
        "associated with that risk."
    )

    st.write(
        "The driver analysis provides additional context around "
        "customer behaviour and helps the business understand "
        "where attention may be required."
    )


with col2:

    st.subheader("Using the Insights")

    st.write(
        "The driver results can be considered together with customer "
        "risk and customer value when deciding which customers "
        "should receive attention first."
    )

    st.write(
        "The next stage connects these insights with the existing "
        "customer action plans, priorities and recommendations."
    )

    # ============================================================
# RETENTION ACTION & CUSTOMER RECOMMENDATIONS
# ============================================================

st.divider()

st.header("Retention Action Center")

st.write(
    "The churn analysis is connected with customer-level actions so "
    "that identified risks can be translated into practical retention steps."
)

ACTION_FILE = OUTPUT_DIR / "customer_action_plan.csv"
PRIORITY_FILE = OUTPUT_DIR / "priority_summary.csv"
RECOMMENDATION_FILE = OUTPUT_DIR / "recommendation_summary.csv"

action_df = load_csv(ACTION_FILE)
priority_df = load_csv(PRIORITY_FILE)
recommendation_df = load_csv(RECOMMENDATION_FILE)


# ------------------------------------------------------------
# Priority Summary
# ------------------------------------------------------------

if priority_df is not None and not priority_df.empty:

    st.subheader("Retention Priority")

    st.write(
        "The priority summary shows how customers are grouped according "
        "to the finalized retention planning results."
    )

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# Recommendation Summary
# ------------------------------------------------------------

if recommendation_df is not None and not recommendation_df.empty:

    st.divider()

    st.subheader("Recommended Retention Actions")

    st.write(
        "These recommendations were generated during the completed "
        "retention analysis and are displayed here for business use."
    )

    st.dataframe(
        recommendation_df,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# Customer Action Plan
# ------------------------------------------------------------

if action_df is not None and not action_df.empty:

    st.divider()

    st.subheader("Customer Action Plan")

    st.write(
        "The customer action plan connects individual customer risk "
        "with the corresponding retention information."
    )

    st.dataframe(
        action_df.head(20),
        use_container_width=True,
        hide_index=True
    )

    if len(action_df) > 20:

        st.caption(
            f"Showing 20 of {len(action_df):,} customer action records."
        )


# ------------------------------------------------------------
# Action Flow
# ------------------------------------------------------------

st.divider()

st.subheader("From Risk to Action")

action1, action2, action3, action4 = st.columns(4)

with action1:

    st.markdown("### 01")

    st.write("Identify")

    st.caption(
        "Find customers showing higher churn risk."
    )


with action2:

    st.markdown("### 02")

    st.write("Prioritize")

    st.caption(
        "Decide which customers need attention first."
    )


with action3:

    st.markdown("### 03")

    st.write("Recommend")

    st.caption(
        "Use the existing retention recommendations."
    )


with action4:

    st.markdown("### 04")

    st.write("Act")

    st.caption(
        "Turn the analysis into targeted customer action."
    )


# ------------------------------------------------------------
# Business Insight
# ------------------------------------------------------------

st.divider()

st.header("Retention Insight")

st.info(
    "The purpose of the retention layer is to move beyond simply "
    "identifying churn risk. Customer risk, priority and recommended "
    "actions can be used together to help the business decide where "
    "retention efforts should be focused."
)

# ============================================================
# CUSTOMER 360 FINAL DATASET
# ============================================================

st.divider()

st.header("Customer 360 Final Dataset")

st.write(
    "This is the finalized customer-level dataset created after the "
    "completed machine learning and business analysis workflow."
)

FINAL_FILE = OUTPUT_DIR / "customer_360_final.csv"

final_df = load_csv(FINAL_FILE)

if final_df is not None and not final_df.empty:

    # Dataset validation
    total_rows = len(final_df)
    total_columns = len(final_df.columns)
    missing_values = int(final_df.isna().sum().sum())
    duplicate_rows = int(final_df.duplicated().sum())

    val1, val2, val3, val4 = st.columns(4)

    with val1:
        st.metric(
            "Rows",
            f"{total_rows:,}"
        )

    with val2:
        st.metric(
            "Columns",
            total_columns
        )

    with val3:
        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )

    with val4:
        st.metric(
            "Duplicate Rows",
            f"{duplicate_rows:,}"
        )

    if missing_values == 0 and duplicate_rows == 0:

        st.success(
            "Final dataset validation passed. No missing values or "
            "duplicate rows were found."
        )

    else:

        st.warning(
            "The final dataset contains missing values or duplicate rows. "
            "Review the validation results before using the data."
        )

    st.divider()

    st.subheader("Dataset Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write(
            f"**Total Customers:** {total_rows:,}"
        )

        st.write(
            f"**Total Features:** {total_columns}"
        )

    with info_col2:

        st.write(
            "**Source:** customer_360_final.csv"
        )

        st.write(
            "**Status:** Finalized ML and business output"
        )

    # --------------------------------------------------------
    # Important columns
    # --------------------------------------------------------

    st.divider()

    st.subheader("Customer-Level Churn Information")

    preferred_columns = [
        "customer_unique_id",
        "customer_city",
        "customer_state",
        "customer_value_tier",
        "churn_flag",
        "predicted_churn",
        "churn_probability",
        "risk_segment",
        "recommendation",
        "reason",
        "priority",
        "owner",
        "timeline",
        "estimated_cost",
        "expected_outcome"
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in final_df.columns
    ]

    if available_columns:

        preview_df = final_df[available_columns].copy()

        st.dataframe(
            preview_df.head(20),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing 20 of {total_rows:,} customer records."
        )

    else:

        st.info(
            "The expected customer-level ML columns were not found "
            "in the final dataset."
        )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    st.divider()

    st.subheader("Download Final Dataset")

    csv_data = final_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Customer 360 Final CSV",
        data=csv_data,
        file_name="customer_360_final.csv",
        mime="text/csv"
    )

else:

    st.error(
        "The finalized customer_360_final.csv file could not be loaded."
    )

    st.divider()

st.header("Customer Churn Explorer")

st.write(
    "Use the filters below to explore individual customers from the "
    "finalized Customer 360 dataset."
)

if final_df is not None and not final_df.empty:

    explorer_df = final_df.copy()

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        if "risk_segment" in explorer_df.columns:

            risk_options = sorted(
                explorer_df["risk_segment"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_risk = st.selectbox(
                "Risk Segment",
                ["All"] + risk_options
            )

            if selected_risk != "All":

                explorer_df = explorer_df[
                    explorer_df["risk_segment"].astype(str)
                    == selected_risk
                ]

    with filter_col2:

        if "customer_value_tier" in explorer_df.columns:

            value_options = sorted(
                explorer_df["customer_value_tier"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_value = st.selectbox(
                "Customer Value",
                ["All"] + value_options
            )

            if selected_value != "All":

                explorer_df = explorer_df[
                    explorer_df["customer_value_tier"].astype(str)
                    == selected_value
                ]

    with filter_col3:

        if "predicted_churn" in explorer_df.columns:

            churn_options = sorted(
                explorer_df["predicted_churn"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_churn = st.selectbox(
                "Predicted Churn",
                ["All"] + churn_options
            )

            if selected_churn != "All":

                explorer_df = explorer_df[
                    explorer_df["predicted_churn"].astype(str)
                    == selected_churn
                ]

    # --------------------------------------------------------
    # Customer ID Search
    # --------------------------------------------------------

    if "customer_unique_id" in explorer_df.columns:

        customer_search = st.text_input(
            "Search Customer ID",
            placeholder="Enter customer ID..."
        )

        if customer_search:

            explorer_df = explorer_df[
                explorer_df["customer_unique_id"]
                .astype(str)
                .str.contains(
                    customer_search,
                    case=False,
                    na=False
                )
            ]

    st.divider()

    st.subheader("Filtered Customers")

    st.metric(
        "Customers Matching Filters",
        f"{len(explorer_df):,}"
    )

    # --------------------------------------------------------
    # Display relevant columns
    # --------------------------------------------------------

    explorer_columns = [
        "customer_unique_id",
        "customer_city",
        "customer_state",
        "customer_value_tier",
        "churn_flag",
        "predicted_churn",
        "churn_probability",
        "risk_segment",
        "recommendation",
        "reason",
        "priority"
    ]

    explorer_columns = [
        column
        for column in explorer_columns
        if column in explorer_df.columns
    ]

    if explorer_columns:

        display_explorer = explorer_df[
            explorer_columns
        ].head(100)

        st.dataframe(
            display_explorer,
            use_container_width=True,
            hide_index=True
        )

        if len(explorer_df) > 100:

            st.caption(
                f"Showing first 100 records out of "
                f"{len(explorer_df):,} matching customers."
            )

    else:

        st.info(
            "Customer-level churn columns are not available "
            "in the final dataset."
        )

    # --------------------------------------------------------
    # Selected Customer Details
    # --------------------------------------------------------

    if (
        "customer_unique_id" in explorer_df.columns
        and not explorer_df.empty
    ):

        st.divider()

        st.subheader("Customer Details")

        customer_ids = (
            explorer_df["customer_unique_id"]
            .dropna()
            .astype(str)
            .head(200)
            .tolist()
        )

        selected_customer = st.selectbox(
            "Select a customer",
            customer_ids
        )

        selected_row = explorer_df[
            explorer_df["customer_unique_id"]
            .astype(str)
            == selected_customer
        ]

        if not selected_row.empty:

            customer = selected_row.iloc[0]

            detail1, detail2, detail3, detail4 = st.columns(4)

            with detail1:

                st.write("**Customer ID**")

                st.write(
                    str(customer.get(
                        "customer_unique_id",
                        "N/A"
                    ))
                )

                st.write("**Location**")

                city = customer.get(
                    "customer_city",
                    "N/A"
                )

                state = customer.get(
                    "customer_state",
                    "N/A"
                )

                st.write(
                    f"{city}, {state}"
                )

            with detail2:

                st.write("**Customer Value**")

                st.write(
                    str(customer.get(
                        "customer_value_tier",
                        "N/A"
                    ))
                )

                st.write("**Risk Segment**")

                st.write(
                    str(customer.get(
                        "risk_segment",
                        "N/A"
                    ))
                )

            with detail3:

                st.write("**Predicted Churn**")

                st.write(
                    str(customer.get(
                        "predicted_churn",
                        "N/A"
                    ))
                )

                st.write("**Churn Probability**")

                probability = customer.get(
                    "churn_probability",
                    None
                )

                if probability is not None:

                    try:

                        probability = float(
                            probability
                        )

                        if probability <= 1:

                            st.write(
                                f"{probability:.2%}"
                            )

                        else:

                            st.write(
                                f"{probability:.2f}%"
                            )

                    except:

                        st.write(
                            str(probability)
                        )

                else:

                    st.write("N/A")

            with detail4:

                st.write("**Priority**")

                st.write(
                    str(customer.get(
                        "priority",
                        "N/A"
                    ))
                )

                st.write("**Recommendation**")

                st.write(
                    str(customer.get(
                        "recommendation",
                        "N/A"
                    ))
                )

            if "reason" in customer.index:

                st.divider()

                st.write("**Reason / Churn Context**")

                st.write(
                    str(customer["reason"])
                )

else:

    st.info(
        "Customer 360 Final dataset is required for the "
        "customer explorer."
    )

    st.divider()

st.header("Key Business Insights")

insight1, insight2 = st.columns(2)

with insight1:

    st.subheader("1. Churn Exposure Is High")

    st.write(
        "The analysis places 68,352 customers in the at-risk group, "
        "which represents 71.13% of the total customer base."
    )

    st.write(
        "With such a large share of customers exposed to churn, "
        "retention should be treated as an ongoing business activity "
        "rather than a one-time intervention."
    )


with insight2:

    st.subheader("2. Churn Has a Direct Revenue Impact")

    st.write(
        "Revenue associated with the at-risk customer group is "
        "₹11,261,919.01."
    )

    st.write(
        "This gives the business a clear financial reason to focus "
        "on retention. Reducing customer loss can help protect "
        "existing revenue instead of relying only on new customer acquisition."
    )


insight3, insight4 = st.columns(2)

with insight3:

    st.subheader("3. High-Value Customers Need Attention")

    st.write(
        "High-value customers generate an average spending of ₹339.79 "
        "and have a churn rate of 70.45%."
    )

    st.write(
        "Although their churn rate is slightly lower than the other "
        "value groups, their higher spending makes them important "
        "customers to monitor."
    )


with insight4:

    st.subheader("4. Risk Should Be Viewed With Customer Value")

    st.write(
        "Churn rates are 70.45% for High Value, 70.81% for Medium Value "
        "and 72.13% for Low Value customers."
    )

    st.write(
        "A customer with high churn risk does not necessarily have the "
        "same business importance as another customer. Retention priority "
        "should therefore consider both risk and customer value."
    )


st.divider()

st.header("Model-Based Business Insight")

st.subheader("Why Recall Matters Here")

st.write(
    "The final XGBoost model achieved a recall of 95.62%. In a churn "
    "management scenario, recall is particularly important because "
    "missing a customer who is actually at risk means losing an "
    "opportunity to intervene."
)

st.write(
    "XGBoost was therefore selected as the final model based on the "
    "completed model evaluation and the retention objective of the project."
)


st.divider()

st.header("Retention Priorities")

priority1, priority2, priority3 = st.columns(3)

with priority1:

    st.subheader("High Risk")

    st.write(
        "Focus first on customers classified as High Risk. "
        "These customers represent the most immediate retention concern."
    )


with priority2:

    st.subheader("High Value + Risk")

    st.write(
        "Give additional attention to high-value customers who are "
        "also exposed to churn risk because their potential revenue "
        "impact is comparatively higher."
    )


with priority3:

    st.subheader("Preventive Retention")

    st.write(
        "Medium-risk customers can be approached before their risk "
        "becomes more serious, helping the business move from reactive "
        "retention to preventive customer management."
    )


st.divider()

st.header("Business Conclusion")

st.write(
    "The analysis shows that customer churn is not only a customer "
    "behaviour problem but also a revenue protection issue. The "
    "combination of churn risk, customer value and revenue exposure "
    "provides a clearer basis for deciding where retention efforts "
    "should be focused."
)

st.write(
    "The next stage of the project uses these findings to move from "
    "identifying risk to deciding what retention action should be taken "
    "for individual customers."
)

st.divider()

st.header("Data & Analysis Lineage")

st.write(
    "The results presented on this page come from the completed "
    "CustomerPulse AI analysis pipeline."
)

line1, line2, line3, line4, line5 = st.columns(5)

with line1:

    st.markdown("### Customer 360")

    st.caption(
        "Cleaned customer-level dataset containing "
        "customer, purchase and behavioural information."
    )


with line2:

    st.markdown("### Model")

    st.caption(
        "Completed churn modelling workflow with "
        "four evaluated classification models."
    )


with line3:

    st.markdown("### Risk")

    st.caption(
        "Final customer-level risk results used to "
        "identify High, Medium and Low Risk customers."
    )


with line4:

    st.markdown("### Revenue")

    st.caption(
        "Customer value and churn exposure used to "
        "estimate the financial impact of customer loss."
    )


with line5:

    st.markdown("### Retention")

    st.caption(
        "Existing recommendations, priorities and "
        "customer action plans used for retention planning."
    )


st.divider()

st.header("Source Files")

source_files = {
    "Clean Customer 360": "customer_360_clean.csv",
    "Final Customer 360": "customer_360_final.csv",
    "Customer Risk Analysis": "customer_risk_analysis.csv",
    "Feature Importance": "feature_importance.csv",
    "High Churn Drivers": "high_churn_drivers.csv",
    "Retention Drivers": "retention_drivers.csv",
    "Customer Action Plan": "customer_action_plan.csv",
    "Priority Summary": "priority_summary.csv",
    "Recommendation Summary": "recommendation_summary.csv",
    "Model Comparison": "roc_auc_comparison.csv"
}

source_df = pd.DataFrame(
    list(source_files.items()),
    columns=["Analysis Component", "Source File"]
)

st.dataframe(
    source_df,
    use_container_width=True,
    hide_index=True
)


st.divider()

st.caption(
    "The Streamlit page presents the finalized results produced during "
    "the completed analysis workflow. No new churn rule or model "
    "training is performed on this page."
)