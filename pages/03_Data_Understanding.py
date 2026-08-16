import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Data Understanding | CustomerPulse AI",
    page_icon="🔍",
    layout="wide"
)


# ============================================================
# RAW DATA PATH
# ============================================================

# Actual project structure:
#
# CUSTOMER PULSE AI PROJECT
#
# ├── 1 data
# │   ├── 01_raw_data
# │   │   ├── olist_customers_dataset.csv
# │   │   ├── olist_order_items_dataset.csv
# │   │   ├── olist_order_payments_dataset.csv
# │   │   ├── olist_order_reviews_dataset.csv
# │   │   ├── olist_orders_dataset.csv
# │   │   ├── olist_products_dataset.csv
# │   │   ├── olist_sellers_dataset.csv
# │   │   └── product_category_name_translation.csv
#
# └── pages
#
# Therefore:

DATA_FOLDER = os.path.join(
    "1 data",
    "01_raw_data"
)


# ============================================================
# DATASETS ACTUALLY USED IN THE PROJECT
# ============================================================

FILES = {

    "Customers":
        "olist_customers_dataset.csv",

    "Orders":
        "olist_orders_dataset.csv",

    "Order Items":
        "olist_order_items_dataset.csv",

    "Payments":
        "olist_order_payments_dataset.csv",

    "Reviews":
        "olist_order_reviews_dataset.csv",

    "Products":
        "olist_products_dataset.csv",

    "Sellers":
        "olist_sellers_dataset.csv",

    "Category Translation":
        "product_category_name_translation.csv"
}


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = {}

    for table_name, file_name in FILES.items():

        file_path = os.path.join(
            DATA_FOLDER,
            file_name
        )

        if os.path.exists(file_path):

            try:

                data[table_name] = pd.read_csv(
                    file_path,
                    low_memory=False
                )

            except Exception as e:

                st.error(
                    f"Error loading {file_name}: {e}"
                )

    return data


data = load_data()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔍 Data Understanding")

st.subheader(
    "Understanding the Structure, Quality and Behaviour of Raw Data"
)

st.write(
    """
    Before performing data cleaning, exploratory analysis,
    feature engineering and churn modelling, the raw e-commerce
    data was examined to understand its structure, scale,
    relationships and quality.

    The Olist dataset is distributed across multiple relational
    tables. Each table represents a different business entity or
    transaction level, such as customers, orders, products,
    payments, reviews and sellers.

    Understanding these differences is essential before combining
    the information into a single customer-level analytical dataset.
    """
)

st.divider()


# ============================================================
# DATASET SELECTION CONTEXT
# ============================================================

st.header("📁 Dataset Selection")

st.write(
    """
    The original Olist dataset contains multiple supporting tables.
    For CustomerPulse AI, the datasets were selected according to
    their relevance to customer behaviour, purchasing activity,
    transaction value, product interaction and customer experience.

    The following datasets form the analytical foundation of the
    project and contribute to the construction of the customer-level
    Customer 360 dataset.
    """
)


dataset_selection = pd.DataFrame({

    "Dataset": [
        "Customers",
        "Orders",
        "Order Items",
        "Payments",
        "Reviews",
        "Products",
        "Sellers",
        "Category Translation"
    ],

    "Business Role": [
        "Customer identity and location",
        "Order lifecycle and purchase activity",
        "Products purchased within orders",
        "Payment behaviour and transaction value",
        "Customer satisfaction and review experience",
        "Product attributes and categories",
        "Seller information",
        "Product category translation"
    ]
})


st.dataframe(
    dataset_selection,
    use_container_width=True,
    hide_index=True
)


st.info(
    """
    Dataset selection was driven by the analytical objective of
    understanding customers and their purchasing behaviour rather
    than by simply using every available table in the original
    dataset.
    """
)


st.divider()


# ============================================================
# CHECK DATA
# ============================================================

if not data:

    st.error(
        "No raw CSV files were loaded."
    )

    st.write(
        "Expected raw-data folder:"
    )

    st.code(
        os.path.abspath(DATA_FOLDER)
    )

    st.stop()


# ============================================================
# RAW DATASET PROFILE
# ============================================================

st.header("📊 Raw Dataset Profile")

st.write(
    """
    Each selected table was profiled independently because the
    tables operate at different levels of granularity. The profile
    provides the initial baseline for rows, columns, duplicate
    records and missing observations.
    """
)


profile_data = []


for table_name, df in data.items():

    profile_data.append({

        "Table":
            table_name,

        "Rows":
            df.shape[0],

        "Columns":
            df.shape[1],

        "Duplicate Rows":
            int(
                df.duplicated().sum()
            ),

        "Missing Cells":
            int(
                df.isna().sum().sum()
            )
    })


profile_df = pd.DataFrame(
    profile_data
)


# ============================================================
# KPI CARDS
# ============================================================

total_rows = sum(
    df.shape[0]
    for df in data.values()
)

total_columns = sum(
    df.shape[1]
    for df in data.values()
)

total_missing = sum(
    int(
        df.isna().sum().sum()
    )
    for df in data.values()
)

