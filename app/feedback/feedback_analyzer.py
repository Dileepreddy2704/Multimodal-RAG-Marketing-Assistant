import pandas as pd


FEEDBACK_FILE = (
    "data/feedback/feedback.csv"
)


class FeedbackAnalyzer:

    def get_feedback_data(self):

        try:

            return pd.read_csv(
                FEEDBACK_FILE
            )

        except:

            return pd.DataFrame()

    def get_average_rating(self):

        df = self.get_feedback_data()

        if len(df) == 0:

            return 0

        return round(
            df["rating"].mean(),
            2
        )

    def get_top_captions(self):

        df = self.get_feedback_data()

        if len(df) == 0:

            return pd.DataFrame()

        result = (
            df.groupby("caption")
            ["rating"]
            .agg(
                ["mean", "count"]
            )
            .reset_index()
        )

        result.columns = [
            "caption",
            "avg_rating",
            "num_ratings"
        ]

        result = result.sort_values(
            by="avg_rating",
            ascending=False
        )

        return result

    def get_total_feedback(self):

        df = self.get_feedback_data()

        return len(df)

    def get_best_caption(self):

        top = self.get_top_captions()

        if len(top) == 0:

            return None

        return top.iloc[0]

    def get_rating_distribution(self):

        df = self.get_feedback_data()

        if len(df) == 0:

            return {}

        return (
            df["rating"]
            .value_counts()
            .sort_index()
            .to_dict()
        )