# ============================================================
# Page 6 - Customer Segmentation / RFM Analysis
# CustomerPulse AI Project
# ============================================================

import os

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation | CustomerPulse AI",
    layout="wide"
)


# ============================================================
# DATA PATH
# ============================================================

DATA_PATHS = [
    Path(__file__).resolve().parents[1] / "1 data" / "02_processed data" / "customer_360_clean.csv",
    Path(__file__).resolve().parents[1] / "1 data" / "02_processed data" / "customer_360.csv",
    Path(__file__).resolve().parents[1] / "1 data" / "03_analysis" / "customer_360_clean.csv",
    Path(__file__).resolve().parents[1] / "1 data" / "03_analysis" / "customer_360_final.csv",
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_customer_data():

    for path in DATA_PATHS:

        if os.path.exists(path):
            df = pd.read_csv(path)
            return df, path

    return None, None


customer_360, loaded_path = load_customer_data()


# ============================================================
# CHECK DATA
# ============================================================

if customer_360 is None:

    st.error("Customer 360 dataset was not found.")

    st.write("The following project paths were checked:")

    for path in DATA_PATHS:
        st.write(path)

    st.warning(
        "No sample or fabricated data has been created."
    )

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "customer_unique_id",
    "recency_days",
    "total_orders",
    "total_spent"
]

missing_columns = [
    column
    for column in required_columns
    if column not in customer_360.columns
]


if missing_columns:

    st.error("Required RFM columns are missing.")

    st.write(
        "Missing columns:",
        missing_columns
    )

    st.write(
        "Available columns:",
        list(customer_360.columns)
    )

    st.stop()


# ============================================================
# CREATE RFM DATASET
# ============================================================

rfm = customer_360[
    [
        "customer_unique_id",
        "recency_days",
        "total_orders",
        "total_spent"
    ]
].copy()


rfm.rename(
    columns={
        "customer_unique_id": "customer_id",
        "recency_days": "recency",
        "total_orders": "frequency",
        "total_spent": "monetary"
    },
    inplace=True
)


# Convert numeric columns
rfm["recency"] = pd.to_numeric(
    rfm["recency"],
    errors="coerce"
)

rfm["frequency"] = pd.to_numeric(
    rfm["frequency"],
    errors="coerce"
)

rfm["monetary"] = pd.to_numeric(
    rfm["monetary"],
    errors="coerce"
)


# Remove rows where RFM variables are unavailable
rfm.dropna(
    subset=[
        "customer_id",
        "recency",
        "frequency",
        "monetary"
    ],
    inplace=True
)


# ============================================================
# RFM SCORING
# ============================================================

# ------------------------------------------------------------
# Recency Score
# Lower recency is better.
# Customers are divided into five groups.
# ------------------------------------------------------------

rfm["R_score"] = pd.qcut(
    rfm["recency"].rank(method="first"),
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)


# ------------------------------------------------------------
# Frequency Score
# Business-rule based scoring used in the analysis.
# ------------------------------------------------------------

def assign_frequency_score(value):

    if value <= 1:
        return 1

    if value == 2:
        return 2

    if value == 3:
        return 3

    if value <= 5:
        return 4

    return 5


rfm["F_score"] = (
    rfm["frequency"]
    .apply(assign_frequency_score)
    .astype(int)
)


# ------------------------------------------------------------
# Monetary Score
# Higher monetary value is better.
# ------------------------------------------------------------

rfm["M_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


# ============================================================
# RFM TOTAL SCORE
# ============================================================

rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)


rfm["RFM_total_score"] = (
    rfm["R_score"]
    + rfm["F_score"]
    + rfm["M_score"]
)


# ============================================================
# RECENCY GROUP
# ============================================================

def assign_recency_group(days):

    if days <= 90:
        return "Active Customers"

    if days <= 180:
        return "Recent Customers"

    if days <= 365:
        return "Inactive Customers"

    return "Highly Inactive Customers"


