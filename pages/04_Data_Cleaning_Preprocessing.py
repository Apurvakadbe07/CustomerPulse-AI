import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Cleaning & Preprocessing | CustomerPulse AI",
    page_icon="🧹",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

RAW_FOLDER = os.path.join(
    "1 data",
    "01_raw_data"
)

PROCESSED_FOLDER = os.path.join(
    "1 data",
    "02_processed_data"
)


RAW_FILES = {
    "Customers": "olist_customers_dataset.csv",
    "Orders": "olist_orders_dataset.csv",
    "Order Items": "olist_order_items_dataset.csv",
    "Payments": "olist_order_payments_dataset.csv",
    "Reviews": "olist_order_reviews_dataset.csv",
    "Products": "olist_products_dataset.csv",
    "Sellers": "olist_sellers_dataset.csv",
    "Category Translation":
        "product_category_name_translation.csv"
}


# ============================================================
# LOAD RAW DATA
# ============================================================

@st.cache_data
def load_raw_data():

    data = {}

    for table_name, file_name in RAW_FILES.items():

        path = os.path.join(
            RAW_FOLDER,
            file_name
        )

        if os.path.exists(path):

            data[table_name] = pd.read_csv(
                path,
                low_memory=False
            )

    return data


raw_data = load_raw_data()


# ============================================================
# LOAD CUSTOMER 360
# ============================================================

@st.cache_data
def load_customer_360():

    possible_files = [

        os.path.join(
            PROCESSED_FOLDER,
            "customer_360.csv"
        ),

        os.path.join(
            PROCESSED_FOLDER,
            "customer_360_clean.csv"
        ),

        os.path.join(
            "03_analysis",
            "customer_360_clean.csv"
        )
    ]

    for path in possible_files:

        if os.path.exists(path):

            return pd.read_csv(
                path,
                low_memory=False
            )

    return None


customer_360 = load_customer_360()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🧹 Data Cleaning & Preprocessing")

st.subheader(
    "Turning Raw E-Commerce Data into a Reliable Analytical Foundation"
)

st.write(
    """
    Raw e-commerce data is rarely ready for direct analysis.

    Before calculating customer behaviour, customer value or churn
    indicators, the underlying data must be checked for missing
    observations, duplicate records, incorrect data types, date
    inconsistencies and extreme numerical observations.

    In CustomerPulse AI, cleaning was therefore treated as a
    business-quality step rather than simply deleting incomplete
    records. Each issue was examined according to the meaning of
    the underlying field and its impact on customer-level analysis.
    """
)

st.divider()


# ============================================================
# CLEANING PIPELINE
# ============================================================

st.header("🔄 Data Cleaning Pipeline")

st.write(
    """
    The cleaning process followed a structured sequence so that
    data-quality issues were addressed before customer-level
    aggregation and modelling.
    """
)


pipeline = [

    "1️⃣ Raw Data Assessment",

    "2️⃣ Missing Value Investigation",

    "3️⃣ Duplicate Validation",

    "4️⃣ Data Type Correction",

    "5️⃣ Date & Time Standardisation",

    "6️⃣ Data Consistency Checks",

    "7️⃣ Outlier & Distribution Inspection",

    "8️⃣ Customer-Level Data Preparation",

    "9️⃣ Final Quality Validation"
]


for step in pipeline:

    st.info(step)


st.divider()


# ============================================================
# RAW DATA QUALITY BASELINE
# ============================================================

st.header("📊 1. Raw Data Quality Baseline")

if raw_data:

    baseline = []

    for table_name, df in raw_data.items():

        baseline.append({

            "Dataset":
                table_name,

            "Rows":
                len(df),

            "Columns":
                len(df.columns),

            "Duplicate Rows":
                int(
                    df.duplicated().sum()
                ),

            "Missing Cells":
                int(
                    df.isna().sum().sum()
                )
        })


    baseline_df = pd.DataFrame(
        baseline
    )


    st.dataframe(
        baseline_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Raw datasets could not be loaded."
    )


st.info(
    """
    **Why this matters:** Before changing the data, a baseline is
    required. Without a before-state, it is difficult to demonstrate
    whether preprocessing actually improved data quality.
    """
)


st.divider()


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

st.header("⚠️ 2. Missing Value Investigation")

st.write(
    """
    Missing values were not treated as automatically removable
    records. Their location and business meaning were first
    examined.
    """
)


missing_expected = pd.DataFrame({

    "Field":
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ],

    "Missing Records":
        [
            160,
            1783,
            2965
        ],

    "Business Interpretation":
        [
            "Order approval timestamp unavailable",
            "Carrier handover timestamp unavailable",
            "Customer delivery timestamp unavailable"
        ]
})


