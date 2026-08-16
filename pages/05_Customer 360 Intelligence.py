import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer 360 | CustomerPulse AI",
    page_icon="👤",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "1 data"
    / "02_processed data"
    / "customer_360.csv"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("👤 Customer 360 Intelligence")

st.subheader(
    "From Transaction-Level Data to a Unified Customer Profile"
)

st.write(
    """
    Customer 360 is the central analytical foundation of CustomerPulse AI.
    The feature engineering process transforms customer, order, payment,
    product and customer-experience information into a unified
    customer-level dataset.

    The objective is to understand each customer through multiple
    dimensions instead of analysing individual transactions in isolation.
    """
)

st.divider()


# ============================================================
# LOAD CUSTOMER 360 DATASET
# ============================================================

if not DATA_FILE.exists():

    st.error(
        "customer_360.csv was not found at the expected project path."
    )

    st.info(
        f"Expected location: {DATA_FILE}"
    )

    st.stop()


try:

    df = pd.read_csv(DATA_FILE)

except Exception as e:

    st.error(
        "The Customer 360 dataset could not be loaded."
    )

    st.exception(e)

    st.stop()


# ============================================================
# BASIC DATA VALIDATION
# ============================================================

required_identifier = "customer_unique_id"

if required_identifier not in df.columns:

    st.error(
        "The required customer identifier column "
        "'customer_unique_id' is not available in customer_360.csv."
    )

    st.stop()


total_rows = len(df)
total_columns = len(df.columns)
unique_customers = df[required_identifier].nunique()
duplicate_rows = df.duplicated().sum()
missing_values = int(df.isnull().sum().sum())


# ============================================================
# DATA FOUNDATION
# ============================================================

st.header("🏗️ Customer 360 Data Foundation")

