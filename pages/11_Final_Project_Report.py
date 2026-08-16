import streamlit as st
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CustomerPulse | Final Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATASET = (
    PROJECT_ROOT
    / "2 Notebook"
    / "outputs"
    / "customer_360_final.csv"
)

PAGE_1_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "dashboard1.png"
)

PAGE_2_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "dashboard2.png"
)

PAGE_3_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "dashboard3.png"
)


# ============================================================
# DATASET CHECK
# ============================================================

if not FINAL_DATASET.exists():
    st.error("Final dataset customer_360_final.csv was not found.")
    st.stop()


# ============================================================
# VISUAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       BACKGROUND
       ======================================================== */

    .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        font-size: 46px !important;
        font-weight: 750 !important;
    }

    h2 {
        font-size: 31px !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 23px !important;
        font-weight: 650 !important;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    .stMarkdown p {
        font-size: 17px !important;
        line-height: 1.7 !important;
    }

    .stCaption {
        font-size: 14px !important;
    }


    /* ========================================================
       REPORT LABEL
       ======================================================== */

    .report-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #8fb7ff;
        text-transform: uppercase;
        margin-bottom: 7px;
    }


    /* ========================================================
       PAGE BADGE
       ======================================================== */

    .page-badge {
        background-color: #18253a;
        border: 1px solid #30425e;
        border-radius: 9px;
        padding: 7px 13px;
        display: inline-block;
        color: #9fc1ff;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }


    /* ========================================================
       SECTION LABEL
       ======================================================== */

    .section-label {
        color: #8fb7ff;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-top: 27px;
        margin-bottom: 5px;
    }


    /* ========================================================
       DASHBOARD LABEL
       ======================================================== */

    .dashboard-label {
        color: #aeb9ca;
        font-size: 14px;
        margin-bottom: 9px;
    }


    /* ========================================================
       INSIGHT BOX
       ======================================================== */

    .insight-box {
        background-color: #111b2d;
        border: 1px solid #263852;
        border-radius: 14px;
        padding: 20px 22px;
        margin: 10px 0 15px 0;
        min-height: 150px;
    }

    .insight-number {
        color: #83adff;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 7px;
    }

    .insight-title {
        color: white;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .insight-description {
        color: #d4dce8;
        font-size: 15.5px;
        line-height: 1.65;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border: none !important;
        border-top: 1px solid #26364d !important;
        margin: 32px 0 !important;
    }


    /* ========================================================
       FINAL BOX
       ======================================================== */

    .final-box {
        background-color: #111b2d;
        border: 1px solid #30425e;
        border-radius: 15px;
        padding: 24px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCTIONS
# ============================================================

def show_dashboard(image_path, name):

    if image_path.exists():

        st.caption(
            f"{name} • Power BI Report"
        )

        st.image(
            str(image_path),
            use_container_width=True
        )

    else:

        st.warning(
            f"{name} dashboard image was not found."
        )


def show_insight(number, title, text):

    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-number">INSIGHT {number}</div>
            <div class="insight-title">{title}</div>
            <div class="insight-description">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="report-label">FINAL ANALYTICS REPORT</div>',
    unsafe_allow_html=True
)

st.title("CustomerPulse")

st.caption(
    "Customer Analytics • Churn Intelligence • Retention Analysis"
)


# ============================================================
# PAGE 1
# ============================================================

st.divider()

st.markdown(
    '<div class="page-badge">PAGE 01</div>',
    unsafe_allow_html=True
)

st.header("Customer Analytics Overview")

st.caption(
    "Customer base, revenue performance and customer value."
)

show_dashboard(
    PAGE_1_IMAGE,
    "Page 1"
)

st.markdown(
    '<div class="section-label">DASHBOARD READOUT</div>',
    unsafe_allow_html=True
)

st.subheader("Key Insights")


c1, c2 = st.columns(2)


with c1:

    show_insight(
        "01",
        "Customer Base",
        "The dashboard covers 96K customers, providing the base "
        "for analyzing revenue, customer value and churn exposure."
    )

    show_insight(
        "02",
        "Revenue Performance",
        "Total revenue is approximately $16.0M. This establishes "
        "the overall revenue base against which customer risk "
        "and potential revenue exposure can be evaluated."
    )

    show_insight(
        "03",
        "Revenue Exposure",
        "Approximately $13.9M of revenue is shown as Revenue at Risk. "
        "This highlights a significant revenue exposure associated "
        "with the customer risk identified in the dashboard."
    )

    show_insight(
        "04",
        "Retention vs Predicted Churn",
        "The dashboard reports a 28.87% Retention Rate and an "
        "87.69% Predicted Churn Rate. Together, these indicators "
        "show a substantial gap between retained customers and "
        "customers identified as likely to churn."
    )


with c2:

    show_insight(
        "05",
        "Revenue Concentration by State",
        "São Paulo is the largest visible revenue contributor at "
        "approximately $6.0M, followed by Rio de Janeiro at around "
        "$2.1M and Minas Gerais at around $1.8M. Revenue is therefore "
        "more concentrated in a few major states."
    )

    show_insight(
        "06",
        "Customer Value Distribution",
        "Customer counts are almost evenly distributed across High, "
        "Medium and Low value tiers, with approximately 32K customers "
        "in each segment. Customer volume is therefore balanced across "
        "the three value groups."
    )

    show_insight(
        "07",
        "Value Tier Revenue Contribution",
        "High-value customers generate approximately $10.88M, compared "
        "with $3.52M from Medium-value and $1.60M from Low-value customers. "
        "This shows that customer count alone does not represent revenue value."
    )

    show_insight(
        "08",
        "Monthly Revenue Trend",
        "Monthly revenue varies considerably across the displayed period. "
        "The chart shows a strong revenue level around May and a notable "
        "decline around August, indicating variation in monthly revenue performance."
    )


# ============================================================
# PAGE 2
# ============================================================

st.divider()

st.markdown(
    '<div class="page-badge">PAGE 02</div>',
    unsafe_allow_html=True
)

st.header("Customer Churn Intelligence")

st.caption(
    "Customer risk, churn probability and customer-value exposure."
)

show_dashboard(
    PAGE_2_IMAGE,
    "Page 2"
)

st.markdown(
    '<div class="section-label">DASHBOARD READOUT</div>',
    unsafe_allow_html=True
)

st.subheader("Key Insights")


c1, c2 = st.columns(2)


with c1:

    show_insight(
        "01",
        "Customer Risk Distribution",
        "High Risk customers account for 51.91% of the displayed "
        "customer base, followed by Medium Risk at 35.78% and "
        "Low Risk at 12.31%. High Risk is therefore the largest "
        "customer risk segment."
    )

    show_insight(
        "02",
        "High-Risk Customer Exposure",
        "Approximately 50K customers are classified as High Risk "
        "in the dashboard. This identifies a large customer group "
        "that requires closer retention attention."
    )

    show_insight(
        "03",
        "Predicted Churn Exposure",
        "The dashboard reports approximately 84K Predicted Churn "
        "Customers. This represents the customer population classified "
        "as predicted churn by the finalized churn output."
    )

    show_insight(
        "04",
        "Churn Probability Profile",
        "The probability distribution shows customer risk spread "
        "across multiple probability levels, with substantial "
        "customer volume toward the higher probability range. "
        "This indicates that churn risk is not uniform across customers."
    )


with c2:

    show_insight(
        "05",
        "Actual Churn by State",
        "Actual churn rates vary across the states displayed in the "
        "dashboard. This highlights geographic differences in recorded "
        "customer churn and provides a basis for state-level comparison."
    )

    show_insight(
        "06",
        "Customer Value vs Churn Probability",
        "The scatter analysis combines customer value with churn "
        "probability, allowing high- and lower-value customers to be "
        "evaluated alongside their predicted churn risk."
    )

    show_insight(
        "07",
        "Risk Segmentation for Action",
        "The risk segmentation converts churn probability into High, "
        "Medium and Low Risk groups. This makes the model output easier "
        "to interpret for customer prioritization and retention analysis."
    )


# ============================================================
# PAGE 3
# ============================================================

st.divider()

st.markdown(
    '<div class="page-badge">PAGE 03</div>',
    unsafe_allow_html=True
)

st.header("Retention Intelligence")

st.caption(
    "Retention actions, revenue exposure and execution analysis."
)

show_dashboard(
    PAGE_3_IMAGE,
    "Page 3"
)

st.markdown(
    '<div class="section-label">DASHBOARD READOUT</div>',
    unsafe_allow_html=True
)

st.subheader("Key Insights")


c1, c2 = st.columns(2)


with c1:

    show_insight(
        "01",
        "High-Risk Customers for Retention",
        "The retention dashboard focuses on approximately 50K High Risk "
        "customers. This connects the churn-risk output with a defined "
        "customer population for retention analysis."
    )

    show_insight(
        "02",
        "High-Risk Revenue Exposure",
        "The High Risk customer segment represents approximately "
        "$8.05M in revenue. This helps quantify the financial exposure "
        "associated with the customers targeted for retention."
    )

    show_insight(
        "03",
        "Primary Revenue-at-Risk Reasons",
        "Only One Purchase Made is the largest visible revenue-at-risk "
        "reason at approximately $9.3M, followed by Poor Customer "
        "Experience at approximately $3.8M. These are the two most "
        "significant reasons shown in the retention analysis."
    )

    show_insight(
        "04",
        "Secondary Revenue-at-Risk Reasons",
        "Low Purchase Frequency and Delivery Delays contribute smaller "
        "amounts of revenue exposure compared with the two leading "
        "reasons. The dashboard therefore provides multiple areas "
        "for retention intervention."
    )

    show_insight(
        "05",
        "Estimated Retention Investment",
        "The dashboard includes an estimated campaign budget of "
        "approximately $1M. This adds an estimated investment view "
        "to the retention planning analysis."
    )


with c2:

    show_insight(
        "06",
        "Projected Campaign ROI",
        "The dashboard reports a 3.67× projected Campaign ROI Multiplier. "
        "This is a modeled planning metric shown by the retention "
        "analysis, rather than an actual realized campaign return."
    )

    show_insight(
        "07",
        "Recommendation Coverage",
        "Recommendation Coverage is reported at 100%, indicating that "
        "recommendation information is available across the records "
        "included in this dashboard measure."
    )

    show_insight(
        "08",
        "Priority-Based Retention",
        "Retention actions are categorized into Critical, High, Medium "
        "and Low priorities. This creates a structured framework for "
        "deciding which customer cases require greater attention."
    )

    show_insight(
        "09",
        "Retention Ownership",
        "Retention activities are mapped to responsible teams such "
        "as CRM & Loyalty, Marketing and Customer Support. This connects "
        "customer-level actions with an accountable business function."
    )

    show_insight(
        "10",
        "Customer-Level Action Plan",
        "The execution table combines churn probability, risk segment, "
        "reason, recommendation, priority, owner and timeline. This "
        "moves the analysis from identifying risk to defining a "
        "specific retention action for individual customers."
    )


# ============================================================
# FINAL SECTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">REPORT CLOSING</div>',
    unsafe_allow_html=True
)

st.subheader("Final Dashboard View")

st.write(
    "The three dashboards present the customer analysis in sequence: "
    "overall customer and revenue performance, customer churn risk, "
    "and retention execution. Together, they connect customer data "
    "with churn prediction, risk segmentation and actionable "
    "retention analysis."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CustomerPulse • Final Dashboard Report"
)