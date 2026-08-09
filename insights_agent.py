import pandas as pd

def generate_insights(df):

    # Summary by theme
    theme_summary = (
        df
        .groupby(["app", "theme", "severity"])
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

def generate_feature_requests(df):

    feature_requests = (
        df[df["category"] == "Feature Request"]
        .groupby("theme")
        .agg(
            request_count=("theme", "size"),
            apps=("app", "nunique")
        )
        .reset_index()
        .sort_values(
            "request_count",
            ascending=False
        )
    )

    app_lists = (
        df[df["category"] == "Feature Request"]
        .groupby("theme")["app"]
        .apply(lambda x: ", ".join(sorted(x.dropna().unique())))
        .reset_index(name="apps_list")
    )

    feature_requests = feature_requests.merge(
        app_lists,
        on="theme",
        how="left"
    )

    return feature_requests[
        ["theme", "request_count", "apps", "apps_list"]
    ]

def get_human_attention_queue(df):

    # Reviews that require manual handling
    return df[
        df["requires_human_reply"] == True
    ].sort_values(
        "severity",
        ascending=False
    )
