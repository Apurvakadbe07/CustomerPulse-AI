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
    / "page 1 dashboard.png"
)

PAGE_2_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "page 2  dashboard.png"
)

PAGE_3_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "page 3 dashboard.png"
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
       Uses background color from .streamlit/config.toml
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

    # HTML is used ONLY for the visual card container.
    # The actual insight text contains NO HTML tags.

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
        "The report covers approximately 96K customers. "
        "This is the complete customer population represented "
        "in the final dashboard and provides the base for the "
        "revenue, customer value and churn analysis."
    )

    show_insight(
        "02",
        "Total Revenue",
        "Total revenue is approximately $16.0M. "
        "This represents the overall revenue recorded for "
        "the customer base included in the completed report."
    )

    show_insight(
        "03",
        "Revenue at Risk",
        "The dashboard reports approximately $13.9M Revenue at Risk. "
        "This represents the revenue exposure shown by the "
        "completed customer risk analysis."
    )

    show_insight(
        "04",
        "Actual vs Predicted Churn",
        "Actual Churn is approximately 71.15%, while Predicted "
        "Churn is approximately 87.69%. Actual Churn represents "
        "the recorded customer outcome, while Predicted Churn "
        "comes from the finalized churn analysis."
    )


with c2:

    show_insight(
        "05",
        "Revenue by State",
        "São Paulo contributes approximately $6.0M in revenue. "
        "Rio de Janeiro contributes around $2.1M, followed by "
        "Minas Gerais at around $1.8M. The chart shows that "
        "revenue contribution varies across states."
    )

    show_insight(
        "06",
        "Customer Value Distribution",
        "The customer base is almost evenly divided by customer "
        "count across the three value tiers. The finalized "
        "analysis contains 32,032 High, 32,029 Medium and "
        "32,034 Low value customers."
    )

    show_insight(
        "07",
        "Revenue by Customer Value",
        "High-value customers contribute approximately $10.88M, "
        "compared with $3.52M from Medium-value customers and "
        "$1.60M from Low-value customers. Similar customer "
        "counts therefore produce very different revenue "
        "contributions."
    )

    show_insight(
        "08",
        "Monthly Revenue",
        "The monthly revenue chart shows changes across the "
        "displayed period. The highest visible level occurs "
        "around May, while the level around August is "
        "considerably lower."
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
        "Risk Distribution",
        "High Risk customers represent approximately 51.91% "
        "of the displayed customer population. Medium Risk "
        "represents 35.78%, while Low Risk represents 12.31%. "
        "High Risk is therefore the largest reported risk group."
    )

    show_insight(
        "02",
        "High Risk Customers",
        "The finalized risk analysis records 11,961 High Risk "
        "customers. This is the highest-risk group in the "
        "finalized risk-segment output."
    )

    show_insight(
        "03",
        "Medium and Low Risk",
        "The finalized risk output records 5,776 Medium Risk "
        "customers and 1,483 Low Risk customers. These groups "
        "represent the lower risk levels in the finalized "
        "segmentation."
    )


with c2:

    show_insight(
        "04",
        "Churn Probability",
        "The churn probability chart shows customers distributed "
        "across different probability levels, with considerable "
        "customer volume visible toward the higher probability "
        "range. This means predicted churn risk differs from "
        "customer to customer."
    )

    show_insight(
        "05",
        "State-wise Actual Churn",
        "The state-wise chart shows differences in actual churn "
        "rates between the locations displayed in the dashboard. "
        "Recorded churn is therefore not at exactly the same "
        "level across all states shown."
    )

    show_insight(
        "06",
        "Customer Value vs Churn Risk",
        "The scatter chart compares customer value with churn "
        "risk. This allows higher- and lower-value customers "
        "to be viewed together with their reported churn risk "
        "instead of analysing the two measures separately."
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
        "High-Risk Customer Targeting",
        "The retention dashboard targets approximately 50K High "
        "Risk customers. This connects the customer-risk analysis "
        "with the retention actions shown in the dashboard."
    )

    show_insight(
        "02",
        "High-Risk Revenue",
        "High-Risk Revenue is approximately $8.05M. "
        "This shows the revenue associated with the High Risk "
        "customer group in the completed retention report."
    )

    show_insight(
        "03",
        "Main Revenue-at-Risk Reasons",
        "Only One Purchase Made is the largest recorded reason, "
        "with approximately $9.3M of revenue exposure. Poor "
        "Customer Experience is the second-largest reason at "
        "around $3.8M."
    )

    show_insight(
        "04",
        "Other Recorded Reasons",
        "The dashboard also records revenue exposure under "
        "other reasons, including Low Purchase Frequency and "
        "Delivery Delay. These appear as smaller categories "
        "compared with the two largest reasons shown."
    )

    show_insight(
        "05",
        "Campaign Budget",
        "The dashboard records an estimated campaign budget of "
        "approximately $1M. This adds the estimated investment "
        "requirement to the customer retention analysis."
    )


with c2:

    show_insight(
        "06",
        "Campaign ROI",
        "The completed dashboard reports a 3.67× Campaign ROI "
        "Multiplier. Based on the calculation used in the "
        "report, the reported return is 3.67 times the "
        "campaign investment."
    )

    show_insight(
        "07",
        "Recommendation Coverage",
        "Recommendation Coverage is shown as 100%. "
        "This indicates that recommendation information is "
        "available across the customer records included in "
        "this dashboard measure."
    )

    show_insight(
        "08",
        "Retention Priorities",
        "Retention actions are divided across Critical, High, "
        "Medium and Low priority levels. This allows the "
        "recorded customer actions to be viewed according "
        "to their assigned priority."
    )

    show_insight(
        "09",
        "Owner and Workload",
        "Customer retention activities are assigned to "
        "recorded owners. This connects each customer action "
        "with the owner responsible for handling that case."
    )

    show_insight(
        "10",
        "Customer-Level Retention Action",
        "The execution table brings together customer ID, "
        "churn probability, risk segment, reason, recommendation, "
        "priority, owner and timeline. This allows individual "
        "customer risk and the corresponding recorded retention "
        "action to be viewed together."
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
    "The three dashboards present the customer base, customer "
    "risk and retention execution in sequence. The report moves "
    "from overall customer and revenue analysis to churn risk "
    "and then to the recorded retention actions."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CustomerPulse • Final Dashboard Report"
)