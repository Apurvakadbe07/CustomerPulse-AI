import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SQL Business Analysis",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 5px;
    color: #ffffff;
}

.subtitle {
    color: #b8c0cc;
    font-size: 16px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    margin-top: 30px;
    margin-bottom: 15px;
    color: #ffffff;
}

.question-box {
    background-color: #20212a;
    color: #e8eaf0;
    padding: 18px;
    border-radius: 10px;
    border-left: 4px solid #4f81bd;
    margin-bottom: 18px;
}

.question-box b {
    color: #ffffff;
}

.insight-box {
    background-color: #20212a;
    color: #e8eaf0;
    padding: 15px;
    border-radius: 8px;
    margin-top: 10px;
    border: 1px solid #343640;
}

.insight-box b {
    color: #ffffff;
}

.insight-box li {
    color: #e8eaf0;
}

.small-text {
    color: #b8c0cc;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():

    if "postgresql" in st.secrets:

        db_config = st.secrets["postgresql"]

        conn = psycopg2.connect(
            host=db_config["host"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            port=db_config.get("port", "5432")
        )

    else:

        st.error(
            "PostgreSQL connection is not configured. "
            "Please configure the database credentials in Streamlit secrets."
        )
        st.stop()

    return conn


@st.cache_data
def run_query(query):

    conn = get_connection()

    return pd.read_sql_query(query, conn)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">SQL Business Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Business analysis performed using PostgreSQL on the Customer 360 dataset'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATABASE STATUS
# ============================================================

try:

    conn = get_connection()

    customer_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total_customers FROM customer_360;",
        conn
    ).iloc[0, 0]

    st.success(
        f"PostgreSQL connected successfully | Customer 360 records: {customer_count:,}"
    )

except Exception as e:

    st.error("Unable to connect to PostgreSQL.")

    st.code(str(e))

    st.stop()


# ============================================================
# SECTION 1
# SQL ANALYSIS OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">SQL Analysis Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Dataset", "Customer 360")

with col2:
    st.metric("Customers", f"{customer_count:,}")

with col3:
    st.metric("Database", "PostgreSQL")

with col4:
    st.metric("Business Questions", "20")


st.markdown("""
The Customer 360 dataset was analysed using SQL to answer business questions
related to customer value, revenue, purchasing behaviour, customer experience,
customer risk and retention priorities.
""")


# ============================================================
# QUERY 1 – OVERALL BUSINESS HEALTH
# ============================================================

st.markdown(
    '<div class="section-title">1. Overall Business Health</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
What is the current overall health of the business in terms of customer base,
revenue, customer loyalty, and operational performance?
</div>
""", unsafe_allow_html=True)


q1 = """
SELECT 
    SUM(total_orders) AS total_orders,

    ROUND(SUM(total_spent)::NUMERIC, 2) AS total_revenue,

    ROUND(AVG(total_spent)::NUMERIC, 2) AS avg_customer_spending,

    ROUND(AVG(average_order_value)::NUMERIC, 2) AS avg_order_value,

    ROUND((AVG(average_review_score) * 1.0)::NUMERIC, 2) 
        AS avg_review_score,

    ROUND((AVG(on_time_delivery_rate) * 100)::NUMERIC, 2) 
        AS avg_on_time_delivery_rate,

    SUM(repeat_customer) AS repeat_customers,

    SUM(one_time_buyer) AS one_time_buyers,

    SUM(vip_customer) AS vip_customers,

    SUM(loyal_customer) AS loyal_customers,

    SUM(at_risk_customer) AS at_risk_customers

FROM customer_360;
"""

df1 = run_query(q1)

r = df1.iloc[0]

kpis = [
    ("Total Orders", f"{int(r['total_orders']):,}"),
    ("Total Revenue", f"₹{r['total_revenue']:,.2f}"),
    ("Avg Customer Spending", f"₹{r['avg_customer_spending']:,.2f}"),
    ("Avg Order Value", f"₹{r['avg_order_value']:,.2f}"),
    ("Avg Review Score", f"{r['avg_review_score']:.2f}"),
    ("On-Time Delivery", f"{r['avg_on_time_delivery_rate']:.2f}%"),
    ("Repeat Customers", f"{int(r['repeat_customers']):,}"),
    ("One-Time Buyers", f"{int(r['one_time_buyers']):,}"),
    ("VIP Customers", f"{int(r['vip_customers']):,}"),
    ("Loyal Customers", f"{int(r['loyal_customers']):,}"),
    ("At-Risk Customers", f"{int(r['at_risk_customers']):,}")
]

cols = st.columns(4)

for i, (label, value) in enumerate(kpis):

    with cols[i % 4]:
        st.metric(label, value)


st.markdown("""
<div class="insight-box">
<b>Business Insight:</b><br>
This analysis provides an overall view of customer activity, revenue,
customer loyalty and operational performance.
</div>
""", unsafe_allow_html=True)


# ============================================================
# QUERY 2
# CUSTOMER VALUE TIER
# ============================================================

st.markdown(
    '<div class="section-title">2. Customer Value Tier Performance & Risk</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customer value tiers contribute the highest revenue and contain the
highest number of at-risk customers?
</div>
""", unsafe_allow_html=True)


q2 = """
SELECT 
    customer_value_tier,

    COUNT(*) AS total_customers,

    SUM(total_orders) AS total_orders,

    ROUND(SUM(total_spent)::NUMERIC,2) AS total_revenue,

    ROUND(AVG(total_spent)::NUMERIC,2) AS avg_customer_spending,

    ROUND(AVG(average_order_value)::NUMERIC,2) AS avg_order_value,

    SUM(repeat_customer) AS repeat_customers,

    SUM(vip_customer) AS vip_customers,

    SUM(loyal_customer) AS loyal_customers,

    SUM(at_risk_customer) AS at_risk_customers,

    ROUND(
        (SUM(at_risk_customer)::NUMERIC / COUNT(*)) * 100,
        2
    ) AS at_risk_percentage

FROM customer_360

GROUP BY customer_value_tier

ORDER BY total_revenue DESC;
"""

df2 = run_query(q2)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        df2,
        x="customer_value_tier",
        y="total_revenue",
        title="Revenue by Customer Value Tier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q2_revenue"
    )