total_duplicates = sum(
    int(
        df.duplicated().sum()
    )
    for df in data.values()
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Datasets",
        len(data)
    )


with col2:

    st.metric(
        "Total Records",
        f"{total_rows:,}"
    )


with col3:

    st.metric(
        "Missing Cells",
        f"{total_missing:,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{total_duplicates:,}"
    )


st.markdown("")


st.dataframe(
    profile_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# ACTUAL DATA PREVIEW
# ============================================================

st.header("👀 Actual Raw Data Preview")

st.write(
    """
    The actual records from the selected raw datasets can be
    inspected below. This preview helps establish the structure
    and nature of the source data before any transformation
    is performed.
    """
)


selected_table = st.selectbox(
    "Select a dataset",
    options=list(data.keys()),
    index=0
)


selected_df = data[selected_table]


st.subheader(
    f"📋 {selected_table}"
)


# ============================================================
# SELECTED TABLE METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{selected_df.shape[0]:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{selected_df.shape[1]:,}"
    )


with col3:

    st.metric(
        "Duplicate Rows",
        f"{selected_df.duplicated().sum():,}"
    )


with col4:

    st.metric(
        "Missing Cells",
        f"{selected_df.isna().sum().sum():,}"
    )


st.dataframe(
    selected_df.head(10),
    use_container_width=True,
    hide_index=True
)


st.caption(
    "Showing the first 10 records of the selected raw dataset."
)


st.divider()


# ============================================================
# CUSTOMER IDENTITY
# ============================================================

st.header("👥 Understanding Customer Identity")

if "Customers" in data:

    customers = data["Customers"]


    customer_records = len(
        customers
    )


    unique_customer_id = (
        customers["customer_id"]
        .nunique()
    )


    unique_customer_unique_id = (
        customers["customer_unique_id"]
        .nunique()
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Customer Records",
            f"{customer_records:,}"
        )


    with col2:

        st.metric(
            "Unique customer_id",
            f"{unique_customer_id:,}"
        )


    with col3:

        st.metric(
            "Unique Customers",
            f"{unique_customer_unique_id:,}"
        )


    st.write(
        f"""
        The customer table contains **{customer_records:,} records**,
        while `customer_unique_id` identifies
        **{unique_customer_unique_id:,} unique customers**.

        This distinction is important for CustomerPulse AI because
        the final analysis operates at the customer level.

        Therefore, `customer_unique_id` is used as the primary
        analytical customer identity when constructing the
        Customer 360 dataset.
        """
    )


st.divider()


# ============================================================
# COLUMN LEVEL UNDERSTANDING
# ============================================================

st.header("🧱 Column-Level Data Understanding")

st.write(
    """
    The selected dataset is examined at the column level to
    understand its data types, missing observations and
    cardinality before preprocessing.
    """
)


column_profile = pd.DataFrame({

    "Column":
        selected_df.columns,

    "Data Type":
        [
            str(
                selected_df[column].dtype
            )
            for column in selected_df.columns
        ],

    "Non-Null Values":
        [
            int(
                selected_df[column].notna().sum()
            )
            for column in selected_df.columns
        ],

    "Missing Values":
        [
            int(
                selected_df[column].isna().sum()
            )
            for column in selected_df.columns
        ],

    "Unique Values":
        [
            int(
                selected_df[column].nunique(
                    dropna=True
                )
            )
            for column in selected_df.columns
        ]
})


st.dataframe(
    column_profile,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# MISSING VALUE INVESTIGATION
# ============================================================

st.header("⚠️ Missing Value Investigation")

st.write(
    """
    Missing values were first identified and quantified at the
    raw-data level.

    At this stage, no values are removed or replaced. The purpose
    is to understand where missing observations occur and what
    they may represent from a business perspective.

    Their treatment is handled separately in the Data Cleaning &
    Preprocessing stage.
    """
)


missing_records = []


for table_name, df in data.items():

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        if missing_count > 0:

            missing_records.append({

                "Table":
                    table_name,

                "Column":
                    column,

                "Missing Values":
                    missing_count,

                "Missing %":
                    round(
                        (
                            missing_count /
                            len(df)
                        ) * 100,
                        2
                    )
            })


if missing_records:

    missing_df = pd.DataFrame(
        missing_records
    )

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No missing values were found in the selected raw datasets."
    )


st.divider()


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

st.header("♻️ Duplicate Record Investigation")

st.write(
    """
    Duplicate rows were checked before any aggregation or
    integration because duplicated records can distort customer
    counts, order counts and monetary metrics.

    Repeated identifiers are not automatically treated as
    duplicates because legitimate one-to-many relationships
    exist across the Olist tables.
    """
)


duplicate_df = profile_df[
    [
        "Table",
        "Rows",
        "Duplicate Rows"
    ]
]


