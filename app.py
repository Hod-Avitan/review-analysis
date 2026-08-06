import streamlit as st
import pandas as pd

from review_agent import analyze_review
from insights_agent import (
    generate_insights,
    generate_release_insights,
    generate_app_insights,
    get_human_attention_queue
)
from reply_agent import generate_reply


st.title("Review Intelligence Agent")


uploaded_file = st.file_uploader(
    "Upload reviews file",
    type=["xlsx"]
)


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
        st.error(
            f"Missing columns: {missing_columns}"
        )
        st.stop()


    st.subheader("Uploaded Reviews")
    st.dataframe(df)

    st.success(
        f"Loaded {len(df)} reviews"
    )


    if st.button("Analyze Reviews"):

        results = []

        with st.spinner("Analyzing reviews..."):

            for _, row in df.iterrows():

                analysis = analyze_review(
                    row["review_text"],
                    row["rating"],
                    row["version"]
                )

                results.append(analysis)


        analysis_df = pd.DataFrame(results)


        final_df = pd.concat(
            [
                df.reset_index(drop=True),
                analysis_df.reset_index(drop=True)
            ],
            axis=1
        )
        st.subheader("Issue Trends Over Time")

        trend_df = (
            final_df
            .groupby(
                [
                    "date",
                    "theme"
                ]
            )
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

        st.subheader("Issues Trend by Release")
        release_trend = (
            final_df
            .groupby(
                [
                    "version",
                    "theme"
                ]
            )
            .size()
            .reset_index(name="count")
        )
        st.dataframe(
            release_trend
        )


        # --------------------------
        # Review Level
        # --------------------------

        st.subheader("Review Level Analysis")

        st.dataframe(
            final_df
        )


        # --------------------------
        # Product Level Insights
        # --------------------------

        st.subheader("Product Level Insights")

        insights = generate_insights(
            final_df
        )

        st.dataframe(
            insights
        )


        # --------------------------
        # Issues by App
        # --------------------------

        st.subheader("Issues by App")

        app_insights = generate_app_insights(
            final_df
        )

        st.dataframe(
            app_insights
        )


        # --------------------------
        # Release Impact
        # --------------------------

        st.subheader(
            "Issues by Release Version"
        )

        release_insights = generate_release_insights(
            final_df
        )

        st.dataframe(
            release_insights
        )


        # --------------------------
        # Charts
        # --------------------------

        st.subheader(
            "Issues by Theme"
        )

        theme_chart = (
            final_df["theme"]
            .value_counts()
        )

        st.bar_chart(
            theme_chart
        )


        st.subheader(
            "Severity Distribution"
        )

        severity_chart = (
            final_df["severity"]
            .value_counts()
        )

        st.bar_chart(
            severity_chart
        )


        # --------------------------
        # Human in the Loop
        # --------------------------

        st.subheader(
            "Reviews Requiring Human Attention"
        )

        human_reviews = get_human_attention_queue(
            final_df
        )

        st.dataframe(
            human_reviews
        )


        # --------------------------
        # Auto Replies
        # --------------------------

        st.subheader(
            "Automatic Reply Suggestions"
        )

        auto_reply_df = final_df[
            final_df["requires_human_reply"] == False
        ].head(5)


        for _, row in auto_reply_df.iterrows():

            st.write(
                "Original Review:"
            )

            st.write(
                row["review_text"]
            )


            st.write(
                "Suggested Reply:"
            )

            st.info(
                generate_reply(
                    row["review_text"]
                )
            )
