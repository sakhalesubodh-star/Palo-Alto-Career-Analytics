
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Palo Alto Career Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
DATA_FOLDER = Path(
    r"C:\Users\nhp\Documents\Palo_Alto_Career_Analytics\Data"
)
DATA_PATH = DATA_FOLDER / "Palo Alto Networks.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

df = load_data(str(DATA_PATH))


# ---------------- INTERACTIVE FILTERS ----------------

st.sidebar.subheader("Employee Filters")

filtered_df = df.copy()

# Department filter
if "Department" in df.columns:
    departments = sorted(
        df["Department"].dropna().unique().tolist()
    )

    selected_departments = st.sidebar.multiselect(
        "Select Department",
        options=departments,
        default=departments
    )

    filtered_df = filtered_df[
        filtered_df["Department"].isin(selected_departments)
    ]

# Job role filter
if "JobRole" in filtered_df.columns:
    job_roles = sorted(
        filtered_df["JobRole"].dropna().unique().tolist()
    )

    selected_roles = st.sidebar.multiselect(
        "Select Job Role",
        options=job_roles,
        default=job_roles
    )

    filtered_df = filtered_df[
        filtered_df["JobRole"].isin(selected_roles)
    ]

# Career cluster filter (available after joining clustering results)
if "CareerCluster" in filtered_df.columns:
    clusters = sorted(
        filtered_df["CareerCluster"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_clusters = st.sidebar.multiselect(
        "Select Career Cluster",
        options=clusters,
        default=clusters
    )

    filtered_df = filtered_df[
        filtered_df["CareerCluster"]
        .astype(str)
        .isin(selected_clusters)
    ]

st.sidebar.caption(
    f"{len(filtered_df):,} of {len(df):,} records selected"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Career Intelligence")
st.sidebar.caption("Palo Alto Networks | HR Analytics")
st.sidebar.divider()

page = st.sidebar.radio(
    "Dashboard Navigation",
    [
        "Overview",
        "Promotion Gap Analysis",
        "Attrition Analysis",
        "Career Clusters",
        "Retention Insights"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Data source: Employee CSV dataset")

# ---------------- HEADER ----------------
st.set_page_config(
    page_title="Career Progression Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Career Progression & Retention Analytics")
st.caption(
    "Employee career progression, promotion gaps, and attrition insights"
)
st.divider()

# ---------------- OVERVIEW ----------------

if page == "Overview":
    st.subheader("HR Analytics Overview")

    # 1. Total employee records
    total_employees = len(filtered_df)

    # 2. Observed attrition rate
    attrition_rate = None

    if "Attrition" in filtered_df.columns:
        attrition = (
            filtered_df["Attrition"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        valid_attrition = attrition.isin(["yes", "no"])

        if valid_attrition.any():
            attrition_rate = (
                (attrition[valid_attrition] == "yes").mean() * 100
            )

    # 3. Average promotion gap
    avg_promotion_gap = None

    if "YearsSinceLastPromotion" in df.columns:
        promotion_years = pd.to_numeric(
            df["YearsSinceLastPromotion"],
            errors="coerce"
        )
        avg_promotion_gap = promotion_years.mean()

    # 4. Number of departments
    department_count = (
        df["Department"].nunique()
        if "Department" in df.columns
        else None
    )

    # Display KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Employees",
        f"{total_employees:,}"
    )

    col2.metric(
        "Observed Attrition Rate",
        f"{attrition_rate:.2f}%"
        if attrition_rate is not None
        else "N/A"
    )

    col3.metric(
        "Average Promotion Gap",
        f"{avg_promotion_gap:.2f} years"
        if pd.notna(avg_promotion_gap)
        else "N/A"
    )

    col4.metric(
        "Departments",
        str(department_count)
        if department_count is not None
        else "N/A"
    )

    st.divider()

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    with st.expander("View dataset columns"):
        st.write(df.columns.tolist())


# ---------------- PROMOTION GAP ANALYSIS ----------------

# ---------------- PROMOTION GAP ANALYSIS ----------------
elif page == "Promotion Gap Analysis":
    st.subheader("Promotion Gap Analysis")

    analysis_df = filtered_df.copy()

    if "YearsSinceLastPromotion" not in analysis_df.columns:
        st.warning(
            "YearsSinceLastPromotion is unavailable in the dataset."
        )
    else:
        analysis_df["YearsSinceLastPromotion"] = pd.to_numeric(
            analysis_df["YearsSinceLastPromotion"],
            errors="coerce"
        )

        analysis_df = analysis_df.dropna(
            subset=["YearsSinceLastPromotion"]
        )

        if analysis_df.empty:
            st.warning("No valid promotion-gap data is available.")
        else:
            # Chart 1: Distribution
            st.markdown("### 1. Promotion Gap Distribution")

            fig1 = px.histogram(
                analysis_df,
                x="YearsSinceLastPromotion",
                nbins=15,
                title="Years Since Last Promotion",
                labels={
                    "YearsSinceLastPromotion":
                    "Years Since Last Promotion"
                },
                color_discrete_sequence=["#2563EB"]
            )

            fig1.update_layout(
                xaxis_title="Years Since Last Promotion",
                yaxis_title="Number of Employees",
                showlegend=False
            )

            st.plotly_chart(fig1, use_container_width=True)

            # Chart 2: Department comparison
            if "Department" in analysis_df.columns:
                st.markdown(
                    "### 2. Average Promotion Gap by Department"
                )

                dept_gap = (
                    analysis_df.groupby("Department")
                    ["YearsSinceLastPromotion"]
                    .mean()
                    .reset_index(name="AveragePromotionGap")
                    .sort_values("AveragePromotionGap")
                )

                fig2 = px.bar(
                    dept_gap,
                    x="Department",
                    y="AveragePromotionGap",
                    title="Average Years Since Last Promotion",
                    labels={
                        "Department": "Department",
                        "AveragePromotionGap": "Average Years"
                    },
                    text_auto=".2f",
                    color="AveragePromotionGap",
                    color_continuous_scale="Blues"
                )

                st.plotly_chart(fig2, use_container_width=True)

            # Chart 3: Promotion gap categories
            st.markdown("### 3. Promotion Gap Categories")

            analysis_df["PromotionGapCategory"] = pd.cut(
                analysis_df["YearsSinceLastPromotion"],
                bins=[-float("inf"), 2, 5, float("inf")],
                labels=["0–2 Years", "3–5 Years", "6+ Years"]
            )

            category_counts = (
                analysis_df["PromotionGapCategory"]
                .value_counts(sort=False)
                .reindex(["0–2 Years", "3–5 Years", "6+ Years"])
                .fillna(0)
                .rename_axis("Promotion Gap Category")
                .reset_index(name="Employees")
            )

            fig3 = px.bar(
                category_counts,
                x="Promotion Gap Category",
                y="Employees",
                title="Employees by Promotion Gap Category",
                text="Employees",
                color="Promotion Gap Category"
            )

            st.plotly_chart(fig3, use_container_width=True)

            st.caption(
                "A longer promotion gap does not by itself prove "
                "career stagnation or promotion ineligibility. "
                "Interpret these patterns alongside role tenure, "
                "job level, performance, and promotion policies."
            )


# ---------------- ATTRITION ANALYSIS ----------------
elif page == "Attrition Analysis":
    st.subheader("Employee Attrition Analysis")

    analysis_df = filtered_df.copy()

    if "Attrition" not in analysis_df.columns:
        st.warning("The Attrition column is unavailable.")
    else:
        # Normalize attrition labels
        analysis_df["AttritionClean"] = (
            analysis_df["Attrition"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        # Use only recognized Yes/No values
        analysis_df = analysis_df[
            analysis_df["AttritionClean"].isin(["yes", "no"])
        ].copy()

        if analysis_df.empty:
            st.warning("No valid attrition records were found.")
        else:
            analysis_df["Left"] = (
                analysis_df["AttritionClean"] == "yes"
            ).astype(int)

            # KPI metrics
            total_valid = len(analysis_df)
            total_left = int(analysis_df["Left"].sum())
            attrition_rate = analysis_df["Left"].mean() * 100

            col1, col2, col3 = st.columns(3)

            col1.metric("Valid Employee Records", f"{total_valid:,}")
            col2.metric("Employees Who Left", f"{total_left:,}")
            col3.metric("Observed Attrition Rate", f"{attrition_rate:.2f}%")

            st.divider()

            # Chart 1: Overall attrition distribution
            st.markdown("### 1. Overall Attrition Distribution")

            attrition_counts = (
                analysis_df["AttritionClean"]
                .map({"yes": "Left", "no": "Stayed"})
                .value_counts()
                .rename_axis("Employee Status")
                .reset_index(name="Employees")
            )

            fig1 = px.pie(
                attrition_counts,
                names="Employee Status",
                values="Employees",
                title="Employees Who Left vs Stayed",
                hole=0.45
            )

            st.plotly_chart(fig1, use_container_width=True)

            # Chart 2: Attrition by department
            if "Department" in analysis_df.columns:
                st.markdown("### 2. Attrition Rate by Department")

                dept_attrition = (
                    analysis_df.groupby("Department")
                    .agg(
                        Employees=("Left", "size"),
                        Employees_Left=("Left", "sum"),
                        Attrition_Rate=("Left", "mean")
                    )
                    .reset_index()
                )

                dept_attrition["Attrition_Rate_Percent"] = (
                    dept_attrition["Attrition_Rate"] * 100
                ).round(2)

                fig2 = px.bar(
                    dept_attrition,
                    x="Department",
                    y="Attrition_Rate_Percent",
                    text="Attrition_Rate_Percent",
                    title="Observed Attrition Rate by Department",
                    labels={
                        "Attrition_Rate_Percent": "Attrition Rate (%)"
                    },
                    hover_data=["Employees", "Employees_Left"]
                )

                st.plotly_chart(fig2, use_container_width=True)

            # Chart 3: Attrition by promotion-gap category
            if "YearsSinceLastPromotion" in analysis_df.columns:
                st.markdown(
                    "### 3. Attrition Rate by Promotion Gap"
                )

                years = pd.to_numeric(
                    analysis_df["YearsSinceLastPromotion"],
                    errors="coerce"
                )

                analysis_df["PromotionGapCategory"] = pd.cut(
                    years,
                    bins=[-float("inf"), 2, 5, float("inf")],
                    labels=["0–2 Years", "3–5 Years", "6+ Years"]
                )

                gap_attrition = (
                    analysis_df.dropna(
                        subset=["PromotionGapCategory"]
                    )
                    .groupby(
                        "PromotionGapCategory",
                        observed=True
                    )
                    .agg(
                        Employees=("Left", "size"),
                        Employees_Left=("Left", "sum"),
                        Attrition_Rate=("Left", "mean")
                    )
                    .reset_index()
                )

                gap_attrition["Attrition_Rate_Percent"] = (
                    gap_attrition["Attrition_Rate"] * 100
                ).round(2)

                fig3 = px.bar(
                    gap_attrition,
                    x="PromotionGapCategory",
                    y="Attrition_Rate_Percent",
                    text="Attrition_Rate_Percent",
                    title="Observed Attrition Rate by Promotion Gap",
                    labels={
                        "PromotionGapCategory": "Promotion Gap",
                        "Attrition_Rate_Percent": "Attrition Rate (%)"
                    },
                    hover_data=["Employees", "Employees_Left"]
                )

                st.plotly_chart(fig3, use_container_width=True)

            st.caption(
                "These charts show associations in the dataset. "
                "They do not establish that promotion gaps cause attrition."
            )


# ---------------- CAREER CLUSTERS ----------------

elif page == "Career Clusters":
    st.subheader("Career Progression Segments")

    analysis_df = filtered_df.copy()

    required_cols = [
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion"
    ]

    if all(col in analysis_df.columns for col in required_cols):
        for col in required_cols:
            analysis_df[col] = pd.to_numeric(
                analysis_df[col], errors="coerce"
            )

        analysis_df["CareerCluster"] = pd.cut(
            analysis_df["YearsSinceLastPromotion"],
            bins=[-float("inf"), 2, 5, float("inf")],
            labels=[
                "Cluster 1: Recent Promotion",
                "Cluster 2: Moderate Promotion Gap",
                "Cluster 3: Long Promotion Gap"
            ]
        )

        st.info(
            "These are exploratory career-progression segments "
            "based on promotion gap, not the previously trained KMeans clusters."
        )

        cluster_counts = (
            analysis_df["CareerCluster"]
            .value_counts(sort=False)
            .rename_axis("Career Segment")
            .reset_index(name="Employees")
        )

        fig = px.bar(
            cluster_counts,
            x="Career Segment",
            y="Employees",
            title="Employees by Career Progression Segment",
            text="Employees"
        )
        st.plotly_chart(fig, use_container_width=True)

        profile = (
            analysis_df.groupby("CareerCluster", observed=False)
            .agg(
                Employees=("Age", "size"),
                Avg_Years_At_Company=("YearsAtCompany", "mean"),
                Avg_Years_In_Role=("YearsInCurrentRole", "mean"),
                Avg_Years_Since_Promotion=("YearsSinceLastPromotion", "mean")
            )
            .round(2)
            .reset_index()
        )

        st.markdown("### Career Segment Profile")
        st.dataframe(profile, use_container_width=True)
    else:
        st.warning("Required career progression columns are missing.")


# ---------------- RETENTION INSIGHTS ----------------

elif page == "Retention Insights":
    st.subheader("Employee Retention Insights")

    analysis_df = filtered_df.copy()

    if "Attrition" not in analysis_df.columns:
        st.warning("The Attrition column is missing.")
    else:
        # The source dataset uses 1 = Yes (left), 0 = No (stayed)
        analysis_df["Left"] = pd.to_numeric(
            analysis_df["Attrition"], errors="coerce"
        )
        analysis_df = analysis_df[
            analysis_df["Left"].isin([0, 1])
        ].copy()

        if analysis_df.empty:
            st.warning("No valid attrition records were found.")
        else:
            analysis_df["Left"] = analysis_df["Left"].astype(int)

            st.markdown("### 1. Retention Priority by Promotion Gap")

            if "YearsSinceLastPromotion" in analysis_df.columns:
                analysis_df["PromotionGapCategory"] = pd.cut(
                    pd.to_numeric(
                        analysis_df["YearsSinceLastPromotion"],
                        errors="coerce"
                    ),
                    bins=[-float("inf"), 2, 5, float("inf")],
                    labels=["0–2 Years", "3–5 Years", "6+ Years"]
                )

                retention = (
                    analysis_df.dropna(subset=["PromotionGapCategory"])
                    .groupby("PromotionGapCategory", observed=True)
                    .agg(
                        Employees=("Left", "size"),
                        Employees_Left=("Left", "sum"),
                        Attrition_Rate=("Left", "mean")
                    )
                    .reset_index()
                )

                retention["Attrition_Rate_Percent"] = (
                    retention["Attrition_Rate"] * 100
                ).round(2)

                fig = px.bar(
                    retention,
                    x="PromotionGapCategory",
                    y="Attrition_Rate_Percent",
                    text="Attrition_Rate_Percent",
                    title="Observed Attrition Rate by Promotion Gap",
                    labels={
                        "PromotionGapCategory": "Years Since Last Promotion",
                        "Attrition_Rate_Percent": "Attrition Rate (%)"
                    },
                    hover_data=["Employees", "Employees_Left"]
                )
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(
                    retention[
                        [
                            "PromotionGapCategory",
                            "Employees",
                            "Employees_Left",
                            "Attrition_Rate_Percent"
                        ]
                    ],
                    use_container_width=True
                )

            st.markdown("### 2. Department Retention Overview")

            if "Department" in analysis_df.columns:
                department = (
                    analysis_df.groupby("Department")
                    .agg(
                        Employees=("Left", "size"),
                        Employees_Left=("Left", "sum"),
                        Attrition_Rate=("Left", "mean")
                    )
                    .reset_index()
                )

                department["Attrition_Rate_Percent"] = (
                    department["Attrition_Rate"] * 100
                ).round(2)

                fig2 = px.bar(
                    department,
                    x="Department",
                    y="Attrition_Rate_Percent",
                    text="Attrition_Rate_Percent",
                    title="Observed Attrition Rate by Department",
                    labels={
                        "Attrition_Rate_Percent": "Attrition Rate (%)"
                    },
                    hover_data=["Employees", "Employees_Left"]
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 3. Recommended Actions")

            st.markdown("""
            - **Review promotion delays:** Examine employees with longer
              promotion gaps and assess their career-development needs.
            - **Strengthen career discussions:** Schedule regular
              manager–employee career conversations.
            - **Review department trends:** Investigate departments with
              comparatively higher observed attrition rates.
            - **Track outcomes:** Monitor promotion progress and retention
              indicators over time.
            """)

            st.caption(
                "These are exploratory associations, not proof that promotion "
                "delays cause attrition. Validate findings before taking "
                "employment decisions."
            )

st.divider()

st.caption(
    "Career Progression & Retention Analytics | "
    "Data Analytics Internship Project | Built with Python and Streamlit"
)