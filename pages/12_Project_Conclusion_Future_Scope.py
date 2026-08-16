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
# FINAL DATASET CHECK
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATASET = (
    PROJECT_ROOT
    / "2 Notebook"
    / "outputs"
    / "customer_360_final.csv"
)

if not FINAL_DATASET.exists():
    st.error(
        "The finalized customer_360_final.csv file was not found."
    )
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.caption("CUSTOMERPULSE • FINAL PROJECT REPORT")

st.title("Project Conclusion & Future Scope")

st.write(
    "Final findings, business interpretation and the next logical "
    "steps for the completed customer retention analysis."
)


# ============================================================
# 01 — PROJECT CONCLUSION
# ============================================================

st.divider()

st.header("Project Conclusion")

st.write(
    "The completed analysis provides a clear view of customer risk, "
    "customer value and the revenue associated with potential churn."
)

st.write(
    "68,352 customers were identified as at risk, representing "
    "71.13% of the total customer base. The finalized business "
    "analysis reported $11,261,919.01 in revenue at risk, with "
    "average spending of $164.76 among at-risk customers."
)

st.write(
    "Customer value also has a clear relationship with revenue. "
    "High-value customers contribute $10,884,246.37 in revenue, "
    "compared with $3,523,030.40 from Medium-value customers and "
    "$1,601,595.35 from Low-value customers."
)

st.write(
    "The final churn model achieved 77.10% accuracy, 77.46% "
    "precision, 95.62% recall, 85.59% F1 Score and 78.15% "
    "ROC-AUC. These results provide the basis for identifying "
    "customers that require further attention."
)

st.write(
    "The final retention output then connects customer risk with "
    "the recorded reason, recommendation, priority, owner and "
    "timeline. This makes the analysis useful at the customer "
    "level rather than stopping at a churn prediction."
)


# ============================================================
# 02 — KEY RESULTS
# ============================================================

st.divider()

st.header("Key Results at a Glance")

st.caption(
    "Finalized figures from the completed CustomerPulse analysis."
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total Customers",
        "96,096"
    )

with c2:
    st.metric(
        "At-Risk Customers",
        "68,352"
    )

with c3:
    st.metric(
        "At-Risk",
        "71.13%"
    )

with c4:
    st.metric(
        "Revenue at Risk",
        "$11.26M"
    )

with c5:
    st.metric(
        "Model Recall",
        "95.62%"
    )


# ============================================================
# 03 — WHAT THE RESULTS MEAN
# ============================================================

st.divider()

st.header("What the Results Mean")

left, right = st.columns(2)


with left:

    st.subheader("Customer Risk")

    st.write(
        "The analysis identified 68,352 at-risk customers. "
        "At 71.13% of the customer base, the risk is not limited "
        "to a small group of customers."
    )

    st.write(
        "This makes customer risk an important part of the overall "
        "customer and revenue picture."
    )


    st.subheader("Revenue Exposure")

    st.write(
        "The reported revenue at risk is $11,261,919.01. "
        "This puts a financial value against the identified "
        "customer risk instead of looking only at customer counts."
    )


with right:

    st.subheader("Customer Value")

    st.write(
        "The three customer value tiers have broadly similar "
        "customer counts, but their revenue contribution is very "
        "different."
    )

    st.write(
        "High-value customers contribute $10.88M, while Medium and "
        "Low-value customers contribute $3.52M and $1.60M "
        "respectively."
    )


    st.subheader("Prediction Quality")

    st.write(
        "The final model recorded 95.62% recall. In practical "
        "terms, this means the model identified a high proportion "
        "of the churn cases represented in the evaluation results."
    )


# ============================================================
# 04 — FROM RISK TO RETENTION
# ============================================================

st.divider()

st.header("From Customer Risk to Retention Action")

st.write(
    "The final customer-level output connects risk information "
    "with the available retention fields."
)

a1, a2, a3, a4, a5 = st.columns(5)

with a1:

    st.subheader("Risk")

    st.write(
        "Churn probability and risk segment show the customer's "
        "recorded risk position."
    )


with a2:

    st.subheader("Reason")

    st.write(
        "The recorded reason provides context for the customer's "
        "retention case."
    )


with a3:

    st.subheader("Recommendation")

    st.write(
        "The recorded recommendation identifies the retention "
        "action associated with the customer."
    )


with a4:

    st.subheader("Priority")

    st.write(
        "Priority helps distinguish the level assigned to the "
        "retention case."
    )


with a5:

    st.subheader("Execution")

    st.write(
        "Owner and timeline provide the available information "
        "for carrying the retention case forward."
    )


# ============================================================
# 05 — RECORDED REVENUE EXPOSURE
# ============================================================

st.divider()

st.header("Recorded Revenue Exposure by Reason")

st.write(
    "The completed Power BI retention report records two major "
    "revenue exposure reasons."
)

r1, r2 = st.columns(2)

with r1:

    st.subheader("Only One Purchase Made")

    st.metric(
        "Recorded Exposure",
        "≈ $9.3M"
    )

    st.write(
        "This is the larger of the two recorded revenue exposure "
        "categories shown on the completed retention dashboard."
    )


with r2:

    st.subheader("Poor Customer Experience")

    st.metric(
        "Recorded Exposure",
        "≈ $3.8M"
    )

    st.write(
        "This is the second recorded revenue exposure category "
        "shown on the completed retention dashboard."
    )


# ============================================================
# 06 — FUTURE SCOPE
# ============================================================

st.divider()

st.header("Future Scope")

st.write(
    "The following are direct extensions of the completed "
    "CustomerPulse workflow."
)


f1, f2 = st.columns(2)


with f1:

    st.subheader("1. Continuous Customer Monitoring")

    st.write(
        "Refresh the customer risk analysis when new customer "
        "and transaction data becomes available, allowing changes "
        "in customer risk to be monitored over time."
    )


    st.subheader("2. Actual Retention Outcome Tracking")

    st.write(
        "Compare retention actions with later customer outcomes "
        "to understand whether the actions were followed by the "
        "expected customer behaviour."
    )


with f2:

    st.subheader("3. Model Performance Monitoring")

    st.write(
        "Compare future predictions with actual customer outcomes "
        "and monitor whether the final model performance remains "
        "consistent over time."
    )


    st.subheader("4. Power BI Reporting Refresh")

    st.write(
        "Update the existing Power BI report with future customer "
        "data so that changes in risk, revenue exposure and "
        "retention execution can be monitored across reporting "
        "periods."
    )


# ============================================================
# 07 — FINAL TAKEAWAY
# ============================================================

st.divider()

st.header("Final Takeaway")

st.write(
    "CustomerPulse provides a structured view of customer risk "
    "and the revenue associated with that risk."
)

st.write(
    "The final results show that customer risk represents a "
    "significant part of the customer base, while customer value "
    "differs substantially in terms of revenue contribution."
)

st.write(
    "The churn model provides the risk identification layer, "
    "and the retention output carries that information into "
    "customer-level recommendations and execution details."
)

st.write(
    "The completed Power BI report brings these results together "
    "for business review. The final outcome is a practical view "
    "of which customer risk exists, what revenue is exposed and "
    "what retention information is available for action."
)


# ============================================================
# FINAL STATUS
# ============================================================

st.divider()

st.success(
    "CustomerPulse final analytical and reporting workflow completed."
)

st.caption(
    "CustomerPulse • Customer Churn Prediction & Retention Intelligence Platform"
)