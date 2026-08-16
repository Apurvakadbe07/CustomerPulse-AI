import streamlit as st


# ============================================================
# CUSTOMERPULSE AI — HOME PAGE
# ============================================================

st.set_page_config(
    page_title="CustomerPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 CustomerPulse AI")

st.sidebar.caption(
    "Customer Churn Prediction & "
    "Retention Intelligence Platform"
)

st.sidebar.divider()

st.sidebar.subheader("Project Navigation")

st.sidebar.write(
    "Explore the complete customer analytics, churn prediction "
    "and retention intelligence workflow using the pages "
    "available in the sidebar."
)

st.sidebar.divider()

st.sidebar.caption(
    "Customer Analytics • Churn Prediction • Retention Intelligence"
)


# ============================================================
# GENERAL PAGE SPACING
# ============================================================

st.write("")
st.write("")


# ============================================================
# HERO SECTION
# ============================================================

with st.container(border=True):

    st.caption(
        "CUSTOMER ANALYTICS • CHURN INTELLIGENCE • RETENTION"
    )

    st.title("CustomerPulse AI")

    st.subheader(
        "Customer Churn Prediction & Retention Intelligence Platform"
    )

    st.write(
        "A complete customer analytics solution that transforms "
        "e-commerce data into actionable customer intelligence. "
        "The project combines data cleaning, Customer 360 analysis, "
        "SQL business analysis, customer segmentation, churn prediction, "
        "retention recommendations and Power BI reporting to identify "
        "customer risk, understand revenue exposure and support "
        "data-driven retention decisions."
    )


# ============================================================
# HERO METRICS
# ============================================================

st.write("")

hero1, hero2, hero3 = st.columns(3)

with hero1:

    st.metric(
        "Analytical Focus",
        "Customer Intelligence"
    )

with hero2:

    st.metric(
        "Prediction Focus",
        "Churn Risk"
    )

with hero3:

    st.metric(
        "Decision Focus",
        "Retention"
    )


st.write("")
st.divider()
st.write("")


# ============================================================
# INTRODUCTION
# ============================================================

st.header("From Customer Data to Business Decisions")

st.write(
    "CustomerPulse AI brings together the major stages of a "
    "customer analytics workflow into one connected project. "
    "The journey begins with the raw e-commerce dataset and "
    "progresses through data preparation, customer intelligence, "
    "exploratory analysis, SQL analysis, segmentation, churn "
    "prediction, retention recommendations and final business "
    "reporting."
)

st.info(
    "The central idea is simple: understand the customer, "
    "identify churn exposure, understand customer value and "
    "support focused retention decisions."
)

st.write("")


# ============================================================
# WHY CUSTOMERPULSE AI MATTERS
# ============================================================

st.header("Why CustomerPulse AI Matters")

st.write("")

importance1, importance2, importance3 = st.columns(3)


with importance1:

    with st.container(border=True):

        st.caption("01 · CUSTOMER VIEW")

        st.subheader("Understand Customers")

        st.write(
            "Customer-level analysis provides a structured view "
            "of customer behaviour instead of looking at individual "
            "transactions in isolation."
        )


with importance2:

    with st.container(border=True):

        st.caption("02 · RISK VIEW")

        st.subheader("Identify Churn Exposure")

        st.write(
            "Churn prediction provides a systematic way to identify "
            "customers with higher exposure to customer loss."
        )


with importance3:

    with st.container(border=True):

        st.caption("03 · ACTION VIEW")

        st.subheader("Support Retention Decisions")

        st.write(
            "Retention recommendations connect customer intelligence "
            "with practical business planning."
        )


st.write("")
st.write("")


# ============================================================
# PROJECT JOURNEY
# ============================================================

st.header("Project Journey")

st.caption(
    "The complete analytical flow followed in CustomerPulse AI."
)

st.write("")


# -------------------------
# ROW 1
# -------------------------

row1 = st.columns(3)

with row1[0]:

    with st.container(border=True):

        st.caption("01")

        st.subheader("Raw Dataset")


with row1[1]:

    with st.container(border=True):

        st.caption("02")

        st.subheader("Data Cleaning")


with row1[2]:

    with st.container(border=True):

        st.caption("03")

        st.subheader("Customer 360 Intelligence")


st.write("")


# -------------------------
# ROW 2
# -------------------------

row2 = st.columns(3)

with row2[0]:

    with st.container(border=True):

        st.caption("04")

        st.subheader("Exploratory Data Analysis")