with col2:

    fig = px.bar(
        df2,
        x="customer_value_tier",
        y="at_risk_percentage",
        title="At-Risk Percentage by Value Tier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q2_risk"
    )

st.dataframe(
    df2,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 3
# STATE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">3. State-wise Revenue & Customer Risk</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which states generate the highest revenue but also have the highest percentage
of at-risk customers?
</div>
""", unsafe_allow_html=True)


q3 = """
SELECT 
    customer_state,

    COUNT(*) AS total_customers,

    ROUND(SUM(total_spent)::NUMERIC,2) AS total_revenue,

    ROUND(AVG(total_spent)::NUMERIC,2) AS avg_customer_spending,

    SUM(total_orders) AS total_orders,

    SUM(repeat_customer) AS repeat_customers,

    SUM(vip_customer) AS vip_customers,

    SUM(at_risk_customer) AS at_risk_customers,

    ROUND(
        (SUM(at_risk_customer)::NUMERIC / COUNT(*)) * 100,
        2
    ) AS at_risk_percentage

FROM customer_360

GROUP BY customer_state

HAVING COUNT(*) >= 100

ORDER BY total_revenue DESC;
"""

df3 = run_query(q3)

col1, col2 = st.columns(2)

with col1:

    top_states = df3.head(10)

    fig = px.bar(
        top_states,
        x="customer_state",
        y="total_revenue",
        title="Top States by Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q3_revenue"
    )

with col2:

    risk_states = df3.sort_values(
        "at_risk_percentage",
        ascending=False
    ).head(10)

    fig = px.bar(
        risk_states,
        x="customer_state",
        y="at_risk_percentage",
        title="States with Highest At-Risk Percentage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q3_risk"
    )

st.dataframe(
    df3,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 4
# MONTHLY REVENUE
# ============================================================

st.markdown(
    '<div class="section-title">4. Monthly Revenue & Customer Acquisition</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which months generated the highest revenue and acquired the most customers?
</div>
""", unsafe_allow_html=True)