st.dataframe(
    duplicate_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# IDENTIFIER ANALYSIS
# ============================================================

st.header("🔑 Identifier & Relationship Analysis")

st.write(
    """
    Identifiers were examined to understand how the datasets
    relate to one another.

    This is particularly important because the raw data contains
    one-to-many relationships between customers, orders, order
    items, payments and other entities.
    """
)


identifier_candidates = [

    "customer_id",

    "customer_unique_id",

    "order_id",

    "order_item_id",

    "product_id",

    "seller_id",

    "review_id"
]


identifier_results = []


for table_name, df in data.items():

    for column in identifier_candidates:

        if column in df.columns:

            records = len(df)

            unique_values = (
                df[column]
                .nunique(
                    dropna=True
                )
            )

            repeated_records = (
                records -
                unique_values
            )

            identifier_results.append({

                "Table":
                    table_name,

                "Identifier":
                    column,

                "Records":
                    records,

                "Unique Values":
                    unique_values,

                "Repeated Records":
                    repeated_records
            })


if identifier_results:

    identifier_df = pd.DataFrame(
        identifier_results
    )

    st.dataframe(
        identifier_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# ORDER STATUS
# ============================================================

if "Orders" in data:

    orders = data["Orders"]


    if "order_status" in orders.columns:

        st.header("📦 Order Status Distribution")

        st.write(
            """
            Order status provides an initial understanding of
            the operational composition of the order dataset.
            """
        )


        status_df = (
            orders["order_status"]
            .value_counts()
            .reset_index()
        )


        status_df.columns = [
            "Order Status",
            "Orders"
        ]


        status_df["Percentage"] = (
            status_df["Orders"]
            /
            status_df["Orders"].sum()
            *
            100
        ).round(2)


        st.dataframe(
            status_df,
            use_container_width=True,
            hide_index=True
        )


st.divider()


# ============================================================
# DATE FIELD IDENTIFICATION
# ============================================================

st.header("📅 Date & Time Fields")

st.write(
    """
    Order lifecycle timestamps are important for later calculations
    such as customer tenure, purchase recency and delivery
    experience.

    These fields are identified at the raw-data stage and will be
    converted into appropriate datetime formats during
    preprocessing.
    """
)


date_fields = []


for table_name, df in data.items():

    for column in df.columns:

        column_lower = column.lower()

        if (
            "date" in column_lower
            or "timestamp" in column_lower
            or "purchase" in column_lower
            or "approved" in column_lower
            or "delivered" in column_lower
        ):

            date_fields.append({

                "Table":
                    table_name,

                "Column":
                    column,

                "Current Data Type":
                    str(
                        df[column].dtype
                    )
            })


if date_fields:

    date_df = pd.DataFrame(
        date_fields
    )

    st.dataframe(
        date_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# INITIAL DATA UNDERSTANDING
# ============================================================

st.header("🧠 Initial Data Understanding Findings")

st.write(
    """
    The raw-data assessment established the following observations
    before cleaning and transformation:
    """
)


with st.expander(
    "1️⃣ Multiple relational datasets"
):

    st.write(
        """
        Customer, order, product, payment, review and seller
        information is distributed across separate but connected
        tables.
        """
    )


with st.expander(
    "2️⃣ Different levels of granularity"
):

    st.write(
        """
        Customer records, orders, order items and payment records
        do not represent the same unit of observation.

        A single customer may have multiple orders, and a single
        order may contain multiple items or payment records.
        """
    )


with st.expander(
    "3️⃣ Customer identity must be defined carefully"
):

    st.write(
        """
        `customer_id` and `customer_unique_id` represent different
        concepts.

        CustomerPulse AI uses `customer_unique_id` as the basis
        for customer-level analysis.
        """
    )


with st.expander(
    "4️⃣ Missing values require contextual treatment"
):

    st.write(
        """
        Missing observations are concentrated in selected fields,
        particularly certain order lifecycle timestamps.

        These values must be interpreted according to the meaning
        of each field rather than removed blindly.
        """
    )


with st.expander(
    "5️⃣ Repeated identifiers are not always duplicates"
):

    st.write(
        """
        Repeated identifiers can be valid because of one-to-many
        relationships. Therefore, true duplicate rows must be
        distinguished from legitimate repeated business records.
        """
    )


with st.expander(
    "6️⃣ Date fields require preprocessing"
):

    st.write(
        """
        Timestamp fields need to be converted into proper datetime
        formats before deriving delivery duration, tenure, recency
        and other behavioural measures.
        """
    )


st.divider()


# ============================================================
# TRANSITION TO CLEANING
# ============================================================

st.header("➡️ What Happens Next?")

st.write(
    """
    The Data Understanding stage establishes the raw-data baseline.

    The next stage focuses on Data Cleaning & Preprocessing, where
    the identified data-quality issues will be investigated and
    handled before exploratory analysis and feature engineering.
    """
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.info(
        "⚠️ Missing Values"
    )


with col2:

    st.info(
        "♻️ Duplicate Validation"
    )


with col3:

    st.info(
        "📅 Date Processing"
    )


with col4:

    st.info(
        "📈 Outlier Investigation"
    )


st.success(
    "Data Understanding → Data Cleaning & Preprocessing → customer 360 engineering → Exploratory Data Analysis"
)