st.dataframe(
    missing_expected,
    use_container_width=True,
    hide_index=True
)


st.subheader("📌 Cleaning Decision")


st.write(
    """
    These missing timestamps were evaluated in the context of the
    order lifecycle.

    A missing delivery-related timestamp does not automatically mean
    that the complete customer record is invalid. Removing such
    customers blindly could discard useful purchasing information.

    Therefore, missing-value treatment was performed according to
    field meaning and downstream analytical requirements rather than
    applying a blanket deletion rule.
    """
)


st.success(
    """
    **Key Insight:** Missing data was treated as a business-context
    problem, not simply as a technical null-value problem.
    """
)


st.divider()


# ============================================================
# DUPLICATE VALIDATION
# ============================================================

st.header("♻️ 3. Duplicate Validation")

st.write(
    """
    Duplicate records were checked before aggregation because
    duplicated transaction records could artificially increase
    order counts, spending and customer activity.
    """
)


if raw_data:

    duplicate_rows = sum(
        int(
            df.duplicated().sum()
        )
        for df in raw_data.values()
    )

else:

    duplicate_rows = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Raw Duplicate Rows",
        f"{duplicate_rows:,}"
    )


with col2:

    st.metric(
        "Final Customer Duplicates",
        "0"
    )


with col3:

    st.metric(
        "Final Unique Customers",
        "96,096"
    )


st.write(
    """
    The raw datasets did not contain duplicate rows that required
    blanket deletion. However, repeated identifiers were still
    treated carefully because repeated customer, order or item IDs
    can represent legitimate one-to-many relationships.
    """
)


st.success(
    """
    **Cleaning Insight:** A repeated identifier is not automatically
    a duplicate record. The business grain of each table must be
    respected before removing anything.
    """
)


st.divider()


# ============================================================
# DATA TYPE CORRECTION
# ============================================================

st.header("🔢 4. Data Type Correction")

st.write(
    """
    Raw datasets contain fields stored in different formats.
    Numerical fields need to remain numerical, categorical fields
    need consistent categorical interpretation and timestamp fields
    need proper datetime representation.
    """
)


if "Orders" in raw_data:

    orders = raw_data["Orders"]


    date_columns = [
        column
        for column in orders.columns
        if (
            "timestamp" in column.lower()
            or "date" in column.lower()
        )
    ]


    if date_columns:

        dtype_table = pd.DataFrame({

            "Column":
                date_columns,

            "Raw Data Type":
                [
                    str(
                        orders[column].dtype
                    )
                    for column in date_columns
                ],

            "Required Analytical Type":
                [
                    "Datetime"
                    for _ in date_columns
                ]
        })


        st.dataframe(
            dtype_table,
            use_container_width=True,
            hide_index=True
        )


st.info(
    """
    **Why this matters:** Date calculations such as delivery
    duration, recency and customer tenure cannot be reliably
    calculated while timestamps are treated merely as text.
    """
)


st.divider()


# ============================================================
# DATE STANDARDISATION
# ============================================================

st.header("📅 5. Date & Time Standardisation")

st.write(
    """
    Order lifecycle timestamps represent different stages of the
    customer journey, from purchase to approval, carrier handover
    and final delivery.

    These fields were converted into appropriate datetime
    representations so that time-based customer and operational
    metrics could be calculated consistently.
    """
)


if "Orders" in raw_data:

    orders = raw_data["Orders"]


    date_columns = [
        column
        for column in orders.columns
        if (
            "timestamp" in column.lower()
            or "date" in column.lower()
        )
    ]


    date_conversion = []


    for column in date_columns:

        converted = pd.to_datetime(
            orders[column],
            errors="coerce"
        )


        date_conversion.append({

            "Column":
                column,

            "Original Type":
                str(
                    orders[column].dtype
                ),

            "Datetime Conversion":
                str(
                    converted.dtype
                ),

            "Valid Dates":
                int(
                    converted.notna().sum()
                ),

            "Invalid / Missing":
                int(
                    converted.isna().sum()
                )
        })


    if date_conversion:

        date_conversion_df = pd.DataFrame(
            date_conversion
        )


        st.dataframe(
            date_conversion_df,
            use_container_width=True,
            hide_index=True
        )


st.success(
    """
    **Cleaning Insight:** Standardised timestamps create a reliable
    foundation for recency, tenure, delivery-time and customer
    experience calculations.
    """
)


st.divider()


# ============================================================
# DATA CONSISTENCY
# ============================================================

st.header("🔎 6. Data Consistency Checks")

st.write(
    """
    After handling structural issues, categorical and numerical
    fields were inspected for values that could create inconsistent
    business interpretations.
    """
)


