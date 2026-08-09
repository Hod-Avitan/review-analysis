import streamlit as st
import pandas as pd
import plotly.express as px

from review_agent import analyze_review
from insights_agent import (
    generate_insights,
    generate_release_insights,
    generate_app_insights,
    get_human_attention_queue,
    generate_feature_requests
)
from reply_agent import generate_reply
@st.cache_data(show_spinner=False)
def analyze_reviews(df):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_reviews = len(df)
    for i, (_, row) in enumerate(df.iterrows()):
        analysis = analyze_review(
            row["review_text"],
            row["rating"],
            row["version"]
        )
        results.append(analysis)
        progress = (i + 1) / total_reviews
        progress_bar.progress(progress)
        status_text.text(
            f"Analyzing reviews: {i + 1}/{total_reviews}"
        )
    progress_bar.empty()
    status_text.empty()

    return pd.DataFrame(results)

st.title("Review Intelligence Agent")
uploaded_file = st.file_uploader("Upload reviews file",type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    required_columns = [
        "app",
        "version",
        "rating",
        "review_text"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.stop()

    st.subheader("Dataset Overview")
    st.caption("Overview of the uploaded review dataset before analysis.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total Reviews",
            len(df)
        )
    with col2:
        st.metric(
            "Applications",
            df["app"].nunique()
        )
    with col3:
        st.metric(
            "Languages",
            df["language"].nunique()
        )
    with st.expander("Review Dataset Preview"):
        st.dataframe(df.head(10))
        st.success(f"Loaded {len(df)} reviews")

    if st.button("Analyze Reviews"):
        with st.spinner("Analyzing reviews..."):
            analysis_df = analyze_reviews(df)

        final_df = pd.concat([df.reset_index(drop=True),analysis_df.reset_index(drop=True)], axis=1)
        st.session_state["final_df"] = final_df
        st.success("Analysis completed successfully")
  
    if "final_df" in st.session_state:
        final_df = st.session_state["final_df"]
       
        # --------------------------
        # Issue Distribution by App
        # --------------------------        
        st.subheader("Issue Distribution by App")
        app_theme_data = (
            final_df
            .groupby(["app", "theme"])
            .size()
            .reset_index(name="count")
        )
        heatmap_data = (
            app_theme_data.pivot(
                index="app",
                columns="theme",
                values="count"
            ).fillna(0))
        fig = px.imshow(
            heatmap_data,
            labels={
                "x": "Issue Type",
                "y": "Application",
                "color": "Number of Reviews"
            },aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

        # --------------------------
        # Product Level Insights - Top Issues Across the Portfolio
        # --------------------------
        st.subheader("Top Issues Across the Portfolio")
        st.caption("Highlights the most common issues across apps to help prioritize product and engineering attention.")
        insights = generate_insights(final_df)
        st.dataframe( insights)

        # --------------------------
        # Issue Trends Over Time
        # --------------------------
        st.subheader("Issue Trends Over Time")
        st.caption("Select an app to identify recurring issues and understand how user problems change over time.")
        apps = sorted(final_df["app"].dropna().unique())
        selected_app = st.selectbox("Select an app",apps)
        app_trend_df = final_df[final_df["app"] == selected_app]
        trend_df = (
            app_trend_df
            .groupby(["date", "theme"])
            .size()
            .reset_index(name="count")
        )
        trend_pivot = (
            trend_df
            .pivot(
                index="date",
                columns="theme",
                values="count"
            )
            .fillna(0)
        )
        st.line_chart(trend_pivot)

        # --------------------------
        # Issues Trend by Release
        # --------------------------        
        st.subheader("Issues Trend by Release")
        st.caption("Analyze whether specific issues increased after a release version was introduced.")
        release_trend = (
            final_df
            .groupby(["app", "version", "theme"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False))
        st.dataframe( release_trend)



        # --------------------------
        # Suggested Feature Requests
        # --------------------------
        st.subheader("Suggested Feature Requests")
        st.caption("Aggregates user requests from reviews and shows which apps are affected.")
        feature_requests = generate_feature_requests( final_df)
        st.dataframe(feature_requests)

        # --------------------------
        # Review Level
        # --------------------------
        with st.expander("Review Level Analysis (Drill Down)"):
            st.dataframe(final_df)

        # --------------------------
        # Human in the Loop
        # --------------------------
        st.subheader( "Reviews Requiring Human Attention" )
        st.caption("Reviews identified as requiring personal attention based on sentiment, severity, or sensitivity.")
        human_reviews = get_human_attention_queue( final_df )
        st.dataframe( human_reviews)

        # --------------------------
        # Auto Replies
        # --------------------------
        st.subheader("Automatic Reply Suggestions")
        st.caption("Suggested responses for lower-risk reviews while keeping sensitive cases under human review.")
        auto_reply_df = final_df[ final_df["requires_human_reply"] == False].head(5)

        for _, row in auto_reply_df.iterrows():
            st.write("Original Review:")
            st.write(row["review_text"])
            st.write("Suggested Reply:")
            st.info(generate_reply(row["review_text"]))
        


        # --------------------------
        # Issues by App
        # --------------------------
        #st.subheader("Issues by App")
        #app_insights = generate_app_insights(final_df)
        #st.dataframe( app_insights)
        # --------------------------
        # Release Impact
        # --------------------------
        #st.subheader( "Issues by Release Version")
        #release_insights = generate_release_insights(final_df)
        #st.dataframe(release_insights)
        # --------------------------
        # Charts
        # --------------------------
        #st.subheader("Issues by Theme")
        #theme_chart = (final_df["theme"].value_counts() )
        #st.bar_chart( theme_chart )
        #st.subheader( "Severity Distribution")
        #severity_chart = ( final_df["severity"].value_counts())
        #st.bar_chart(severity_chart)

