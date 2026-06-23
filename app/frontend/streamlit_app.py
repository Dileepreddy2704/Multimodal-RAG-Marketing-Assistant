import os
import sys
import requests
import streamlit as st

from PIL import Image

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.feedback.feedback_manager import (
    FeedbackManager
)

from app.feedback.feedback_analyzer import (
    FeedbackAnalyzer
)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

CAPTION_API_URL = (
    f"{BACKEND_URL}/generate"
)

CONTENT_API_URL = (
    f"{BACKEND_URL}/generate-content"
)

UPLOAD_DIR = "data/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

feedback_manager = FeedbackManager()

feedback_analyzer = FeedbackAnalyzer()

st.set_page_config(
    page_title="Multimodal RAG Marketing Assistant",
    layout="wide"
)

st.title(
    "🖼️ Multimodal RAG Marketing Assistant"
)

# Session State

if "captions" not in st.session_state:
    st.session_state.captions = []

if "marketing_content" not in st.session_state:
    st.session_state.marketing_content = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "retrieved_docs" not in st.session_state:
    st.session_state.retrieved_docs = []

if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = ""

# Upload Image

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "jfif",
        "webp"
    ]
)

if uploaded_file is not None:

    file_ext = (
        uploaded_file.name
        .split(".")[-1]
        .lower()
    )

    if file_ext == "jfif":

        jpg_name = (
            os.path.splitext(
                uploaded_file.name
            )[0]
            + ".jpg"
        )

        save_path = os.path.join(
            UPLOAD_DIR,
            jpg_name
        )

        image = Image.open(
            uploaded_file
        )

        image.save(
            save_path,
            "JPEG"
        )

    else:

        save_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(
            save_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

    # Image Preview

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.image(
            save_path,
            caption="Uploaded Image",
            width=350
        )

    st.markdown("---")

    # Generate Captions

    if st.button(
        "Generate Captions"
    ):

        with st.spinner(
            "Generating captions..."
        ):

            response = requests.post(
                CAPTION_API_URL,
                json={
                    "image_path": save_path
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.captions = (
                    data["captions"]
                )

                st.session_state.prediction = (
                    data["prediction"]
                )

                st.session_state.retrieved_docs = (
                    data["retrieved_docs"]
                )

                st.session_state.marketing_content = ""

                st.success(
                    "Captions Generated"
                )

            else:

                st.error(
                    response.text
                )

    # AI Understanding Panel

    if st.session_state.prediction:

        st.subheader(
            "🧠 AI Understanding"
        )

        st.write(
            f"**Predicted Category:** "
            f"{st.session_state.prediction['label']}"
        )

        confidence = (
            st.session_state.prediction[
                "confidence"
            ] * 100
        )

        st.write(
            f"**Confidence:** "
            f"{confidence:.2f}%"
        )

        st.write(
            "**Retrieved Knowledge:**"
        )

        for doc in st.session_state.retrieved_docs:

            st.write(
                f"• {doc}"
            )

        st.markdown("---")

    # Show Captions

    if len(
        st.session_state.captions
    ) > 0:

        st.subheader(
            "Generated Captions"
        )

        st.session_state.selected_caption = st.radio(
            "Select a Caption",
            st.session_state.captions
        )

        st.markdown("---")

        # Marketing Content Section

        content_type = st.selectbox(
            "Content Type",
            [
                "Instagram Post",
                "Facebook Ad",
                "Product Description",
                "Email Marketing Copy",
                "LinkedIn Post"
            ]
        )

        if st.button(
            "Generate Marketing Content"
        ):

            with st.spinner(
                "Generating marketing content..."
            ):

                response = requests.post(
                    CONTENT_API_URL,
                    json={
                        "caption":
                            st.session_state.selected_caption,
                        "content_type":
                            content_type
                    }
                )

                if response.status_code == 200:

                    st.session_state.marketing_content = (
                        response.json()[
                            "content"
                        ]
                    )

                else:

                    st.error(
                        response.text
                    )

    # Marketing Content Display

    if st.session_state.marketing_content:

        st.markdown("---")

        st.subheader(
            "Generated Marketing Content"
        )

        st.text_area(
            "",
            st.session_state.marketing_content,
            height=250
        )

        st.markdown("---")

        st.subheader(
            "How useful was this generated content?"
        )

        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5,
            key="content_rating"
        )

        if st.button(
            "Save Feedback"
        ):

            feedback_manager.save_feedback(
                image_name=uploaded_file.name,
                caption=st.session_state.selected_caption,
                rating=rating
            )

            st.success(
                "Feedback Saved Successfully ✅"
            )

# Feedback Analytics

st.markdown("---")

st.subheader(
    "📊 Feedback Analytics"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average Rating",
        feedback_analyzer.get_average_rating()
    )

with col2:

    st.metric(
        "Total Feedback",
        feedback_analyzer.get_total_feedback()
    )

with col3:

    best = (
        feedback_analyzer.get_best_caption()
    )

    if best is not None:

        st.metric(
            "Top Rating",
            round(
                best["avg_rating"],
                2
            )
        )

best = (
    feedback_analyzer.get_best_caption()
)

if best is not None:

    st.success(
        f"🏆 Best Caption: "
        f"{best['caption']}"
    )

distribution = (
    feedback_analyzer
    .get_rating_distribution()
)

if len(distribution) > 0:

    st.subheader(
        "📈 Rating Distribution"
    )

    st.bar_chart(
        distribution
    )

top_captions = (
    feedback_analyzer
    .get_top_captions()
)

if len(top_captions) > 0:

    st.subheader(
        "🏅 Top Rated Captions"
    )

    st.dataframe(
        top_captions,
        use_container_width=True
    )