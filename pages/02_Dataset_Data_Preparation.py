import streamlit as st 
import pandas as pd 
 
 
# ============================================================ 
# PAGE CONFIGURATION 
# ============================================================ 
 
st.set_page_config( 
    page_title="Dataset & Data Preparation | CustomerPulse AI", 
    page_icon="🗂️", 
    layout="wide" 
) 
 
 
# ============================================================ 
# PAGE TITLE 
# ============================================================ 
 
st.title("🗂️ Dataset & Data Preparation") 
 
st.subheader( 
    "Building the Data Foundation for Customer-Level Analytics" 
) 
 
st.write( 
    """ 
    CustomerPulse AI is built using the Olist Brazilian E-Commerce 
    Dataset, a publicly available e-commerce dataset containing 
    information about customers, orders, products, payments, reviews, 
    sellers and geographical details. 
 
    The dataset was selected because it provides multiple dimensions 
    of the customer journey rather than containing only sales or 
    customer-profile information. This makes it suitable for studying 
    purchasing behaviour, customer value, customer experience and 
    potential churn exposure within a single analytical project. 
    """ 
) 
 
st.divider() 
 
 
# ============================================================ 
# DATASET SOURCE 
# ============================================================ 
 
st.header("🌐 Dataset Source") 
 
st.write( 
    """ 
    The project uses the Olist Brazilian E-Commerce Dataset available 
    through Kaggle. Olist is a Brazilian e-commerce marketplace, and 
    the dataset represents real commercial transactions collected 
    from its marketplace operations. 
 
    The dataset contains approximately 100,000 orders placed between 
    2016 and 2018 and provides multiple relational tables connected 
    through customer, order, product, seller and review identifiers. 
 
    These relationships make the dataset particularly useful for 
    building a customer-level analytical model instead of analysing 
    each transaction independently. 
    """ 
) 
 
st.info( 
    "Dataset: Olist Brazilian E-Commerce Dataset" 
) 
 
st.write( 
    "Source: Kaggle — Brazilian E-Commerce Public Dataset by Olist" 
)

# ============================================================
# DATASET LINK
# ============================================================

st.markdown(
    "🔗 **Dataset Reference:** "
    "[Open Brazilian E-Commerce Public Dataset by Olist on Kaggle]"
    "(https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)"
)
 
 
# ========================================================= 
# WHY THIS DATASET? 
# ========================================================= 
 
st.header("🎯 Why Was This Dataset Selected?") 
 
st.write( 
    """ 
    The primary reason for selecting the Olist dataset was its 
    ability to represent multiple aspects of an e-commerce customer 
    relationship. 
 
    A churn analysis requires more than customer IDs and order 
    amounts. To understand why customers may become inactive, the 
    analysis benefits from information about purchase history, 
    spending, payment behaviour, product categories, reviews and 
    delivery experience. 
 
    The Olist dataset provides these dimensions across connected 
    relational tables. This allows the project to move from raw 
    transactional information towards a consolidated Customer 360 
    perspective. 
 
    The dataset also contains a sufficiently large customer 
    population to make customer segmentation, churn analysis and 
    predictive modelling meaningful. 
    """ 
) 
 
 
# ========================================================= 
# DATASET CHARACTERISTICS 
# ========================================================= 
 
st.header("📊 Dataset at a Glance") 
 
col1, col2, col3, col4 = st.columns(4) 
 
with col1: 
    st.metric( 
        "Approx. Orders", 
        "100K+" 
    ) 
 
with col2: 
    st.metric( 
        "Unique Customers", 
        "96,096" 
    ) 
 
with col3: 
    st.metric( 
        "Raw Tables", 
        "9" 
    ) 
 
with col4: 
    st.metric( 
        "Final Customer Records", 
        "96,096" 
    ) 
 
 
st.divider() 
 
 
# ========================================================= 
# RAW DATA TABLES 
# ========================================================= 
 
st.header("🗃️ Raw Dataset Tables") 
 
