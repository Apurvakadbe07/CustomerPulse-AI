# ============================================================
# PAGE 10
# RETENTION RECOMMENDATION ENGINE
# ============================================================

from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=" AI Retention Recommendation Engine",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = (
    PROJECT_ROOT
    / "2 Notebook"
    / "outputs"
)

FINAL_DATASET_PATH = (
    OUTPUT_DIR
    / "customer_360_final.csv"
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_final_dataset(file_path):

    try:

        return pd.read_csv(file_path)

    except FileNotFoundError:

        return None

    except Exception as exc:

        st.error(
            f"Unable to load the finalized customer dataset: {exc}"
        )

        return None


df = load_final_dataset(
    FINAL_DATASET_PATH
)


# ============================================================
# FINAL DATASET CHECK
# ============================================================

if df is None:

    st.warning(
        "customer_360_final.csv was not found in "
        "2 Notebook/outputs. This page cannot continue "
        "without the finalized dataset."
    )

    st.stop()


# ============================================================
# RETENTION COLUMNS TO CHECK
# ============================================================

RETENTION_COLUMNS = [
    "customer_unique_id",
    "recommendation",
    "reason",
    "priority",
    "owner",
    "timeline",
    "estimated_cost",
    "expected_outcome",
]


# ============================================================
# ACTUAL COLUMN AVAILABILITY
# ============================================================

available_columns = [
    column
    for column in RETENTION_COLUMNS
    if column in df.columns
]

missing_columns = [
    column
    for column in RETENTION_COLUMNS
    if column not in df.columns
]


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <style>

    .page-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #667085;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .section-caption {
        font-size: 14px;
        color: #667085;
        margin-bottom: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="page-title">Retention Recommendation Engine</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="page-subtitle">
    Customer-level retention actions organized for practical execution,
    ownership and follow-up.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# REQUIRED CUSTOMER ID CHECK
# ============================================================

if "customer_unique_id" not in df.columns:

    st.warning(
        "customer_unique_id is not available in the final dataset. "
        "Customer-level retention operations cannot be displayed."
    )

    st.stop()


# ============================================================
# WORKING COPY
# ============================================================

retention_df = df.copy()

retention_df = retention_df[
    retention_df["customer_unique_id"].notna()
].copy()


# ============================================================
# NO VALID CUSTOMER DATA
# ============================================================

if retention_df.empty:

    st.warning(
        "The final dataset does not contain valid customer records."
    )

    st.stop()


# ============================================================
# SMALL HELPER FUNCTIONS
# ============================================================

def get_non_empty_series(dataframe, column):

    if column not in dataframe.columns:

        return pd.Series(dtype="object")

    series = dataframe[column].dropna()

    series = series[
        series.astype(str).str.strip() != ""
    ]

    return series


def format_display_value(value):

    if pd.isna(value):

        return "Not recorded"

    value = str(value).strip()

    if not value:

        return "Not recorded"

    return value


# ============================================================
# RETENTION COMMAND CENTER
# ============================================================

st.markdown(
    '<div class="section-title">Retention Command Center</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-caption">
    Overview of the retention actions recorded in the finalized
    customer dataset.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW COUNTS
# ============================================================

total_customers = (
    retention_df["customer_unique_id"]
    .astype(str)
    .nunique()
)


# Recommendation information
if "recommendation" in retention_df.columns:

    recommendation_series = get_non_empty_series(
        retention_df,
        "recommendation"
    )

    recommendation_types = (
        recommendation_series.nunique()
    )

else:

    recommendation_series = pd.Series(
        dtype="object"
    )

    recommendation_types = None


# Priority information
if "priority" in retention_df.columns:

    priority_series = get_non_empty_series(
        retention_df,
        "priority"
    )

    priority_types = (
        priority_series.nunique()
    )

else:

    priority_series = pd.Series(
        dtype="object"
    )

    priority_types = None


# Owner information
if "owner" in retention_df.columns:

    owner_series = get_non_empty_series(
        retention_df,
        "owner"
    )

    owner_types = owner_series.nunique()

else:

    owner_series = pd.Series(
        dtype="object"
    )

    owner_types = None


# Timeline information
if "timeline" in retention_df.columns:

    timeline_series = get_non_empty_series(
        retention_df,
        "timeline"
    )

    timeline_types = timeline_series.nunique()

else:

    timeline_series = pd.Series(
        dtype="object"
    )

    timeline_types = None


# ============================================================
# TOP KPI ROW
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Customers",
        f"{total_customers:,}"
    )


with kpi2:

    if recommendation_types is not None:

        st.metric(
            "Recommendation Types",
            f"{recommendation_types:,}"
        )

    else:

        st.metric(
            "Recommendation Types",
            "Unavailable"
        )


with kpi3:

    if priority_types is not None:

        st.metric(
            "Priority Types",
            f"{priority_types:,}"
        )

    else:

        st.metric(
            "Priority Types",
            "Unavailable"
        )


with kpi4:

    if owner_types is not None:

        st.metric(
            "Responsible Owners",
            f"{owner_types:,}"
        )

    else:

        st.metric(
            "Responsible Owners",
            "Unavailable"
        )


# ============================================================
# SECOND KPI ROW
# ============================================================

kpi5, kpi6, kpi7, kpi8 = st.columns(4)


with kpi5:

    if timeline_types is not None:

        st.metric(
            "Timeline Categories",
            f"{timeline_types:,}"
        )

    else:

        st.metric(
            "Timeline Categories",
            "Unavailable"
        )


with kpi6:

    if "recommendation" in retention_df.columns:

        recorded_recommendations = (
            retention_df["recommendation"]
            .notna()
            .sum()
        )

        st.metric(
            "Recorded Recommendations",
            f"{recorded_recommendations:,}"
        )

    else:

        st.metric(
            "Recorded Recommendations",
            "Unavailable"
        )


with kpi7:

    if "estimated_cost" in retention_df.columns:

        numeric_cost = pd.to_numeric(
            retention_df["estimated_cost"],
            errors="coerce"
        )

        valid_cost = numeric_cost.dropna()

        if not valid_cost.empty:

            st.metric(
                "Recorded Cost",
                f"{valid_cost.sum():,.0f}"
            )

        else:

            st.metric(
                "Recorded Cost",
                "Unavailable"
            )

    else:

        st.metric(
            "Recorded Cost",
            "Unavailable"
        )


with kpi8:

    if "expected_outcome" in retention_df.columns:

        outcome_count = (
            get_non_empty_series(
                retention_df,
                "expected_outcome"
            )
            .nunique()
        )

        st.metric(
            "Outcome Types",
            f"{outcome_count:,}"
        )

    else:

        st.metric(
            "Outcome Types",
            "Unavailable"
        )


# ============================================================
# ACTION FIELD AVAILABILITY
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Action Field Availability</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-caption">
    Shows how many customer records contain usable values in the
    available retention fields.
    </div>
    """,
    unsafe_allow_html=True,
)


coverage_records = []


for column, label in [
    ("recommendation", "Recommendation"),
    ("reason", "Reason"),
    ("priority", "Priority"),
    ("owner", "Responsible Owner"),
    ("timeline", "Timeline"),
    ("estimated_cost", "Estimated Cost"),
    ("expected_outcome", "Expected Outcome"),
]:

    if column not in retention_df.columns:

        continue


    if column == "estimated_cost":

        usable_values = pd.to_numeric(
            retention_df[column],
            errors="coerce"
        ).notna()

    else:

        usable_values = (
            retention_df[column]
            .notna()
            &
            (
                retention_df[column]
                .astype(str)
                .str.strip()
                != ""
            )
        )


    coverage_records.append(
        {
            "Action Field": label,
            "Customer Records": int(
                usable_values.sum()
            ),
        }
    )


if coverage_records:

    coverage_df = pd.DataFrame(
        coverage_records
    )


    fig_coverage = px.bar(
        coverage_df,
        x="Action Field",
        y="Customer Records",
        text="Customer Records",
    )


    fig_coverage.update_traces(
        textposition="outside"
    )


    fig_coverage.update_layout(
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=25,
            b=20,
        ),
        xaxis_title=None,
        yaxis_title="Customer Records",
        showlegend=False,
    )


    st.plotly_chart(
        fig_coverage,
        use_container_width=True,
    )

else:

    st.info(
        "No retention action fields are available "
        "for this overview."
    )


# ============================================================
# RECOMMENDATION OVERVIEW
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Recommendation Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-caption">
    Distribution of the recommendation values actually recorded
    in the finalized dataset.
    </div>
    """,
    unsafe_allow_html=True,
)


if "recommendation" not in retention_df.columns:

    st.info(
        "The recommendation column is not available in the "
        "final dataset. This overview has been skipped."
    )

