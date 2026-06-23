import os
import pandas as pd
from datetime import datetime


FEEDBACK_FILE = "data/feedback/feedback.csv"


class FeedbackManager:

    def save_feedback(
        self,
        image_name,
        caption,
        rating
    ):

        row = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "image_name": image_name,
            "caption": caption,
            "rating": rating
        }

        df = pd.DataFrame([row])

        if os.path.exists(FEEDBACK_FILE):

            df.to_csv(
                FEEDBACK_FILE,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                FEEDBACK_FILE,
                index=False
            )

        return True