st.write( 
    """ 
    The original dataset is organised into nine relational tables. 
    Each table describes a different part of the e-commerce 
    ecosystem. These tables are connected using common identifiers 
    and are combined selectively according to the analytical 
    requirement. 
    """ 
) 
 
 
tables = [ 
    ( 
        "1", 
        "olist_customers_dataset.csv", 
        "Customer Information", 
        """ 
        Contains customer identifiers and location-related 
        information. This table provides the customer-level 
        foundation required to connect customers with their 
        respective orders. 
        """ 
    ), 
    ( 
        "2", 
        "olist_orders_dataset.csv", 
        "Order Information", 
        """ 
        Contains order-level information including order status 
        and important timestamps representing different stages 
        of the order lifecycle. This table is central to analysing 
        customer purchasing activity and order history. 
        """ 
    ), 
    ( 
        "3", 
        "olist_order_items_dataset.csv", 
        "Order Item Information", 
        """ 
        Contains product-level details associated with orders, 
        including product, seller, price and freight information. 
        It is useful for calculating customer spending and 
        understanding purchase-level behaviour. 
        """ 
    ), 
    ( 
        "4", 
        "olist_order_payments_dataset.csv", 
        "Payment Information", 
        """ 
        Contains payment-related information for orders, including 
        payment methods, instalments and payment values. This table 
        supports analysis of customer payment behaviour and 
        transaction value. 
        """ 
    ), 
    ( 
        "5", 
        "olist_order_reviews_dataset.csv", 
        "Customer Review Information", 
        """ 
        Contains customer review scores and review-related 
        information. These records provide an important customer 
        experience dimension that can be incorporated into 
        customer-level analysis. 
        """ 
    ), 
    ( 
        "6", 
        "olist_products_dataset.csv", 
        "Product Information", 
        """ 
        Contains information describing products available on the 
        marketplace. Product attributes can be connected with order 
        items to understand the type of products customers purchase. 
        """ 
    ), 
    ( 
        "7", 
        "olist_sellers_dataset.csv", 
        "Seller Information", 
        """ 
        Contains seller identifiers and seller location information. 
        Seller data provides additional context for understanding 
        the marketplace structure and order fulfilment ecosystem. 
        """ 
    ), 
    ( 
        "8", 
        "olist_geolocation_dataset.csv", 
        "Geographical Information", 
        """ 
        Contains Brazilian geographical information that can be 
        associated with customer and seller locations. It provides 
        additional geographical context for location-based analysis. 
        """ 
    ), 
    ( 
        "9", 
        "product_category_name_translation.csv", 
        "Product Category Translation", 
        """ 
        Provides English translations for Portuguese product 
        category names, making product-category analysis easier 
        to interpret and present. 
        """ 
    ) 
] 
 
 
for number, filename, purpose, description in tables: 
 
    with st.expander( 
        f"{number}. {filename} — {purpose}" 
    ): 
 
        st.write(description) 
 
 
st.divider() 
 
 
# ========================================================= 
# TABLE RELATIONSHIP 
# ========================================================= 
 
st.header("🔗 How the Tables Work Together") 
 
st.write( 
    """ 
    The raw dataset is relational in nature. No single table 
    contains everything required for customer churn analysis. 
 
    The customer table provides the customer identity, while the 
    order table connects customers with their purchasing history. 
    Order items provide product and price-level information, while 
    payment records provide transaction and payment details. 
    Reviews add a customer-experience dimension. 
 
    Product and seller tables provide additional context around 
    the transactions, while geographical and category-translation 
    tables support location and interpretation requirements. 
 
    The analytical objective is therefore not to blindly merge every 
    table. Instead, the required information is selected according 
    to the business question and consolidated at the appropriate 
    customer level. 
    """ 
) 
 
 
st.code( 
    """ 
Customers 
    ↓ 
Orders 
    ↓ 
Order Items ─── Products 
    ↓ 
Payments 
    ↓ 
Reviews 
 
Orders ─── Sellers 
Customers / Sellers ─── Geolocation 
 
Products ─── Category Translation 
    """, 
    language="text" 
) 
 
 
st.divider() 
 
 
# ========================================================= 
# DATA PREPARATION STRATEGY 
# ========================================================= 
 
st.header("🧭 Data Preparation Strategy") 
 
st.write( 
    """ 
    The raw dataset is not directly used for machine learning or 
    business reporting. A structured preparation process is required 
    before the data can be converted into customer-level intelligence. 
 
    The preparation strategy follows a progressive approach. First, 
    the raw tables are inspected independently to understand their 
    structure and quality. Relevant tables are then connected using 
    appropriate identifiers. Customer-level measures are calculated, 
    unnecessary transaction-level duplication is controlled, and the 
    resulting information is consolidated into a Customer 360 dataset. 
    """ 
) 
 
 
# ========================================================= 
# PREPARATION FLOW 
# ========================================================= 
 
st.subheader("Data Preparation Flow") 
 
st.write( 
    """ 
    **Raw Olist Tables** 
 
    The process begins with the original relational datasets 
    containing customer, order, payment, product, review and 
    marketplace information. 
    """ 
) 
 
st.write( 
    """ 
    **↓ Data Understanding** 
 
    Each table is inspected for columns, data types, record counts, 
    missing values, duplicate records and relationships with other 
    tables. 
    """ 
) 
 
st.write( 
    """ 
    **↓ Data Cleaning** 
 
    Data-quality issues are identified and handled before creating 
    analytical features. 
    """ 
) 
 
st.write( 
    """ 
    **↓ Table Integration** 
 
    Relevant tables are connected through customer and order-level 
    identifiers to construct the required analytical view. 
    """ 
) 
 
st.write( 
    """ 
    **↓ Customer-Level Aggregation** 
 
    Transaction-level records are transformed into customer-level 
    measures such as order count, spending, review behaviour, 
    delivery experience and purchasing patterns. 
    """ 
) 
 