else:

    recommendation_data = (
        retention_df["recommendation"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    recommendation_data = (
        recommendation_data[
            recommendation_data != ""
        ]
    )


    if recommendation_data.empty:

        st.info(
            "No usable recommendation values are available "
            "in the final dataset."
        )

    else:

        recommendation_counts = (
            recommendation_data
            .value_counts()
            .reset_index()
        )

        recommendation_counts.columns = [
            "Recommendation",
            "Customers",
        ]


        chart_col, table_col = st.columns(
            [1.8, 1]
        )


        with chart_col:

            fig_recommendations = px.bar(
                recommendation_counts,
                x="Customers",
                y="Recommendation",
                orientation="h",
                text="Customers",
            )


            fig_recommendations.update_traces(
                textposition="outside"
            )


            fig_recommendations.update_layout(
                height=max(
                    360,
                    min(
                        650,
                        len(
                            recommendation_counts
                        ) * 55
                    ),
                ),
                margin=dict(
                    l=20,
                    r=30,
                    t=20,
                    b=20,
                ),
                xaxis_title="Customers",
                yaxis_title=None,
                showlegend=False,
            )


            st.plotly_chart(
                fig_recommendations,
                use_container_width=True,
            )


        with table_col:

            st.dataframe(
                recommendation_counts,
                use_container_width=True,
                hide_index=True,
                height=360,
            )


# ============================================================
# DATASET AVAILABILITY NOTICE
# ============================================================

if missing_columns:

    st.caption(
        "Some retention fields are not present in the finalized "
        "dataset. Related features have been omitted rather than "
        "using assumed or substitute values."
    )

#2
# ============================================================
# PRIORITY MANAGEMENT
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Priority Management</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-caption">
    Review the distribution of retention priorities recorded
    for customer action.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHECK PRIORITY COLUMN
# ============================================================

if "priority" not in retention_df.columns:

    st.warning(
        "The `priority` column is not available in "
        "customer_360_final.csv. Priority Management has "
        "been skipped."
    )

else:

    # ========================================================
    # GET ACTUAL PRIORITY VALUES
    # ========================================================

    priority_data = (
        retention_df["priority"]
        .dropna()
        .astype(str)
        .str.strip()
    )


    priority_data = priority_data[
        priority_data != ""
    ]


    # ========================================================
    # CHECK ACTUAL DATA
    # ========================================================

    if priority_data.empty:

        st.info(
            "The `priority` column exists, but it does not "
            "contain usable values in the final dataset."
        )

    else:

        # ====================================================
        # ACTUAL PRIORITY DISTRIBUTION
        # ====================================================

        priority_counts = (
            priority_data
            .value_counts()
            .reset_index()
        )


        priority_counts.columns = [
            "Priority",
            "Customers",
        ]


        # ====================================================
        # PRIORITY OVERVIEW
        # ====================================================

        priority_col1, priority_col2, priority_col3 = st.columns(3)


        with priority_col1:

            st.metric(
                "Priority Categories",
                f"{priority_counts.shape[0]:,}"
            )


        with priority_col2:

            st.metric(
                "Customers with Priority",
                f"{priority_data.shape[0]:,}"
            )


        with priority_col3:

            highest_volume_priority = (
                priority_counts.iloc[0]["Priority"]
            )

            highest_volume_count = (
                priority_counts.iloc[0]["Customers"]
            )

            st.metric(
                "Largest Priority Group",
                str(highest_volume_priority)
            )


        # ====================================================
        # PRIORITY VISUALIZATION
        # ====================================================

        st.markdown(
            "### Priority Distribution"
        )


        priority_chart_col, priority_table_col = st.columns(
            [1.8, 1]
        )


        # ====================================================
        # BAR CHART
        # ====================================================

        with priority_chart_col:

            fig_priority = px.bar(
                priority_counts,
                x="Priority",
                y="Customers",
                text="Customers",
            )


            fig_priority.update_traces(
                textposition="outside"
            )


            fig_priority.update_layout(
                height=390,
                margin=dict(
                    l=20,
                    r=20,
                    t=25,
                    b=20,
                ),
                xaxis_title=None,
                yaxis_title="Customers",
                showlegend=False,
            )


            st.plotly_chart(
                fig_priority,
                use_container_width=True,
            )


        # ====================================================
        # PRIORITY TABLE
        # ====================================================

        with priority_table_col:

            st.dataframe(
                priority_counts,
                use_container_width=True,
                hide_index=True,
                height=390,
            )


        # ====================================================
        # PRIORITY SHARE
        # ====================================================

        st.markdown(
            "### Priority Share"
        )


        priority_share = priority_counts.copy()


        total_priority_records = (
            priority_share["Customers"].sum()
        )


        if total_priority_records > 0:

            priority_share["Share"] = (
                priority_share["Customers"]
                / total_priority_records
                * 100
            )


            priority_share["Share"] = (
                priority_share["Share"]
                .round(2)
            )


            priority_share_display = (
                priority_share[
                    [
                        "Priority",
                        "Customers",
                        "Share",
                    ]
                ]
                .copy()
            )


            priority_share_display["Share"] = (
                priority_share_display["Share"]
                .astype(str)
                + "%"
            )


            st.dataframe(
                priority_share_display,
                use_container_width=True,
                hide_index=True,
            )


        # ====================================================
        # ACTUAL VALUES INFORMATION
        # ====================================================

        with st.expander(
            "View Recorded Priority Values",
            expanded=False,
        ):

            actual_priority_values = (
                priority_data
                .drop_duplicates()
                .tolist()
            )


            priority_value_df = pd.DataFrame(
                {
                    "Priority Value in Final Dataset":
                        actual_priority_values
                }
            )


            st.dataframe(
                priority_value_df,
                use_container_width=True,
                hide_index=True,
            )
#3
# ============================================================
# CUSTOMER RETENTION WORKSPACE
# ============================================================

st.markdown("---")

st.subheader("Customer Retention Workspace")

st.caption(
    "Select a customer to review the retention action recorded "
    "for that customer in the finalized dataset."
)


# ============================================================
# COLUMNS CHECKED
# ============================================================

workspace_columns = [
    "customer_unique_id",
    "recommendation",
    "reason",
    "priority",
    "owner",
    "timeline",
    "estimated_cost",
    "expected_outcome",
]


# ============================================================
# CUSTOMER ID CHECK
# ============================================================

if "customer_unique_id" not in retention_df.columns:

    st.warning(
        "The customer_unique_id column is not available in "
        "customer_360_final.csv. Customer Retention Workspace "
        "cannot be displayed."
    )

else:

    workspace_df = retention_df.copy()

    workspace_df = workspace_df[
        workspace_df["customer_unique_id"].notna()
    ].copy()


    if workspace_df.empty:

        st.info(
            "No valid customer records are available in "
            "the final dataset."
        )

    else:

        # ====================================================
        # SEARCH
        # ====================================================

        search_col, count_col = st.columns(
            [3, 1]
        )


        with search_col:

            customer_search = st.text_input(
                "Search Customer ID",
                placeholder="Enter customer ID or part of the ID",
                key="retention_workspace_search",
            )


        with count_col:

            customer_count = (
                workspace_df[
                    "customer_unique_id"
                ]
                .astype(str)
                .nunique()
            )

            st.metric(
                "Customers Available",
                f"{customer_count:,}"
            )


        # ====================================================
        # SEARCH FILTER
        # ====================================================

        if customer_search.strip():

            search_value = (
                customer_search
                .strip()
                .lower()
            )

            filtered_workspace_df = workspace_df[
                workspace_df[
                    "customer_unique_id"
                ]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    na=False,
                    regex=False,
                )
            ].copy()

        else:

            filtered_workspace_df = workspace_df.copy()


        # ====================================================
        # NO SEARCH RESULT
        # ====================================================

        if filtered_workspace_df.empty:

            st.info(
                "No customer was found for the entered search."
            )

        else:

            st.caption(
                f"{len(filtered_workspace_df):,} "
                "customer record(s) available."
            )


            # =================================================
            # CUSTOMER SELECTION
            # =================================================

            customer_options = (
                filtered_workspace_df[
                    "customer_unique_id"
                ]
                .astype(str)
                .drop_duplicates()
                .tolist()
            )


            selected_customer_id = st.selectbox(
                "Select Customer",
                customer_options,
                key="retention_workspace_customer",
            )


            # =================================================
            # SELECTED CUSTOMER
            # =================================================

            selected_rows = workspace_df[
                workspace_df[
                    "customer_unique_id"
                ]
                .astype(str)
                == str(selected_customer_id)
            ].copy()


            if selected_rows.empty:

                st.warning(
                    "The selected customer record could not "
                    "be retrieved from the final dataset."
                )

            else:

                selected_customer = (
                    selected_rows.iloc[0]
                )


                # =================================================
                # CASE HEADER
                # =================================================

                st.markdown("---")

                st.subheader("Retention Case")

                st.write(
                    f"Customer ID: {selected_customer_id}"
                )


                # =================================================
                # RECOMMENDED ACTION
                # =================================================

                if "recommendation" in selected_customer.index:

                    recommendation_value = (
                        selected_customer[
                            "recommendation"
                        ]
                    )

                    if pd.isna(
                        recommendation_value
                    ):

                        recommendation_text = (
                            "Not recorded"
                        )

                    else:

                        recommendation_text = str(
                            recommendation_value
                        ).strip()

                        if not recommendation_text:

                            recommendation_text = (
                                "Not recorded"
                            )


                    st.markdown(
                        "#### Recommended Action"
                    )

                    st.info(
                        recommendation_text
                    )

                else:

                    st.info(
                        "The recommendation column is not "
                        "available in the final dataset."
                    )


                # =================================================
                # REASON
                # =================================================

                if "reason" in selected_customer.index:

                    reason_value = (
                        selected_customer["reason"]
                    )

                    if pd.isna(reason_value):

                        reason_text = "Not recorded"

                    else:

                        reason_text = str(
                            reason_value
                        ).strip()

                        if not reason_text:

                            reason_text = "Not recorded"


                    st.markdown(
                        "#### Reason for Action"
                    )

                    st.write(
                        reason_text
                    )

                else:

                    st.info(
                        "The reason column is not available "
                        "in the final dataset."
                    )


                # =================================================
                # OPERATIONAL DETAILS
                # =================================================

                st.markdown(
                    "#### Operational Details"
                )


                operational_fields = [
                    (
                        "priority",
                        "Priority",
                    ),
                    (
                        "owner",
                        "Responsible Owner",
                    ),
                    (
                        "timeline",
                        "Timeline",
                    ),
                    (
                        "estimated_cost",
                        "Estimated Cost",
                    ),
                ]


                available_operational_fields = [
                    field
                    for field, label
                    in operational_fields
                    if field in selected_customer.index
                ]


                if available_operational_fields:

                    # ---------------------------------------------
                    # USE TWO COLUMNS
                    # ---------------------------------------------

                    operational_pairs = []


                    for field, label in operational_fields:

                        if field in selected_customer.index:

                            operational_pairs.append(
                                (
                                    field,
                                    label,
                                )
                            )


                    for i in range(
                        0,
                        len(operational_pairs),
                        2
                    ):

                        row_fields = (
                            operational_pairs[
                                i:i + 2
                            ]
                        )

                        detail_columns = st.columns(
                            len(row_fields)
                        )


                        for (
                            detail_column,
                            field_label_pair
                        ) in zip(
                            detail_columns,
                            row_fields
                        ):

                            field = (
                                field_label_pair[0]
                            )

                            field_label = (
                                field_label_pair[1]
                            )

                            raw_value = (
                                selected_customer[field]
                            )


                            # -------------------------------------
                            # SAFE VALUE
                            # -------------------------------------

                            if pd.isna(raw_value):

                                display_value = (
                                    "Not recorded"
                                )

                            else:

                                display_value = str(
                                    raw_value
                                ).strip()

                                if not display_value:

                                    display_value = (
                                        "Not recorded"
                                    )


                            # -------------------------------------
                            # NATIVE STREAMLIT DISPLAY
                            # -------------------------------------

                            with detail_column:

                                st.caption(
                                    field_label
                                )

                                st.write(
                                    display_value
                                )


                                st.divider()


                else:

                    st.info(
                        "No operational detail columns are "
                        "available for this customer."
                    )


                # =================================================
                # EXPECTED OUTCOME
                # =================================================

                if "expected_outcome" in selected_customer.index:

                    outcome_value = (
                        selected_customer[
                            "expected_outcome"
                        ]
                    )


                    if pd.isna(outcome_value):

                        outcome_text = (
                            "Not recorded"
                        )

                    else:

                        outcome_text = str(
                            outcome_value
                        ).strip()

                        if not outcome_text:

                            outcome_text = (
                                "Not recorded"
                            )


                    st.markdown(
                        "#### Expected Outcome"
                    )

                    st.success(
                        outcome_text
                    )

                else:

                    st.info(
                        "The expected_outcome column is not "
                        "available in the final dataset."
                    )


                # =================================================
                # COMPLETE RECORDED DETAILS
                # =================================================

                with st.expander(
                    "View Recorded Retention Details"
                ):

                    detail_rows = []


                    for field in workspace_columns:

                        if field not in selected_customer.index:

                            continue


                        value = (
                            selected_customer[field]
                        )


                        if pd.isna(value):

                            display_value = (
                                "Not recorded"
                            )

                        else:

                            display_value = str(
                                value
                            ).strip()

                            if not display_value:

                                display_value = (
                                    "Not recorded"
                                )


                        detail_rows.append(
                            {
                                "Field": field,
                                "Final Dataset Value":
                                    display_value,
                            }
                        )


                    if detail_rows:

                        detail_df = pd.DataFrame(
                            detail_rows
                        )


                        st.dataframe(
                            detail_df,
                            use_container_width=True,
                            hide_index=True,
                        )

                    else:

                        st.info(
                            "No retention details are available "
                            "for the selected customer."
                        )
 #4
 # ============================================================
# RETENTION INVESTMENT
# ============================================================

st.markdown("---")

st.subheader("Retention Investment")

st.caption(
    "Review the estimated investment recorded for retention "
    "actions in the finalized customer dataset."
)


# ============================================================
# REQUIRED COLUMN CHECK
# ============================================================

if "estimated_cost" not in retention_df.columns:

    st.warning(
        "The estimated_cost column is not available in "
        "customer_360_final.csv. Retention Investment cannot "
        "be calculated."
    )

else:

    # ========================================================
    # ACTUAL COST DATA
    # ========================================================

    investment_df = retention_df.copy()

    investment_df["_estimated_cost_numeric"] = pd.to_numeric(
        investment_df["estimated_cost"],
        errors="coerce"
    )


    # ========================================================
    # VALID COST RECORDS
    # ========================================================

    valid_investment_df = investment_df[
        investment_df["_estimated_cost_numeric"].notna()
    ].copy()


    # ========================================================
    # NO VALID COST DATA
    # ========================================================

    if valid_investment_df.empty:

        st.info(
            "The estimated_cost column exists, but it does not "
            "contain usable numeric values in the final dataset."
        )

    else:

        # ====================================================
        # BASIC INVESTMENT METRICS
        # ====================================================

        total_investment = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .sum()
        )


        average_investment = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .mean()
        )


        median_investment = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .median()
        )


        maximum_investment = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .max()
        )


        minimum_investment = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .min()
        )


        # ====================================================
        # KPI ROW
        # ====================================================

        investment_kpi_1, investment_kpi_2 = st.columns(2)


        with investment_kpi_1:

            st.metric(
                "Total Estimated Investment",
                f"{total_investment:,.0f}"
            )


        with investment_kpi_2:

            st.metric(
                "Average Estimated Cost",
                f"{average_investment:,.2f}"
            )


        investment_kpi_3, investment_kpi_4 = st.columns(2)


        with investment_kpi_3:

            st.metric(
                "Median Estimated Cost",
                f"{median_investment:,.0f}"
            )


        with investment_kpi_4:

            st.metric(
                "Highest Recorded Cost",
                f"{maximum_investment:,.0f}"
            )


        # ====================================================
        # COST DISTRIBUTION
        # ====================================================

        st.markdown("### Estimated Cost Distribution")

        st.caption(
            "Distribution based only on the actual estimated_cost "
            "values recorded in the finalized dataset."
        )


        cost_distribution = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
            .value_counts()
            .sort_index()
            .reset_index()
        )


        cost_distribution.columns = [
            "Estimated Cost",
            "Customers",
        ]


        cost_distribution["Estimated Cost"] = (
            cost_distribution[
                "Estimated Cost"
            ]
            .astype(float)
        )


        cost_chart_col, cost_table_col = st.columns(
            [1.8, 1]
        )


        # ====================================================
        # COST CHART
        # ====================================================

        with cost_chart_col:

            fig_cost = px.bar(
                cost_distribution,
                x="Estimated Cost",
                y="Customers",
                text="Customers",
            )


            fig_cost.update_traces(
                textposition="outside"
            )


            fig_cost.update_layout(
                height=380,
                margin=dict(
                    l=20,
                    r=20,
                    t=25,
                    b=20,
                ),
                xaxis_title="Estimated Cost",
                yaxis_title="Customers",
                showlegend=False,
            )


            st.plotly_chart(
                fig_cost,
                use_container_width=True,
            )


        # ====================================================
        # COST TABLE
        # ====================================================

        with cost_table_col:

            display_cost_distribution = (
                cost_distribution.copy()
            )


            display_cost_distribution[
                "Estimated Cost"
            ] = (
                display_cost_distribution[
                    "Estimated Cost"
                ]
                .map(
                    lambda value:
                    f"{value:,.0f}"
                )
            )


            st.dataframe(
                display_cost_distribution,
                use_container_width=True,
                hide_index=True,
                height=380,
            )


        # ====================================================
        # PRIORITY-WISE INVESTMENT
        # ====================================================

        if "priority" in valid_investment_df.columns:

            priority_investment_df = (
                valid_investment_df[
                    [
                        "priority",
                        "_estimated_cost_numeric",
                    ]
                ]
                .copy()
            )


            priority_investment_df[
                "priority"
            ] = (
                priority_investment_df[
                    "priority"
                ]
                .astype(str)
                .str.strip()
            )


            priority_investment_df = (
                priority_investment_df[
                    priority_investment_df[
                        "priority"
                    ]
                    .notna()
                    &
                    (
                        priority_investment_df[
                            "priority"
                        ]
                        != ""
                    )
                ]
            )


            if not priority_investment_df.empty:

                st.markdown("---")

                st.markdown(
                    "### Investment by Recorded Priority"
                )

                st.caption(
                    "Priority values are taken directly from "
                    "the final dataset."
                )


                priority_investment = (
                    priority_investment_df
                    .groupby(
                        "priority",
                        as_index=False
                    )
                    .agg(
                        Customers=(
                            "_estimated_cost_numeric",
                            "size"
                        ),
                        Total_Investment=(
                            "_estimated_cost_numeric",
                            "sum"
                        ),
                        Average_Cost=(
                            "_estimated_cost_numeric",
                            "mean"
                        ),
                    )
                    .sort_values(
                        "Total_Investment",
                        ascending=False,
                    )
                )


                priority_investment[
                    "Average_Cost"
                ] = (
                    priority_investment[
                        "Average_Cost"
                    ]
                    .round(2)
                )


                priority_investment[
                    "Investment_Share"
                ] = (
                    priority_investment[
                        "Total_Investment"
                    ]
                    / total_investment
                    * 100
                ).round(2)


                priority_chart_col, priority_table_col = (
                    st.columns([1.7, 1])
                )


                # ============================================
                # PRIORITY INVESTMENT CHART
                # ============================================

                with priority_chart_col:

                    fig_priority_investment = px.bar(
                        priority_investment,
                        x="priority",
                        y="Total_Investment",
                        text="Total_Investment",
                    )


                    fig_priority_investment.update_traces(
                        texttemplate="%{text:,.0f}",
                        textposition="outside",
                    )


                    fig_priority_investment.update_layout(
                        height=390,
                        margin=dict(
                            l=20,
                            r=20,
                            t=30,
                            b=20,
                        ),
                        xaxis_title=None,
                        yaxis_title="Estimated Investment",
                        showlegend=False,
                    )


                    st.plotly_chart(
                        fig_priority_investment,
                        use_container_width=True,
                    )


                # ============================================
                # PRIORITY INVESTMENT TABLE
                # ============================================

                with priority_table_col:

                    priority_display = (
                        priority_investment[
                            [
                                "priority",
                                "Customers",
                                "Total_Investment",
                                "Average_Cost",
                                "Investment_Share",
                            ]
                        ]
                        .copy()
                    )


                    priority_display.columns = [
                        "Priority",
                        "Customers",
                        "Total Investment",
                        "Average Cost",
                        "Investment Share",
                    ]


                    priority_display[
                        "Total Investment"
                    ] = (
                        priority_display[
                            "Total Investment"
                        ]
                        .map(
                            lambda value:
                            f"{value:,.0f}"
                        )
                    )


                    priority_display[
                        "Average Cost"
                    ] = (
                        priority_display[
                            "Average Cost"
                        ]
                        .map(
                            lambda value:
                            f"{value:,.2f}"
                        )
                    )


                    priority_display[
                        "Investment Share"
                    ] = (
                        priority_display[
                            "Investment Share"
                        ]
                        .map(
                            lambda value:
                            f"{value:.2f}%"
                        )
                    )


                    st.dataframe(
                        priority_display,
                        use_container_width=True,
                        hide_index=True,
                        height=390,
                    )


        else:

            st.info(
                "The priority column is not available in the "
                "final dataset. Priority-wise investment analysis "
                "has been skipped."
            )


        # ====================================================
        # RECORDED COST SUMMARY
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### Recorded Investment Summary"
        )


        summary_columns = [
            "estimated_cost"
        ]


        if "priority" in valid_investment_df.columns:

            summary_columns.append(
                "priority"
            )


        if "recommendation" in valid_investment_df.columns:

            summary_columns.append(
                "recommendation"
            )


        summary_source = (
            valid_investment_df[
                summary_columns
            ]
            .copy()
        )


        summary_source[
            "Estimated Cost"
        ] = (
            valid_investment_df[
                "_estimated_cost_numeric"
            ]
        )


        summary_source = summary_source.drop(
            columns=["estimated_cost"],
            errors="ignore",
        )


        # Rename actual fields only
        rename_mapping = {}


        if "priority" in summary_source.columns:

            rename_mapping[
                "priority"
            ] = "Priority"


        if "recommendation" in summary_source.columns:

            rename_mapping[
                "recommendation"
            ] = "Recommendation"


        summary_source = summary_source.rename(
            columns=rename_mapping
        )


        # Put estimated cost first
        ordered_columns = [
            "Estimated Cost"
        ] + [
            column
            for column in summary_source.columns
            if column != "Estimated Cost"
        ]


        summary_source = summary_source[
            ordered_columns
        ]


        st.dataframe(
            summary_source.head(1000),
            use_container_width=True,
            hide_index=True,
            height=380,
        )


        st.caption(
            "The detailed table is limited to the first 1,000 "
            "records for display performance. Calculations above "
            "use all valid estimated_cost records."
        )


        # ====================================================
        # CLEAN TEMPORARY COLUMN
        # ====================================================

        # This does not modify the CSV.
        # It only removes the temporary column from the
        # in-memory dataframe used by this section.

        investment_df.drop(
            columns=["_estimated_cost_numeric"],
            errors="ignore",
        ) 