q4 = """
WITH monthly_summary AS (

    SELECT

        DATE_TRUNC('month', first_purchase_date::DATE) AS purchase_month,

        COUNT(customer_unique_id) AS new_customers,

        SUM(total_orders) AS total_orders,

        ROUND(SUM(total_spent)::NUMERIC,2) AS total_revenue,

        ROUND(AVG(total_spent)::NUMERIC,2) AS avg_customer_spending,

        SUM(repeat_customer) AS repeat_customers,

        SUM(vip_customer) AS vip_customers

    FROM customer_360

    GROUP BY DATE_TRUNC('month', first_purchase_date::DATE)
)

SELECT *

FROM monthly_summary

ORDER BY purchase_month;
"""

df4 = run_query(q4)

col1, col2 = st.columns(2)

with col1:

    fig = px.line(
        df4,
        x="purchase_month",
        y="total_revenue",
        title="Monthly Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q4_revenue"
    )

with col2:

    fig = px.line(
        df4,
        x="purchase_month",
        y="new_customers",
        title="Monthly New Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q4_customers"
    )

st.dataframe(
    df4,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 5
# PARETO ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">5. Pareto Revenue Analysis</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers contribute to approximately 80% of the total revenue?
</div>
""", unsafe_allow_html=True)


q5 = """
WITH customer_revenue AS (

    SELECT
        customer_unique_id,
        total_spent

    FROM customer_360
),

pareto_analysis AS (

    SELECT
        customer_unique_id,
        total_spent,

        SUM(total_spent) OVER (
            ORDER BY total_spent DESC
        ) AS cumulative_revenue,

        SUM(total_spent) OVER () AS total_revenue,

        ROW_NUMBER() OVER (
            ORDER BY total_spent DESC
        ) AS customer_rank

    FROM customer_revenue
)

SELECT

    customer_rank,

    customer_unique_id,

    ROUND(total_spent::NUMERIC,2) AS customer_revenue,

    ROUND(cumulative_revenue::NUMERIC,2) AS cumulative_revenue,

    ROUND(
        (cumulative_revenue / total_revenue * 100)::NUMERIC,
        2
    ) AS cumulative_revenue_percentage

FROM pareto_analysis

WHERE cumulative_revenue <= total_revenue * 0.80

ORDER BY customer_rank

LIMIT 10;
"""

df5 = run_query(q5)

q5_summary = """
WITH customer_revenue AS (

    SELECT
        customer_unique_id,
        total_spent

    FROM customer_360
),

pareto_analysis AS (

    SELECT
        customer_unique_id,
        total_spent,

        SUM(total_spent) OVER (
            ORDER BY total_spent DESC
        ) AS cumulative_revenue,

        SUM(total_spent) OVER () AS total_revenue

    FROM customer_revenue
)

SELECT

    COUNT(*) AS customers_contributing_80_percent,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_360),
        2
    ) AS percentage_of_customer_base,

    ROUND(MAX(cumulative_revenue)::NUMERIC,2) AS revenue_covered,

    ROUND(MAX(total_revenue * 0.80)::NUMERIC,2)
        AS target_80_percent_revenue,

    ROUND(MAX(total_spent)::NUMERIC,2)
        AS highest_customer_revenue,

    ROUND(MIN(total_spent)::NUMERIC,2)
        AS lowest_customer_revenue

FROM pareto_analysis

WHERE cumulative_revenue <= total_revenue * 0.80;
"""

df5s = run_query(q5_summary)

st.dataframe(
    df5,
    use_container_width=True,
    hide_index=True
)

r5 = df5s.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Customers Contributing 80%",
        f"{int(r5['customers_contributing_80_percent']):,}"
    )

with c2:
    st.metric(
        "Customer Base %",
        f"{r5['percentage_of_customer_base']:.2f}%"
    )

with c3:
    st.metric(
        "Revenue Covered",
        f"₹{r5['revenue_covered']:,.2f}"
    )

with c4:
    st.metric(
        "Target 80% Revenue",
        f"₹{r5['target_80_percent_revenue']:,.2f}"
    )


# ============================================================
# QUERY 6
# HIGH SPENDING LOW FREQUENCY
# ============================================================

st.markdown(
    '<div class="section-title">6. High-Spending Customers with Low Purchase Frequency</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers spend the most but purchase infrequently?
</div>
""", unsafe_allow_html=True)