st.write( 
    """ 
    **↓ Customer 360** 
 
    The resulting customer-level information becomes the foundation 
    for exploratory analysis, SQL analysis, segmentation and 
    predictive modelling. 
    """ 
) 
 
 
st.divider() 
 
 
# ========================================================= 
# CUSTOMER 360 
# ========================================================= 
 
st.header("👤 From Raw Tables to Customer 360") 
 
st.write( 
    """ 
    The most important transformation in the data preparation stage 
    is the movement from transaction-level records to a customer-level 
    analytical dataset. 
 
    A single customer can appear across multiple orders, order items, 
    payments and reviews. If these records were treated independently, 
    the analysis could overrepresent customers with more transactions. 
 
    CustomerPulse AI therefore aggregates relevant information around 
    the customer identity. This creates a consistent analytical grain 
    where one row represents one unique customer. 
    """ 
) 
 
 
st.success( 
    """ 
    Final Customer 360 grain: 
 
    One row = One unique customer 
    """ 
) 
 
 
# ========================================================= 
# CUSTOMER 360 DIMENSIONS 
# ========================================================= 
 
st.header("🧩 Customer 360 Dimensions") 
 
col1, col2, col3 = st.columns(3) 
 
with col1: 
 
    st.subheader("👤 Customer Profile") 
 
    st.write( 
        """ 
        Customer identifiers and geographical information provide 
        the basic profile required to distinguish and analyse 
        individual customers. 
        """ 
    ) 
 
 
with col2: 
 
    st.subheader("🛒 Purchase Behaviour") 
 
    st.write( 
        """ 
        Order count, purchase frequency, recency and tenure provide 
        a behavioural view of how customers interact with the 
        marketplace. 
        """ 
    ) 
 
 
with col3: 
 
    st.subheader("💰 Spending Behaviour") 
 
    st.write( 
        """ 
        Customer spending and related measures provide an economic 
        view of the customer's contribution to the business. 
        """ 
    ) 
 
 
col1, col2, col3 = st.columns(3) 
 
with col1: 
 
    st.subheader("⭐ Customer Experience") 
 
    st.write( 
        """ 
        Review-related measures provide an additional perspective 
        on customer experience and satisfaction. 
        """ 
    ) 
 
 
with col2: 
 
    st.subheader("🚚 Delivery Experience") 
 
    st.write( 
        """ 
        Delivery-related measures help capture the fulfilment 
        experience associated with customer orders. 
        """ 
    ) 
 
 
with col3: 
 
    st.subheader("💳 Payment Behaviour") 
 
    st.write( 
        """ 
        Payment information provides additional context about 
        transaction behaviour and customer purchasing patterns. 
        """ 
    ) 
 
 
st.divider() 
 
 
# ========================================================= 
# FINAL DATA FOUNDATION 
# ========================================================= 
 
st.header("🏗️ Final Data Foundation") 
 
st.write( 
    """ 
    After preparation and customer-level aggregation, the project 
    works with a consolidated Customer 360 dataset containing 
    96,096 unique customers. 
 
    This dataset becomes the common analytical foundation for the 
    subsequent stages of CustomerPulse AI. The same customer-level 
    foundation is then extended through feature engineering, 
    business analysis, segmentation and machine learning. 
    """ 
) 
 
 
col1, col2, col3 = st.columns(3) 
 
with col1: 
    st.metric( 
        "Unique Customers", 
        "96,096" 
    ) 
 
with col2: 
    st.metric( 
        "Customer-Level Records", 
        "96,096" 
    ) 
 
with col3: 
    st.metric( 
        "Analytical Grain", 
        "1 Row / Customer" 
    ) 
 
 
# ========================================================= 
# DATA JOURNEY SUMMARY 
# ========================================================= 
 
st.header("🔄 Data Journey") 
 
st.write( 
    """ 
    The complete data journey can be summarised as: 
 
    Olist Brazilian E-Commerce Dataset 
    → Data Understanding 
    → Data Cleaning 
    → Relevant Table Integration 
    → Customer-Level Aggregation 
    → Customer 360 
    → Feature Engineering 
    → SQL Analysis 
    → Segmentation 
    → Churn Prediction 
    → Retention Recommendation 
    → Power BI 
    """ 
) 
 
 
# ========================================================= 
# FINAL TAKEAWAY 
# ========================================================= 
 
st.header("💡 Dataset Takeaway") 
 
st.success( 
    """ 
    The strength of the Olist dataset for this project lies in its 
    relational structure. Instead of providing only sales records, 
    it captures multiple dimensions of the e-commerce customer 
    journey. 
 
    This allowed CustomerPulse AI to transform fragmented 
    transaction-level information into a unified customer-level 
    analytical foundation on which the complete churn and retention 
    workflow could be built. 
    """ 
) 