with row2[1]:

    with st.container(border=True):

        st.caption("05")

        st.subheader("SQL Analysis")


with row2[2]:

    with st.container(border=True):

        st.caption("06")

        st.subheader("Customer Segmentation & RFM Analysis")


st.write("")


# -------------------------
# ROW 3
# -------------------------

row3 = st.columns(3)

with row3[0]:

    with st.container(border=True):

        st.caption("07")

        st.subheader("Churn Prediction")


with row3[1]:

    with st.container(border=True):

        st.caption("08")

        st.subheader("AI Retention Recommendation")


with row3[2]:

    with st.container(border=True):

        st.caption("09")

        st.subheader("Final Power BI Report")


st.write("")
st.write("")


# ============================================================
# HOW THE PROJECT PROGRESSES
# ============================================================

st.header("How the Project Progresses")

st.write("")

progress1, progress2, progress3, progress4 = st.columns(4)


with progress1:

    st.subheader("Understand")

    st.write(
        "Build customer intelligence from the available "
        "e-commerce data."
    )


with progress2:

    st.subheader("Analyse")

    st.write(
        "Explore customer behaviour and perform structured "
        "business analysis."
    )


with progress3:

    st.subheader("Predict")

    st.write(
        "Use the completed churn prediction workflow to "
        "identify churn exposure."
    )


with progress4:

    st.subheader("Act")

    st.write(
        "Translate customer risk into retention-focused "
        "recommendations and planning."
    )


st.write("")
st.write("")


# ============================================================
# PROJECT VALUE
# ============================================================

st.header("What Makes the Workflow Valuable")

st.write("")

value1, value2 = st.columns(2)


with value1:

    with st.container(border=True):

        st.subheader("Connected Customer View")

        st.write(
            "The project connects customer information, purchasing "
            "behaviour, customer value and churn-related information "
            "into a customer-level analytical workflow."
        )


    with st.container(border=True):

        st.subheader("From Analysis to Action")

        st.write(
            "The workflow continues beyond analysis and prediction "
            "into retention recommendations and operational planning."
        )


with value2:

    with st.container(border=True):

        st.subheader("Risk With Business Context")

        st.write(
            "Churn risk is considered alongside customer-level "
            "information to support more focused retention planning."
        )


    with st.container(border=True):

        st.subheader("Decision-Oriented Reporting")

        st.write(
            "The final reporting layer brings the completed analysis "
            "together into an interactive business intelligence "
            "environment."
        )


st.write("")
st.write("")


# ============================================================
# PROJECT OUTPUT LAYERS
# ============================================================

st.header("Project Output Layers")

st.write("")

out1, out2, out3, out4 = st.columns(4)


with out1:

    st.subheader("Customer Intelligence")

    st.caption(
        "Customer-level analytical foundation"
    )


with out2:

    st.subheader("Churn Intelligence")

    st.caption(
        "Customer churn risk and prediction"
    )


with out3:

    st.subheader("Retention Intelligence")

    st.caption(
        "Recommendations and action planning"
    )


with out4:

    st.subheader("Business Reporting")

    st.caption(
        "Interactive Power BI reporting"
    )


st.write("")
st.write("")


# ============================================================
# TECHNOLOGY
# ============================================================

st.header("Technology & Analytical Stack")

st.write("")

tech1, tech2, tech3, tech4 = st.columns(4)


with tech1:

    st.subheader("Python")

    st.caption(
        "Data analysis and modelling"
    )


with tech2:

    st.subheader("SQL / PostgreSQL")

    st.caption(
        "Structured business analysis"
    )


with tech3:

    st.subheader("Machine Learning")

    st.caption(
        "Churn prediction workflow"
    )


with tech4:

    st.subheader("Streamlit / Power BI")

    st.caption(
        "Application and reporting"
    )


st.write("")
st.write("")


# ============================================================
# FINAL PROJECT STATEMENT
# ============================================================

st.divider()

st.write("")

st.header("CustomerPulse AI at a Glance")

st.write("")

st.success(
    "Raw Dataset → Data Cleaning → Customer 360 Intelligence → "
    "EDA → SQL Analysis → Customer Segmentation & RFM Analysis → "
    "Churn Prediction → AI Retention Recommendation → "
    "Final Power BI Report"
)

st.write("")

st.write(
    "Use the sidebar to explore each stage of the completed "
    "CustomerPulse AI project."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CustomerPulse AI · Customer Churn Prediction & "
    "Retention Intelligence Platform"
)