st.write(
    """
    The Customer 360 dataset is treated as the single source of
    truth for this page. All displayed statistics and feature-level
    observations are calculated directly from the dataset loaded above.
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Customer Records",
        f"{total_rows:,}"
    )

with col2:

    st.metric(
        "Unique Customers",
        f"{unique_customers:,}"
    )

with col3:

    st.metric(
        "Available Features",
        f"{total_columns:,}"
    )

with col4:

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


st.write("")


if duplicate_rows == 0 and missing_values == 0:

    st.success(
        "Customer 360 validation: no duplicate rows and no missing values "
        "were found in the loaded Customer 360 dataset."
    )

else:

    if duplicate_rows > 0:

        st.warning(
            f"Duplicate rows detected: {duplicate_rows:,}"
        )

    if missing_values > 0:

        st.warning(
            f"Missing values detected: {missing_values:,}"
        )


st.divider()


# ============================================================
# FEATURE ENGINEERING JOURNEY
# ============================================================

st.header("🔄 Customer 360 Feature Engineering Journey")

st.write(
    """
    The notebook builds Customer 360 progressively. Each stage adds a
    different perspective of customer behaviour before the feature tables
    are consolidated into the customer-level dataset.
    """
)

journey = [
    (
        "01",
        "Customer Profile",
        "Customer identity and geographical attributes."
    ),
    (
        "02",
        "Purchase Behaviour",
        "Order activity, delivered orders, cancelled orders and purchase dates."
    ),
    (
        "03",
        "Payment Behaviour",
        "Spending, order value, payment installments and preferred payment method."
    ),
    (
        "04",
        "Product Behaviour",
        "Items purchased, product diversity, category diversity and favourite category."
    ),
    (
        "05",
        "Customer Experience",
        "Review scores, delivery duration, delivery delay and delivery timeliness."
    ),
    (
        "06",
        "Advanced Behaviour",
        "Recency, tenure, purchase frequency, purchase gap and spending intensity."
    ),
    (
        "07",
        "Business Intelligence Features",
        "One-time buyer, repeat customer, high spender, VIP, loyal and at-risk indicators."
    ),
    (
        "08",
        "Final Customer 360",
        "Feature tables are consolidated around customer_unique_id."
    ),
]


for number, title, description in journey:

    with st.expander(
        f"{number}  |  {title}",
        expanded=False
    ):

        st.write(description)


st.divider()


# ============================================================
# FEATURE DEFINITIONS FROM NOTEBOOK
# ============================================================

feature_groups = {

    "Customer Profile": [
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ],

    "Purchase Behaviour": [
        "total_orders",
        "delivered_orders",
        "cancelled_orders",
        "first_purchase_date",
        "last_purchase_date"
    ],

    "Payment Behaviour": [
        "total_spent",
        "average_order_value",
        "maximum_order_value",
        "minimum_order_value",
        "average_payment_installments",
        "preferred_payment_type"
    ],

    "Product Behaviour": [
        "total_items_purchased",
        "unique_products",
        "unique_categories",
        "favorite_category",
        "average_items_per_order"
    ],

    "Customer Experience": [
        "average_review_score",
        "average_delivery_days",
        "average_delivery_delay",
        "on_time_delivery_rate",
        "delayed_delivery_rate"
    ],

    "Advanced Behaviour": [
        "recency_days",
        "customer_tenure_days",
        "purchase_frequency",
        "average_purchase_gap",
        "spending_intensity",
        "repeat_customer",
        "cancel_rate"
    ],

    "Business Intelligence": [
        "one_time_buyer",
        "high_spender",
        "vip_customer",
        "loyal_customer",
        "at_risk_customer",
        "customer_value_tier"
    ]
}


# ============================================================
# AVAILABLE / MISSING FEATURES
# ============================================================

st.header("🧩 Customer 360 Feature Map")

st.write(
    """
    The following feature groups are based on the feature-engineering
    stages implemented in the Customer 360 notebook.

    Only columns actually available in customer_360.csv are displayed
    as active features.
    """
)

feature_summary = []

for group_name, columns in feature_groups.items():

    available = [
        col for col in columns
        if col in df.columns
    ]

    missing = [
        col for col in columns
        if col not in df.columns
    ]

    feature_summary.append(
        {
            "Feature Group": group_name,
            "Available Features": len(available),
            "Missing Features": len(missing)
        }
    )


feature_summary_df = pd.DataFrame(
    feature_summary
)

st.dataframe(
    feature_summary_df,
    use_container_width=True,
    hide_index=True
)


st.write("")


# ============================================================
# FEATURE GROUP DETAILS
# ============================================================

for group_name, columns in feature_groups.items():

    available_columns = [
        col for col in columns
        if col in df.columns
    ]

    missing_columns = [
        col for col in columns
        if col not in df.columns
    ]

    st.subheader(group_name)

    if available_columns:

        st.write(
            "Available features:"
        )

        st.write(
            ", ".join(available_columns)
        )

    else:

        st.info(
            "No features from this group are available in customer_360.csv."
        )

    if missing_columns:

        st.warning(
            "Skipped because the following notebook features are not "
            "present in customer_360.csv: "
            + ", ".join(missing_columns)
        )

    st.write("")


st.divider()


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.header("👤 Customer Profile")

profile_columns = [
    col
    for col in feature_groups["Customer Profile"]
    if col in df.columns
]

if profile_columns:

    profile_data = df[profile_columns].copy()

    st.dataframe(
        profile_data.head(10),
        use_container_width=True,
        hide_index=True
    )

    if "customer_state" in df.columns:

        state_counts = (
            df["customer_state"]
            .value_counts(dropna=False)
            .reset_index()
        )

        state_counts.columns = [
            "customer_state",
            "customers"
        ]

        fig = px.bar(
            state_counts.head(15),
            x="customer_state",
            y="customers",
            title="Customer Distribution by State"
        )

        fig.update_layout(
            xaxis_title="Customer State",
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Customer profile features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# PURCHASE BEHAVIOUR
# ============================================================

st.header("🛒 Purchase Behaviour")

purchase_columns = [
    col
    for col in feature_groups["Purchase Behaviour"]
    if col in df.columns
]

if purchase_columns:

    metric_columns = [
        col
        for col in [
            "total_orders",
            "delivered_orders",
            "cancelled_orders"
        ]
        if col in df.columns
    ]

    if metric_columns:

        cols = st.columns(len(metric_columns))

        for i, col_name in enumerate(metric_columns):

            with cols[i]:

                st.metric(
                    col_name.replace("_", " ").title(),
                    f"{df[col_name].sum():,.0f}"
                )

    st.write("")

    numeric_purchase_columns = [
        col
        for col in purchase_columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    if numeric_purchase_columns:

        selected_purchase_feature = st.selectbox(
            "Explore purchase behaviour feature",
            numeric_purchase_columns,
            key="purchase_feature"
        )

        fig = px.histogram(
            df,
            x=selected_purchase_feature,
            title=(
                selected_purchase_feature
                .replace("_", " ")
                .title()
            ),
            nbins=30
        )

        fig.update_layout(
            xaxis_title=selected_purchase_feature.replace("_", " ").title(),
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Purchase behaviour features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# PAYMENT BEHAVIOUR
# ============================================================

st.header("💳 Payment Behaviour")

payment_columns = [
    col
    for col in feature_groups["Payment Behaviour"]
    if col in df.columns
]

if payment_columns:

    payment_metric_columns = [
        col
        for col in [
            "total_spent",
            "average_order_value",
            "maximum_order_value",
            "minimum_order_value",
            "average_payment_installments"
        ]
        if col in df.columns
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    if payment_metric_columns:

        cols = st.columns(
            min(len(payment_metric_columns), 4)
        )

        for i, col_name in enumerate(payment_metric_columns[:4]):

            with cols[i]:

                st.metric(
                    col_name.replace("_", " ").title(),
                    f"{df[col_name].mean():,.2f}"
                )

    st.write("")

    if "preferred_payment_type" in df.columns:

        payment_distribution = (
            df["preferred_payment_type"]
            .value_counts(dropna=False)
            .reset_index()
        )

        payment_distribution.columns = [
            "payment_type",
            "customers"
        ]

        fig = px.bar(
            payment_distribution,
            x="payment_type",
            y="customers",
            title="Preferred Payment Type"
        )

        fig.update_layout(
            xaxis_title="Payment Type",
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Payment behaviour features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# PRODUCT BEHAVIOUR
# ============================================================

st.header("📦 Product Behaviour")

product_columns = [
    col
    for col in feature_groups["Product Behaviour"]
    if col in df.columns
]

if product_columns:

    product_numeric = [
        col
        for col in [
            "total_items_purchased",
            "unique_products",
            "unique_categories",
            "average_items_per_order"
        ]
        if col in df.columns
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    if product_numeric:

        cols = st.columns(
            min(len(product_numeric), 4)
        )

        for i, col_name in enumerate(product_numeric[:4]):

            with cols[i]:

                st.metric(
                    col_name.replace("_", " ").title(),
                    f"{df[col_name].mean():,.2f}"
                )

    st.write("")

    if "favorite_category" in df.columns:

        category_counts = (
            df["favorite_category"]
            .value_counts(dropna=False)
            .reset_index()
        )

        category_counts.columns = [
            "favorite_category",
            "customers"
        ]

        fig = px.bar(
            category_counts.head(15),
            x="customers",
            y="favorite_category",
            orientation="h",
            title="Most Recorded Favourite Product Categories"
        )

        fig.update_layout(
            xaxis_title="Customers",
            yaxis_title="Favourite Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Product behaviour features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# CUSTOMER EXPERIENCE
# ============================================================

st.header("⭐ Customer Experience")

experience_columns = [
    col
    for col in feature_groups["Customer Experience"]
    if col in df.columns
]

if experience_columns:

    experience_numeric = [
        col
        for col in experience_columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    if experience_numeric:

        cols = st.columns(
            min(len(experience_numeric), 4)
        )

        for i, col_name in enumerate(experience_numeric[:4]):

            with cols[i]:

                st.metric(
                    col_name.replace("_", " ").title(),
                    f"{df[col_name].mean():,.2f}"
                )

    st.write("")

    if "average_review_score" in df.columns:

        review_distribution = (
            df["average_review_score"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        review_distribution.columns = [
            "review_score",
            "customers"
        ]

        fig = px.bar(
            review_distribution,
            x="review_score",
            y="customers",
            title="Customer Review Score Distribution"
        )

        fig.update_layout(
            xaxis_title="Average Review Score",
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Customer experience features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# ADVANCED BEHAVIOUR
# ============================================================

st.header("📈 Advanced Customer Behaviour")

advanced_columns = [
    col
    for col in feature_groups["Advanced Behaviour"]
    if col in df.columns
]

if advanced_columns:

    advanced_numeric = [
        col
        for col in [
            "recency_days",
            "customer_tenure_days",
            "purchase_frequency",
            "average_purchase_gap",
            "spending_intensity",
            "cancel_rate"
        ]
        if col in df.columns
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    if advanced_numeric:

        cols = st.columns(
            min(len(advanced_numeric), 4)
        )

        for i, col_name in enumerate(advanced_numeric[:4]):

            with cols[i]:

                st.metric(
                    col_name.replace("_", " ").title(),
                    f"{df[col_name].mean():,.2f}"
                )

    st.write("")

    selectable_advanced = [
        col
        for col in advanced_numeric
        if col in df.columns
    ]

    if selectable_advanced:

        selected_advanced_feature = st.selectbox(
            "Explore advanced behaviour feature",
            selectable_advanced,
            key="advanced_feature"
        )

        fig = px.histogram(
            df,
            x=selected_advanced_feature,
            title=(
                selected_advanced_feature
                .replace("_", " ")
                .title()
            ),
            nbins=30
        )

        fig.update_layout(
            xaxis_title=selected_advanced_feature.replace("_", " ").title(),
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Advanced behaviour features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# BUSINESS INTELLIGENCE FEATURES
# ============================================================

st.header("📊 Business Intelligence Features")

bi_columns = [
    col
    for col in feature_groups["Business Intelligence"]
    if col in df.columns
]

if bi_columns:

    flag_columns = [
        col
        for col in [
            "one_time_buyer",
            "high_spender",
            "vip_customer",
            "loyal_customer",
            "at_risk_customer"
        ]
        if col in df.columns
    ]

    if flag_columns:

        cols = st.columns(
            min(len(flag_columns), 5)
        )

        for i, col_name in enumerate(flag_columns):

            with cols[i]:

                actual_values = (
                    df[col_name]
                    .dropna()
                    .unique()
                    .tolist()
                )

                if set(actual_values).issubset({0, 1}):

                    count = int(
                        (df[col_name] == 1).sum()
                    )

                    st.metric(
                        col_name.replace("_", " ").title(),
                        f"{count:,}"
                    )

                else:

                    st.metric(
                        col_name.replace("_", " ").title(),
                        f"{df[col_name].nunique():,} values"
                    )

    st.write("")

    if "customer_value_tier" in df.columns:

        value_distribution = (
            df["customer_value_tier"]
            .value_counts(dropna=False)
            .reset_index()
        )

        value_distribution.columns = [
            "customer_value_tier",
            "customers"
        ]

        fig = px.pie(
            value_distribution,
            names="customer_value_tier",
            values="customers",
            hole=0.45,
            title="Customer Value Tier Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Business intelligence features are not available in customer_360.csv."
    )


st.divider()


# ============================================================
# FEATURE EXPLORER
# ============================================================

st.header("🔎 Customer 360 Feature Explorer")

st.write(
    """
    Explore any available feature directly from the Customer 360
    dataset. No additional values or categories are created by the page.
    """
)

available_all_features = [
    col
    for col in df.columns
    if col != required_identifier
]

if available_all_features:

    selected_feature = st.selectbox(
        "Select a Customer 360 feature",
        available_all_features,
        key="feature_explorer"
    )

    selected_series = df[selected_feature]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Data Type",
            str(selected_series.dtype)
        )

    with col2:

        st.metric(
            "Unique Values",
            f"{selected_series.nunique(dropna=True):,}"
        )

    with col3:

        st.metric(
            "Missing Values",
            f"{selected_series.isnull().sum():,}"
        )

    st.write("")

    if pd.api.types.is_numeric_dtype(selected_series):

        summary = selected_series.describe()

        summary_df = (
            summary
            .rename_axis("Statistic")
            .reset_index(name="Value")
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.histogram(
            df,
            x=selected_feature,
            nbins=40,
            title=(
                selected_feature
                .replace("_", " ")
                .title()
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        value_counts = (
            selected_series
            .value_counts(dropna=False)
            .head(20)
            .reset_index()
        )

        value_counts.columns = [
            selected_feature,
            "customers"
        ]

        st.dataframe(
            value_counts,
            use_container_width=True,
            hide_index=True
        )

        if not value_counts.empty:

            fig = px.bar(
                value_counts,
                x="customers",
                y=selected_feature,
                orientation="h",
                title=(
                    selected_feature
                    .replace("_", " ")
                    .title()
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


st.divider()


# ============================================================
# FINAL CUSTOMER 360 VALIDATION
# ============================================================

st.header("✅ Final Customer 360 Validation")

validation_col1, validation_col2, validation_col3, validation_col4 = (
    st.columns(4)
)

with validation_col1:

    st.metric(
        "Dataset Rows",
        f"{len(df):,}"
    )

with validation_col2:

    st.metric(
        "Unique Customers",
        f"{df[required_identifier].nunique():,}"
    )

with validation_col3:

    st.metric(
        "Duplicate Rows",
        f"{df.duplicated().sum():,}"
    )

with validation_col4:

    st.metric(
        "Total Missing Values",
        f"{int(df.isnull().sum().sum()):,}"
    )


st.write("")


if (
    df[required_identifier].nunique() == len(df)
    and df.duplicated().sum() == 0
    and df.isnull().sum().sum() == 0
):

    st.success(
        "Customer 360 validation completed successfully. "
        "The Customer 360 dataset contains one unique customer record per row, "
        "with no duplicate rows and no missing values."
    )

else:

    st.warning(
        "The Customer 360 dataset does not currently satisfy all "
        "Customer 360 validation checks. Review the validation metrics above."
    )


st.divider()


# ============================================================
# CUSTOMER 360 DATA PREVIEW
# ============================================================

st.header("📋 Customer 360 Dataset Preview")

st.caption(
    "Preview of the actual Customer 360 dataset used by this page."
)

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# FINAL TAKEAWAY
# ============================================================

st.header("💡 Customer 360 Takeaway")

st.success(
    """
    Customer 360 brings together multiple dimensions of the customer
    relationship into a single customer-level analytical foundation.

    Purchase behaviour explains how customers interact with the
    marketplace, payment and product features describe transaction
    behaviour, customer-experience features capture reviews and
    delivery, and advanced behavioural features provide additional
    customer-level measures.

    These engineered features form the foundation for the subsequent
    analytical stages of CustomerPulse AI.
    """
)