#5
# ============================================================
# OWNER & WORKLOAD
# ============================================================

st.markdown("---")

st.subheader("Owner & Workload")

st.caption(
    "Review the distribution of retention cases across the "
    "responsible owners recorded in the finalized dataset."
)


# ============================================================
# CHECK ACTUAL OWNER COLUMN
# ============================================================

if "owner" not in retention_df.columns:

    st.warning(
        "The owner column is not available in "
        "customer_360_final.csv. Owner & Workload analysis "
        "has been skipped."
    )

else:

    # ========================================================
    # CREATE WORKING COPY
    # ========================================================

    owner_workload_df = retention_df[
        [
            "customer_unique_id",
            "owner",
        ]
        + (
            ["recommendation"]
            if "recommendation" in retention_df.columns
            else []
        )
        + (
            ["priority"]
            if "priority" in retention_df.columns
            else []
        )
        + (
            ["timeline"]
            if "timeline" in retention_df.columns
            else []
        )
    ].copy()


    # ========================================================
    # CLEAN OWNER VALUES
    # ========================================================

    owner_workload_df["owner"] = (
        owner_workload_df["owner"]
        .astype("string")
        .str.strip()
    )


    owner_workload_df = owner_workload_df[
        owner_workload_df["owner"].notna()
        &
        (
            owner_workload_df["owner"] != ""
        )
    ].copy()


    # ========================================================
    # CHECK VALID OWNER DATA
    # ========================================================

    if owner_workload_df.empty:

        st.info(
            "The owner column exists, but no usable owner "
            "values are available in the final dataset."
        )

    else:

        # ====================================================
        # ACTUAL OWNER WORKLOAD
        # ====================================================

        owner_counts = (
            owner_workload_df
            .groupby(
                "owner",
                as_index=False
            )
            .agg(
                Cases=(
                    "customer_unique_id",
                    "count",
                )
            )
            .sort_values(
                "Cases",
                ascending=False,
            )
        )


        # ====================================================
        # WORKLOAD SHARE
        # ====================================================

        total_owner_cases = (
            owner_counts["Cases"].sum()
        )


        if total_owner_cases > 0:

            owner_counts["Workload Share"] = (
                owner_counts["Cases"]
                / total_owner_cases
                * 100
            )

            owner_counts["Workload Share"] = (
                owner_counts["Workload Share"]
                .round(2)
            )

        else:

            owner_counts["Workload Share"] = 0.0


        # ====================================================
        # OVERVIEW METRICS
        # ====================================================

        owner_kpi_1, owner_kpi_2, owner_kpi_3 = st.columns(3)


        with owner_kpi_1:

            st.metric(
                "Responsible Owners",
                f"{owner_counts.shape[0]:,}"
            )


        with owner_kpi_2:

            st.metric(
                "Assigned Cases",
                f"{total_owner_cases:,}"
            )


        with owner_kpi_3:

            highest_workload_owner = (
                owner_counts.iloc[0]["owner"]
            )

            st.metric(
                "Largest Workload",
                str(highest_workload_owner)
            )


        # ====================================================
        # WORKLOAD DISTRIBUTION
        # ====================================================

        st.markdown(
            "### Workload Distribution"
        )

        st.caption(
            "Owner values and case counts are taken directly "
            "from the final dataset."
        )


        owner_chart_col, owner_table_col = st.columns(
            [1.7, 1]
        )


        # ====================================================
        # OWNER CHART
        # ====================================================

        with owner_chart_col:

            fig_owner = px.bar(
                owner_counts,
                x="Cases",
                y="owner",
                orientation="h",
                text="Cases",
            )


            fig_owner.update_traces(
                textposition="outside"
            )


            fig_owner.update_layout(
                height=max(
                    360,
                    min(
                        600,
                        owner_counts.shape[0] * 75,
                    ),
                ),
                margin=dict(
                    l=20,
                    r=35,
                    t=25,
                    b=20,
                ),
                xaxis_title="Retention Cases",
                yaxis_title=None,
                showlegend=False,
            )


            st.plotly_chart(
                fig_owner,
                use_container_width=True,
            )


        # ====================================================
        # OWNER TABLE
        # ====================================================

        with owner_table_col:

            owner_display = (
                owner_counts[
                    [
                        "owner",
                        "Cases",
                        "Workload Share",
                    ]
                ]
                .copy()
            )


            owner_display.columns = [
                "Responsible Owner",
                "Cases",
                "Workload Share",
            ]


            owner_display["Workload Share"] = (
                owner_display["Workload Share"]
                .map(
                    lambda value:
                    f"{value:.2f}%"
                )
            )


            st.dataframe(
                owner_display,
                use_container_width=True,
                hide_index=True,
                height=360,
            )


        # ====================================================
        # OWNER CASE DETAILS
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### Owner Case Details"
        )

        st.caption(
            "Additional breakdowns are shown only when the "
            "corresponding fields are present in the final dataset."
        )


        # ====================================================
        # RECOMMENDATION BY OWNER
        # ====================================================

        if "recommendation" in owner_workload_df.columns:

            owner_recommendation_df = (
                owner_workload_df[
                    [
                        "owner",
                        "recommendation",
                    ]
                ]
                .copy()
            )


            owner_recommendation_df[
                "recommendation"
            ] = (
                owner_recommendation_df[
                    "recommendation"
                ]
                .astype("string")
                .str.strip()
            )


            owner_recommendation_df = (
                owner_recommendation_df[
                    owner_recommendation_df[
                        "recommendation"
                    ].notna()
                    &
                    (
                        owner_recommendation_df[
                            "recommendation"
                        ] != ""
                    )
                ]
            )


            if not owner_recommendation_df.empty:

                owner_recommendation_counts = (
                    owner_recommendation_df
                    .groupby(
                        [
                            "owner",
                            "recommendation",
                        ],
                        as_index=False,
                    )
                    .size()
                )


                owner_recommendation_counts = (
                    owner_recommendation_counts
                    .rename(
                        columns={
                            "size": "Cases"
                        }
                    )
                )


                recommendation_owner_pivot = (
                    owner_recommendation_counts
                    .pivot(
                        index="owner",
                        columns="recommendation",
                        values="Cases",
                    )
                    .fillna(0)
                    .astype(int)
                )


                st.markdown(
                    "#### Recommendation Mix by Owner"
                )


                st.dataframe(
                    recommendation_owner_pivot,
                    use_container_width=True,
                )

            else:

                st.info(
                    "No usable recommendation values are "
                    "available for an owner-level breakdown."
                )

        else:

            st.info(
                "The recommendation column is not available "
                "in the final dataset. Recommendation workload "
                "breakdown has been skipped."
            )


        # ====================================================
        # PRIORITY BY OWNER
        # ====================================================

        if "priority" in owner_workload_df.columns:

            owner_priority_df = (
                owner_workload_df[
                    [
                        "owner",
                        "priority",
                    ]
                ]
                .copy()
            )


            owner_priority_df["priority"] = (
                owner_priority_df["priority"]
                .astype("string")
                .str.strip()
            )


            owner_priority_df = (
                owner_priority_df[
                    owner_priority_df["priority"].notna()
                    &
                    (
                        owner_priority_df["priority"]
                        != ""
                    )
                ]
            )


            if not owner_priority_df.empty:

                owner_priority_counts = (
                    owner_priority_df
                    .groupby(
                        [
                            "owner",
                            "priority",
                        ],
                        as_index=False,
                    )
                    .size()
                    .rename(
                        columns={
                            "size": "Cases"
                        }
                    )
                )


                priority_owner_pivot = (
                    owner_priority_counts
                    .pivot(
                        index="owner",
                        columns="priority",
                        values="Cases",
                    )
                    .fillna(0)
                    .astype(int)
                )


                st.markdown(
                    "#### Priority Mix by Owner"
                )


                st.dataframe(
                    priority_owner_pivot,
                    use_container_width=True,
                )

            else:

                st.info(
                    "No usable priority values are available "
                    "for an owner-level breakdown."
                )

        else:

            st.info(
                "The priority column is not available in "
                "the final dataset. Priority workload "
                "breakdown has been skipped."
            )


        # ====================================================
        # TIMELINE BY OWNER
        # ====================================================

        if "timeline" in owner_workload_df.columns:

            owner_timeline_df = (
                owner_workload_df[
                    [
                        "owner",
                        "timeline",
                    ]
                ]
                .copy()
            )


            owner_timeline_df["timeline"] = (
                owner_timeline_df["timeline"]
                .astype("string")
                .str.strip()
            )


            owner_timeline_df = (
                owner_timeline_df[
                    owner_timeline_df["timeline"].notna()
                    &
                    (
                        owner_timeline_df["timeline"]
                        != ""
                    )
                ]
            )


            if not owner_timeline_df.empty:

                owner_timeline_counts = (
                    owner_timeline_df
                    .groupby(
                        [
                            "owner",
                            "timeline",
                        ],
                        as_index=False,
                    )
                    .size()
                    .rename(
                        columns={
                            "size": "Cases"
                        }
                    )
                )


                timeline_owner_pivot = (
                    owner_timeline_counts
                    .pivot(
                        index="owner",
                        columns="timeline",
                        values="Cases",
                    )
                    .fillna(0)
                    .astype(int)
                )


                st.markdown(
                    "#### Timeline Mix by Owner"
                )


                st.dataframe(
                    timeline_owner_pivot,
                    use_container_width=True,
                )

            else:

                st.info(
                    "No usable timeline values are available "
                    "for an owner-level breakdown."
                )

        else:

            st.info(
                "The timeline column is not available in "
                "the final dataset. Timeline workload "
                "breakdown has been skipped."
            )


        # ====================================================
        # OWNER DETAIL TABLE
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### Owner Workload Register"
        )

        st.caption(
            "Customer-level owner assignments from the "
            "finalized dataset."
        )


        register_columns = [
            "customer_unique_id",
            "owner",
        ]


        if "recommendation" in owner_workload_df.columns:

            register_columns.append(
                "recommendation"
            )


        if "priority" in owner_workload_df.columns:

            register_columns.append(
                "priority"
            )


        if "timeline" in owner_workload_df.columns:

            register_columns.append(
                "timeline"
            )


        owner_register = (
            owner_workload_df[
                register_columns
            ]
            .copy()
        )


        owner_register = owner_register.rename(
            columns={
                "customer_unique_id":
                    "Customer ID",
                "owner":
                    "Responsible Owner",
                "recommendation":
                    "Recommendation",
                "priority":
                    "Priority",
                "timeline":
                    "Timeline",
            }
        )


        st.dataframe(
            owner_register.head(1000),
            use_container_width=True,
            hide_index=True,
            height=400,
        )


        st.caption(
            "The workload calculations use all available owner "
            "records. The detailed register is limited to the "
            "first 1,000 records for display performance."
        ) 