rfm["recency_group"] = (
    rfm["recency"]
    .apply(assign_recency_group)
)


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

def assign_customer_segment(row):

    r_score = row["R_score"]
    f_score = row["F_score"]
    m_score = row["M_score"]
    total_score = row["RFM_total_score"]

    if (
        r_score >= 4
        and f_score >= 3
        and m_score >= 4
    ):
        return "Premium Customers"

    if (
        r_score >= 4
        and m_score >= 4
    ):
        return "High Value Customers"

    if total_score >= 8:
        return "Active Customers"

    if total_score >= 6:
        return "Promising Customers"

    if (
        r_score >= 3
        and m_score <= 2
    ):
        return "Price Sensitive Customers"

    return "Lost Customers"


rfm["customer_segment"] = rfm.apply(
    assign_customer_segment,
    axis=1
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("Customer Segmentation & RFM Analysis")

st.write(
    "Customer segmentation based on Recency, Frequency and Monetary behaviour."
)


# ============================================================
# SECTION 1 - OVERVIEW
# ============================================================

st.header("1. Segmentation Overview")

st.write(
    """
    Customer 360 data was used to evaluate customer purchasing behaviour.
    RFM analysis was applied using three measures: Recency, Frequency and
    Monetary value. These measures were then used to create customer
    segments based on observed purchasing behaviour.
    """
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:
    st.metric(
        "Customers",
        f"{len(rfm):,}"
    )


with kpi2:
    st.metric(
        "Average Recency",
        f"{rfm['recency'].mean():.2f} days"
    )


with kpi3:
    st.metric(
        "Average Frequency",
        f"{rfm['frequency'].mean():.2f}"
    )


with kpi4:
    st.metric(
        "Average Monetary",
        f"₹{rfm['monetary'].mean():,.2f}"
    )


# ============================================================
# SECTION 2 - RFM FRAMEWORK
# ============================================================

st.header("2. RFM Framework")

rfm1, rfm2, rfm3 = st.columns(3)


with rfm1:

    st.subheader("Recency")

    st.write(
        """
        Number of days since the customer's last purchase.

        Lower recency indicates more recent customer activity.
        """
    )


with rfm2:

    st.subheader("Frequency")

    st.write(
        """
        Total number of orders placed by the customer.

        Higher frequency indicates stronger repeat purchasing behaviour.
        """
    )


with rfm3:

    st.subheader("Monetary")

    st.write(
        """
        Total amount spent by the customer.

        Higher monetary value indicates greater customer spending.
        """
    )


# ============================================================
# SECTION 3 - RFM DATASET VALIDATION
# ============================================================

st.header("3. RFM Dataset Validation")

validation = pd.DataFrame(
    {
        "Check": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"
        ],
        "Result": [
            len(rfm),
            rfm.shape[1],
            int(rfm.isna().sum().sum()),
            int(rfm.duplicated().sum())
        ]
    }
)


st.dataframe(
    validation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 4 - RFM STATISTICS
# ============================================================

st.header("4. RFM Statistics")

statistics = pd.DataFrame(
    {
        "Metric": [
            "Recency",
            "Frequency",
            "Monetary"
        ],
        "Mean": [
            rfm["recency"].mean(),
            rfm["frequency"].mean(),
            rfm["monetary"].mean()
        ],
        "Median": [
            rfm["recency"].median(),
            rfm["frequency"].median(),
            rfm["monetary"].median()
        ],
        "Minimum": [
            rfm["recency"].min(),
            rfm["frequency"].min(),
            rfm["monetary"].min()
        ],
        "Maximum": [
            rfm["recency"].max(),
            rfm["frequency"].max(),
            rfm["monetary"].max()
        ]
    }
)


statistics_display = statistics.copy()

for column in [
    "Mean",
    "Median",
    "Minimum",
    "Maximum"
]:
    statistics_display[column] = (
        statistics_display[column]
        .round(2)
    )


st.dataframe(
    statistics_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 5 - RECENCY ANALYSIS
# ============================================================

st.header("5. Recency Analysis")

recency_order = [
    "Active Customers",
    "Recent Customers",
    "Inactive Customers",
    "Highly Inactive Customers"
]


recency_summary = (
    rfm["recency_group"]
    .value_counts()
    .reindex(recency_order)
    .fillna(0)
    .reset_index()
)


recency_summary.columns = [
    "Recency Group",
    "Customers"
]


recency_summary["Percentage"] = (
    recency_summary["Customers"]
    / len(rfm)
    * 100
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        recency_summary,
        x="Recency Group",
        y="Customers",
        text="Customers",
        title="Customers by Recency Group"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Customers",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.pie(
        recency_summary,
        names="Recency Group",
        values="Customers",
        hole=0.5,
        title="Recency Group Distribution"
    )

    fig.update_layout(
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    recency_summary.round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 6 - FREQUENCY ANALYSIS
# ============================================================

st.header("6. Frequency Analysis")

frequency_summary = (
    rfm["frequency"]
    .value_counts()
    .sort_index()
    .reset_index()
)


frequency_summary.columns = [
    "Orders",
    "Customers"
]


frequency_summary["Percentage"] = (
    frequency_summary["Customers"]
    / len(rfm)
    * 100
)


frequency_chart = frequency_summary.head(10)


fig = px.bar(
    frequency_chart,
    x="Orders",
    y="Customers",
    text="Customers",
    title="Customer Distribution by Number of Orders"
)


fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)


fig.update_layout(
    xaxis_title="Number of Orders",
    yaxis_title="Customers",
    height=420
)


st.plotly_chart(
    fig,
    use_container_width=True
)


one_order_percentage = (
    (rfm["frequency"] == 1)
    .mean()
    * 100
)


st.info(
    f"{one_order_percentage:.2f}% of customers have placed exactly one order."
)


# ============================================================
# SECTION 7 - MONETARY ANALYSIS
# ============================================================

st.header("7. Monetary Analysis")


col1, col2 = st.columns(2)


with col1:

    fig = px.histogram(
        rfm,
        x="monetary",
        nbins=40,
        title="Customer Spending Distribution"
    )

    fig.update_layout(
        xaxis_title="Total Spending",
        yaxis_title="Customers",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    monetary_statistics = pd.DataFrame(
        {
            "Metric": [
                "Average Spending",
                "Median Spending",
                "Minimum Spending",
                "Maximum Spending"
            ],
            "Value": [
                f"₹{rfm['monetary'].mean():,.2f}",
                f"₹{rfm['monetary'].median():,.2f}",
                f"₹{rfm['monetary'].min():,.2f}",
                f"₹{rfm['monetary'].max():,.2f}"
            ]
        }
    )

    st.dataframe(
        monetary_statistics,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SECTION 8 - RFM SCORING
# ============================================================

st.header("8. RFM Scoring")

st.write(
    """
    Each customer receives separate Recency, Frequency and Monetary scores.
    The three scores are combined to create the RFM score and total RFM score.
    """
)


score1, score2, score3 = st.columns(3)


with score1:

    r_score = (
        rfm["R_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    r_score.columns = [
        "Score",
        "Customers"
    ]

    fig = px.bar(
        r_score,
        x="Score",
        y="Customers",
        title="Recency Score"
    )

    fig.update_layout(
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with score2:

    f_score = (
        rfm["F_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    f_score.columns = [
        "Score",
        "Customers"
    ]

    fig = px.bar(
        f_score,
        x="Score",
        y="Customers",
        title="Frequency Score"
    )

    fig.update_layout(
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with score3:

    m_score = (
        rfm["M_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    m_score.columns = [
        "Score",
        "Customers"
    ]

    fig = px.bar(
        m_score,
        x="Score",
        y="Customers",
        title="Monetary Score"
    )

    fig.update_layout(
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SECTION 9 - TOTAL RFM SCORE
# ============================================================

st.header("9. RFM Total Score")

score_metrics = st.columns(3)


with score_metrics[0]:

    st.metric(
        "Average RFM Score",
        f"{rfm['RFM_total_score'].mean():.2f}"
    )


with score_metrics[1]:

    st.metric(
        "Median RFM Score",
        f"{rfm['RFM_total_score'].median():.0f}"
    )


with score_metrics[2]:

    st.metric(
        "Score Range",
        f"{rfm['RFM_total_score'].min()} - "
        f"{rfm['RFM_total_score'].max()}"
    )


total_score_distribution = (
    rfm["RFM_total_score"]
    .value_counts()
    .sort_index()
    .reset_index()
)


total_score_distribution.columns = [
    "RFM Total Score",
    "Customers"
]


fig = px.bar(
    total_score_distribution,
    x="RFM Total Score",
    y="Customers",
    title="RFM Total Score Distribution"
)


fig.update_layout(
    height=400,
    xaxis_title="RFM Total Score",
    yaxis_title="Customers"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 10 - CUSTOMER SEGMENTS
# ============================================================

st.header("10. Customer Segments")

segment_order = [
    "Active Customers",
    "High Value Customers",
    "Promising Customers",
    "Lost Customers",
    "Price Sensitive Customers",
    "Premium Customers"
]


segment_summary = (
    rfm.groupby("customer_segment")
    .agg(
        Customers=("customer_id", "count"),
        Average_Recency=("recency", "mean"),
        Average_Frequency=("frequency", "mean"),
        Average_Monetary=("monetary", "mean"),
        Total_Revenue=("monetary", "sum"),
        Average_RFM_Score=("RFM_total_score", "mean")
    )
    .reindex(segment_order)
)


segment_summary["Customer_Percentage"] = (
    segment_summary["Customers"]
    / len(rfm)
    * 100
)


segment_summary["Revenue_Percentage"] = (
    segment_summary["Total_Revenue"]
    / rfm["monetary"].sum()
    * 100
)


segment_display = segment_summary.reset_index()


segment_display.rename(
    columns={
        "customer_segment": "Customer Segment",
        "Customers": "Customers",
        "Customer_Percentage": "Customer %",
        "Average_Recency": "Avg Recency",
        "Average_Frequency": "Avg Frequency",
        "Average_Monetary": "Avg Monetary",
        "Total_Revenue": "Total Revenue",
        "Revenue_Percentage": "Revenue %",
        "Average_RFM_Score": "Avg RFM Score"
    },
    inplace=True
)


st.dataframe(
    segment_display.round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 11 - SEGMENT DISTRIBUTION
# ============================================================

st.header("11. Segment Distribution")


segment_chart = (
    rfm["customer_segment"]
    .value_counts()
    .reindex(segment_order)
    .fillna(0)
    .reset_index()
)


segment_chart.columns = [
    "Customer Segment",
    "Customers"
]


segment_chart["Percentage"] = (
    segment_chart["Customers"]
    / len(rfm)
    * 100
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        segment_chart,
        x="Customers",
        y="Customer Segment",
        orientation="h",
        text="Customers",
        title="Customer Count by Segment"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        yaxis_title="",
        xaxis_title="Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.pie(
        segment_chart,
        names="Customer Segment",
        values="Customers",
        hole=0.5,
        title="Customer Segment Share"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SECTION 12 - SEGMENT REVENUE
# ============================================================

st.header("12. Revenue Contribution by Segment")


revenue_data = segment_summary.reset_index()


revenue_data.rename(
    columns={
        "customer_segment": "Customer Segment"
    },
    inplace=True
)


fig = px.bar(
    revenue_data,
    x="Total_Revenue",
    y="Customer Segment",
    orientation="h",
    text="Revenue_Percentage",
    title="Revenue Contribution by Customer Segment"
)


fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig.update_layout(
    height=450,
    xaxis_title="Total Revenue",
    yaxis_title=""
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 13 - CUSTOMER VALUE AND RFM
# ============================================================

st.header("13. Customer Spending vs RFM Score")

st.write(
    "This view compares customer spending with the overall RFM score."
)


scatter_data = rfm[
    [
        "customer_id",
        "RFM_total_score",
        "monetary",
        "recency",
        "frequency",
        "customer_segment"
    ]
].copy()


if len(scatter_data) > 10000:

    scatter_data = scatter_data.sample(
        10000,
        random_state=42
    )


fig = px.scatter(
    scatter_data,
    x="RFM_total_score",
    y="monetary",
    color="customer_segment",
    hover_data=[
        "customer_id",
        "recency",
        "frequency"
    ],
    opacity=0.6,
    title="RFM Score vs Customer Spending"
)


fig.update_layout(
    height=500,
    xaxis_title="RFM Total Score",
    yaxis_title="Total Spending",
    legend_title="Customer Segment"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 14 - SEGMENT INSIGHTS
# ============================================================

st.header("14. Key Customer Segmentation Insights")


# Use actual calculated values instead of hard-coded results.

largest_segment = (
    segment_summary["Customers"]
    .idxmax()
)

largest_segment_count = (
    segment_summary.loc[
        largest_segment,
        "Customers"
    ]
)

largest_segment_percentage = (
    segment_summary.loc[
        largest_segment,
        "Customer_Percentage"
    ]
)


highest_revenue_segment = (
    segment_summary["Total_Revenue"]
    .idxmax()
)

highest_revenue_percentage = (
    segment_summary.loc[
        highest_revenue_segment,
        "Revenue_Percentage"
    ]
)


highest_rfm_segment = (
    segment_summary["Average_RFM_Score"]
    .idxmax()
)


one_order_pct = (
    (rfm["frequency"] == 1)
    .mean()
    * 100
)


insights = [
    f"{one_order_pct:.2f}% of customers have placed exactly one order.",

    f"{largest_segment} is the largest customer segment with "
    f"{largest_segment_count:,.0f} customers "
    f"({largest_segment_percentage:.2f}% of the customer base).",

    f"{highest_revenue_segment} contributes the highest share of "
    f"revenue at {highest_revenue_percentage:.2f}% of total revenue.",

    f"{highest_rfm_segment} has the highest average RFM score "
    f"among the identified customer segments."
]


for insight in insights:

    st.write(
        f"- {insight}"
    )


# ============================================================
# SECTION 15 - SEGMENT LEVEL BEHAVIOUR
# ============================================================

st.header("15. Segment Behaviour Comparison")


behaviour_data = segment_summary[
    [
        "Average_Recency",
        "Average_Frequency",
        "Average_Monetary",
        "Average_RFM_Score"
    ]
].reset_index()


behaviour_data.rename(
    columns={
        "customer_segment": "Customer Segment"
    },
    inplace=True
)


st.dataframe(
    behaviour_data.round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 16 - RFM DATASET PREVIEW
# ============================================================

st.header("16. RFM Dataset Preview")


preview_columns = [
    "customer_id",
    "recency",
    "frequency",
    "monetary",
    "R_score",
    "F_score",
    "M_score",
    "RFM_score",
    "RFM_total_score",
    "customer_segment"
]


st.dataframe(
    rfm[preview_columns].head(100),
    use_container_width=True,
    height=400,
    hide_index=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.header("17. Export RFM Segmentation Data")


download_data = rfm.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download RFM Segmentation CSV",
    data=download_data,
    file_name="customer_rfm_segmentation.csv",
    mime="text/csv",
    key="download_customer_rfm_segmentation"
)