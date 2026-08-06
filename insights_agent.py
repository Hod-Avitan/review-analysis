import pandas as pd


def generate_insights(df):

    # Summary by theme
    theme_summary = (
        df
        .groupby(["theme", "severity"])
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False
        )
    )

    return theme_summary


def generate_release_insights(df):

    # Identify issues introduced or increased by release version
    release_summary = (
        df
        .groupby(["version", "theme"])
        .size()
        .reset_index(name="count")
        .sort_values(
            ["version", "count"],
            ascending=[True, False]
        )
    )

    return release_summary


def generate_app_insights(df):

    # Compare issues across apps
    app_summary = (
        df
        .groupby(["app", "theme"])
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False
        )
    )

    return app_summary


def get_human_attention_queue(df):

    # Reviews that require manual handling
    return df[
        df["requires_human_reply"] == True
    ].sort_values(
        "severity",
        ascending=False
    )