if "Orders" in raw_data:

    orders = raw_data["Orders"]


    if "order_status" in orders.columns:

        status_values = (
            orders["order_status"]
            .value_counts()
            .reset_index()
        )


        status_values.columns = [
            "Order Status",
            "Records"
        ]


        st.subheader(
            "Order Status Validation"
        )


        st.dataframe(
            status_values,
            use_container_width=True,
            hide_index=True
        )


st.info(
    """
    **Why this matters:** Business categories such as order status
    must remain consistent because later analysis depends on
    grouping records into meaningful operational states.
    """
)


st.divider()


# ============================================================
# OUTLIER SECTION
# ============================================================

st.header("📈 7. Outlier & Distribution Inspection")

st.write(
    """
    Extreme numerical observations were investigated before
    customer-level aggregation.

    Outliers were not removed simply because they were statistically
    unusual. In e-commerce data, a high transaction value or
    shipping charge can represent a genuine business transaction.

    Therefore, statistical detection was used as an investigation
    tool, followed by business interpretation.
    """
)


# ============================================================
# IQR FUNCTION
# ============================================================

def calculate_outliers(df, column):

    if column not in df.columns:
        return None

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(series) == 0:
        return None

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outliers = series[
        (series < lower_bound)
        |
        (series > upper_bound)
    ]

    return {

        "Column":
            column,

        "Q1":
            round(q1, 2),

        "Q3":
            round(q3, 2),

        "Lower Bound":
            round(lower_bound, 2),

        "Upper Bound":
            round(upper_bound, 2),

        "Outlier Records":
            len(outliers),

        "Outlier %":
            round(
                len(outliers)
                /
                len(series)
                *
                100,
                2
            )
    }


# ============================================================
# NUMERICAL OUTLIER ANALYSIS
# ============================================================

outlier_results = []


if "Order Items" in raw_data:

    order_items = raw_data["Order Items"]


    for column in [
        "price",
        "freight_value"
    ]:

        result = calculate_outliers(
            order_items,
            column
        )


        if result:

            outlier_results.append(
                result
            )


if "Payments" in raw_data:

    payments = raw_data["Payments"]


    result = calculate_outliers(
        payments,
        "payment_value"
    )


    if result:

        outlier_results.append(
            result
        )


if outlier_results:

    outlier_df = pd.DataFrame(
        outlier_results
    )


    st.dataframe(
        outlier_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No applicable numerical columns were found for outlier analysis."
    )


st.info(
    """
    **Interpretation principle:** IQR identifies observations that
    are statistically extreme; it does not prove that those records
    are erroneous. Genuine high-value purchases should not be
    deleted merely because they lie outside the normal range.
    """
)


st.divider()


# ============================================================
# OUTLIER DECISION
# ============================================================

st.header("🎯 Outlier Treatment Decision")

st.write(
    """
    Outlier analysis was therefore used to distinguish between
    unusual observations and genuinely invalid records.

    The objective was to preserve legitimate customer and
    transaction behaviour while preventing clearly erroneous
    observations from distorting downstream analysis.
    """
)


with st.expander(
    "Why were outliers investigated?"
):

    st.write(
        """
        Highly skewed transaction values can strongly influence
        averages, spending metrics and customer-value calculations.

        Investigating extreme observations helps determine whether
        they represent genuine high-value behaviour or data-quality
        problems.
        """
    )


with st.expander(
    "Why should genuine high-value customers not be deleted?"
):

    st.write(
        """
        In an e-commerce business, a high-value transaction may be
        completely legitimate. Removing it only because it is
        statistically unusual could remove exactly the customers
        the business is interested in understanding.
        """
    )


with st.expander(
    "What was the cleaning principle?"
):

    st.write(
        """
        Statistical detection was followed by business reasoning.
        Only observations requiring correction or exclusion should
        be treated as data-quality problems; legitimate extreme
        behaviour should remain part of the analytical population.
        """
    )


st.success(
    """
    **Key Insight:** Outlier treatment was driven by business
    validity, not by statistical thresholds alone.
    """
)


st.divider()


# ============================================================
# CUSTOMER-LEVEL PREPARATION
# ============================================================

st.header("👥 8. Customer-Level Data Preparation")

st.write(
    """
    After the individual tables were cleaned and standardised,
    the data was prepared for customer-level analysis.

    Transactional information was consolidated so that multiple
    orders and related records could be represented through
    customer-level behavioural and experience measures.
    """
)


st.markdown(
    """
    **Raw Transactions**

    Orders + Items + Payments + Reviews + Products + Sellers

    ↓

    **Cleaning & Standardisation**

    Missing values + Data types + Dates + Quality checks

    ↓

    **Customer-Level Aggregation**

    Purchase behaviour + Spending + Engagement + Experience

    ↓

    **Customer 360**
    """
)


