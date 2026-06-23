from fastapi import FastAPI
from pydantic import BaseModel

from app.llm.caption_generator import (
    MarketingCaptionGenerator
)

from app.llm.marketing_content_generator import (
    MarketingContentGenerator
)


app = FastAPI(
    title="Multimodal RAG Caption API"
)

caption_generator = MarketingCaptionGenerator()

content_generator = MarketingContentGenerator()


class CaptionRequest(BaseModel):

    image_path: str


class MarketingContentRequest(BaseModel):

    caption: str

    content_type: str


@app.get("/")
def root():

    return {
        "message": "API Running"
    }


@app.post("/generate")
def generate_caption(
    request: CaptionRequest
):

    result = caption_generator.generate_captions(
        request.image_path
    )

    return {
        "captions": result["captions"],
        "prediction": result["prediction"],
        "retrieved_docs": [
            doc.metadata.get(
                "title",
                "Unknown"
            )
            for doc in result["documents"]
        ]
    }


@app.post("/generate-content")
def generate_content(
    request: MarketingContentRequest
):

    content = content_generator.generate_content(
        caption=request.caption,
        content_type=request.content_type
    )

    return {
        "content": content
    }