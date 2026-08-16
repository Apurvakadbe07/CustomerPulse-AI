import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CustomerPulse AI | EDA",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATA PATH
# ============================================================

DATA_PATH = Path(
    r"D:\customer pulse AI project\1 data\02_processed data\customer_360.csv"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("Exploratory Data Analysis")
st.caption(
    "Data Understanding & Validation"
)


# ============================================================
# LOAD CUSTOMER 360 DATASET
# ============================================================

if not DATA_PATH.exists():

    st.error(
        f"Customer 360 dataset was not found:\n\n{DATA_PATH}"
    )

    st.stop()


try:

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=[
            "first_purchase_date",
            "last_purchase_date"
        ]
    )

except ValueError:

    # If the date columns are not present, do not assume them.
    # Load the dataset without forced date parsing.
    try:

        df = pd.read_csv(DATA_PATH)

    except Exception as e:

        st.error(
            f"Unable to load customer_360.csv:\n\n{e}"
        )

        st.stop()

except Exception as e:

    st.error(
        f"Unable to load customer_360.csv:\n\n{e}"
    )

    st.stop()


# ============================================================
# BASIC LOAD VALIDATION
# ============================================================

if df.empty:

    st.warning(
        "customer_360.csv was loaded, but the dataset contains no rows."
    )

    st.stop()


# ============================================================
# PART 1 — DATASET VALIDATION
# ============================================================

st.header("1. Data Understanding & Validation")


# ============================================================
# DATASET METRICS
# ============================================================

total_customers = df.shape[0]

total_features = df.shape[1]

duplicate_rows = df.duplicated().sum()

missing_values = df.isnull().sum().sum()


# ============================================================
# CUSTOMER ID VALIDATION
# ============================================================

customer_id_column = "customer_unique_id"


if customer_id_column in df.columns:

    duplicate_customers = (
        df[customer_id_column]
        .duplicated()
        .sum()
    )

else:

    duplicate_customers = None


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


with col2:

    st.metric(
        "Total Features",
        f"{total_features:,}"
    )


with col3:

    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )


with col4:

    if duplicate_customers is not None:

        st.metric(
            "Duplicate Customers",
            f"{duplicate_customers:,}"
        )

    else:

        st.metric(
            "Duplicate Customers",
            "N/A"
        )


with col5:

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


st.divider()


# ============================================================
# DATASET STATUS
# ============================================================

if (
    duplicate_rows == 0
    and missing_values == 0
    and (
        duplicate_customers is None
        or duplicate_customers == 0
    )
):

    st.success(
        "Dataset is clean and ready for detailed EDA."
    )

else:

    st.warning(
        "One or more validation checks require attention."
    )


# ============================================================
# DATA TYPES
# ============================================================

st.subheader("Data Types")

dtype_table = pd.DataFrame(
    {
        "Column": df.columns,
        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ]
    }
)