q6 = """
SELECT

    customer_unique_id,

    ROUND(total_spent::NUMERIC,2) AS total_spent,

    total_orders,

    ROUND(purchase_frequency::NUMERIC,2) AS purchase_frequency,

    ROUND(average_order_value::NUMERIC,2) AS average_order_value,

    recency_days,

    customer_value_tier

FROM customer_360

WHERE total_spent >
(
    SELECT PERCENTILE_CONT(0.95)
    WITHIN GROUP (ORDER BY total_spent)
    FROM customer_360
)

AND purchase_frequency <
(
    SELECT AVG(purchase_frequency)
    FROM customer_360
)

ORDER BY total_spent DESC

LIMIT 20;
"""

df6 = run_query(q6)

st.dataframe(
    df6,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 7
# CLV
# ============================================================

st.markdown(
    '<div class="section-title">7. Customer Lifetime Value by Customer Value Tier</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customer value tier generates the highest Customer Lifetime Value?
</div>
""", unsafe_allow_html=True)


q7 = """
SELECT

    customer_value_tier,

    COUNT(*) AS total_customers,

    ROUND(
        AVG(total_spent)::NUMERIC,2
    ) AS avg_customer_lifetime_value,

    ROUND(
        SUM(total_spent)::NUMERIC,2
    ) AS total_revenue,

    ROUND(
        AVG(total_orders)::NUMERIC,2
    ) AS avg_orders,

    ROUND(
        AVG(average_order_value)::NUMERIC,2
    ) AS avg_order_value,

    ROUND(
        AVG(customer_tenure_days)::NUMERIC,2
    ) AS avg_customer_tenure,

    SUM(vip_customer) AS vip_customers,

    SUM(loyal_customer) AS loyal_customers

FROM customer_360

GROUP BY customer_value_tier

ORDER BY avg_customer_lifetime_value DESC;
"""

df7 = run_query(q7)

fig = px.bar(
    df7,
    x="customer_value_tier",
    y="avg_customer_lifetime_value",
    title="Average Customer Lifetime Value by Tier"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="q7_clv"
)

st.dataframe(
    df7,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 8
# EARLY AT RISK
# ============================================================

st.markdown(
    '<div class="section-title">8. Early Identification of At-Risk Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers show early signs of becoming at-risk based on purchase frequency and recency?
</div>
""", unsafe_allow_html=True)


q8 = """
SELECT

    customer_unique_id,

    ROUND(total_spent::NUMERIC,2) AS total_spent,

    total_orders,

    ROUND(purchase_frequency::NUMERIC,2) AS purchase_frequency,

    recency_days,

    ROUND(average_order_value::NUMERIC,2) AS average_order_value,

    customer_value_tier

FROM customer_360

WHERE recency_days >
(
    SELECT PERCENTILE_CONT(0.75)
    WITHIN GROUP (ORDER BY recency_days)
    FROM customer_360
)

AND purchase_frequency <
(
    SELECT AVG(purchase_frequency)
    FROM customer_360
)

ORDER BY
    recency_days DESC,
    purchase_frequency ASC,
    total_spent DESC

LIMIT 20;
"""

df8 = run_query(q8)

st.dataframe(
    df8,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 9
# INACTIVE REPEAT CUSTOMERS
# ============================================================

st.markdown(
    '<div class="section-title">9. Inactive Repeat Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers have been inactive for the longest period despite previously making multiple purchases?
</div>
""", unsafe_allow_html=True)


q9 = """
SELECT

    customer_unique_id,

    total_orders,

    ROUND(total_spent::NUMERIC,2) AS total_spent,

    ROUND(average_order_value::NUMERIC,2) AS average_order_value,

    recency_days,

    ROUND(purchase_frequency::NUMERIC,2) AS purchase_frequency,

    customer_value_tier

FROM customer_360

WHERE total_orders >= 3

AND recency_days >
(
    SELECT PERCENTILE_CONT(0.90)
    WITHIN GROUP (ORDER BY recency_days)
    FROM customer_360
)

ORDER BY
    recency_days DESC,
    total_orders DESC,
    total_spent DESC

LIMIT 20;
"""

df9 = run_query(q9)

st.dataframe(
    df9,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 10
# HIGH AOV LOW FREQUENCY
# ============================================================

st.markdown(
    '<div class="section-title">10. High AOV – Low Frequency Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers have high Average Order Value but low purchase frequency?
</div>
""", unsafe_allow_html=True)


q10 = """
WITH percentile_values AS
(
    SELECT

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY average_order_value)
        AS high_aov_threshold,

        PERCENTILE_CONT(0.25)
        WITHIN GROUP (ORDER BY purchase_frequency)
        AS low_frequency_threshold

    FROM customer_360
),

customer_segments AS
(
    SELECT

        c.customer_unique_id,

        c.customer_city,

        c.customer_state,

        c.total_orders,

        c.total_spent,

        c.average_order_value,

        c.purchase_frequency,

        CASE

            WHEN c.average_order_value >= p.high_aov_threshold
            AND c.purchase_frequency <= p.low_frequency_threshold

            THEN 'High AOV - Low Frequency'

        END AS customer_segment

    FROM customer_360 c

    CROSS JOIN percentile_values p
)

SELECT

    customer_unique_id,

    customer_city,

    customer_state,

    total_orders,

    ROUND(total_spent::NUMERIC,2) AS total_spent,

    ROUND(average_order_value::NUMERIC,2) AS average_order_value,

    ROUND(purchase_frequency::NUMERIC,2) AS purchase_frequency

FROM customer_segments

WHERE customer_segment = 'High AOV - Low Frequency'

ORDER BY total_spent DESC

LIMIT 20;
"""

df10 = run_query(q10)

st.dataframe(
    df10,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 11
# REPEAT PURCHASE RATE
# ============================================================

st.markdown(
    '<div class="section-title">11. Repeat Purchase Rate by Customer Value Tier</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customer value tiers have the highest repeat purchase rate?
</div>
""", unsafe_allow_html=True)


q11 = """
SELECT

    customer_value_tier,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN repeat_customer = 1 THEN 1
            ELSE 0
        END
    ) AS repeat_customers,

    ROUND(
        (
            SUM(
                CASE
                    WHEN repeat_customer = 1 THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS repeat_purchase_rate

FROM customer_360

GROUP BY customer_value_tier

ORDER BY repeat_purchase_rate DESC;
"""

df11 = run_query(q11)

fig = px.bar(
    df11,
    x="customer_value_tier",
    y="repeat_purchase_rate",
    title="Repeat Purchase Rate by Value Tier"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="q11_repeat"
)

st.dataframe(
    df11,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 12
# DELIVERY DELAY
# ============================================================

st.markdown(
    '<div class="section-title">12. Impact of Delivery Delay on Customer Risk</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
How does delivery delay affect customer risk?
</div>
""", unsafe_allow_html=True)


q12 = """
SELECT

    delivery_delay_category,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN at_risk_customer = 1 THEN 1
            ELSE 0
        END
    ) AS at_risk_customers,

    ROUND(
        (
            SUM(
                CASE
                    WHEN at_risk_customer = 1 THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS at_risk_percentage,

    ROUND(
        AVG(average_review_score)::NUMERIC,
        2
    ) AS avg_review_score

FROM customer_360

GROUP BY delivery_delay_category

ORDER BY at_risk_percentage DESC;
"""

df12 = run_query(q12)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        df12,
        x="delivery_delay_category",
        y="at_risk_percentage",
        title="At-Risk Percentage by Delivery Delay"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q12_risk"
    )

with col2:

    fig = px.bar(
        df12,
        x="delivery_delay_category",
        y="avg_review_score",
        title="Review Score by Delivery Delay"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="q12_review"
    )

st.dataframe(
    df12,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 13
# REVIEW SCORE
# ============================================================

st.markdown(
    '<div class="section-title">13. Review Score, Repeat Purchases & Risk</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
How do review scores influence repeat purchases and at-risk behavior?
</div>
""", unsafe_allow_html=True)


q13 = """
SELECT

    CASE

        WHEN average_review_score >= 4.5
            THEN 'Excellent (4.5 - 5.0)'

        WHEN average_review_score >= 3.5
            THEN 'Good (3.5 - 4.49)'

        WHEN average_review_score >= 2.5
            THEN 'Average (2.5 - 3.49)'

        ELSE 'Poor (Below 2.5)'

    END AS review_category,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN repeat_customer = 1 THEN 1
            ELSE 0
        END
    ) AS repeat_customers,

    ROUND(
        (
            SUM(
                CASE
                    WHEN repeat_customer = 1 THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS repeat_purchase_rate,

    SUM(
        CASE
            WHEN at_risk_customer = 1 THEN 1
            ELSE 0
        END
    ) AS at_risk_customers,

    ROUND(
        (
            SUM(
                CASE
                    WHEN at_risk_customer = 1 THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS at_risk_percentage

FROM customer_360

GROUP BY review_category

ORDER BY repeat_purchase_rate DESC;
"""

df13 = run_query(q13)

fig = px.bar(
    df13,
    x="review_category",
    y="repeat_purchase_rate",
    title="Repeat Purchase Rate by Review Category"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="q13_repeat"
)

st.dataframe(
    df13,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 14
# STATE CANCELLATION
# ============================================================

st.markdown(
    '<div class="section-title">14. State-wise Cancellation Rate & Satisfaction</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which states have the highest cancellation rates and lowest customer satisfaction?
</div>
""", unsafe_allow_html=True)


q14 = """
SELECT

    customer_state,

    COUNT(*) AS total_customers,

    ROUND(
        AVG(cancel_rate)::NUMERIC,
        2
    ) AS avg_cancellation_rate,

    ROUND(
        AVG(average_review_score)::NUMERIC,
        2
    ) AS avg_review_score,

    ROUND(
        SUM(total_spent)::NUMERIC,
        2
    ) AS total_revenue

FROM customer_360

GROUP BY customer_state

HAVING COUNT(*) >= 100

ORDER BY
    avg_cancellation_rate DESC,
    avg_review_score ASC

LIMIT 20;
"""

df14 = run_query(q14)

fig = px.bar(
    df14,
    x="customer_state",
    y="avg_cancellation_rate",
    title="Cancellation Rate by State"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="q14_cancel"
)

st.dataframe(
    df14,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 15
# OVERALL RISK
# ============================================================

st.markdown(
    '<div class="section-title">15. Overall Customer Risk Distribution</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
What percentage of customers are classified as at-risk?
</div>
""", unsafe_allow_html=True)


q15 = """
SELECT

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN at_risk_customer = 1 THEN 1
            ELSE 0
        END
    ) AS at_risk_customers,

    ROUND(
        (
            SUM(
                CASE
                    WHEN at_risk_customer = 1 THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS at_risk_percentage

FROM customer_360;
"""

df15 = run_query(q15)

r15 = df15.iloc[0]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Customers",
        f"{int(r15['total_customers']):,}"
    )

with c2:
    st.metric(
        "At-Risk Customers",
        f"{int(r15['at_risk_customers']):,}"
    )

with c3:
    st.metric(
        "At-Risk Percentage",
        f"{r15['at_risk_percentage']:.2f}%"
    )


# ============================================================
# QUERY 16
# FACTORS ASSOCIATED WITH RISK
# ============================================================

st.markdown(
    '<div class="section-title">16. Factors Associated with At-Risk Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which factors are most strongly associated with at-risk customers?
</div>
""", unsafe_allow_html=True)


q16 = """
SELECT

    CASE
        WHEN at_risk_customer = 1
            THEN 'At Risk'
        ELSE 'Not At Risk'
    END AS customer_status,

    COUNT(*) AS total_customers,

    ROUND(
        AVG(average_review_score)::NUMERIC,
        2
    ) AS avg_review_score,

    ROUND(
        AVG(purchase_frequency)::NUMERIC,
        2
    ) AS avg_purchase_frequency,

    ROUND(
        AVG(average_delivery_delay)::NUMERIC,
        2
    ) AS avg_delivery_delay,

    ROUND(
        AVG(cancel_rate)::NUMERIC,
        4
    ) AS avg_cancellation_rate,

    ROUND(
        AVG(customer_tenure_days)::NUMERIC,
        2
    ) AS avg_customer_tenure

FROM customer_360

GROUP BY customer_status

ORDER BY total_customers DESC;
"""

df16 = run_query(q16)

st.dataframe(
    df16,
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div class="insight-box">
<b>Business Insight:</b><br>
Comparing at-risk and non-at-risk customers helps identify differences in
purchase behaviour, customer experience, cancellation behaviour and tenure.
</div>
""", unsafe_allow_html=True)


# ============================================================
# QUERY 17
# REVENUE AT RISK
# ============================================================

st.markdown(
    '<div class="section-title">17. Revenue Associated with At-Risk Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
How much revenue is associated with at-risk customers?
</div>
""", unsafe_allow_html=True)


q17 = """
SELECT

    COUNT(*) AS at_risk_customers,

    ROUND(
        SUM(total_spent)::NUMERIC,
        2
    ) AS revenue_at_risk,

    ROUND(
        AVG(total_spent)::NUMERIC,
        2
    ) AS average_revenue_per_customer,

    ROUND(
        (
            SUM(total_spent)
            /
            (
                SELECT SUM(total_spent)
                FROM customer_360
            )
        )::NUMERIC * 100,
        2
    ) AS revenue_at_risk_percentage

FROM customer_360

WHERE at_risk_customer = 1;
"""

df17 = run_query(q17)

r17 = df17.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "At-Risk Customers",
        f"{int(r17['at_risk_customers']):,}"
    )

with c2:
    st.metric(
        "Revenue at Risk",
        f"₹{r17['revenue_at_risk']:,.2f}"
    )

with c3:
    st.metric(
        "Avg Revenue / Customer",
        f"₹{r17['average_revenue_per_customer']:,.2f}"
    )

with c4:
    st.metric(
        "Revenue at Risk %",
        f"{r17['revenue_at_risk_percentage']:.2f}%"
    )


# ============================================================
# QUERY 18
# VIP HIGH SPENDER RISK
# ============================================================

st.markdown(
    '<div class="section-title">18. High-Risk VIP & High-Spending Customers</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which VIP and high-spending customers are at the highest risk?
</div>
""", unsafe_allow_html=True)


q18 = """
SELECT

    customer_unique_id,

    customer_city,

    customer_state,

    ROUND(total_spent::NUMERIC,2) AS total_spent,

    customer_value_tier,

    vip_customer,

    high_spender,

    recency_days,

    ROUND(
        average_review_score::NUMERIC,2
    ) AS review_score,

    ROUND(
        average_delivery_delay::NUMERIC,2
    ) AS delivery_delay

FROM customer_360

WHERE at_risk_customer = 1

AND (vip_customer = 1 OR high_spender = 1)

ORDER BY
    total_spent DESC,
    recency_days DESC

LIMIT 20;
"""

df18 = run_query(q18)

st.dataframe(
    df18,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 19
# CUSTOMER RISK SCORE
# ============================================================

st.markdown(
    '<div class="section-title">19. Customer Risk Score Model</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
How can customers be classified into Low, Medium, and High Risk using key
behavioral and experience metrics?
</div>
""", unsafe_allow_html=True)


q19 = """
WITH customer_risk_score AS (

    SELECT

        customer_unique_id,

        customer_city,

        customer_state,

        total_spent,

        recency_days,

        purchase_frequency,

        average_review_score,

        average_delivery_delay,

        (
            CASE
                WHEN recency_days >= 365 THEN 20
                WHEN recency_days >= 180 THEN 15
                WHEN recency_days >= 90 THEN 10
                ELSE 0
            END +

            CASE
                WHEN purchase_frequency < 0.50 THEN 20
                WHEN purchase_frequency < 1.00 THEN 10
                ELSE 0
            END +

            CASE
                WHEN total_spent < 100 THEN 20
                WHEN total_spent < 300 THEN 10
                ELSE 0
            END +

            CASE
                WHEN average_review_score < 2 THEN 20
                WHEN average_review_score < 3 THEN 15
                WHEN average_review_score < 4 THEN 10
                ELSE 0
            END +

            CASE
                WHEN average_delivery_delay > 10 THEN 20
                WHEN average_delivery_delay > 5 THEN 10
                ELSE 0
            END
        ) AS risk_score

    FROM customer_360
)

SELECT

    customer_unique_id,

    customer_city,

    customer_state,

    ROUND(
        total_spent::NUMERIC,2
    ) AS total_spent,

    recency_days,

    ROUND(
        purchase_frequency::NUMERIC,2
    ) AS purchase_frequency,

    ROUND(
        average_review_score::NUMERIC,2
    ) AS review_score,

    ROUND(
        average_delivery_delay::NUMERIC,2
    ) AS delivery_delay,

    risk_score,

    CASE

        WHEN risk_score >= 50
            THEN 'High Risk'

        WHEN risk_score >= 25
            THEN 'Medium Risk'

        ELSE 'Low Risk'

    END AS risk_category

FROM customer_risk_score

ORDER BY
    risk_score DESC,
    total_spent DESC

LIMIT 20;
"""

df19 = run_query(q19)

st.dataframe(
    df19,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# QUERY 20
# RETENTION PRIORITY
# ============================================================

st.markdown(
    '<div class="section-title">20. Priority Customers for Retention Campaigns</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="question-box">
<b>Business Question:</b><br>
Which customers should be targeted first for retention campaigns based on
high spending, high recency, low purchase frequency, low review score,
high delivery delay, and high cancellation rate?
</div>
""", unsafe_allow_html=True)


q20 = """
WITH retention_priority AS (

    SELECT

        customer_unique_id,

        customer_city,

        customer_state,

        total_spent,

        recency_days,

        purchase_frequency,

        average_review_score,

        average_delivery_delay,

        cancel_rate,

        customer_value_tier,

        (
            CASE
                WHEN total_spent >= 1000 THEN 25
                WHEN total_spent >= 500 THEN 15
                ELSE 5
            END +

            CASE
                WHEN recency_days >= 365 THEN 20
                WHEN recency_days >= 180 THEN 10
                ELSE 0
            END +

            CASE
                WHEN purchase_frequency < 0.50 THEN 20
                WHEN purchase_frequency < 1 THEN 10
                ELSE 0
            END +

            CASE
                WHEN average_review_score < 2 THEN 15
                WHEN average_review_score < 3 THEN 10
                WHEN average_review_score < 4 THEN 5
                ELSE 0
            END +

            CASE
                WHEN average_delivery_delay > 10 THEN 10
                WHEN average_delivery_delay > 5 THEN 5
                ELSE 0
            END +

            CASE
                WHEN cancel_rate >= 0.50 THEN 10
                WHEN cancel_rate >= 0.20 THEN 5
                ELSE 0
            END

        ) AS retention_score

    FROM customer_360
)

SELECT

    customer_unique_id,

    customer_city,

    customer_state,

    ROUND(
        total_spent::NUMERIC,2
    ) AS total_spent,

    recency_days,

    ROUND(
        purchase_frequency::NUMERIC,2
    ) AS purchase_frequency,

    ROUND(
        average_review_score::NUMERIC,2
    ) AS review_score,

    ROUND(
        average_delivery_delay::NUMERIC,2
    ) AS delivery_delay,

    ROUND(
        cancel_rate::NUMERIC,2
    ) AS cancellation_rate,

    customer_value_tier,

    retention_score,

    CASE

        WHEN retention_score >= 70
            THEN 'Immediate Action'

        WHEN retention_score >= 50
            THEN 'High Priority'

        WHEN retention_score >= 30
            THEN 'Medium Priority'

        ELSE 'Low Priority'

    END AS retention_priority

FROM retention_priority

ORDER BY
    retention_score DESC,
    total_spent DESC

LIMIT 20;
"""

df20 = run_query(q20)

st.dataframe(
    df20,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FINAL SQL FINDINGS
# ============================================================

st.markdown(
    '<div class="section-title">SQL Analysis Summary</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="insight-box">

<b>Key Areas Covered:</b>

<ul>
<li>Overall business performance</li>
<li>Customer value and revenue contribution</li>
<li>Geographic revenue and risk</li>
<li>Monthly customer acquisition and revenue</li>
<li>Revenue concentration through Pareto analysis</li>
<li>Customer purchasing behaviour</li>
<li>Customer Lifetime Value</li>
<li>Inactive and early-risk customers</li>
<li>Repeat purchase behaviour</li>
<li>Delivery and review experience</li>
<li>Cancellation behaviour</li>
<li>Revenue exposure from at-risk customers</li>
<li>High-value customers at risk</li>
<li>SQL-based customer risk scoring</li>
<li>Retention campaign prioritisation</li>
</ul>

</div>
""", unsafe_allow_html=True)


st.markdown("---")

st.caption(
    "SQL Business Analysis | Customer 360 Dataset | PostgreSQL"
)