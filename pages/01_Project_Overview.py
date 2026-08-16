import streamlit as st

st.set_page_config(
    page_title="CustomerPulse AI",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📊 CustomerPulse AI")

st.subheader(
    "AI-Powered Customer Churn Prediction & Retention Intelligence Platform"
)

st.write(
    """
    CustomerPulse AI is an end-to-end customer analytics project
    developed to understand customer behaviour, identify customers
    exposed to churn, evaluate the business value associated with
    those customers, and support focused retention decisions.
    """
)

st.divider()


# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.header("📌 Project Overview")

st.write(
    """
    CustomerPulse AI addresses a common challenge in e-commerce:
    a business can have a large amount of customer and transaction
    data, but still lack a clear understanding of which customers
    are becoming inactive, which customers are more likely to churn,
    and which of those customers are important from a business
    perspective.

    The project uses the Olist Brazilian E-Commerce dataset to
    construct a customer-level analytical view from transactional
    records. Instead of analysing individual orders in isolation,
    the project consolidates customer information, purchasing
    behaviour, spending patterns, reviews, delivery experience and
    other relevant characteristics into a unified Customer 360 view.

    This customer-level foundation is then used for exploratory
    analysis, SQL-based business analysis, customer segmentation
    and churn prediction. The final outputs connect customer risk
    with customer value so that retention efforts can be prioritised
    more effectively.
    """
)


# =========================================================
# BUSINESS CONTEXT
# =========================================================

st.header("🏢 Business Context")

st.write(
    """
    E-commerce businesses operate in an environment where customer
    behaviour directly influences long-term revenue. Every order,
    payment, review and delivery interaction creates information
    about the relationship between the customer and the business.

    However, transaction-level data does not automatically provide
    a complete picture of customer health. A customer may have
    purchased multiple times in the past but gradually reduce
    purchase activity. Another customer may have a high historical
    spend but show signs of becoming inactive.

    From a business perspective, these situations are important
    because customer churn is not simply a loss of one transaction.
    Repeated customer relationships can represent a meaningful
    source of revenue, and losing valuable customers can create
    significant business exposure.

    Therefore, the business needs a structured way to understand
    customer behaviour, identify potential churn risk, measure
    the value associated with that risk and determine where
    retention efforts should be concentrated.
    """
)


# =========================================================
# BUSINESS PROBLEM
# =========================================================

st.header("⚠️ Business Problem")

st.write(
    """
    The central business problem is the difficulty of identifying
    and prioritising customers who may churn within a large
    e-commerce customer base.

    The available data contains information about customers,
    orders, payments, reviews, products and delivery. However,
    these datasets individually describe only parts of the
    customer journey.

    The business therefore faces a larger analytical challenge:
    converting fragmented historical transaction records into
    a reliable customer-level understanding that can support
    retention decisions.
    """
)


# =========================================================
# BUSINESS CHALLENGES
# =========================================================

st.subheader("1. Fragmented Customer Information")

st.write(
    """
    Customer information is distributed across multiple datasets.
    Customer records, orders, payments, reviews and delivery
    information need to be connected before the business can
    obtain a complete view of an individual customer.

    Without this consolidation, important behavioural signals
    remain separated across different tables and are difficult
    to interpret together.
    """
)


st.subheader("2. Difficulty Understanding Customer Behaviour")

st.write(
    """
    Customers do not behave in the same way. Some customers
    purchase repeatedly, some purchase only once, and others
    gradually reduce their activity over time.

    Understanding these differences requires more than simply
    counting orders. Recency, purchase frequency, spending,
    tenure and customer experience need to be considered together.
    """
)


st.subheader("3. Churn Risk Is Not Directly Visible")

st.write(
    """
    Historical transaction data shows what customers have already
    done, but it does not directly tell the business which customers
    are most likely to stop purchasing.

    A systematic predictive approach is therefore required to
    identify patterns associated with customer churn and estimate
    the likelihood of future customer loss.
    """
)


st.subheader("4. Customers Have Different Business Value")

st.write(
    """
    Every customer does not contribute the same amount of revenue.
    A high-spending customer and a low-spending customer may have
    similar churn risk but very different business importance.

    Therefore, churn risk needs to be interpreted together with
    customer value rather than treating every at-risk customer
    equally.
    """
)


st.subheader("5. Churn Creates Revenue Exposure")

st.write(
    """
    Customer churn is not only a customer-count problem. When
    customers with meaningful purchasing history become inactive,
    the business can also face potential revenue exposure.

    Measuring revenue associated with at-risk customers provides
    a stronger business perspective on the scale of the retention
    problem.
    """
)


st.subheader("6. Retention Efforts Need Prioritisation")

st.write(
    """
    A business cannot necessarily apply the same retention effort
    to every customer. Resources such as discounts, campaigns and
    personalised communication need to be directed towards
    customers where intervention can have greater business value.

    This creates the need for a structured risk and priority
    framework.
    """
)


st.divider()


# =========================================================
# CORE BUSINESS QUESTION
# =========================================================

st.header("🎯 Core Business Question")

st.info(
    """
    Which customers are likely to leave, how much business value
    is exposed, and where should retention efforts be focused first?
    """
)

st.write(
    """
    This question defines the direction of the complete project.
    The objective is not simply to calculate a churn percentage
    or build a machine learning model.

    The objective is to understand the customer behind the risk.
    Customer behaviour explains how the customer has interacted
    with the business, churn prediction estimates the level of
    risk, and customer value helps determine the potential
    business importance of that risk.

    Combining these perspectives creates a more meaningful basis
    for retention decision-making.
    """
)


# =========================================================
# PROJECT OBJECTIVES
# =========================================================

st.header("🎯 Project Objectives")

st.write(
    """
    The primary objective of CustomerPulse AI is to develop a
    complete analytical pipeline that moves from raw e-commerce
    transaction data to customer-level intelligence and finally
    to retention-focused business decisions.
    """
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Customer Intelligence")

    st.write(
        """
        Build a unified Customer 360 view that captures customer
        profile, purchasing behaviour, spending, reviews, delivery
        experience, tenure and other relevant characteristics.

        The purpose is to replace fragmented transaction-level
        information with a consolidated view of each customer.
        """
    )

with col2:

    st.subheader("Churn Intelligence")

    st.write(
        """
        Identify customers who show higher exposure to churn and
        use predictive modelling to estimate churn probability.

        The purpose is to provide the business with a consistent
        method for identifying customers who may require attention.
        """
    )


# =========================================================
# WHAT WE SOLVED
# =========================================================

st.header("✅ What We Solved")

st.write(
    """
    The project addresses the business problem through several
    connected analytical layers. Each layer solves a specific
    limitation of the raw data and prepares the foundation for
    the next stage.
    """
)

st.subheader("From Fragmented Data to Customer 360")

st.write(
    """
    Multiple e-commerce datasets were consolidated to create a
    customer-level analytical dataset. This provides a unified
    foundation for understanding individual customer behaviour
    instead of analysing isolated transactions.
    """
)

st.subheader("From Historical Behaviour to Churn Risk")

st.write(
    """
    Customer behavioural features were used to build predictive
    models capable of identifying customers with higher probability
    of churn. Multiple classification models were evaluated before
    selecting the final model.
    """
)

st.subheader("From Churn Risk to Business Value")

st.write(
    """
    Churn exposure was analysed together with customer spending
    and value tiers. This allows the business to understand not
    only how many customers are at risk, but also the financial
    importance of those customers.
    """
)

st.subheader("From Prediction to Retention Priority")

st.write(
    """
    The project extends the analysis beyond prediction by creating
    risk segments, priorities and retention recommendations.
    This provides a pathway from analytical output towards
    practical retention planning.
    """
)


# =========================================================
# ANALYTICAL JOURNEY
# =========================================================
# =========================================================
# ANALYTICAL JOURNEY
# =========================================================

st.header("🔄 Analytical Journey")

st.write(
    """
    CustomerPulse AI follows a structured end-to-end analytical
    workflow. Each stage builds on the previous stage and moves
    the project from raw e-commerce data towards customer
    intelligence, churn prediction, retention recommendations
    and final business reporting.
    """
)

# ---------------------------------------------------------
# 01 — RAW DATASET
# ---------------------------------------------------------

st.subheader("01 — Raw E-Commerce Dataset")

st.write(
    """
    The project starts with the Olist Brazilian E-Commerce
    dataset containing the underlying customer, order, payment,
    product, review, delivery and seller information required
    for customer-level analysis.
    """
)

# ---------------------------------------------------------
# 02 — DATA CLEANING
# ---------------------------------------------------------

st.subheader("02 — Data Cleaning & Preparation")

st.write(
    """
    The raw datasets are examined and prepared for analysis.
    Data-quality issues such as missing values, duplicate records,
    inconsistent data and unsuitable data types are addressed
    before the datasets are used in subsequent analytical stages.
    """
)

# ---------------------------------------------------------
# 03 — CUSTOMER 360 INTELLIGENCE
# ---------------------------------------------------------

st.subheader("03 — Customer 360 Intelligence")

st.write(
    """
    Relevant information is consolidated at the customer level
    to create a unified Customer 360 view. The resulting dataset
    brings together customer profile information, purchasing
    behaviour, spending, reviews, delivery experience, tenure
    and other customer-level characteristics.
    """
)

# ---------------------------------------------------------
# 04 — EXPLORATORY DATA ANALYSIS
# ---------------------------------------------------------

st.subheader("04 — Exploratory Data Analysis")

st.write(
    """
    The prepared customer-level data is explored through
    descriptive analysis and visualisation to understand
    customer behaviour, purchasing patterns, spending,
    customer experience and other important characteristics
    present in the dataset.
    """
)

# ---------------------------------------------------------
# 05 — SQL ANALYSIS
# ---------------------------------------------------------

st.subheader("05 — SQL Business Analysis")

st.write(
    """
    SQL is used to answer structured business questions from
    the customer-level data, including customer exposure,
    customer value, spending and revenue-related analysis.
    """
)

# ---------------------------------------------------------
# 06 — CUSTOMER SEGMENTATION & RFM ANALYSIS
# ---------------------------------------------------------

st.subheader("06 — Customer Segmentation & RFM Analysis")

st.write(
    """
    Customers are analysed and differentiated using customer
    behaviour and value characteristics. RFM analysis provides
    a structured view using Recency, Frequency and Monetary
    behaviour, supporting meaningful customer segmentation
    and value-based interpretation.
    """
)

# ---------------------------------------------------------
# 07 — CHURN PREDICTION
# ---------------------------------------------------------

st.subheader("07 — Churn Prediction")

st.write(
    """
    Machine learning is applied to the prepared customer-level
    features to predict customer churn risk. Multiple
    classification models are evaluated and the finalized
    churn prediction workflow is used to identify customers
    with higher churn exposure.
    """
)

# ---------------------------------------------------------
# 08 — AI RETENTION RECOMMENDATION
# ---------------------------------------------------------

st.subheader("08 — AI Retention Recommendation")

st.write(
    """
    The churn and customer intelligence outputs are carried
    forward into the retention stage, where customer-specific
    retention recommendations and priorities are provided
    through the finalized retention recommendation workflow.
    """
)

# ---------------------------------------------------------
# 09 — FINAL POWER BI REPORT
# ---------------------------------------------------------

st.subheader("09 — Final Power BI Report")

st.write(
    """
    The completed customer intelligence, churn, revenue risk
    and retention outputs are presented through the final
    Power BI reporting layer, providing an interactive
    business-facing view of the project results.
    """
)

st.divider()


# =========================================================
# KEY PROJECT RESULTS
# =========================================================

st.header("📊 Key Project Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Customers Analysed", "96,096")

with col2:
    st.metric("Customers at Risk", "68,352")

with col3:
    st.metric("At-Risk Percentage", "71.13%")

with col4:
    st.metric("Revenue at Risk", "₹11.26M")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("High-Risk Customers", "11,961")

with col2:
    st.metric("XGBoost Recall", "95.62%")

with col3:
    st.metric("XGBoost F1 Score", "85.59%")


# =========================================================
# BUSINESS INTERPRETATION
# =========================================================

st.header("💼 Business Interpretation")

st.write(
    """
    The analysis identified 68,352 customers as being at risk,
    representing 71.13% of the analysed customer base. This
    indicates that customer churn exposure is significant and
    requires structured attention.
    """
)

st.write(
    """
    However, the number of at-risk customers alone does not
    determine the business priority. Customer value also needs
    to be considered because customers contribute different
    levels of revenue.
    """
)

st.write(
    """
    A high-value customer with elevated churn risk represents
    a different business situation from a low-value customer
    with similar risk. Therefore, the project connects customer
    value with churn risk to provide a more meaningful basis
    for retention prioritisation.
    """
)


# =========================================================
# FINAL TAKEAWAY
# =========================================================

st.header("🏁 Final Business Takeaway")

st.success(
    """
    CustomerPulse AI moves the business from simply understanding
    historical customer transactions towards identifying which
    customers require attention, understanding their potential
    business importance and supporting focused retention decisions.
    """
)

st.write(
    """
    The project ultimately connects four important layers:
    customer behaviour, customer value, churn risk and retention
    priority.

    This creates a complete analytical path from raw data to
    business decision-making.
    """
)