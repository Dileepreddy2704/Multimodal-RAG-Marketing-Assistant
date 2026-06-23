from app.feedback.feedback_manager import (
    FeedbackManager
)

manager = FeedbackManager()

manager.save_feedback(
    image_name="shoe.jpg",
    caption="Step Up Your Style",
    rating=5
)

print(
    "Feedback Saved Successfully"
)