#6
# ============================================================
# RETENTION TIMELINE
# ============================================================

st.subheader("Retention Timeline")
st.caption(
    "Operational view of when recorded retention actions are scheduled to be handled."
)

# ------------------------------------------------------------
# Validate timeline column before using it
# ------------------------------------------------------------

TIMELINE_COLUMN = "timeline"

if TIMELINE_COLUMN not in df.columns:

    st.warning(
        "The 'timeline' column is not available in the final dataset. "
        "Retention Timeline has been skipped because no timeline information "
        "is present in customer_360_final.csv."
    )

else:

    # --------------------------------------------------------
    # Inspect actual timeline values
    # --------------------------------------------------------

    timeline_series = df[TIMELINE_COLUMN].copy()

    # Keep only recorded/non-empty values.
    # No categories or values are invented.
    timeline_values = timeline_series.dropna()

    # Convert values to strings only for safe display/grouping.
    timeline_values = timeline_values.astype(str).str.strip()

    # Remove empty strings created by blank cells.
    timeline_values = timeline_values[timeline_values != ""]

    if timeline_values.empty:

        st.info(
            "The 'timeline' column exists in the final dataset, "
            "but it contains no recorded timeline values. "
            "Retention Timeline has been skipped."
        )

    else:

        # ----------------------------------------------------
        # Actual timeline distribution
        # ----------------------------------------------------

        timeline_counts = (
            timeline_values
            .value_counts(dropna=False)
            .rename_axis("timeline")
            .reset_index(name="cases")
        )

        # Preserve the actual order returned from the dataset's
        # observed values. No chronological order is assumed.
        actual_timeline_order = timeline_counts["timeline"].tolist()

        total_timeline_cases = int(timeline_counts["cases"].sum())

        # ----------------------------------------------------
        # Operational summary
        # ----------------------------------------------------

        st.markdown("### Scheduled Retention Workload")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric(
                "Recorded Timeline Cases",
                f"{total_timeline_cases:,}"
            )

        with metric_col2:
            st.metric(
                "Timeline Categories",
                f"{len(actual_timeline_order):,}"
            )

        with metric_col3:
            if total_timeline_cases > 0:
                top_timeline = timeline_counts.iloc[0]["timeline"]
                top_timeline_cases = int(
                    timeline_counts.iloc[0]["cases"]
                )

                st.metric(
                    "Highest Recorded Workload",
                    f"{top_timeline_cases:,}"
                )

                st.caption(
                    f"Recorded as: {top_timeline}"
                )
            else:
                st.metric(
                    "Highest Recorded Workload",
                    "0"
                )

        # ----------------------------------------------------
        # Timeline workload distribution
        # ----------------------------------------------------

        st.markdown("### Workload by Recorded Timeline")

        col_chart, col_table = st.columns([2, 1])

        with col_chart:

            import plotly.express as px

            fig_timeline = px.bar(
                timeline_counts,
                x="timeline",
                y="cases",
                text="cases",
                category_orders={
                    "timeline": actual_timeline_order
                }
            )

            fig_timeline.update_traces(
                textposition="outside"
            )

            fig_timeline.update_layout(
                xaxis_title="Recorded Timeline",
                yaxis_title="Retention Cases",
                showlegend=False,
                height=430,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig_timeline,
                use_container_width=True
            )

        with col_table:

            timeline_display = timeline_counts.copy()

            timeline_display["share"] = (
                timeline_display["cases"]
                / total_timeline_cases
                * 100
            ).round(2)

            timeline_display = timeline_display.rename(
                columns={
                    "timeline": "Timeline",
                    "cases": "Cases",
                    "share": "Workload Share %"
                }
            )

            st.dataframe(
                timeline_display,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Operational interpretation
        # ----------------------------------------------------

        st.markdown("### Timeline Coverage")

        st.info(
            f"The final dataset contains {total_timeline_cases:,} "
            f"customer records with a recorded retention timeline "
            f"across {len(actual_timeline_order):,} observed timeline value(s). "
            "The distribution above reflects the values recorded in the "
            "final dataset without imposing an assumed chronological order."
        )

        # ----------------------------------------------------
        # Detailed timeline workload
        # ----------------------------------------------------

        with st.expander("View Recorded Timeline Details"):

            detail_df = df[
                df[TIMELINE_COLUMN].notna()
            ].copy()

            detail_df[TIMELINE_COLUMN] = (
                detail_df[TIMELINE_COLUMN]
                .astype(str)
                .str.strip()
            )

            detail_df = detail_df[
                detail_df[TIMELINE_COLUMN] != ""
            ]

            st.dataframe(
                detail_df,
                use_container_width=True,
                hide_index=True
            )     
#7
# ============================================================
# CUSTOMER ACTION PLAN
# ============================================================

st.subheader("Customer Action Plan")
st.caption(
    "Customer-level operational view based only on retention action information "
    "recorded in the final dataset."
)

# ------------------------------------------------------------
# Source validation
# ------------------------------------------------------------

required_source_columns = [
    "customer_unique_id",
    "recommendation",
    "reason",
    "priority",
    "owner",
    "timeline",
    "estimated_cost",
    "expected_outcome"
]

available_source_columns = [
    col for col in required_source_columns
    if col in df.columns
]

missing_source_columns = [
    col for col in required_source_columns
    if col not in df.columns
]

# ------------------------------------------------------------
# Show missing fields safely
# ------------------------------------------------------------

if missing_source_columns:

    st.info(
        "Some expected action-plan fields are not available in the final "
        "dataset. Only the fields actually present will be used."
    )

    st.caption(
        "Unavailable fields: "
        + ", ".join(missing_source_columns)
    )

# ------------------------------------------------------------
# Check whether enough actual information exists
# ------------------------------------------------------------

if not available_source_columns:

    st.warning(
        "No customer action-plan fields are available in the final dataset. "
        "Customer Action Plan has been skipped."
    )

else:

    # --------------------------------------------------------
    # Work only with columns actually present
    # --------------------------------------------------------

    action_plan_df = df[available_source_columns].copy()

    # --------------------------------------------------------
    # Remove completely empty columns
    # --------------------------------------------------------

    usable_columns = []

    for column in action_plan_df.columns:

        non_null_values = action_plan_df[column].dropna()

        if len(non_null_values) == 0:
            continue

        if action_plan_df[column].dtype == "object":

            non_empty_values = (
                non_null_values
                .astype(str)
                .str.strip()
            )

            if (non_empty_values != "").any():
                usable_columns.append(column)

        else:
            usable_columns.append(column)

    action_plan_df = action_plan_df[usable_columns]

    # --------------------------------------------------------
    # Check whether any actual action information remains
    # --------------------------------------------------------

    if action_plan_df.empty or action_plan_df.shape[1] == 0:

        st.warning(
            "The available action-plan fields contain no recorded values. "
            "Customer Action Plan has been skipped."
        )

    else:

        # ----------------------------------------------------
        # Customer Action Plan Summary
        # ----------------------------------------------------

        st.markdown("### Action Plan Overview")

        metric_columns = st.columns(3)

        with metric_columns[0]:

            if "customer_unique_id" in action_plan_df.columns:

                customer_count = (
                    action_plan_df["customer_unique_id"]
                    .dropna()
                    .nunique()
                )

                st.metric(
                    "Customers in Action Plan",
                    f"{customer_count:,}"
                )

            else:

                st.metric(
                    "Customer Identifier",
                    "Not available"
                )

        with metric_columns[1]:

            if "recommendation" in action_plan_df.columns:

                recommendation_count = (
                    action_plan_df["recommendation"]
                    .dropna()
                    .astype(str)
                    .str.strip()
                )

                recommendation_count = (
                    recommendation_count[
                        recommendation_count != ""
                    ]
                    .nunique()
                )

                st.metric(
                    "Recorded Recommendations",
                    f"{recommendation_count:,}"
                )

            else:

                st.metric(
                    "Recommendation",
                    "Not available"
                )

        with metric_columns[2]:

            if "owner" in action_plan_df.columns:

                owner_count = (
                    action_plan_df["owner"]
                    .dropna()
                    .astype(str)
                    .str.strip()
                )

                owner_count = (
                    owner_count[
                        owner_count != ""
                    ]
                    .nunique()
                )

                st.metric(
                    "Recorded Owners",
                    f"{owner_count:,}"
                )

            else:

                st.metric(
                    "Owner",
                    "Not available"
                )

        # ----------------------------------------------------
        # Customer-level operational table
        # ----------------------------------------------------

        st.markdown("### Customer Action Workspace")

        display_df = action_plan_df.copy()

        # Rename only columns that actually exist
        rename_map = {}

        if "customer_unique_id" in display_df.columns:
            rename_map["customer_unique_id"] = "Customer ID"

        if "recommendation" in display_df.columns:
            rename_map["recommendation"] = "Recommendation"

        if "reason" in display_df.columns:
            rename_map["reason"] = "Reason"

        if "priority" in display_df.columns:
            rename_map["priority"] = "Priority"

        if "owner" in display_df.columns:
            rename_map["owner"] = "Owner"

        if "timeline" in display_df.columns:
            rename_map["timeline"] = "Timeline"

        if "estimated_cost" in display_df.columns:
            rename_map["estimated_cost"] = "Estimated Cost"

        if "expected_outcome" in display_df.columns:
            rename_map["expected_outcome"] = "Expected Outcome"

        display_df = display_df.rename(
            columns=rename_map
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Customer search
        # ----------------------------------------------------

        if "customer_unique_id" in action_plan_df.columns:

            st.markdown("### Customer Action Lookup")

            customer_ids = (
                action_plan_df["customer_unique_id"]
                .dropna()
                .astype(str)
                .str.strip()
            )

            customer_ids = sorted(
                customer_ids[
                    customer_ids != ""
                ].unique()
            )

            if customer_ids:

                selected_customer = st.selectbox(
                    "Select Customer",
                    customer_ids
                )

                selected_customer_df = action_plan_df[
                    action_plan_df["customer_unique_id"]
                    .astype(str)
                    .str.strip()
                    == selected_customer
                ].copy()

                if not selected_customer_df.empty:

                    st.markdown(
                        "#### Recorded Customer Action Details"
                    )

                    detail_columns = []

                    for column in [
                        "customer_unique_id",
                        "recommendation",
                        "reason",
                        "priority",
                        "owner",
                        "timeline",
                        "estimated_cost",
                        "expected_outcome"
                    ]:

                        if column in selected_customer_df.columns:
                            detail_columns.append(column)

                    customer_detail = (
                        selected_customer_df[
                            detail_columns
                        ]
                        .T
                        .reset_index()
                    )

                    customer_detail.columns = [
                        "Field",
                        "Recorded Value"
                    ]

                    customer_detail["Field"] = (
                        customer_detail["Field"]
                        .replace(rename_map)
                    )

                    st.dataframe(
                        customer_detail,
                        use_container_width=True,
                        hide_index=True
                    )

            else:

                st.info(
                    "The customer identifier exists, but no non-empty "
                    "customer identifiers are recorded."
                )

        # ----------------------------------------------------
        # Priority distribution
        # ----------------------------------------------------

        if "priority" in action_plan_df.columns:

            priority_values = (
                action_plan_df["priority"]
                .dropna()
                .astype(str)
                .str.strip()
            )

            priority_values = priority_values[
                priority_values != ""
            ]

            if not priority_values.empty:

                priority_counts = (
                    priority_values
                    .value_counts()
                    .rename_axis("priority")
                    .reset_index(name="customers")
                )

                st.markdown("### Recorded Priority Distribution")

                col1, col2 = st.columns([2, 1])

                with col1:

                    import plotly.express as px

                    fig_priority = px.bar(
                        priority_counts,
                        x="priority",
                        y="customers",
                        text="customers"
                    )

                    fig_priority.update_traces(
                        textposition="outside"
                    )

                    fig_priority.update_layout(
                        xaxis_title="Recorded Priority",
                        yaxis_title="Customers",
                        showlegend=False,
                        height=400,
                        margin=dict(
                            l=20,
                            r=20,
                            t=30,
                            b=20
                        )
                    )

                    st.plotly_chart(
                        fig_priority,
                        use_container_width=True
                    )

                with col2:

                    st.dataframe(
                        priority_counts,
                        use_container_width=True,
                        hide_index=True
                    )

        # ----------------------------------------------------
        # Recorded recommendation distribution
        # ----------------------------------------------------

        if "recommendation" in action_plan_df.columns:

            recommendation_values = (
                action_plan_df["recommendation"]
                .dropna()
                .astype(str)
                .str.strip()
            )

            recommendation_values = (
                recommendation_values[
                    recommendation_values != ""
                ]
            )

            if not recommendation_values.empty:

                recommendation_counts = (
                    recommendation_values
                    .value_counts()
                    .rename_axis("recommendation")
                    .reset_index(name="customers")
                )

                st.markdown(
                    "### Recorded Retention Recommendations"
                )

                st.dataframe(
                    recommendation_counts,
                    use_container_width=True,
                    hide_index=True
                )

        # ----------------------------------------------------
        # Detailed operational fields
        # ----------------------------------------------------

        with st.expander(
            "View Available Action-Plan Fields"
        ):

            st.write(
                "The following fields are available in the final dataset "
                "and were used for this section:"
            )

            st.write(
                ", ".join(action_plan_df.columns.tolist())
            )                                            
#8
# ============================================================
# EXPECTED OUTCOME
# ============================================================

st.subheader("Expected Outcome")
st.caption(
    "Operational view of expected outcomes recorded in the final dataset."
)

# ------------------------------------------------------------
# Strict column validation
# ------------------------------------------------------------

EXPECTED_OUTCOME_COLUMN = "expected_outcome"

if EXPECTED_OUTCOME_COLUMN not in df.columns:

    st.warning(
        "The 'expected_outcome' column is not available in the final dataset. "
        "Expected Outcome has been skipped."
    )

else:

    # --------------------------------------------------------
    # Inspect actual values only
    # --------------------------------------------------------

    expected_outcome_values = (
        df[EXPECTED_OUTCOME_COLUMN]
        .dropna()
        .astype(str)
        .str.strip()
    )

    expected_outcome_values = expected_outcome_values[
        expected_outcome_values != ""
    ]

    # --------------------------------------------------------
    # No recorded values
    # --------------------------------------------------------

    if expected_outcome_values.empty:

        st.info(
            "The 'expected_outcome' column exists in the final dataset, "
            "but no non-empty expected outcome values are recorded."
        )

    else:

        # ----------------------------------------------------
        # Actual outcome distribution
        # ----------------------------------------------------

        outcome_counts = (
            expected_outcome_values
            .value_counts()
            .rename_axis("expected_outcome")
            .reset_index(name="customers")
        )

        total_recorded_outcomes = int(
            outcome_counts["customers"].sum()
        )

        unique_outcomes = int(
            outcome_counts["expected_outcome"].nunique()
        )

        # ----------------------------------------------------
        # Operational summary
        # ----------------------------------------------------

        st.markdown("### Recorded Outcome Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Recorded Outcome Cases",
                f"{total_recorded_outcomes:,}"
            )

        with col2:
            st.metric(
                "Recorded Outcome Values",
                f"{unique_outcomes:,}"
            )

        with col3:
            top_outcome = outcome_counts.iloc[0]["expected_outcome"]
            top_outcome_count = int(
                outcome_counts.iloc[0]["customers"]
            )

            st.metric(
                "Most Recorded Outcome",
                f"{top_outcome_count:,}"
            )

            st.caption(
                f"Recorded value: {top_outcome}"
            )

        # ----------------------------------------------------
        # Distribution
        # ----------------------------------------------------

        st.markdown("### Expected Outcome Distribution")

        chart_col, table_col = st.columns([2, 1])

        with chart_col:

            import plotly.express as px

            fig_outcome = px.bar(
                outcome_counts,
                x="expected_outcome",
                y="customers",
                text="customers"
            )

            fig_outcome.update_traces(
                textposition="outside"
            )

            fig_outcome.update_layout(
                xaxis_title="Recorded Expected Outcome",
                yaxis_title="Customer Records",
                showlegend=False,
                height=430,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig_outcome,
                use_container_width=True
            )

        with table_col:

            outcome_table = outcome_counts.copy()

            outcome_table["share"] = (
                outcome_table["customers"]
                / total_recorded_outcomes
                * 100
            ).round(2)

            outcome_table = outcome_table.rename(
                columns={
                    "expected_outcome": "Expected Outcome",
                    "customers": "Records",
                    "share": "Share %"
                }
            )

            st.dataframe(
                outcome_table,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Actual recorded outcome details
        # ----------------------------------------------------

        st.markdown("### Recorded Expected Outcomes")

        st.dataframe(
            outcome_counts.rename(
                columns={
                    "expected_outcome": "Expected Outcome",
                    "customers": "Customer Records"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Customer-level records
        # ----------------------------------------------------

        if "customer_unique_id" in df.columns:

            st.markdown("### Customer-Level Outcome View")

            customer_outcome_df = df[
                [
                    "customer_unique_id",
                    EXPECTED_OUTCOME_COLUMN
                ]
            ].copy()

            customer_outcome_df[
                EXPECTED_OUTCOME_COLUMN
            ] = (
                customer_outcome_df[
                    EXPECTED_OUTCOME_COLUMN
                ]
                .astype("string")
                .str.strip()
            )

            customer_outcome_df = customer_outcome_df[
                customer_outcome_df[
                    EXPECTED_OUTCOME_COLUMN
                ].notna()
                &
                (
                    customer_outcome_df[
                        EXPECTED_OUTCOME_COLUMN
                    ] != ""
                )
            ]

            customer_outcome_df = (
                customer_outcome_df.rename(
                    columns={
                        "customer_unique_id": "Customer ID",
                        EXPECTED_OUTCOME_COLUMN:
                            "Expected Outcome"
                    }
                )
            )

            st.dataframe(
                customer_outcome_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "The customer identifier column is not available "
                "in the final dataset, so the customer-level outcome "
                "view cannot be displayed."
            )

        # ----------------------------------------------------
        # Actual values inspection
        # ----------------------------------------------------

        with st.expander(
            "View Actual Expected Outcome Values"
        ):

            st.write(
                outcome_counts[
                    "expected_outcome"
                ].tolist()
            )    
#9
# ============================================================
# RETENTION STRATEGY INSIGHTS
# ============================================================

st.subheader("Retention Strategy Insights")
st.caption(
    "Business-focused retention observations derived only from "
    "recorded values in the final customer dataset."
)

# ------------------------------------------------------------
# Helper: safely identify usable columns
# ------------------------------------------------------------

def has_usable_column(dataframe, column_name):
    if column_name not in dataframe.columns:
        return False

    series = dataframe[column_name].dropna()

    if series.empty:
        return False

    if series.dtype == "object":
        series = series.astype(str).str.strip()
        series = series[series != ""]

        if series.empty:
            return False

    return True


def get_non_empty_values(dataframe, column_name):
    if not has_usable_column(dataframe, column_name):
        return None

    values = dataframe[column_name].dropna()

    if values.dtype == "object":
        values = values.astype(str).str.strip()
        values = values[values != ""]

    return values


# ------------------------------------------------------------
# Validate actual retention-related fields
# ------------------------------------------------------------

strategy_columns = [
    "recommendation",
    "priority",
    "owner",
    "timeline",
    "estimated_cost",
    "expected_outcome",
    "reason",
    "customer_value_tier",
    "risk_segment"
]

available_strategy_columns = [
    column
    for column in strategy_columns
    if has_usable_column(df, column)
]


# ------------------------------------------------------------
# No usable strategy information
# ------------------------------------------------------------

if not available_strategy_columns:

    st.warning(
        "No usable retention-strategy fields are available in the "
        "final dataset. Retention Strategy Insights has been skipped."
    )

else:

    # --------------------------------------------------------
    # Recorded strategy coverage
    # --------------------------------------------------------

    st.markdown("### Recorded Retention Structure")

    coverage_data = []

    for column in available_strategy_columns:

        values = get_non_empty_values(df, column)

        if values is not None:

            coverage_data.append(
                {
                    "Field": column,
                    "Recorded Records": int(len(values)),
                    "Distinct Values": int(values.nunique())
                }
            )

    if coverage_data:

        coverage_df = pd.DataFrame(coverage_data)

        st.dataframe(
            coverage_df,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # Recommendation-based operational insight
    # --------------------------------------------------------

    if has_usable_column(df, "recommendation"):

        recommendation_values = get_non_empty_values(
            df,
            "recommendation"
        )

        recommendation_counts = (
            recommendation_values
            .value_counts()
            .rename_axis("recommendation")
            .reset_index(name="records")
        )

        if not recommendation_counts.empty:

            st.markdown("### Recorded Retention Actions")

            chart_col, insight_col = st.columns([2, 1])

            with chart_col:

                import plotly.express as px

                fig_recommendation = px.bar(
                    recommendation_counts,
                    x="recommendation",
                    y="records",
                    text="records"
                )

                fig_recommendation.update_traces(
                    textposition="outside"
                )

                fig_recommendation.update_layout(
                    xaxis_title="Recorded Recommendation",
                    yaxis_title="Customer Records",
                    showlegend=False,
                    height=420,
                    margin=dict(
                        l=20,
                        r=20,
                        t=30,
                        b=20
                    )
                )

                st.plotly_chart(
                    fig_recommendation,
                    use_container_width=True
                )

            with insight_col:

                highest_recorded_action = (
                    recommendation_counts.iloc[0]
                )

                st.info(
                    f"The highest-volume recorded retention action is "
                    f"'{highest_recorded_action['recommendation']}', "
                    f"appearing in "
                    f"{int(highest_recorded_action['records']):,} "
                    f"customer record(s)."
                )

            st.dataframe(
                recommendation_counts.rename(
                    columns={
                        "recommendation": "Recorded Recommendation",
                        "records": "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Priority and recommendation relationship
    # --------------------------------------------------------

    if (
        has_usable_column(df, "priority")
        and
        has_usable_column(df, "recommendation")
    ):

        priority_recommendation = df[
            ["priority", "recommendation"]
        ].copy()

        priority_recommendation["priority"] = (
            priority_recommendation["priority"]
            .astype(str)
            .str.strip()
        )

        priority_recommendation["recommendation"] = (
            priority_recommendation["recommendation"]
            .astype(str)
            .str.strip()
        )

        priority_recommendation = (
            priority_recommendation[
                (priority_recommendation["priority"] != "")
                &
                (priority_recommendation["recommendation"] != "")
            ]
        )

        if not priority_recommendation.empty:

            priority_action = (
                priority_recommendation
                .groupby(
                    ["priority", "recommendation"],
                    as_index=False
                )
                .size()
                .rename(columns={"size": "records"})
            )

            st.markdown(
                "### Recorded Priority and Action Alignment"
            )

            st.dataframe(
                priority_action.rename(
                    columns={
                        "priority": "Recorded Priority",
                        "recommendation":
                            "Recorded Recommendation",
                        "records": "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Owner and recommendation relationship
    # --------------------------------------------------------

    if (
        has_usable_column(df, "owner")
        and
        has_usable_column(df, "recommendation")
    ):

        owner_recommendation = df[
            ["owner", "recommendation"]
        ].copy()

        owner_recommendation["owner"] = (
            owner_recommendation["owner"]
            .astype(str)
            .str.strip()
        )

        owner_recommendation["recommendation"] = (
            owner_recommendation["recommendation"]
            .astype(str)
            .str.strip()
        )

        owner_recommendation = (
            owner_recommendation[
                (owner_recommendation["owner"] != "")
                &
                (owner_recommendation["recommendation"] != "")
            ]
        )

        if not owner_recommendation.empty:

            owner_action = (
                owner_recommendation
                .groupby(
                    ["owner", "recommendation"],
                    as_index=False
                )
                .size()
                .rename(columns={"size": "records"})
                .sort_values(
                    "records",
                    ascending=False
                )
            )

            st.markdown(
                "### Recorded Owner-to-Action Workload"
            )

            st.dataframe(
                owner_action.rename(
                    columns={
                        "owner": "Recorded Owner",
                        "recommendation":
                            "Recorded Recommendation",
                        "records": "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Timeline and recommendation relationship
    # --------------------------------------------------------

    if (
        has_usable_column(df, "timeline")
        and
        has_usable_column(df, "recommendation")
    ):

        timeline_recommendation = df[
            ["timeline", "recommendation"]
        ].copy()

        timeline_recommendation["timeline"] = (
            timeline_recommendation["timeline"]
            .astype(str)
            .str.strip()
        )

        timeline_recommendation["recommendation"] = (
            timeline_recommendation["recommendation"]
            .astype(str)
            .str.strip()
        )

        timeline_recommendation = (
            timeline_recommendation[
                (timeline_recommendation["timeline"] != "")
                &
                (timeline_recommendation["recommendation"] != "")
            ]
        )

        if not timeline_recommendation.empty:

            timeline_action = (
                timeline_recommendation
                .groupby(
                    ["timeline", "recommendation"],
                    as_index=False
                )
                .size()
                .rename(columns={"size": "records"})
                .sort_values(
                    "records",
                    ascending=False
                )
            )

            st.markdown(
                "### Recorded Timeline and Action Alignment"
            )

            st.dataframe(
                timeline_action.rename(
                    columns={
                        "timeline": "Recorded Timeline",
                        "recommendation":
                            "Recorded Recommendation",
                        "records": "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Cost visibility
    # --------------------------------------------------------

    if has_usable_column(df, "estimated_cost"):

        cost_series = pd.to_numeric(
            df["estimated_cost"],
            errors="coerce"
        ).dropna()

        if not cost_series.empty:

            st.markdown("### Recorded Retention Investment")

            cost_col1, cost_col2, cost_col3 = st.columns(3)

            with cost_col1:
                st.metric(
                    "Recorded Cost Records",
                    f"{len(cost_series):,}"
                )

            with cost_col2:
                st.metric(
                    "Total Recorded Estimated Cost",
                    f"{cost_series.sum():,.2f}"
                )

            with cost_col3:
                st.metric(
                    "Average Recorded Estimated Cost",
                    f"{cost_series.mean():,.2f}"
                )

            st.caption(
                "These figures reflect only numeric values actually "
                "recorded in the estimated_cost field."
            )

    # --------------------------------------------------------
    # Expected outcome linkage
    # --------------------------------------------------------

    if (
        has_usable_column(df, "recommendation")
        and
        has_usable_column(df, "expected_outcome")
    ):

        recommendation_outcome = df[
            ["recommendation", "expected_outcome"]
        ].copy()

        recommendation_outcome["recommendation"] = (
            recommendation_outcome["recommendation"]
            .astype(str)
            .str.strip()
        )

        recommendation_outcome["expected_outcome"] = (
            recommendation_outcome["expected_outcome"]
            .astype(str)
            .str.strip()
        )

        recommendation_outcome = (
            recommendation_outcome[
                (recommendation_outcome["recommendation"] != "")
                &
                (recommendation_outcome["expected_outcome"] != "")
            ]
        )

        if not recommendation_outcome.empty:

            outcome_alignment = (
                recommendation_outcome
                .groupby(
                    [
                        "recommendation",
                        "expected_outcome"
                    ],
                    as_index=False
                )
                .size()
                .rename(columns={"size": "records"})
                .sort_values(
                    "records",
                    ascending=False
                )
            )

            st.markdown(
                "### Recorded Action and Expected Outcome Alignment"
            )

            st.dataframe(
                outcome_alignment.rename(
                    columns={
                        "recommendation":
                            "Recorded Recommendation",
                        "expected_outcome":
                            "Recorded Expected Outcome",
                        "records":
                            "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Customer value / risk context
    # --------------------------------------------------------
    # These fields are used only if they actually exist.
    # No values or categories are assumed.

    context_columns = []

    for column in [
        "customer_value_tier",
        "risk_segment"
    ]:

        if has_usable_column(df, column):
            context_columns.append(column)

    if (
        context_columns
        and
        has_usable_column(df, "recommendation")
    ):

        context_view_columns = (
            context_columns
            + ["recommendation"]
        )

        context_df = df[
            context_view_columns
        ].copy()

        for column in context_view_columns:

            context_df[column] = (
                context_df[column]
                .astype(str)
                .str.strip()
            )

        for column in context_view_columns:

            context_df = context_df[
                context_df[column] != ""
            ]

        if not context_df.empty:

            group_columns = (
                context_columns
                + ["recommendation"]
            )

            context_summary = (
                context_df
                .groupby(
                    group_columns,
                    as_index=False
                )
                .size()
                .rename(columns={"size": "records"})
                .sort_values(
                    "records",
                    ascending=False
                )
            )

            st.markdown(
                "### Recorded Customer Context and Actions"
            )

            st.dataframe(
                context_summary.rename(
                    columns={
                        "customer_value_tier":
                            "Recorded Customer Value Tier",
                        "risk_segment":
                            "Recorded Risk Segment",
                        "recommendation":
                            "Recorded Recommendation",
                        "records":
                            "Customer Records"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # Final business summary
    # --------------------------------------------------------

    st.markdown("### Retention Strategy Summary")

    summary_points = []

    if has_usable_column(df, "recommendation"):

        recommendation_values = get_non_empty_values(
            df,
            "recommendation"
        )

        if recommendation_values is not None:

            summary_points.append(
                f"{recommendation_values.nunique():,} distinct "
                "retention recommendation value(s) are recorded."
            )

    if has_usable_column(df, "owner"):

        owner_values = get_non_empty_values(
            df,
            "owner"
        )

        if owner_values is not None:

            summary_points.append(
                f"{owner_values.nunique():,} distinct owner value(s) "
                "are recorded."
            )

    if has_usable_column(df, "timeline"):

        timeline_values = get_non_empty_values(
            df,
            "timeline"
        )

        if timeline_values is not None:

            summary_points.append(
                f"{timeline_values.nunique():,} distinct timeline "
                "value(s) are recorded."
            )

    if has_usable_column(df, "expected_outcome"):

        outcome_values = get_non_empty_values(
            df,
            "expected_outcome"
        )

        if outcome_values is not None:

            summary_points.append(
                f"{outcome_values.nunique():,} distinct expected "
                "outcome value(s) are recorded."
            )

    if has_usable_column(df, "estimated_cost"):

        numeric_cost = pd.to_numeric(
            df["estimated_cost"],
            errors="coerce"
        ).dropna()

        if not numeric_cost.empty:

            summary_points.append(
                f"{len(numeric_cost):,} numeric estimated-cost "
                "record(s) are available."
            )

    if summary_points:

        for point in summary_points:
            st.write(f"• {point}")

    else:

        st.info(
            "No sufficient recorded retention information was available "
            "to create the strategy summary."
        )                    