st.info(
    """
    **Why this step matters:** Churn is a customer-level business
    problem. The final analytical dataset therefore needs one
    consistent customer-level representation rather than separate
    transaction-level records.
    """
)


st.divider()


# ============================================================
# FINAL VALIDATION
# ============================================================

st.header("✅ 9. Final Data Quality Validation")

st.write(
    """
    The final validation confirms whether the cleaned Customer 360
    dataset is suitable for exploratory analysis, SQL analysis,
    segmentation and subsequent modelling.
    """
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Unique Customers",
        "96,096"
    )


with col2:

    st.metric(
        "Customer 360 Features",
        "37"
    )


with col3:

    st.metric(
        "Missing Values",
        "0"
    )


with col4:

    st.metric(
        "Duplicate Customers",
        "0"
    )


st.divider()


# ============================================================
# ACTUAL CUSTOMER 360 VALIDATION
# ============================================================

if customer_360 is not None:

    st.subheader(
        "🔍 Actual Customer 360 Validation"
    )


    validation = pd.DataFrame({

        "Validation Check":
            [
                "Rows",
                "Columns",
                "Unique Customers",
                "Missing Values",
                "Duplicate Rows"
            ],

        "Result":
            [
                len(customer_360),

                len(
                    customer_360.columns
                ),

                (
                    customer_360[
                        "customer_unique_id"
                    ].nunique()
                    if
                    "customer_unique_id"
                    in customer_360.columns
                    else "N/A"
                ),

                int(
                    customer_360.isna()
                    .sum()
                    .sum()
                ),

                int(
                    customer_360
                    .duplicated()
                    .sum()
                )
            ]
    })


    st.dataframe(
        validation,
        use_container_width=True,
        hide_index=True
    )


    if (
        len(customer_360) == 96096
        and
        int(
            customer_360.isna()
            .sum()
            .sum()
        ) == 0
        and
        int(
            customer_360.duplicated()
            .sum()
        ) == 0
    ):

        st.success(
            """
            Customer 360 passed the final data-quality validation:
            96,096 customers, no missing values and no duplicate
            customer records.
            """
        )


st.divider()


# ============================================================
# BEFORE → AFTER
# ============================================================

st.header("📊 Before vs After Data Preparation")


before_after = pd.DataFrame({

    "Quality Dimension": [

        "Customer Population",

        "Missing Values",

        "Duplicate Customers",

        "Analytical Grain",

        "Data Readiness"
    ],

    "Before Cleaning": [

        "Distributed across multiple tables",

        "Present in selected fields",

        "Required validation",

        "Transaction / table level",

        "Not ready for modelling"
    ],

    "After Cleaning": [

        "96,096 unique customers",

        "0",

        "0",

        "Customer level",

        "Ready for EDA & modelling"
    ]
})


st.dataframe(
    before_after,
    use_container_width=True,
    hide_index=True
)


st.success(
    """
    **Overall Insight:** The cleaning stage transformed fragmented
    transaction-level information into a consistent customer-level
    analytical foundation, while preserving the business meaning
    of legitimate transactions.
    """
)


st.divider()


# ============================================================
# KEY TAKEAWAYS
# ============================================================

st.header("💡 Key Cleaning Insights")

st.markdown(
    """
    ### 1. Missing values were concentrated in order lifecycle fields

    The most important missing observations were associated with
    order approval and delivery timestamps. These fields require
    contextual treatment because a missing operational timestamp
    does not automatically invalidate the customer's purchasing
    history.

    ### 2. Duplicate handling required understanding data grain

    A repeated identifier can represent a valid business
    relationship. Therefore, duplicate rows and repeated IDs were
    evaluated separately.

    ### 3. Dates were critical for customer behaviour analysis

    Proper date handling created the foundation for later metrics
    such as recency, tenure and delivery experience.

    ### 4. Outliers were investigated rather than blindly deleted

    Extreme transaction values may represent legitimate high-value
    customers. Statistical detection was therefore followed by
    business interpretation.

    ### 5. The final Customer 360 dataset became analysis-ready

    The cleaned dataset contains **96,096 customers**, **37
    analytical features**, **0 missing values** and **0 duplicate
    customer records**.
    """
)


st.divider()


# ============================================================
# NEXT STAGE
# ============================================================

st.header("➡️ Next Stage: Exploratory Data Analysis")

st.write(
    """
    With the data quality established, the next stage focuses on
    understanding customer behaviour through exploratory analysis.

    The objective will shift from:

    **“Is the data reliable?”**

    to:

    **“What does the cleaned data tell us about customers,
    purchasing behaviour, customer experience and potential churn?”**
    """
)


st.success(
    """
    Data Understanding
    →
    Cleaning & Preprocessing
    →
    Exploratory Data Analysis
    """
)