st.dataframe(
    dtype_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

st.subheader("Missing Value Check")

missing_table = (
    df.isnull()
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

missing_table.columns = [
    "Column",
    "Missing Values"
]


if missing_values == 0:

    st.info(
        "No missing values were found in the dataset."
    )

else:

    missing_table = missing_table[
        missing_table["Missing Values"] > 0
    ]

    st.dataframe(
        missing_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DUPLICATE ROW CHECK
# ============================================================

st.subheader("Duplicate Row Check")

duplicate_row_table = pd.DataFrame(
    {
        "Metric": [
            "Duplicate Rows"
        ],
        "Value": [
            duplicate_rows
        ]
    }
)

st.dataframe(
    duplicate_row_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DUPLICATE CUSTOMER CHECK
# ============================================================

st.subheader("Duplicate Customer Check")


if customer_id_column in df.columns:

    duplicate_customer_table = pd.DataFrame(
        {
            "Metric": [
                "Duplicate Customers"
            ],
            "Value": [
                duplicate_customers
            ]
        }
    )

    st.dataframe(
        duplicate_customer_table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "customer_unique_id is not present in the loaded dataset. "
        "Duplicate customer validation was skipped."
    )


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

st.subheader("Descriptive Statistics")

with st.expander(
    "View descriptive statistics"
):

    descriptive_statistics = df.describe(
        include="all"
    ).T

    descriptive_statistics.index.name = "Column"

    descriptive_statistics = (
        descriptive_statistics
        .reset_index()
    )

    st.dataframe(
        descriptive_statistics,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATASET PREVIEW
# ============================================================

st.subheader("Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FINAL VALIDATION SUMMARY
# ============================================================

st.subheader("Validation Summary")


validation_data = {
    "Total Customers": total_customers,
    "Total Features": total_features,
    "Duplicate Rows": duplicate_rows,
    "Duplicate Customers": (
        duplicate_customers
        if duplicate_customers is not None
        else "Not Available"
    ),
    "Missing Values": missing_values
}


validation_summary = pd.DataFrame(
    {
        "Metric": list(validation_data.keys()),
        "Value": list(validation_data.values())
    }
)


st.dataframe(
    validation_summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PART 1 COMPLETION
# ============================================================

if (
    duplicate_rows == 0
    and missing_values == 0
    and (
        duplicate_customers is None
        or duplicate_customers == 0
    )
):

    st.success(
        "Data Understanding & Validation completed successfully."
    )

else:

    st.info(
        "Data Understanding & Validation completed. "
        "Review the validation results before continuing."
    )
#2
# ============================================================
# PART 2 — NUMERICAL FEATURE ANALYSIS
# ============================================================

st.header("2. Numerical Feature Analysis")

st.caption(
    "Numerical features are identified directly from the loaded "
    "customer_360.csv dataset."
)


# ============================================================
# SELECT NUMERICAL FEATURES
# ============================================================

numerical_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


# ============================================================
# NUMERICAL FEATURE VALIDATION
# ============================================================

if not numerical_columns:

    st.warning(
        "No numerical features were found in the loaded dataset."
    )

else:

    st.info(
        f"Total Numerical Features: {len(numerical_columns)}"
    )


# ============================================================
# NUMERICAL FEATURE LIST
# ============================================================

if numerical_columns:

    with st.expander("View Numerical Features"):

        numerical_feature_table = pd.DataFrame(
            {
                "Numerical Feature": numerical_columns
            }
        )

        st.dataframe(
            numerical_feature_table,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# SUMMARY STATISTICS
# ============================================================

if numerical_columns:

    st.subheader("Summary Statistics")

    numerical_summary = (
        df[numerical_columns]
        .describe()
        .T
        .reset_index()
    )

    numerical_summary = numerical_summary.rename(
        columns={
            "index": "Feature"
        }
    )

    st.dataframe(
        numerical_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SKEWNESS ANALYSIS
# ============================================================

if numerical_columns:

    st.subheader("Skewness Analysis")

    skewness = pd.DataFrame(
        {
            "Skewness": df[numerical_columns].skew()
        }
    )

    skewness = skewness.sort_values(
        by="Skewness",
        ascending=False
    )


    # ========================================================
    # SKEWNESS CLASSIFICATION
    # ========================================================

    def classify_skewness(value):

        if value > 1:

            return "Highly Right Skewed"

        elif value > 0.5:

            return "Moderately Right Skewed"

        elif value < -1:

            return "Highly Left Skewed"

        elif value < -0.5:

            return "Moderately Left Skewed"

        else:

            return "Approximately Symmetric"


    skewness["Distribution"] = (
        skewness["Skewness"]
        .apply(classify_skewness)
    )

    skewness = (
        skewness
        .reset_index()
        .rename(
            columns={
                "index": "Feature"
            }
        )
    )


    # ========================================================
    # SKEWNESS TABLE
    # ========================================================

    st.dataframe(
        skewness,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DISTRIBUTION ANALYSIS
# ============================================================

if numerical_columns:

    st.subheader("Feature Distributions")

    st.caption(
        "Select a numerical feature to inspect its distribution."
    )

    selected_feature = st.selectbox(
        "Select Numerical Feature",
        options=numerical_columns,
        key="eda_numerical_feature"
    )


    # ========================================================
    # SELECTED FEATURE DATA
    # ========================================================

    feature_data = df[selected_feature].dropna()


    if feature_data.empty:

        st.warning(
            f"No valid values are available for '{selected_feature}'."
        )

    else:

        # ====================================================
        # FEATURE SUMMARY
        # ====================================================

        feature_col1, feature_col2, feature_col3, feature_col4 = (
            st.columns(4)
        )


        with feature_col1:

            st.metric(
                "Count",
                f"{feature_data.count():,}"
            )


        with feature_col2:

            st.metric(
                "Mean",
                f"{feature_data.mean():,.2f}"
            )


        with feature_col3:

            st.metric(
                "Median",
                f"{feature_data.median():,.2f}"
            )


        with feature_col4:

            st.metric(
                "Skewness",
                f"{feature_data.skew():,.2f}"
            )


        # ====================================================
        # HISTOGRAM
        # ====================================================

        histogram = px.histogram(
            df,
            x=selected_feature,
            nbins=30,
            marginal="box",
            title=f"Distribution of {selected_feature}"
        )

        histogram.update_layout(
            xaxis_title=selected_feature,
            yaxis_title="Count",
            height=500
        )

        st.plotly_chart(
            histogram,
            use_container_width=True
        )


# ============================================================
# SKEWNESS DISTRIBUTION SUMMARY
# ============================================================

if numerical_columns:

    st.subheader("Distribution Classification Summary")


    distribution_counts = (
        skewness["Distribution"]
        .value_counts()
        .reset_index()
    )

    distribution_counts.columns = [
        "Distribution",
        "Feature Count"
    ]


    st.dataframe(
        distribution_counts,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HIGHLY SKEWED FEATURES
# ============================================================

if numerical_columns:

    highly_skewed = skewness[
        (
            skewness["Skewness"] > 1
        )
        |
        (
            skewness["Skewness"] < -1
        )
    ].copy()


    st.subheader("Highly Skewed Features")


    if highly_skewed.empty:

        st.info(
            "No highly skewed numerical features were identified "
            "using the notebook's classification logic."
        )

    else:

        st.dataframe(
            highly_skewed,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# INITIAL BUSINESS OBSERVATIONS
# ============================================================

if numerical_columns:

    st.subheader("Initial Numerical Analysis Observations")

    st.info(
        "Numerical analysis is used to understand feature "
        "distributions, skewness and potential outlier behaviour. "
        "No outlier treatment is performed in this section."
    )
#3
# ============================================================
# PART 3 — CATEGORICAL FEATURE ANALYSIS
# ============================================================

st.header("3. Categorical Feature Analysis")

st.caption(
    "Categorical distributions reproduced from the EDA notebook "
    "using the loaded customer_360.csv dataset."
)


# ============================================================
# CATEGORICAL COLUMNS IDENTIFICATION
# ============================================================

categorical_columns = df.select_dtypes(
    include=["object", "category", "string"]
).columns.tolist()


# ============================================================
# CATEGORICAL FEATURE VALIDATION
# ============================================================

if not categorical_columns:

    st.warning(
        "No categorical features were found in the loaded dataset."
    )

else:

    st.info(
        f"Total Categorical Features Found: "
        f"{len(categorical_columns)}"
    )


# ============================================================
# CATEGORICAL FEATURE LIST
# ============================================================

if categorical_columns:

    with st.expander("View Categorical Features"):

        categorical_feature_table = pd.DataFrame(
            {
                "Categorical Feature": categorical_columns
            }
        )

        st.dataframe(
            categorical_feature_table,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# HELPER FUNCTION
# ============================================================

def show_top_categories(
    data,
    column_name,
    top_n=10,
    chart_title=None
):

    """
    Reproduces the notebook's value_counts().head(top_n)
    logic without assuming that the requested column exists.
    """

    if column_name not in data.columns:

        st.warning(
            f"'{column_name}' is not available in the loaded "
            "customer_360.csv dataset. This analysis was skipped."
        )

        return


    # --------------------------------------------------------
    # Check actual datatype
    # --------------------------------------------------------

    if not (
        pd.api.types.is_object_dtype(data[column_name])
        or
        pd.api.types.is_categorical_dtype(data[column_name])
        or
        pd.api.types.is_string_dtype(data[column_name])
    ):

        st.warning(
            f"'{column_name}' is present, but its actual datatype "
            "is not categorical. This analysis was skipped."
        )

        return


    # --------------------------------------------------------
    # Actual notebook logic
    # --------------------------------------------------------

    category_counts = (
        data[column_name]
        .value_counts()
        .head(top_n)
    )


    if category_counts.empty:

        st.info(
            f"No categorical values are available for "
            f"'{column_name}'."
        )

        return


    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    result_table = (
        category_counts
        .rename("Customers")
        .reset_index()
    )

    result_table.columns = [
        "Category",
        "Customers"
    ]


    result_table["Percentage"] = (
        result_table["Customers"]
        / len(data)
        * 100
    )


    result_table["Percentage"] = (
        result_table["Percentage"]
        .round(2)
    )


    st.dataframe(
        result_table,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Plotly chart
    # --------------------------------------------------------

    chart_data = result_table.sort_values(
        "Customers",
        ascending=True
    )


    fig = px.bar(
        chart_data,
        x="Customers",
        y="Category",
        orientation="h",
        title=(
            chart_title
            if chart_title is not None
            else f"Top {top_n} {column_name}"
        ),
        text="Customers"
    )


    fig.update_layout(
        height=max(
            400,
            min(650, 80 + len(chart_data) * 45)
        ),
        xaxis_title="Customers",
        yaxis_title=""
    )


    fig.update_traces(
        textposition="outside"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CUSTOMER STATE
# ============================================================

st.subheader("Customer State Distribution")

show_top_categories(
    df,
    "customer_state",
    top_n=10,
    chart_title="Top 10 Customer States"
)


# ============================================================
# CUSTOMER CITY
# ============================================================

st.subheader("Customer City Distribution")

show_top_categories(
    df,
    "customer_city",
    top_n=10,
    chart_title="Top 10 Customer Cities"
)


# ============================================================
# PREFERRED PAYMENT TYPE
# ============================================================

st.subheader("Preferred Payment Type")

show_top_categories(
    df,
    "preferred_payment_type",
    top_n=10,
    chart_title="Preferred Payment Type Distribution"
)


# ============================================================
# FAVORITE PRODUCT CATEGORY
# ============================================================

st.subheader("Favourite Product Category")

show_top_categories(
    df,
    "favorite_category",
    top_n=10,
    chart_title="Top 10 Favourite Product Categories"
)


# ============================================================
# CUSTOMER VALUE TIER
# ============================================================

st.subheader("Customer Value Tier Distribution")


value_tier_column = "customer_value_tier"


if value_tier_column not in df.columns:

    st.warning(
        f"'{value_tier_column}' is not available in the loaded "
        "customer_360.csv dataset. This analysis was skipped."
    )

else:

    if not (
        pd.api.types.is_object_dtype(df[value_tier_column])
        or
        pd.api.types.is_categorical_dtype(df[value_tier_column])
        or
        pd.api.types.is_string_dtype(df[value_tier_column])
    ):

        st.warning(
            f"'{value_tier_column}' exists but its actual datatype "
            "is not categorical. This analysis was skipped."
        )

    else:

        # ----------------------------------------------------
        # Notebook logic:
        # tier_counts = df["customer_value_tier"].value_counts()
        # ----------------------------------------------------

        tier_counts = (
            df[value_tier_column]
            .value_counts()
        )


        if tier_counts.empty:

            st.info(
                "No customer value tier values are available."
            )

        else:

            tier_table = (
                tier_counts
                .rename("Customers")
                .reset_index()
            )

            tier_table.columns = [
                "Customer Value Tier",
                "Customers"
            ]


            tier_table["Percentage"] = (
                tier_table["Customers"]
                / len(df)
                * 100
            )


            tier_table["Percentage"] = (
                tier_table["Percentage"]
                .round(2)
            )


            st.dataframe(
                tier_table,
                use_container_width=True,
                hide_index=True
            )


            tier_chart = px.bar(
                tier_table,
                x="Customer Value Tier",
                y="Customers",
                text="Customers",
                title="Customer Value Tier Distribution"
            )


            tier_chart.update_layout(
                height=450,
                xaxis_title="Customer Value Tier",
                yaxis_title="Number of Customers"
            )


            tier_chart.update_traces(
                textposition="outside"
            )


            st.plotly_chart(
                tier_chart,
                use_container_width=True
            )


# ============================================================
# CATEGORICAL ANALYSIS SUMMARY
# ============================================================

st.subheader("Categorical Analysis Summary")

analysis_columns = [
    "customer_state",
    "customer_city",
    "preferred_payment_type",
    "favorite_category",
    "customer_value_tier"
]


available_analysis_columns = [
    column
    for column in analysis_columns
    if column in df.columns
]


if not available_analysis_columns:

    st.warning(
        "None of the categorical features analysed in the "
        "EDA notebook are available in the loaded dataset."
    )

else:

    summary_rows = []

    for column in available_analysis_columns:

        summary_rows.append(
            {
                "Feature": column,
                "Unique Values": int(
                    df[column].nunique(dropna=True)
                ),
                "Missing Values": int(
                    df[column].isna().sum()
                )
            }
        )


    categorical_summary = pd.DataFrame(
        summary_rows
    )


    st.dataframe(
        categorical_summary,
        use_container_width=True,
        hide_index=True
    )
#4
# ============================================================
# PART 5 — CORRELATION ANALYSIS
# ============================================================

st.header("5. Correlation Analysis")

st.caption(
    "Pearson correlation analysis of the continuous numerical "
    "features defined in the EDA notebook."
)


# ============================================================
# CONTINUOUS FEATURES — NOTEBOOK DEFINITION
# ============================================================

continuous_features = [
    "total_orders",
    "delivered_orders",
    "cancelled_orders",
    "total_spent",
    "average_order_value",
    "maximum_order_value",
    "minimum_order_value",
    "average_payment_installments",
    "total_items_purchased",
    "unique_products",
    "unique_categories",
    "average_items_per_order",
    "average_review_score",
    "average_delivery_days",
    "average_delivery_delay",
    "recency_days",
    "customer_tenure_days",
    "purchase_frequency",
    "average_purchase_gap",
    "spending_intensity"
]


# ============================================================
# VALIDATE CONTINUOUS FEATURES
# ============================================================

available_continuous_features = []
missing_continuous_features = []
non_numeric_continuous_features = []


for feature in continuous_features:

    if feature not in df.columns:

        missing_continuous_features.append(feature)

        continue


    if not pd.api.types.is_numeric_dtype(df[feature]):

        non_numeric_continuous_features.append(feature)

        continue


    available_continuous_features.append(feature)


# ============================================================
# FEATURE VALIDATION TABLE
# ============================================================

st.subheader("Continuous Feature Validation")


validation_rows = []


for feature in continuous_features:

    if feature in available_continuous_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Available",
                "Data Type": str(df[feature].dtype)
            }
        )

    elif feature in missing_continuous_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    else:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Non-Numeric — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )


continuous_validation = pd.DataFrame(
    validation_rows
)


st.dataframe(
    continuous_validation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FEATURE COUNT
# ============================================================

if available_continuous_features:

    st.info(
        f"Continuous features available for correlation analysis: "
        f"{len(available_continuous_features)}"
    )

else:

    st.warning(
        "No valid continuous numerical features are available "
        "for correlation analysis."
    )


# ============================================================
# CORRELATION MATRIX
# ============================================================

if available_continuous_features:

    st.subheader("Pearson Correlation Matrix")


    # --------------------------------------------------------
    # Notebook logic:
    # correlation_matrix = df[continuous_features].corr()
    # --------------------------------------------------------

    correlation_matrix = (
        df[available_continuous_features]
        .corr(method="pearson")
    )


    # --------------------------------------------------------
    # Display rounded matrix
    # --------------------------------------------------------

    st.dataframe(
        correlation_matrix.round(2),
        use_container_width=True
    )


    # ========================================================
    # CORRELATION HEATMAP
    # ========================================================

    st.subheader("Correlation Heatmap")


    # --------------------------------------------------------
    # Upper triangle mask
    # --------------------------------------------------------

    mask = np.triu(
        np.ones_like(
            correlation_matrix,
            dtype=bool
        )
    )


    heatmap_values = correlation_matrix.copy()


    # --------------------------------------------------------
    # Hide upper triangle
    # --------------------------------------------------------

    heatmap_values = heatmap_values.mask(mask)


    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_values.values,
            x=heatmap_values.columns.tolist(),
            y=heatmap_values.index.tolist(),
            zmin=-1,
            zmax=1,
            zmid=0,
            text=heatmap_values.round(2).values,
            texttemplate="%{text}",
            hovertemplate=(
                "%{y}<br>"
                "%{x}<br>"
                "Correlation: %{z:.2f}"
                "<extra></extra>"
            ),
            colorbar={
                "title": "Correlation"
            }
        )
    )


    heatmap_fig.update_layout(
        height=750,
        xaxis_title="Features",
        yaxis_title="Features"
    )


    st.plotly_chart(
        heatmap_fig,
        use_container_width=True
    )


    # ========================================================
    # HIGHLY CORRELATED FEATURE PAIRS
    # ========================================================

    st.subheader("Highly Correlated Feature Pairs")


    # --------------------------------------------------------
    # Notebook logic:
    # correlation_matrix.unstack()
    # --------------------------------------------------------

    corr_pairs = (
        correlation_matrix
        .unstack()
        .reset_index()
    )


    corr_pairs.columns = [
        "Feature 1",
        "Feature 2",
        "Correlation"
    ]


    # --------------------------------------------------------
    # Remove self correlation
    # --------------------------------------------------------

    corr_pairs = corr_pairs[
        corr_pairs["Feature 1"]
        != corr_pairs["Feature 2"]
    ].copy()


    # --------------------------------------------------------
    # Remove duplicate pairs
    # --------------------------------------------------------

    corr_pairs["Pair"] = corr_pairs.apply(
        lambda row: tuple(
            sorted(
                [
                    row["Feature 1"],
                    row["Feature 2"]
                ]
            )
        ),
        axis=1
    )


    corr_pairs = corr_pairs.drop_duplicates(
        subset="Pair"
    )


    # --------------------------------------------------------
    # Notebook threshold:
    # abs(Correlation) >= 0.80
    # --------------------------------------------------------

    high_corr = corr_pairs[
        corr_pairs["Correlation"].abs() >= 0.80
    ].copy()


    high_corr = high_corr.sort_values(
        by="Correlation",
        ascending=False
    )


    high_corr = high_corr.drop(
        columns="Pair"
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    if high_corr.empty:

        st.info(
            "No feature pairs meet the notebook's strong "
            "correlation threshold of |correlation| >= 0.80."
        )

    else:

        high_corr_display = high_corr.copy()

        high_corr_display["Correlation"] = (
            high_corr_display["Correlation"]
            .round(3)
        )


        st.dataframe(
            high_corr_display,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # TOP CORRELATION PAIRS
    # ========================================================

    st.subheader("Strongest Correlation Pairs")


    strongest_pairs = corr_pairs.copy()


    strongest_pairs["Absolute Correlation"] = (
        strongest_pairs["Correlation"]
        .abs()
    )


    strongest_pairs = (
        strongest_pairs
        .sort_values(
            by="Absolute Correlation",
            ascending=False
        )
        .head(10)
    )


    strongest_pairs = strongest_pairs.drop(
        columns="Pair"
    )


    strongest_pairs["Correlation"] = (
        strongest_pairs["Correlation"]
        .round(3)
    )


    strongest_pairs["Absolute Correlation"] = (
        strongest_pairs["Absolute Correlation"]
        .round(3)
    )


    if strongest_pairs.empty:

        st.info(
            "No correlation pairs are available."
        )

    else:

        st.dataframe(
            strongest_pairs,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # CORRELATION INTERPRETATION
    # ========================================================

    st.subheader("Correlation Interpretation")


    st.info(
        "Correlation values range from -1 to +1. "
        "Positive values indicate a positive linear relationship, "
        "while negative values indicate a negative linear relationship. "
        "Correlation does not imply causation."
    )


    # ========================================================
    # BUSINESS INSIGHTS FROM NOTEBOOK
    # ========================================================

    st.subheader("EDA Correlation Findings")


    st.markdown(
        """
        **Key findings documented in the EDA notebook:**

        - Spending-related features exhibit extremely strong
          positive correlations (>0.95), indicating that they
          capture similar aspects of customer purchasing behaviour.

        - Customer Tenure and Average Purchase Gap show a very
          high positive correlation (0.985), reflecting long-term
          customer engagement patterns.

        - Total Items Purchased and Average Items Per Order are
          also strongly correlated, suggesting similar purchasing
          behaviour.
        """
    )


    # ========================================================
    # BUSINESS DECISION
    # ========================================================

    st.subheader("EDA Business Decision")


    st.info(
        "No features are removed during EDA. Highly correlated "
        "features are reviewed later during feature selection "
        "before machine learning."
    )


# ============================================================
# NO FEATURE REMOVAL
# ============================================================

st.caption(
    "Correlation analysis does not modify the source dataset "
    "or remove any features."
)
#5
# ============================================================
# PART 5 — CORRELATION ANALYSIS
# ============================================================

st.header("5. Correlation Analysis")

st.caption(
    "Understanding relationships between numerical customer "
    "features using Pearson correlation."
)


# ============================================================
# CONTINUOUS FEATURES USED IN THE NOTEBOOK
# ============================================================

continuous_features = [
    "total_orders",
    "delivered_orders",
    "cancelled_orders",
    "total_spent",
    "average_order_value",
    "maximum_order_value",
    "minimum_order_value",
    "average_payment_installments",
    "total_items_purchased",
    "unique_products",
    "unique_categories",
    "average_items_per_order",
    "average_review_score",
    "average_delivery_days",
    "average_delivery_delay",
    "recency_days",
    "customer_tenure_days",
    "purchase_frequency",
    "average_purchase_gap",
    "spending_intensity"
]


# ============================================================
# CHECK FEATURES AGAINST ACTUAL DATASET
# ============================================================

available_continuous_features = []
missing_continuous_features = []
non_numeric_continuous_features = []


for feature in continuous_features:

    if feature not in df.columns:

        missing_continuous_features.append(feature)

    elif not pd.api.types.is_numeric_dtype(df[feature]):

        non_numeric_continuous_features.append(feature)

    else:

        available_continuous_features.append(feature)


# ============================================================
# FEATURE VALIDATION
# ============================================================

st.subheader("Correlation Feature Validation")


validation_rows = []


for feature in continuous_features:

    if feature in available_continuous_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Available",
                "Data Type": str(df[feature].dtype)
            }
        )

    elif feature in missing_continuous_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    else:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Non-Numeric — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )


validation_df = pd.DataFrame(
    validation_rows
)


st.dataframe(
    validation_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

if len(available_continuous_features) < 2:

    st.warning(
        "At least two valid numerical features are required "
        "for correlation analysis."
    )

else:

    st.info(
        f"Valid continuous features used: "
        f"{len(available_continuous_features)}"
    )


    # ========================================================
    # PEARSON CORRELATION MATRIX
    # ========================================================

    st.subheader("Pearson Correlation Matrix")


    correlation_matrix = (
        df[available_continuous_features]
        .corr(method="pearson")
    )


    st.dataframe(
        correlation_matrix.round(2),
        use_container_width=True
    )


    # ========================================================
    # CORRELATION HEATMAP
    # ========================================================

    st.subheader("Correlation Heatmap")


    heatmap_data = correlation_matrix.copy()


    heatmap_fig = px.imshow(
        heatmap_data,
        text_auto=".2f",
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        title="Pearson Correlation Heatmap"
    )


    heatmap_fig.update_layout(
        height=800,
        xaxis_title="Features",
        yaxis_title="Features",
        coloraxis_colorbar_title="Correlation"
    )


    st.plotly_chart(
        heatmap_fig,
        use_container_width=True
    )


    # ========================================================
    # CORRELATION PAIRS
    # ========================================================

    st.subheader("Feature Correlation Pairs")


    corr_pairs = (
        correlation_matrix
        .unstack()
        .reset_index()
    )


    corr_pairs.columns = [
        "Feature 1",
        "Feature 2",
        "Correlation"
    ]


    # --------------------------------------------------------
    # REMOVE SELF-CORRELATION
    # --------------------------------------------------------

    corr_pairs = corr_pairs[
        corr_pairs["Feature 1"]
        != corr_pairs["Feature 2"]
    ].copy()


    # --------------------------------------------------------
    # CREATE UNIQUE FEATURE PAIR
    # --------------------------------------------------------

    corr_pairs["Pair"] = corr_pairs.apply(
        lambda row: tuple(
            sorted(
                [
                    row["Feature 1"],
                    row["Feature 2"]
                ]
            )
        ),
        axis=1
    )


    # --------------------------------------------------------
    # REMOVE DUPLICATE PAIRS
    # --------------------------------------------------------

    corr_pairs = corr_pairs.drop_duplicates(
        subset="Pair"
    )


    # ========================================================
    # STRONG CORRELATION THRESHOLD
    # ========================================================

    correlation_threshold = 0.80


    high_corr = corr_pairs[
        corr_pairs["Correlation"].abs()
        >= correlation_threshold
    ].copy()


    high_corr = high_corr.sort_values(
        by="Correlation",
        ascending=False
    )


    high_corr = high_corr.drop(
        columns="Pair"
    )


    # ========================================================
    # HIGHLY CORRELATED PAIRS TABLE
    # ========================================================

    st.subheader(
        "Highly Correlated Feature Pairs"
    )


    if high_corr.empty:

        st.info(
            "No feature pairs meet the notebook's "
            "strong-correlation threshold "
            "(absolute correlation ≥ 0.80)."
        )

    else:

        high_corr["Correlation"] = (
            high_corr["Correlation"]
            .round(3)
        )


        st.dataframe(
            high_corr,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # TOP CORRELATION PAIRS
    # ========================================================

    st.subheader(
        "Strongest Correlation Pairs"
    )


    strongest_pairs = corr_pairs.copy()


    strongest_pairs["Absolute Correlation"] = (
        strongest_pairs["Correlation"]
        .abs()
    )


    strongest_pairs = (
        strongest_pairs
        .sort_values(
            by="Absolute Correlation",
            ascending=False
        )
        .head(10)
    )


    strongest_pairs = strongest_pairs.drop(
        columns="Pair"
    )


    strongest_pairs["Correlation"] = (
        strongest_pairs["Correlation"]
        .round(3)
    )


    strongest_pairs["Absolute Correlation"] = (
        strongest_pairs["Absolute Correlation"]
        .round(3)
    )


    if strongest_pairs.empty:

        st.info(
            "No valid correlation pairs were found."
        )

    else:

        st.dataframe(
            strongest_pairs,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # CORRELATION RANGE
    # ========================================================

    st.subheader(
        "Correlation Range"
    )


    valid_correlations = (
        corr_pairs["Correlation"]
        .dropna()
    )


    if not valid_correlations.empty:

        min_correlation = valid_correlations.min()
        max_correlation = valid_correlations.max()


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Minimum Correlation",
                f"{min_correlation:.3f}"
            )


        with col2:

            st.metric(
                "Maximum Correlation",
                f"{max_correlation:.3f}"
            )


    # ========================================================
    # NOTEBOOK CONCLUSION
    # ========================================================

    st.subheader(
        "Correlation Analysis Conclusion"
    )


    st.info(
        "Correlation analysis revealed several highly correlated "
        "feature pairs, particularly among spending-related "
        "variables. These relationships are reviewed for "
        "redundancy, but no features are removed at this stage."
    )


    st.caption(
        "Feature selection and multicollinearity handling belong "
        "to the later machine-learning stage."
    )
#6
# ============================================================
# PART 6 — CUSTOMER PURCHASE BEHAVIOUR
# ============================================================

st.header("6. Customer Purchase Behaviour")

st.caption(
    "Analysis of customer spending, order behaviour, "
    "purchase frequency and customer value."
)


# ============================================================
# HELPER — CHECK REQUIRED COLUMNS
# ============================================================

def check_required_columns(data, required_columns):

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:

        st.warning(
            "The following required columns are not available "
            "in customer_360.csv. The related analysis was skipped: "
            + ", ".join(missing_columns)
        )

        return False

    return True


# ============================================================
# 1. CUSTOMER SPENDING DISTRIBUTION
# ============================================================

st.subheader("Customer Spending Distribution")


if check_required_columns(
    df,
    ["total_spent"]
):

    spending_data = df["total_spent"].dropna()


    if spending_data.empty:

        st.warning(
            "No valid values are available for total_spent."
        )

    else:

        # ----------------------------------------------------
        # Summary metrics
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Customers",
                f"{len(spending_data):,}"
            )


        with col2:

            st.metric(
                "Average Spending",
                f"{spending_data.mean():,.2f}"
            )


        with col3:

            st.metric(
                "Median Spending",
                f"{spending_data.median():,.2f}"
            )


        with col4:

            st.metric(
                "Maximum Spending",
                f"{spending_data.max():,.2f}"
            )


        # ----------------------------------------------------
        # Full distribution
        # ----------------------------------------------------

        spending_fig = px.histogram(
            df,
            x="total_spent",
            nbins=50,
            marginal="box",
            title="Customer Spending Distribution"
        )


        spending_fig.update_layout(
            height=500,
            xaxis_title="Total Spending",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            spending_fig,
            use_container_width=True
        )


        st.info(
            "The notebook identifies the spending distribution "
            "as highly right-skewed. Extreme values are excluded "
            "only for visualization purposes in the notebook; "
            "the underlying records are not removed."
        )


# ============================================================
# 2. TOP 10 HIGHEST-SPENDING CUSTOMERS
# ============================================================

st.subheader("Top 10 Highest-Spending Customers")


required_top_spender_columns = [
    "customer_unique_id",
    "total_spent"
]


if check_required_columns(
    df,
    required_top_spender_columns
):

    top_spenders = (
        df[
            [
                "customer_unique_id",
                "total_spent"
            ]
        ]
        .sort_values(
            by="total_spent",
            ascending=False
        )
        .head(10)
        .copy()
    )


    top_spenders = top_spenders.rename(
        columns={
            "customer_unique_id": "Customer ID",
            "total_spent": "Total Spending"
        }
    )


    st.dataframe(
        top_spenders,
        use_container_width=True,
        hide_index=True
    )


    top_spender_chart = px.bar(
        top_spenders.sort_values(
            "Total Spending",
            ascending=True
        ),
        x="Total Spending",
        y="Customer ID",
        orientation="h",
        text="Total Spending",
        title="Top 10 Highest-Spending Customers"
    )


    top_spender_chart.update_layout(
        height=500,
        xaxis_title="Total Spending",
        yaxis_title="Customer ID"
    )


    top_spender_chart.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )


    st.plotly_chart(
        top_spender_chart,
        use_container_width=True
    )


# ============================================================
# 3. REPEAT VS ONE-TIME BUYERS
# ============================================================

st.subheader("Repeat vs One-Time Buyers")


repeat_columns = [
    "one_time_buyer",
    "repeat_customer"
]


if check_required_columns(
    df,
    repeat_columns
):

    customer_type = pd.DataFrame(
        {
            "Customer Type": [
                "One-Time Buyer",
                "Repeat Customer"
            ],
            "Customers": [
                df["one_time_buyer"].sum(),
                df["repeat_customer"].sum()
            ]
        }
    )


    customer_type["Percentage"] = (
        customer_type["Customers"]
        / len(df)
        * 100
    )


    customer_type["Percentage"] = (
        customer_type["Percentage"]
        .round(2)
    )


    st.dataframe(
        customer_type,
        use_container_width=True,
        hide_index=True
    )


    repeat_fig = px.bar(
        customer_type,
        x="Customer Type",
        y="Customers",
        text="Customers",
        title="Repeat vs One-Time Buyers"
    )


    repeat_fig.update_layout(
        height=450,
        xaxis_title="Customer Type",
        yaxis_title="Customers"
    )


    repeat_fig.update_traces(
        textposition="outside"
    )


    st.plotly_chart(
        repeat_fig,
        use_container_width=True
    )


# ============================================================
# 4. CUSTOMER SPENDING BY CUSTOMER TYPE
# ============================================================

st.subheader("Customer Spending by Customer Type")


spending_type_columns = [
    "repeat_customer",
    "total_spent"
]


if check_required_columns(
    df,
    spending_type_columns
):

    customer_spending = df[
        [
            "repeat_customer",
            "total_spent"
        ]
    ].copy()


    customer_spending["Customer Type"] = (
        customer_spending["repeat_customer"]
        .map(
            {
                0: "One-Time Buyer",
                1: "Repeat Customer"
            }
        )
    )


    # --------------------------------------------------------
    # Check whether mapping produced valid categories
    # --------------------------------------------------------

    if customer_spending["Customer Type"].isna().any():

        st.warning(
            "Some repeat_customer values could not be mapped "
            "to the customer types defined in the notebook. "
            "Those records were excluded from this comparison."
        )


    customer_spending_valid = (
        customer_spending
        .dropna(
            subset=[
                "Customer Type",
                "total_spent"
            ]
        )
    )


    if customer_spending_valid.empty:

        st.warning(
            "No valid customer-type spending records are available."
        )

    else:

        spending_type_summary = (
            customer_spending_valid
            .groupby("Customer Type")["total_spent"]
            .agg(
                [
                    "count",
                    "mean",
                    "median",
                    "min",
                    "max"
                ]
            )
            .reset_index()
        )


        spending_type_summary.columns = [
            "Customer Type",
            "Customers",
            "Average Spending",
            "Median Spending",
            "Minimum Spending",
            "Maximum Spending"
        ]


        st.dataframe(
            spending_type_summary,
            use_container_width=True,
            hide_index=True
        )


        spending_type_fig = px.box(
            customer_spending_valid,
            x="Customer Type",
            y="total_spent",
            points=False,
            title="Customer Spending by Customer Type"
        )


        spending_type_fig.update_layout(
            height=500,
            xaxis_title="Customer Type",
            yaxis_title="Total Spending"
        )


        st.plotly_chart(
            spending_type_fig,
            use_container_width=True
        )


# ============================================================
# 5. CUSTOMER VALUE TIER DISTRIBUTION
# ============================================================

st.subheader("Customer Value Tier Distribution")


if check_required_columns(
    df,
    ["customer_value_tier"]
):

    tier_counts = (
        df["customer_value_tier"]
        .value_counts()
    )


    if tier_counts.empty:

        st.warning(
            "No customer value tier values are available."
        )

    else:

        tier_table = (
            tier_counts
            .rename("Customers")
            .reset_index()
        )


        tier_table.columns = [
            "Customer Value Tier",
            "Customers"
        ]


        tier_table["Percentage"] = (
            tier_table["Customers"]
            / len(df)
            * 100
        )


        tier_table["Percentage"] = (
            tier_table["Percentage"]
            .round(2)
        )


        st.dataframe(
            tier_table,
            use_container_width=True,
            hide_index=True
        )


        tier_fig = px.bar(
            tier_table,
            x="Customer Value Tier",
            y="Customers",
            text="Customers",
            title="Customer Value Tier Distribution"
        )


        tier_fig.update_layout(
            height=450,
            xaxis_title="Customer Value Tier",
            yaxis_title="Customers"
        )


        tier_fig.update_traces(
            textposition="outside"
        )


        st.plotly_chart(
            tier_fig,
            use_container_width=True
        )


# ============================================================
# 6. SPENDING ACROSS CUSTOMER VALUE TIERS
# ============================================================

st.subheader(
    "Spending Distribution Across Customer Value Tiers"
)


tier_spending_columns = [
    "customer_value_tier",
    "total_spent"
]


if check_required_columns(
    df,
    tier_spending_columns
):

    tier_spending = df[
        [
            "customer_value_tier",
            "total_spent"
        ]
    ].dropna()


    if tier_spending.empty:

        st.warning(
            "No valid records are available for customer "
            "value tier spending analysis."
        )

    else:

        tier_spending_summary = (
            tier_spending
            .groupby("customer_value_tier")["total_spent"]
            .agg(
                [
                    "count",
                    "mean",
                    "median",
                    "min",
                    "max"
                ]
            )
            .reset_index()
        )


        tier_spending_summary.columns = [
            "Customer Value Tier",
            "Customers",
            "Average Spending",
            "Median Spending",
            "Minimum Spending",
            "Maximum Spending"
        ]


        st.dataframe(
            tier_spending_summary,
            use_container_width=True,
            hide_index=True
        )


        tier_spending_fig = px.box(
            tier_spending,
            x="customer_value_tier",
            y="total_spent",
            points=False,
            title="Spending Distribution Across Customer Value Tiers"
        )


        tier_spending_fig.update_layout(
            height=500,
            xaxis_title="Customer Value Tier",
            yaxis_title="Total Spending"
        )


        st.plotly_chart(
            tier_spending_fig,
            use_container_width=True
        )


# ============================================================
# 7. PURCHASE BEHAVIOUR SUMMARY
# ============================================================

st.subheader("Purchase Behaviour Summary")


summary_metrics = []


if "total_orders" in df.columns:

    summary_metrics.append(
        {
            "Metric": "Average Orders per Customer",
            "Value": round(
                df["total_orders"].mean(),
                2
            )
        }
    )


if "total_items_purchased" in df.columns:

    summary_metrics.append(
        {
            "Metric": "Average Items Purchased",
            "Value": round(
                df["total_items_purchased"].mean(),
                2
            )
        }
    )


if "purchase_frequency" in df.columns:

    summary_metrics.append(
        {
            "Metric": "Average Purchase Frequency",
            "Value": round(
                df["purchase_frequency"].mean(),
                2
            )
        }
    )


if "average_order_value" in df.columns:

    summary_metrics.append(
        {
            "Metric": "Average Order Value",
            "Value": round(
                df["average_order_value"].mean(),
                2
            )
        }
    )


if summary_metrics:

    purchase_summary = pd.DataFrame(
        summary_metrics
    )


    st.dataframe(
        purchase_summary,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No additional purchase-behaviour metrics are available "
        "in the loaded dataset."
    )


# ============================================================
# 8. NOTEBOOK-SUPPORTED BUSINESS INSIGHTS
# ============================================================

st.subheader("Purchase Behaviour Insights")


st.info(
    "The EDA notebook finds that most customers have limited "
    "purchase frequency and that repeat customers represent "
    "a smaller share of the customer base."
)


st.info(
    "The notebook also identifies substantial variation in "
    "customer spending and order values."
)


# ============================================================
# DATASET PROTECTION
# ============================================================

st.caption(
    "This section only analyses customer_360.csv. "
    "No rows or source values are modified."
)
#7
# ============================================================
# DELIVERY & CUSTOMER EXPERIENCE ANALYSIS
# ============================================================

st.header("Delivery & Customer Experience")

st.caption(
    "Analysis of delivery performance, delivery delays, "
    "customer review scores and delivery experience."
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

experience_columns = [
    "average_delivery_days",
    "average_delivery_delay",
    "average_review_score",
    "on_time_delivery_rate",
    "delayed_delivery_rate"
]


available_experience_columns = []
missing_experience_columns = []
non_numeric_experience_columns = []


for column in experience_columns:

    if column not in df.columns:

        missing_experience_columns.append(column)

    elif not pd.api.types.is_numeric_dtype(df[column]):

        non_numeric_experience_columns.append(column)

    else:

        available_experience_columns.append(column)


# ============================================================
# VALIDATION
# ============================================================

validation_rows = []


for column in experience_columns:

    if column in available_experience_columns:

        validation_rows.append(
            {
                "Feature": column,
                "Status": "Available",
                "Data Type": str(df[column].dtype)
            }
        )

    elif column in missing_experience_columns:

        validation_rows.append(
            {
                "Feature": column,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    else:

        validation_rows.append(
            {
                "Feature": column,
                "Status": "Non-Numeric — Skipped",
                "Data Type": str(df[column].dtype)
            }
        )


experience_validation = pd.DataFrame(
    validation_rows
)


with st.expander("View Data Validation"):

    st.dataframe(
        experience_validation,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DELIVERY METRICS
# ============================================================

delivery_metric_columns = [
    column
    for column in [
        "average_delivery_days",
        "average_delivery_delay",
        "average_review_score",
        "on_time_delivery_rate",
        "delayed_delivery_rate"
    ]
    if column in available_experience_columns
]


if delivery_metric_columns:

    metric_columns = st.columns(
        len(delivery_metric_columns)
    )


    metric_labels = {
        "average_delivery_days": "Average Delivery Days",
        "average_delivery_delay": "Average Delivery Delay",
        "average_review_score": "Average Review Score",
        "on_time_delivery_rate": "On-Time Delivery Rate",
        "delayed_delivery_rate": "Delayed Delivery Rate"
    }


    for metric_column, metric_container in zip(
        delivery_metric_columns,
        metric_columns
    ):

        value = df[metric_column].mean()


        if pd.isna(value):

            display_value = "N/A"

        elif metric_column in [
            "on_time_delivery_rate",
            "delayed_delivery_rate"
        ]:

            display_value = f"{value * 100:.2f}%"

        else:

            display_value = f"{value:.2f}"


        with metric_container:

            st.metric(
                metric_labels.get(
                    metric_column,
                    metric_column
                ),
                display_value
            )


# ============================================================
# DELIVERY DAYS DISTRIBUTION
# ============================================================

if "average_delivery_days" in available_experience_columns:

    st.subheader("Delivery Duration Distribution")


    delivery_days = (
        df["average_delivery_days"]
        .dropna()
    )


    if delivery_days.empty:

        st.warning(
            "No valid delivery-duration values are available."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Mean Delivery Days",
                f"{delivery_days.mean():.2f}"
            )


        with col2:

            st.metric(
                "Median Delivery Days",
                f"{delivery_days.median():.2f}"
            )


        delivery_days_fig = px.histogram(
            df,
            x="average_delivery_days",
            nbins=30,
            marginal="box",
            title="Distribution of Average Delivery Days"
        )


        delivery_days_fig.update_layout(
            height=500,
            xaxis_title="Average Delivery Days",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            delivery_days_fig,
            use_container_width=True
        )


# ============================================================
# DELIVERY DELAY DISTRIBUTION
# ============================================================

if "average_delivery_delay" in available_experience_columns:

    st.subheader("Delivery Delay Distribution")


    delay_data = (
        df["average_delivery_delay"]
        .dropna()
    )


    if delay_data.empty:

        st.warning(
            "No valid delivery-delay values are available."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Mean Delivery Delay",
                f"{delay_data.mean():.2f} days"
            )


        with col2:

            st.metric(
                "Median Delivery Delay",
                f"{delay_data.median():.2f} days"
            )


        delay_fig = px.histogram(
            df,
            x="average_delivery_delay",
            nbins=40,
            marginal="box",
            title="Distribution of Average Delivery Delay"
        )


        delay_fig.update_layout(
            height=500,
            xaxis_title="Average Delivery Delay (Days)",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            delay_fig,
            use_container_width=True
        )


        st.info(
            "Negative delivery-delay values are preserved exactly "
            "as recorded in the dataset. They are not converted "
            "to zero."
        )


# ============================================================
# REVIEW SCORE DISTRIBUTION
# ============================================================

if "average_review_score" in available_experience_columns:

    st.subheader("Customer Review Score Distribution")


    review_data = (
        df["average_review_score"]
        .dropna()
    )


    if review_data.empty:

        st.warning(
            "No valid review-score values are available."
        )

    else:

        review_fig = px.histogram(
            df,
            x="average_review_score",
            nbins=20,
            title="Distribution of Customer Review Scores"
        )


        review_fig.update_layout(
            height=500,
            xaxis_title="Average Review Score",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            review_fig,
            use_container_width=True
        )


# ============================================================
# ON-TIME VS DELAYED DELIVERY
# ============================================================

if (
    "on_time_delivery_rate"
    in available_experience_columns
    and
    "delayed_delivery_rate"
    in available_experience_columns
):

    st.subheader("On-Time vs Delayed Delivery")


    on_time_rate = df[
        "on_time_delivery_rate"
    ].mean()


    delayed_rate = df[
        "delayed_delivery_rate"
    ].mean()


    delivery_performance = pd.DataFrame(
        {
            "Delivery Status": [
                "On-Time",
                "Delayed"
            ],
            "Rate": [
                on_time_rate * 100,
                delayed_rate * 100
            ]
        }
    )


    delivery_performance["Rate"] = (
        delivery_performance["Rate"]
        .round(2)
    )


    st.dataframe(
        delivery_performance,
        use_container_width=True,
        hide_index=True
    )


    performance_fig = px.bar(
        delivery_performance,
        x="Delivery Status",
        y="Rate",
        text="Rate",
        title="On-Time vs Delayed Delivery Rate"
    )


    performance_fig.update_layout(
        height=450,
        xaxis_title="Delivery Status",
        yaxis_title="Rate (%)"
    )


    performance_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    st.plotly_chart(
        performance_fig,
        use_container_width=True
    )


# ============================================================
# REVIEW SCORE VS DELIVERY DELAY
# ============================================================

relationship_columns = [
    "average_delivery_delay",
    "average_review_score"
]


if all(
    column in available_experience_columns
    for column in relationship_columns
):

    st.subheader(
        "Review Score vs Delivery Delay"
    )


    relationship_data = df[
        [
            "average_delivery_delay",
            "average_review_score"
        ]
    ].dropna()


    if relationship_data.empty:

        st.warning(
            "No valid records are available for the "
            "delivery-delay and review-score relationship."
        )

    else:

        correlation_value = (
            relationship_data[
                "average_delivery_delay"
            ]
            .corr(
                relationship_data[
                    "average_review_score"
                ]
            )
        )


        st.metric(
            "Delivery Delay vs Review Score Correlation",
            f"{correlation_value:.3f}"
        )


        relationship_fig = px.scatter(
            relationship_data,
            x="average_delivery_delay",
            y="average_review_score",
            title="Review Score vs Delivery Delay",
            opacity=0.5
        )


        relationship_fig.update_layout(
            height=550,
            xaxis_title="Average Delivery Delay (Days)",
            yaxis_title="Average Review Score"
        )


        st.plotly_chart(
            relationship_fig,
            use_container_width=True
        )


        st.info(
            "The notebook reports a weak negative relationship "
            "between delivery delay and customer review score. "
            "Delivery delay alone does not fully explain "
            "customer satisfaction."
        )


# ============================================================
# DELIVERY & EXPERIENCE SUMMARY
# ============================================================

st.subheader("Delivery & Customer Experience Summary")


summary_rows = []


if "average_delivery_days" in available_experience_columns:

    summary_rows.append(
        {
            "Metric": "Average Delivery Days",
            "Value": round(
                df["average_delivery_days"].mean(),
                2
            )
        }
    )


if "average_delivery_delay" in available_experience_columns:

    summary_rows.append(
        {
            "Metric": "Average Delivery Delay",
            "Value": round(
                df["average_delivery_delay"].mean(),
                2
            )
        }
    )


if "average_review_score" in available_experience_columns:

    summary_rows.append(
        {
            "Metric": "Average Review Score",
            "Value": round(
                df["average_review_score"].mean(),
                2
            )
        }
    )


if "on_time_delivery_rate" in available_experience_columns:

    summary_rows.append(
        {
            "Metric": "On-Time Delivery Rate",
            "Value": round(
                df["on_time_delivery_rate"].mean() * 100,
                2
            )
        }
    )


if "delayed_delivery_rate" in available_experience_columns:

    summary_rows.append(
        {
            "Metric": "Delayed Delivery Rate",
            "Value": round(
                df["delayed_delivery_rate"].mean() * 100,
                2
            )
        }
    )


if summary_rows:

    experience_summary = pd.DataFrame(
        summary_rows
    )


    st.dataframe(
        experience_summary,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No delivery or customer-experience metrics "
        "are available in the dataset."
    )


# ============================================================
# NOTEBOOK-SUPPORTED OBSERVATIONS
# ============================================================

st.subheader("Customer Experience Findings")


st.info(
    "The EDA notebook finds that customers generally receive "
    "positive review scores and that most deliveries are completed "
    "on time."
)


st.info(
    "The notebook also identifies a weak negative relationship "
    "between delivery delay and review score."
)


st.caption(
    "No source rows or values are modified during this analysis."
)
#8
# ============================================================
# TIME-BASED CUSTOMER ANALYSIS
# ============================================================

st.header("Time-Based Customer Analysis")

st.caption(
    "Analysis of customer acquisition, last purchase activity, "
    "recency and customer tenure."
)


# ============================================================
# REQUIRED TIME FEATURES
# ============================================================

time_features = [
    "first_purchase_date",
    "last_purchase_date",
    "recency_days",
    "customer_tenure_days"
]


available_time_features = []
missing_time_features = []
invalid_datetime_features = []
non_numeric_time_features = []


for feature in time_features:

    if feature not in df.columns:

        missing_time_features.append(feature)

        continue


    if feature in [
        "first_purchase_date",
        "last_purchase_date"
    ]:

        if pd.api.types.is_datetime64_any_dtype(
            df[feature]
        ):

            available_time_features.append(feature)

        else:

            invalid_datetime_features.append(feature)

    else:

        if pd.api.types.is_numeric_dtype(
            df[feature]
        ):

            available_time_features.append(feature)

        else:

            non_numeric_time_features.append(feature)


# ============================================================
# VALIDATION
# ============================================================

validation_rows = []


for feature in time_features:

    if feature in available_time_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Available",
                "Data Type": str(df[feature].dtype)
            }
        )

    elif feature in missing_time_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    elif feature in invalid_datetime_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Not Datetime — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )

    else:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Non-Numeric — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )


time_validation = pd.DataFrame(
    validation_rows
)


with st.expander("View Time Feature Validation"):

    st.dataframe(
        time_validation,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MONTHLY CUSTOMER ACQUISITION
# ============================================================

if "first_purchase_date" in available_time_features:

    st.subheader(
        "Monthly Customer Acquisition Trend"
    )


    acquisition_data = df[
        ["first_purchase_date"]
    ].dropna().copy()


    if acquisition_data.empty:

        st.warning(
            "No valid first_purchase_date values are available."
        )

    else:

        monthly_customers = (
            acquisition_data
            .groupby(
                acquisition_data[
                    "first_purchase_date"
                ].dt.to_period("M")
            )
            .size()
            .reset_index(
                name="customers"
            )
        )


        monthly_customers[
            "first_purchase_date"
        ] = (
            monthly_customers[
                "first_purchase_date"
            ]
            .astype(str)
        )


        acquisition_fig = px.line(
            monthly_customers,
            x="first_purchase_date",
            y="customers",
            markers=True,
            title="Monthly Customer Acquisition Trend"
        )


        acquisition_fig.update_layout(
            height=500,
            xaxis_title="Month",
            yaxis_title="Customers"
        )


        st.plotly_chart(
            acquisition_fig,
            use_container_width=True
        )


# ============================================================
# MONTHLY LAST PURCHASE
# ============================================================

if "last_purchase_date" in available_time_features:

    st.subheader(
        "Monthly Last Purchase Trend"
    )


    last_purchase_data = df[
        ["last_purchase_date"]
    ].dropna().copy()


    if last_purchase_data.empty:

        st.warning(
            "No valid last_purchase_date values are available."
        )

    else:

        monthly_last_purchase = (
            last_purchase_data
            .groupby(
                last_purchase_data[
                    "last_purchase_date"
                ].dt.to_period("M")
            )
            .size()
            .reset_index(
                name="customers"
            )
        )


        monthly_last_purchase[
            "last_purchase_date"
        ] = (
            monthly_last_purchase[
                "last_purchase_date"
            ]
            .astype(str)
        )


        last_purchase_fig = px.line(
            monthly_last_purchase,
            x="last_purchase_date",
            y="customers",
            markers=True,
            title="Monthly Last Purchase Trend"
        )


        last_purchase_fig.update_layout(
            height=500,
            xaxis_title="Month",
            yaxis_title="Customers"
        )


        st.plotly_chart(
            last_purchase_fig,
            use_container_width=True
        )


# ============================================================
# RECENCY DISTRIBUTION
# ============================================================

if "recency_days" in available_time_features:

    st.subheader(
        "Customer Recency Distribution"
    )


    recency_data = (
        df["recency_days"]
        .dropna()
    )


    if recency_data.empty:

        st.warning(
            "No valid recency_days values are available."
        )

    else:

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Recency",
                f"{recency_data.mean():.2f} days"
            )


        with col2:

            st.metric(
                "Median Recency",
                f"{recency_data.median():.2f} days"
            )


        with col3:

            st.metric(
                "Maximum Recency",
                f"{recency_data.max():.0f} days"
            )


        recency_fig = px.histogram(
            df,
            x="recency_days",
            nbins=40,
            marginal="box",
            title="Distribution of Customer Recency"
        )


        recency_fig.update_layout(
            height=500,
            xaxis_title="Recency (Days)",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            recency_fig,
            use_container_width=True
        )


# ============================================================
# CUSTOMER TENURE DISTRIBUTION
# ============================================================

if "customer_tenure_days" in available_time_features:

    st.subheader(
        "Customer Tenure Distribution"
    )


    tenure_data = (
        df["customer_tenure_days"]
        .dropna()
    )


    if tenure_data.empty:

        st.warning(
            "No valid customer_tenure_days values are available."
        )

    else:

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Tenure",
                f"{tenure_data.mean():.2f} days"
            )


        with col2:

            st.metric(
                "Median Tenure",
                f"{tenure_data.median():.2f} days"
            )


        with col3:

            st.metric(
                "Maximum Tenure",
                f"{tenure_data.max():.0f} days"
            )


        tenure_fig = px.histogram(
            df,
            x="customer_tenure_days",
            nbins=40,
            marginal="box",
            title="Distribution of Customer Tenure"
        )


        tenure_fig.update_layout(
            height=500,
            xaxis_title="Customer Tenure (Days)",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            tenure_fig,
            use_container_width=True
        )


# ============================================================
# CUSTOMER TENURE VS RECENCY
# ============================================================

if (
    "customer_tenure_days" in available_time_features
    and
    "recency_days" in available_time_features
):

    st.subheader(
        "Customer Tenure vs Recency"
    )


    tenure_recency_data = df[
        [
            "customer_tenure_days",
            "recency_days"
        ]
    ].dropna()


    if tenure_recency_data.empty:

        st.warning(
            "No valid records are available for "
            "tenure vs recency analysis."
        )

    else:

        tenure_recency_fig = px.density_heatmap(
            tenure_recency_data,
            x="customer_tenure_days",
            y="recency_days",
            nbinsx=30,
            nbinsy=30,
            title="Customer Tenure vs Recency"
        )


        tenure_recency_fig.update_layout(
            height=600,
            xaxis_title="Customer Tenure (Days)",
            yaxis_title="Recency (Days)"
        )


        st.plotly_chart(
            tenure_recency_fig,
            use_container_width=True
        )


# ============================================================
# FIRST AND LAST PURCHASE RANGE
# ============================================================

if (
    "first_purchase_date" in available_time_features
    and
    "last_purchase_date" in available_time_features
):

    st.subheader(
        "Purchase Date Range"
    )


    first_dates = (
        df["first_purchase_date"]
        .dropna()
    )


    last_dates = (
        df["last_purchase_date"]
        .dropna()
    )


    if not first_dates.empty:

        st.write(
            f"First recorded customer purchase: "
            f"{first_dates.min()}"
        )


    if not last_dates.empty:

        st.write(
            f"Latest recorded customer purchase: "
            f"{last_dates.max()}"
        )


# ============================================================
# RECENCY AND TENURE SUMMARY
# ============================================================

st.subheader(
    "Time-Based Customer Summary"
)


summary_rows = []


if "recency_days" in available_time_features:

    summary_rows.append(
        {
            "Metric": "Average Recency (Days)",
            "Value": round(
                df["recency_days"].mean(),
                2
            )
        }
    )


if "customer_tenure_days" in available_time_features:

    summary_rows.append(
        {
            "Metric": "Average Customer Tenure (Days)",
            "Value": round(
                df["customer_tenure_days"].mean(),
                2
            )
        }
    )


if "first_purchase_date" in available_time_features:

    summary_rows.append(
        {
            "Metric": "Earliest First Purchase",
            "Value": str(
                df["first_purchase_date"].min()
            )
        }
    )


if "last_purchase_date" in available_time_features:

    summary_rows.append(
        {
            "Metric": "Latest Last Purchase",
            "Value": str(
                df["last_purchase_date"].max()
            )
        }
    )


if summary_rows:

    time_summary = pd.DataFrame(
        summary_rows
    )


    st.dataframe(
        time_summary,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No valid time-based features are available."
    )


# ============================================================
# NOTEBOOK-SUPPORTED OBSERVATION
# ============================================================

if (
    "recency_days" in available_time_features
    and
    "customer_tenure_days" in available_time_features
):

    st.info(
        "The time-based analysis compares customer recency "
        "with customer tenure to understand the relationship "
        "between customer history and recent purchasing activity."
    )


# ============================================================
# DATA PROTECTION
# ============================================================

st.caption(
    "No source rows or values are modified during this analysis."
)
#9
# ============================================================
# FEATURE RELATIONSHIP ANALYSIS
# ============================================================

st.header("Feature Relationship Analysis")

st.caption(
    "Understanding relationships between customer behaviour, "
    "purchase patterns, customer value and customer experience."
)


# ============================================================
# REQUIRED FEATURES
# ============================================================

relationship_features = [
    "total_orders",
    "total_spent",
    "average_order_value",
    "customer_value_tier",
    "average_review_score",
    "average_delivery_delay"
]


available_relationship_features = []
missing_relationship_features = []
invalid_relationship_features = []


for feature in relationship_features:

    if feature not in df.columns:

        missing_relationship_features.append(feature)

        continue


    if feature in [
        "total_orders",
        "total_spent",
        "average_order_value",
        "average_review_score",
        "average_delivery_delay"
    ]:

        if pd.api.types.is_numeric_dtype(
            df[feature]
        ):

            available_relationship_features.append(
                feature
            )

        else:

            invalid_relationship_features.append(
                feature
            )

    else:

        available_relationship_features.append(
            feature
        )


# ============================================================
# FEATURE VALIDATION
# ============================================================

validation_rows = []


for feature in relationship_features:

    if feature in available_relationship_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Available",
                "Data Type": str(df[feature].dtype)
            }
        )

    elif feature in missing_relationship_features:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    else:

        validation_rows.append(
            {
                "Feature": feature,
                "Status": "Invalid Data Type — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )


relationship_validation = pd.DataFrame(
    validation_rows
)


with st.expander("View Feature Validation"):

    st.dataframe(
        relationship_validation,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TOTAL ORDERS VS TOTAL SPENDING
# ============================================================

if (
    "total_orders" in available_relationship_features
    and
    "total_spent" in available_relationship_features
):

    st.subheader(
        "Order Behaviour vs Total Spending"
    )


    orders_spending_data = df[
        [
            "total_orders",
            "total_spent"
        ]
    ].dropna()


    if orders_spending_data.empty:

        st.warning(
            "No valid records are available for "
            "order behaviour vs spending analysis."
        )

    else:

        orders_spending_correlation = (
            orders_spending_data[
                "total_orders"
            ]
            .corr(
                orders_spending_data[
                    "total_spent"
                ]
            )
        )


        st.metric(
            "Correlation",
            f"{orders_spending_correlation:.3f}"
        )


        orders_spending_fig = px.density_heatmap(
            orders_spending_data,
            x="total_orders",
            y="total_spent",
            nbinsx=20,
            nbinsy=30,
            title=(
                "Relationship Between Order Frequency "
                "and Total Spending"
            )
        )


        orders_spending_fig.update_layout(
            height=550,
            xaxis_title="Total Orders",
            yaxis_title="Total Spending"
        )


        st.plotly_chart(
            orders_spending_fig,
            use_container_width=True
        )


# ============================================================
# PURCHASE FEATURE CORRELATION
# ============================================================

purchase_features = [
    "total_orders",
    "total_spent",
    "average_order_value"
]


available_purchase_features = [
    feature
    for feature in purchase_features
    if feature in available_relationship_features
]


if len(available_purchase_features) >= 2:

    st.subheader(
        "Purchase Behaviour Feature Correlation"
    )


    purchase_corr = (
        df[
            available_purchase_features
        ]
        .corr()
    )


    st.dataframe(
        purchase_corr.round(3),
        use_container_width=True
    )


    purchase_corr_fig = px.imshow(
        purchase_corr,
        text_auto=".2f",
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        title="Purchase Behaviour Feature Correlation"
    )


    purchase_corr_fig.update_layout(
        height=500,
        xaxis_title="Features",
        yaxis_title="Features"
    )


    st.plotly_chart(
        purchase_corr_fig,
        use_container_width=True
    )


elif len(available_purchase_features) == 1:

    st.warning(
        "Only one purchase feature is available. "
        "Correlation analysis requires at least two features."
    )


# ============================================================
# CUSTOMER VALUE TIER VS TOTAL SPENDING
# ============================================================

if (
    "customer_value_tier"
    in available_relationship_features
    and
    "total_spent"
    in available_relationship_features
):

    st.subheader(
        "Customer Value Tier vs Spending"
    )


    tier_spending_data = df[
        [
            "customer_value_tier",
            "total_spent"
        ]
    ].dropna()


    if tier_spending_data.empty:

        st.warning(
            "No valid records are available for "
            "customer value tier spending analysis."
        )

    else:

        tier_spending_fig = px.box(
            tier_spending_data,
            x="customer_value_tier",
            y="total_spent",
            title=(
                "Spending Distribution Across "
                "Customer Value Tiers"
            )
        )


        tier_spending_fig.update_layout(
            height=550,
            xaxis_title="Customer Value Tier",
            yaxis_title="Total Spending"
        )


        st.plotly_chart(
            tier_spending_fig,
            use_container_width=True
        )


# ============================================================
# AVERAGE ORDER VALUE VS TOTAL SPENDING
# ============================================================

if (
    "average_order_value"
    in available_relationship_features
    and
    "total_spent"
    in available_relationship_features
):

    st.subheader(
        "Average Order Value vs Total Spending"
    )


    aov_spending_data = df[
        [
            "average_order_value",
            "total_spent"
        ]
    ].dropna()


    if aov_spending_data.empty:

        st.warning(
            "No valid records are available for "
            "AOV vs total spending analysis."
        )

    else:

        aov_spending_correlation = (
            aov_spending_data[
                "average_order_value"
            ]
            .corr(
                aov_spending_data[
                    "total_spent"
                ]
            )
        )


        st.metric(
            "Correlation",
            f"{aov_spending_correlation:.3f}"
        )


        aov_spending_fig = px.density_heatmap(
            aov_spending_data,
            x="average_order_value",
            y="total_spent",
            nbinsx=30,
            nbinsy=30,
            title=(
                "Relationship Between Average Order Value "
                "and Total Spending"
            )
        )


        aov_spending_fig.update_layout(
            height=550,
            xaxis_title="Average Order Value",
            yaxis_title="Total Spending"
        )


        st.plotly_chart(
            aov_spending_fig,
            use_container_width=True
        )


# ============================================================
# AVERAGE REVIEW SCORE DISTRIBUTION
# ============================================================

if (
    "average_review_score"
    in available_relationship_features
):

    st.subheader(
        "Average Customer Review Score"
    )


    review_data = (
        df[
            "average_review_score"
        ]
        .dropna()
    )


    if review_data.empty:

        st.warning(
            "No valid review-score values are available."
        )

    else:

        review_fig = px.histogram(
            df,
            x="average_review_score",
            nbins=20,
            title=(
                "Distribution of Average Customer "
                "Review Score"
            )
        )


        review_fig.update_layout(
            height=500,
            xaxis_title="Average Review Score",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            review_fig,
            use_container_width=True
        )


# ============================================================
# DELIVERY DELAY VS REVIEW SCORE
# ============================================================

if (
    "average_delivery_delay"
    in available_relationship_features
    and
    "average_review_score"
    in available_relationship_features
):

    st.subheader(
        "Delivery Delay vs Review Score"
    )


    delivery_review_data = df[
        [
            "average_delivery_delay",
            "average_review_score"
        ]
    ].dropna()


    if delivery_review_data.empty:

        st.warning(
            "No valid records are available for "
            "delivery delay vs review score analysis."
        )

    else:

        delivery_review_correlation = (
            delivery_review_data[
                "average_delivery_delay"
            ]
            .corr(
                delivery_review_data[
                    "average_review_score"
                ]
            )
        )


        st.metric(
            "Correlation",
            f"{delivery_review_correlation:.3f}"
        )


        delivery_review_fig = px.density_heatmap(
            delivery_review_data,
            x="average_delivery_delay",
            y="average_review_score",
            nbinsx=35,
            nbinsy=20,
            title=(
                "Relationship Between Delivery Delay "
                "and Review Score"
            )
        )


        delivery_review_fig.update_layout(
            height=550,
            xaxis_title="Average Delivery Delay",
            yaxis_title="Average Review Score"
        )


        st.plotly_chart(
            delivery_review_fig,
            use_container_width=True
        )


        st.info(
            "Negative delivery-delay values are preserved "
            "exactly as recorded in the dataset."
        )


# ============================================================
# RELATIONSHIP SUMMARY
# ============================================================

st.subheader(
    "Feature Relationship Summary"
)


relationship_summary = []


if (
    "total_orders" in available_relationship_features
    and
    "total_spent" in available_relationship_features
):

    relationship_summary.append(
        {
            "Relationship":
                "Total Orders vs Total Spending",
            "Correlation":
                round(
                    df[
                        [
                            "total_orders",
                            "total_spent"
                        ]
                    ]
                    .corr()
                    .loc[
                        "total_orders",
                        "total_spent"
                    ],
                    3
                )
        }
    )


if (
    "average_order_value"
    in available_relationship_features
    and
    "total_spent"
    in available_relationship_features
):

    relationship_summary.append(
        {
            "Relationship":
                "Average Order Value vs Total Spending",
            "Correlation":
                round(
                    df[
                        [
                            "average_order_value",
                            "total_spent"
                        ]
                    ]
                    .corr()
                    .loc[
                        "average_order_value",
                        "total_spent"
                    ],
                    3
                )
        }
    )


if (
    "average_delivery_delay"
    in available_relationship_features
    and
    "average_review_score"
    in available_relationship_features
):

    relationship_summary.append(
        {
            "Relationship":
                "Delivery Delay vs Review Score",
            "Correlation":
                round(
                    df[
                        [
                            "average_delivery_delay",
                            "average_review_score"
                        ]
                    ]
                    .corr()
                    .loc[
                        "average_delivery_delay",
                        "average_review_score"
                    ],
                    3
                )
        }
    )


if relationship_summary:

    relationship_summary_df = pd.DataFrame(
        relationship_summary
    )


    st.dataframe(
        relationship_summary_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No valid feature relationships could be calculated "
        "from the available dataset."
    )


st.caption(
    "All relationships are calculated from the loaded "
    "customer_360 dataset. No source data is modified."
)
#10
import numpy as np


# ============================================================
# CUSTOMER SEGMENTATION ANALYSIS
# ============================================================

st.header("Customer Segmentation Analysis")

st.caption(
    "Customer segmentation based on purchasing behaviour "
    "and spending patterns."
)


# ============================================================
# SEGMENTATION FEATURE VALIDATION
# ============================================================

segmentation_features = [
    "total_orders",
    "total_spent",
    "average_order_value"
]

segment_validation_rows = []

available_segmentation_features = []
missing_segmentation_features = []
invalid_segmentation_features = []


for feature in segmentation_features:

    if feature not in df.columns:

        missing_segmentation_features.append(feature)

        segment_validation_rows.append(
            {
                "Feature": feature,
                "Status": "Missing — Skipped",
                "Data Type": "Not Available"
            }
        )

    elif not pd.api.types.is_numeric_dtype(
        df[feature]
    ):

        invalid_segmentation_features.append(feature)

        segment_validation_rows.append(
            {
                "Feature": feature,
                "Status": "Non-Numeric — Skipped",
                "Data Type": str(df[feature].dtype)
            }
        )

    else:

        available_segmentation_features.append(
            feature
        )

        segment_validation_rows.append(
            {
                "Feature": feature,
                "Status": "Available",
                "Data Type": str(df[feature].dtype)
            }
        )


# ============================================================
# SEGMENTATION FEATURE VALIDATION DISPLAY
# ============================================================

with st.expander("View Segmentation Feature Validation"):

    st.dataframe(
        pd.DataFrame(segment_validation_rows),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SEGMENTATION DATASET
# ============================================================

if len(available_segmentation_features) == 3:

    segmentation_df = df[
        [
            "total_orders",
            "total_spent",
            "average_order_value"
        ]
    ].copy()


    # ========================================================
    # SEGMENTATION FEATURE SUMMARY
    # ========================================================

    st.subheader(
        "Segmentation Feature Summary"
    )


    st.dataframe(
        segmentation_df.describe().round(2),
        use_container_width=True
    )


    # ========================================================
    # CUSTOMER SPENDING DISTRIBUTION — LOG SCALE
    # ========================================================

    st.subheader(
        "Customer Spending Distribution"
    )


    spending_data = (
        segmentation_df[
            "total_spent"
        ]
        .dropna()
    )


    if spending_data.empty:

        st.warning(
            "No valid total_spent values are available."
        )

    else:

        log_spending = np.log1p(
            spending_data
        )


        spending_log_df = pd.DataFrame(
            {
                "Log Total Spending": log_spending
            }
        )


        spending_fig = px.histogram(
            spending_log_df,
            x="Log Total Spending",
            nbins=40,
            marginal="box",
            title="Distribution of Customer Spending (Log Scale)"
        )


        spending_fig.update_layout(
            height=500,
            xaxis_title="Log(Total Spending + 1)",
            yaxis_title="Number of Customers"
        )


        st.plotly_chart(
            spending_fig,
            use_container_width=True,
            key="segmentation_spending_distribution"
        )


    # ========================================================
    # CUSTOMER ORDER FREQUENCY GROUPS
    # ========================================================

    st.subheader(
        "Customer Distribution by Order Frequency"
    )


    order_group = pd.cut(
        segmentation_df[
            "total_orders"
        ],
        bins=[
            0,
            1,
            2,
            5,
            np.inf
        ],
        labels=[
            "Single Order",
            "2 Orders",
            "3-5 Orders",
            "5+ Orders"
        ]
    )


    order_group_count = (
        order_group
        .value_counts(
            sort=False,
            dropna=False
        )
        .reset_index()
    )


    order_group_count.columns = [
        "Order Group",
        "Customer Count"
    ]


    st.dataframe(
        order_group_count,
        use_container_width=True,
        hide_index=True
    )


    order_group_fig = px.bar(
        order_group_count,
        x="Order Group",
        y="Customer Count",
        title="Customer Distribution by Order Frequency Groups"
    )


    order_group_fig.update_layout(
        height=500,
        xaxis_title="Order Frequency Group",
        yaxis_title="Number of Customers"
    )


    st.plotly_chart(
        order_group_fig,
        use_container_width=True,
        key="segmentation_order_frequency"
    )


    # ========================================================
    # SPENDING-BASED CUSTOMER SEGMENTS
    # ========================================================

    st.subheader(
        "Spending-Based Customer Segments"
    )


    # Exact segmentation logic
    spending_segment = pd.qcut(
        segmentation_df[
            "total_spent"
        ],
        q=3,
        labels=[
            "Low Value",
            "Medium Value",
            "High Value"
        ],
        duplicates="drop"
    )


    segmentation_df[
        "spending_segment"
    ] = spending_segment


    segment_distribution = (
        segmentation_df[
            "spending_segment"
        ]
        .value_counts(
            sort=False,
            dropna=False
        )
        .reset_index()
    )


    segment_distribution.columns = [
        "Customer Segment",
        "Customer Count"
    ]


    st.dataframe(
        segment_distribution,
        use_container_width=True,
        hide_index=True
    )


    segment_distribution_fig = px.bar(
        segment_distribution,
        x="Customer Segment",
        y="Customer Count",
        title="Customer Distribution Across Spending Segments"
    )


    segment_distribution_fig.update_layout(
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers"
    )


    st.plotly_chart(
        segment_distribution_fig,
        use_container_width=True,
        key="segmentation_spending_segment_distribution"
    )


    # ========================================================
    # SEGMENT-WISE SPENDING
    # ========================================================

    st.subheader(
        "Average Spending Across Customer Segments"
    )


    segment_spending = (
        segmentation_df
        .groupby(
            "spending_segment",
            observed=False
        )[
            "total_spent"
        ]
        .mean()
        .reset_index()
    )


    segment_spending.columns = [
        "Customer Segment",
        "Average Total Spending"
    ]


    st.dataframe(
        segment_spending.round(2),
        use_container_width=True,
        hide_index=True
    )


    segment_spending_fig = px.bar(
        segment_spending,
        x="Customer Segment",
        y="Average Total Spending",
        title="Average Spending Across Customer Segments"
    )


    segment_spending_fig.update_layout(
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Average Total Spending"
    )


    st.plotly_chart(
        segment_spending_fig,
        use_container_width=True,
        key="segmentation_average_spending"
    )


    # ========================================================
    # SEGMENT-WISE ORDER FREQUENCY
    # ========================================================

    st.subheader(
        "Average Order Frequency Across Customer Segments"
    )


    segment_orders = (
        segmentation_df
        .groupby(
            "spending_segment",
            observed=False
        )[
            "total_orders"
        ]
        .mean()
        .reset_index()
    )


    segment_orders.columns = [
        "Customer Segment",
        "Average Number of Orders"
    ]


    st.dataframe(
        segment_orders.round(2),
        use_container_width=True,
        hide_index=True
    )


    segment_orders_fig = px.bar(
        segment_orders,
        x="Customer Segment",
        y="Average Number of Orders",
        title="Average Order Frequency Across Customer Segments"
    )


    segment_orders_fig.update_layout(
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Average Number of Orders"
    )


    st.plotly_chart(
        segment_orders_fig,
        use_container_width=True,
        key="segmentation_average_order_frequency"
    )


    # ========================================================
    # CUSTOMER SEGMENT PROFILING
    # ========================================================

    st.subheader(
        "Customer Segment Profile"
    )


    profile_features = [
        "total_orders",
        "total_spent",
        "average_order_value",
        "average_review_score"
    ]


    profile_available = [
        feature
        for feature in profile_features
        if feature in df.columns
        and pd.api.types.is_numeric_dtype(
            df[feature]
        )
    ]


    if len(profile_available) == len(
        profile_features
    ):

        profile_source = df[
            profile_features
        ].copy()


        profile_source[
            "spending_segment"
        ] = spending_segment


        segment_profile = (
            profile_source
            .groupby(
                "spending_segment",
                observed=False
            )[
                profile_features
            ]
            .mean()
            .reset_index()
        )


        st.dataframe(
            segment_profile.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:

        missing_profile_features = [
            feature
            for feature in profile_features
            if feature not in df.columns
            or not pd.api.types.is_numeric_dtype(
                df[feature]
            )
        ]


        st.warning(
            "Segment profiling was skipped because "
            "these notebook-required features are unavailable: "
            + ", ".join(
                missing_profile_features
            )
        )


    # ========================================================
    # SEGMENT-WISE SPENDING & ORDER COMPARISON
    # ========================================================

    st.subheader(
        "Purchase Behaviour Comparison Across Customer Segments"
    )


    segment_comparison = (
        segmentation_df
        .groupby(
            "spending_segment",
            observed=False
        )[
            [
                "total_spent",
                "total_orders"
            ]
        ]
        .mean()
        .reset_index()
    )


    segment_comparison_melted = (
        segment_comparison
        .melt(
            id_vars="spending_segment",
            value_vars=[
                "total_spent",
                "total_orders"
            ],
            var_name="Metric",
            value_name="Average Value"
        )
    )


    comparison_fig = px.bar(
        segment_comparison_melted,
        x="spending_segment",
        y="Average Value",
        color="Metric",
        barmode="group",
        title="Purchase Behaviour Comparison Across Customer Segments"
    )


    comparison_fig.update_layout(
        height=550,
        xaxis_title="Customer Segment",
        yaxis_title="Average Value"
    )


    st.plotly_chart(
        comparison_fig,
        use_container_width=True,
        key="segmentation_purchase_behaviour_comparison"
    )


    # ========================================================
    # SEGMENT DISTRIBUTION PERCENTAGE
    # ========================================================

    st.subheader(
        "Customer Segment Distribution Percentage"
    )


    segment_count = (
        segmentation_df[
            "spending_segment"
        ]
        .value_counts(
            sort=False,
            dropna=False
        )
        .reset_index()
    )


    segment_count.columns = [
        "Customer Segment",
        "Customer Count"
    ]


    total_segment_customers = (
        segment_count[
            "Customer Count"
        ].sum()
    )


    if total_segment_customers > 0:

        segment_count[
            "Percentage"
        ] = (
            segment_count[
                "Customer Count"
            ]
            /
            total_segment_customers
        ) * 100


        segment_count[
            "Percentage"
        ] = segment_count[
            "Percentage"
        ].round(2)

    else:

        segment_count[
            "Percentage"
        ] = 0.0


    st.dataframe(
        segment_count,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # CUSTOMER COUNT ACROSS SEGMENTS
    # ========================================================

    segment_count_fig = px.bar(
        segment_count,
        x="Customer Segment",
        y="Customer Count",
        title="Customer Distribution Across Spending Segments"
    )


    segment_count_fig.update_layout(
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers"
    )


    st.plotly_chart(
        segment_count_fig,
        use_container_width=True,
        key="segmentation_customer_count_distribution"
    )


    # ========================================================
    # FINAL SEGMENT PROFILE
    # ========================================================

    st.subheader(
        "Final Customer Segment Profile"
    )


    final_profile_features = [
        "customer_unique_id",
        "total_orders",
        "total_spent",
        "average_order_value",
        "average_review_score"
    ]


    final_profile_missing = [
        feature
        for feature in final_profile_features
        if feature not in df.columns
    ]


    final_profile_numeric = [
        "total_orders",
        "total_spent",
        "average_order_value",
        "average_review_score"
    ]


    final_profile_invalid = [
        feature
        for feature in final_profile_numeric
        if feature not in df.columns
        or not pd.api.types.is_numeric_dtype(
            df[feature]
        )
    ]


    if (
        not final_profile_missing
        and
        not final_profile_invalid
    ):

        final_profile_source = df[
            final_profile_features
        ].copy()


        final_profile_source[
            "spending_segment"
        ] = spending_segment


        final_segment_profile = (
            final_profile_source
            .groupby(
                "spending_segment",
                observed=False
            )
            .agg(
                customers=(
                    "customer_unique_id",
                    "count"
                ),
                avg_orders=(
                    "total_orders",
                    "mean"
                ),
                avg_spending=(
                    "total_spent",
                    "mean"
                ),
                avg_order_value=(
                    "average_order_value",
                    "mean"
                ),
                avg_review_score=(
                    "average_review_score",
                    "mean"
                )
            )
            .reset_index()
        )


        st.dataframe(
            final_segment_profile.round(2),
            use_container_width=True,
            hide_index=True
        )


    else:

        problems = (
            final_profile_missing
            +
            final_profile_invalid
        )


        st.warning(
            "Final segment profile was skipped because "
            "required notebook features are unavailable: "
            + ", ".join(
                problems
            )
        )


else:

    st.warning(
        "Customer segmentation could not be performed because "
        "the exact required segmentation features "
        "(total_orders, total_spent and average_order_value) "
        "are not all available as numeric columns."
    )


# ============================================================
# SOURCE DATA PROTECTION
# ============================================================

st.caption(
    "The segmentation analysis uses a temporary in-memory "
    "spending_segment column. The source customer_360.csv "
    "is not overwritten."
)
#11
# ============================================================
# EDA SUMMARY & KEY BUSINESS INSIGHTS
# ============================================================

st.header("EDA Summary & Key Business Insights")

st.caption(
    "Summary of the findings produced from the Exploratory "
    "Data Analysis."
)


# ============================================================
# DATASET REFERENCE
# ============================================================
# The EDA dataset is already loaded earlier in the page as df.
# Use df consistently throughout the EDA page.
# No second dataset is created here.

if "df" not in globals():

    st.error(
        "The EDA dataset is not loaded. "
        "Please make sure customer_360.csv is loaded before "
        "the EDA sections."
    )

else:

    customer_360 = df


    # ========================================================
    # DATASET SUMMARY
    # ========================================================

    st.subheader("Dataset Summary")


    dataset_summary = pd.DataFrame(
        {
            "Metric": [
                "Total Customers / Rows",
                "Total Features",
                "Missing Values",
                "Duplicate Rows"
            ],
            "Value": [
                customer_360.shape[0],
                customer_360.shape[1],
                int(
                    customer_360.isnull()
                    .sum()
                    .sum()
                ),
                int(
                    customer_360.duplicated()
                    .sum()
                )
            ]
        }
    )


    st.dataframe(
        dataset_summary,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DATASET VALIDATION STATUS
    # ========================================================

    st.subheader("Dataset Validation")


    missing_values_count = int(
        customer_360.isnull()
        .sum()
        .sum()
    )


    duplicate_rows_count = int(
        customer_360.duplicated()
        .sum()
    )


    if (
        missing_values_count == 0
        and
        duplicate_rows_count == 0
    ):

        st.success(
            "No missing values and no duplicate rows "
            "were detected in the loaded EDA dataset."
        )

    else:

        if missing_values_count > 0:

            st.warning(
                f"{missing_values_count} missing values "
                "were detected in the loaded dataset."
            )


        if duplicate_rows_count > 0:

            st.warning(
                f"{duplicate_rows_count} duplicate rows "
                "were detected in the loaded dataset."
            )


    # ========================================================
    # IMPORTANT CUSTOMER METRICS
    # ========================================================

    st.subheader(
        "Important Customer Metrics Summary"
    )


    metric_columns = [
        "total_orders",
        "total_spent",
        "average_order_value",
        "average_review_score",
        "average_delivery_days"
    ]


    available_metric_columns = [
        column
        for column in metric_columns
        if column in customer_360.columns
    ]


    missing_metric_columns = [
        column
        for column in metric_columns
        if column not in customer_360.columns
    ]


    if missing_metric_columns:

        st.info(
            "The following notebook features are not available "
            "in the loaded dataset and are therefore skipped: "
            + ", ".join(missing_metric_columns)
        )


    metric_rows = []


    for column in available_metric_columns:

        if not pd.api.types.is_numeric_dtype(
            customer_360[column]
        ):

            continue


        metric_labels = {
            "total_orders":
                "Average Orders per Customer",

            "total_spent":
                "Average Customer Spending",

            "average_order_value":
                "Average Order Value",

            "average_review_score":
                "Average Review Score",

            "average_delivery_days":
                "Average Delivery Days"
        }


        metric_rows.append(
            {
                "Metric": metric_labels.get(
                    column,
                    column
                ),
                "Value": round(
                    customer_360[column].mean(),
                    2
                )
            }
        )


    if metric_rows:

        key_metrics = pd.DataFrame(
            metric_rows
        )


        st.dataframe(
            key_metrics,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No valid numerical customer metrics "
            "are available."
        )


    # ========================================================
    # CUSTOMER ORDER BEHAVIOUR
    # ========================================================

    st.subheader(
        "Customer Order Behaviour Summary"
    )


    if "total_orders" not in customer_360.columns:

        st.warning(
            "The notebook feature 'total_orders' "
            "is not available in the loaded dataset."
        )

    elif not pd.api.types.is_numeric_dtype(
        customer_360["total_orders"]
    ):

        st.warning(
            "The 'total_orders' feature is not numeric. "
            "Order behaviour analysis is skipped."
        )

    else:

        order_data = customer_360[
            "total_orders"
        ].dropna()


        if order_data.empty:

            st.warning(
                "No valid total_orders values are available."
            )

        else:

            single_order_count = int(
                (order_data == 1).sum()
            )


            repeat_customer_count = int(
                (order_data > 1).sum()
            )


            order_summary = pd.DataFrame(
                {
                    "Category": [
                        "Single Order Customers",
                        "Repeat Customers"
                    ],
                    "Customer Count": [
                        single_order_count,
                        repeat_customer_count
                    ]
                }
            )


            st.dataframe(
                order_summary,
                use_container_width=True,
                hide_index=True
            )


            order_summary_fig = px.bar(
                order_summary,
                x="Category",
                y="Customer Count",
                title=(
                    "Customer Distribution by "
                    "Purchase Frequency"
                ),
                text="Customer Count"
            )


            order_summary_fig.update_layout(
                height=500,
                xaxis_title="Customer Type",
                yaxis_title="Number of Customers"
            )


            st.plotly_chart(
                order_summary_fig,
                use_container_width=True,
                key="eda_summary_customer_order_behaviour"
            )


    # ========================================================
    # PURCHASE BEHAVIOUR SUMMARY
    # ========================================================

    st.subheader(
        "Purchase Behaviour Summary"
    )


    purchase_columns = [
        "total_orders",
        "total_spent",
        "average_order_value"
    ]


    available_purchase_columns = [
        column
        for column in purchase_columns
        if column in customer_360.columns
        and pd.api.types.is_numeric_dtype(
            customer_360[column]
        )
    ]


    missing_purchase_columns = [
        column
        for column in purchase_columns
        if column not in customer_360.columns
    ]


    if missing_purchase_columns:

        st.info(
            "The following purchase features are not "
            "available and are skipped: "
            + ", ".join(missing_purchase_columns)
        )


    purchase_rows = []


    purchase_labels = {
        "total_orders":
            "Average Orders per Customer",

        "total_spent":
            "Average Customer Spending",

        "average_order_value":
            "Average Order Value"
    }


    for column in available_purchase_columns:

        purchase_rows.append(
            {
                "Metric": purchase_labels.get(
                    column,
                    column
                ),
                "Value": round(
                    customer_360[column].mean(),
                    2
                )
            }
        )


    if purchase_rows:

        purchase_summary = pd.DataFrame(
            purchase_rows
        )


        st.dataframe(
            purchase_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No valid purchase behaviour features "
            "are available."
        )


    # ========================================================
    # CUSTOMER EXPERIENCE SUMMARY
    # ========================================================

    st.subheader(
        "Customer Experience Summary"
    )


    experience_columns = [
        "average_review_score",
        "average_delivery_days",
        "average_delivery_delay",
        "on_time_delivery_rate",
        "delayed_delivery_rate"
    ]


    available_experience_columns = [
        column
        for column in experience_columns
        if column in customer_360.columns
        and pd.api.types.is_numeric_dtype(
            customer_360[column]
        )
    ]


    missing_experience_columns = [
        column
        for column in experience_columns
        if column not in customer_360.columns
    ]


    if missing_experience_columns:

        st.info(
            "The following customer-experience features "
            "are not available and are skipped: "
            + ", ".join(missing_experience_columns)
        )


    experience_labels = {
        "average_review_score":
            "Average Review Score",

        "average_delivery_days":
            "Average Delivery Days",

        "average_delivery_delay":
            "Average Delivery Delay",

        "on_time_delivery_rate":
            "On-Time Delivery Rate",

        "delayed_delivery_rate":
            "Delayed Delivery Rate"
    }


    experience_rows = []


    for column in available_experience_columns:

        value = customer_360[column].mean()


        if column in [
            "on_time_delivery_rate",
            "delayed_delivery_rate"
        ]:

            value = value * 100


        experience_rows.append(
            {
                "Metric": experience_labels.get(
                    column,
                    column
                ),
                "Value": round(
                    value,
                    2
                )
            }
        )


    if experience_rows:

        experience_summary = pd.DataFrame(
            experience_rows
        )


        st.dataframe(
            experience_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No valid customer-experience features "
            "are available."
        )


    # ========================================================
    # TIME-BASED SUMMARY
    # ========================================================

    st.subheader(
        "Time-Based Summary"
    )


    time_columns = [
        "recency_days",
        "customer_tenure_days"
    ]


    available_time_columns = [
        column
        for column in time_columns
        if column in customer_360.columns
        and pd.api.types.is_numeric_dtype(
            customer_360[column]
        )
    ]


    missing_time_columns = [
        column
        for column in time_columns
        if column not in customer_360.columns
    ]


    if missing_time_columns:

        st.info(
            "The following time-based features are not "
            "available and are skipped: "
            + ", ".join(missing_time_columns)
        )


    time_labels = {
        "recency_days":
            "Average Recency (Days)",

        "customer_tenure_days":
            "Average Customer Tenure (Days)"
    }


    time_rows = []


    for column in available_time_columns:

        time_rows.append(
            {
                "Metric": time_labels.get(
                    column,
                    column
                ),
                "Value": round(
                    customer_360[column].mean(),
                    2
                )
            }
        )


    if time_rows:

        time_summary = pd.DataFrame(
            time_rows
        )


        st.dataframe(
            time_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No valid time-based features "
            "are available."
        )


    # ========================================================
    # CUSTOMER SEGMENTATION SUMMARY
    # ========================================================

    st.subheader(
        "Customer Segmentation Summary"
    )


    if "spending_segment" in customer_360.columns:

        segment_data = customer_360[
            "spending_segment"
        ].dropna()


        if segment_data.empty:

            st.info(
                "The spending_segment column exists, "
                "but contains no valid values."
            )

        else:

            segmentation_summary = (
                segment_data
                .value_counts(
                    sort=False
                )
                .reset_index()
            )


            segmentation_summary.columns = [
                "Customer Segment",
                "Customer Count"
            ]


            st.dataframe(
                segmentation_summary,
                use_container_width=True,
                hide_index=True
            )


    else:

        st.info(
            "The temporary 'spending_segment' feature "
            "is not present in the current dataset. "
            "Segmentation summary is therefore skipped."
        )


    # ========================================================
    # DATA-DRIVEN EDA OBSERVATIONS
    # ========================================================

    st.subheader(
        "EDA Observations"
    )


    observations = []


    # --------------------------------------------------------
    # Purchase frequency observation
    # --------------------------------------------------------

    if (
        "total_orders" in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["total_orders"]
        )
    ):

        valid_orders = (
            customer_360["total_orders"]
            .dropna()
        )


        if not valid_orders.empty:

            single_order_count = int(
                (valid_orders == 1).sum()
            )


            repeat_customer_count = int(
                (valid_orders > 1).sum()
            )


            total_valid_orders = len(
                valid_orders
            )


            if total_valid_orders > 0:

                single_order_percentage = (
                    single_order_count
                    / total_valid_orders
                    * 100
                )


                repeat_customer_percentage = (
                    repeat_customer_count
                    / total_valid_orders
                    * 100
                )


                observations.append(
                    {
                        "Analysis Area":
                            "Customer Purchase Frequency",

                        "Observation":
                            (
                                f"{single_order_percentage:.2f}% "
                                "of customers have one order, "
                                f"while "
                                f"{repeat_customer_percentage:.2f}% "
                                "have more than one order."
                            )
                    }
                )


    # --------------------------------------------------------
    # Spending variation
    # --------------------------------------------------------

    if (
        "total_spent" in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["total_spent"]
        )
    ):

        spending_data = (
            customer_360["total_spent"]
            .dropna()
        )


        if not spending_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Customer Spending",

                    "Observation":
                        (
                            f"Average customer spending is "
                            f"{spending_data.mean():.2f}, "
                            f"with a median of "
                            f"{spending_data.median():.2f}."
                        )
                }
            )


    # --------------------------------------------------------
    # Review score
    # --------------------------------------------------------

    if (
        "average_review_score"
        in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["average_review_score"]
        )
    ):

        review_data = (
            customer_360["average_review_score"]
            .dropna()
        )


        if not review_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Customer Review Experience",

                    "Observation":
                        (
                            f"Average review score is "
                            f"{review_data.mean():.2f}."
                        )
                }
            )


    # --------------------------------------------------------
    # Delivery
    # --------------------------------------------------------

    if (
        "average_delivery_days"
        in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["average_delivery_days"]
        )
    ):

        delivery_data = (
            customer_360["average_delivery_days"]
            .dropna()
        )


        if not delivery_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Delivery Performance",

                    "Observation":
                        (
                            f"Average delivery duration is "
                            f"{delivery_data.mean():.2f} days."
                        )
                }
            )


    # --------------------------------------------------------
    # Delivery delay
    # --------------------------------------------------------

    if (
        "average_delivery_delay"
        in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["average_delivery_delay"]
        )
    ):

        delay_data = (
            customer_360["average_delivery_delay"]
            .dropna()
        )


        if not delay_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Delivery Delay",

                    "Observation":
                        (
                            f"Average delivery delay is "
                            f"{delay_data.mean():.2f} days."
                        )
                }
            )


    # --------------------------------------------------------
    # Time behaviour
    # --------------------------------------------------------

    if (
        "recency_days" in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["recency_days"]
        )
    ):

        recency_data = (
            customer_360["recency_days"]
            .dropna()
        )


        if not recency_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Customer Recency",

                    "Observation":
                        (
                            f"Average customer recency is "
                            f"{recency_data.mean():.2f} days."
                        )
                }
            )


    if (
        "customer_tenure_days"
        in customer_360.columns
        and
        pd.api.types.is_numeric_dtype(
            customer_360["customer_tenure_days"]
        )
    ):

        tenure_data = (
            customer_360["customer_tenure_days"]
            .dropna()
        )


        if not tenure_data.empty:

            observations.append(
                {
                    "Analysis Area":
                        "Customer Tenure",

                    "Observation":
                        (
                            f"Average customer tenure is "
                            f"{tenure_data.mean():.2f} days."
                        )
                }
            )


    # ========================================================
    # DISPLAY OBSERVATIONS
    # ========================================================

    if observations:

        observations_df = pd.DataFrame(
            observations
        )


        st.dataframe(
            observations_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No data-driven observations could be generated "
            "from the currently available features."
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    st.subheader(
        "EDA Conclusion"
    )


    st.info(
        "The summary above is generated directly from the "
        "features available in the loaded EDA dataset. "
        "Analyses are skipped whenever the required feature "
        "is unavailable or has an unsuitable datatype."
    )


    st.caption(
        "No source data is modified during the EDA summary."
    )
#12
# ============================================================
# FINAL EDA CONCLUSION & EXPORT
# ============================================================

st.header("Final EDA Conclusion & Export")

st.caption(
    "Final validation and export of the cleaned Customer 360 dataset."
)


# ============================================================
# FINAL CUSTOMER 360 VALIDATION
# ============================================================

st.subheader("Final Customer 360 Validation")


required_id_column = "customer_unique_id"


if required_id_column not in customer_360.columns:

    st.warning(
        "Required notebook feature "
        "'customer_unique_id' is missing. "
        "Unique customer validation cannot be performed."
    )

else:

    final_validation = pd.DataFrame({
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Unique Customers",
            "Duplicate Rows",
            "Missing Values"
        ],

        "Value": [
            customer_360.shape[0],
            customer_360.shape[1],
            customer_360["customer_unique_id"].nunique(),
            customer_360.duplicated().sum(),
            customer_360.isnull().sum().sum()
        ]
    })


    st.dataframe(
        final_validation,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FINAL FEATURE LIST
# ============================================================

st.subheader("Final Feature List")


feature_summary = pd.DataFrame({
    "Feature Name": customer_360.columns
})


st.dataframe(
    feature_summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FINAL DATASET SHAPE
# ============================================================

st.subheader("Final Dataset Shape")


st.write(
    f"Current Customer 360 shape: {customer_360.shape}"
)


# ============================================================
# REMOVE TEMPORARY SEGMENTATION FEATURE
# ============================================================

if "spending_segment" in customer_360.columns:

    customer_360_clean = customer_360.drop(
        columns=["spending_segment"]
    )

else:

    customer_360_clean = customer_360.copy()


st.write(
    f"Final clean Customer 360 shape: "
    f"{customer_360_clean.shape}"
)


# ============================================================
# FINAL CLEAN DATASET VALIDATION
# ============================================================

st.subheader("Final Clean Dataset Validation")


clean_validation = pd.DataFrame({
    "Metric": [
        "Total Rows",
        "Total Columns",
        "Unique Customers",
        "Duplicate Rows",
        "Missing Values"
    ],

    "Value": [
        customer_360_clean.shape[0],
        customer_360_clean.shape[1],

        (
            customer_360_clean["customer_unique_id"].nunique()
            if "customer_unique_id"
            in customer_360_clean.columns
            else "Unavailable"
        ),

        customer_360_clean.duplicated().sum(),

        customer_360_clean.isnull().sum().sum()
    ]
})


st.dataframe(
    clean_validation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EDA CONCLUSION
# ============================================================

st.subheader("EDA Conclusion")


st.write(
    "The Exploratory Data Analysis has been completed on the "
    "Customer 360 dataset."
)


st.write(
    "The final dataset contains validated customer-level "
    "information with the required features."
)


# ============================================================
# EXPORT PATH
# ============================================================

export_path = Path(
    r"D:\customer pulse AI project"
) / "1 data" / "03_analysis" / "customer_360_clean.csv"


st.subheader("Final Dataset Export")


st.write(
    f"Export location: `{export_path}`"
)


# ============================================================
# EXPORT
# ============================================================

try:

    export_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    customer_360_clean.to_csv(
        export_path,
        index=False
    )


    st.success(
        "Dataset exported successfully."
    )


    st.write(
        f"File Name: {export_path.name}"
    )


    st.write(
        f"Rows: {customer_360_clean.shape[0]}"
    )


    st.write(
        f"Columns: {customer_360_clean.shape[1]}"
    )


    st.write(
        f"Path: {export_path}"
    )


except Exception as e:

    st.error(
        f"Dataset export failed: {e}"
    )