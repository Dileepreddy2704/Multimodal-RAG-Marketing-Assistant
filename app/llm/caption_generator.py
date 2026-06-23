from app.rag.multimodal_retriever import MultiModalRetriever
from app.llm.groq_client import GroqClient


class MarketingCaptionGenerator:

    def __init__(self):

        self.retriever = MultiModalRetriever()

        self.llm = GroqClient()

    def generate_captions(
        self,
        image_path
    ):

        result = self.retriever.retrieve_from_image(
            image_path
        )

        prediction = result["prediction"]

        documents = result["documents"]

        context = "\n".join(
            [
                doc.page_content
                for doc in documents
            ]
        )

        prompt = f"""
You are a professional marketing copywriter.

Product Type:
{prediction['label']}

Retrieved Product Knowledge:
{context}

Generate 5 short marketing captions.

Requirements:
- Catchy
- Modern
- Suitable for advertisements
- Maximum 12 words each

Return ONLY the captions.
One caption per line.
No explanations.
"""

        response = self.llm.generate(
            prompt
        )

        captions = []

        for line in response.split("\n"):

            line = line.strip()

            if line:
                captions.append(line)

        return {
            "captions": captions,
            "prediction": prediction,
            "documents": documents
        }


if __name__ == "__main__":

    IMAGE_PATH = "data/sample_images/shoe.jpg"

    generator = MarketingCaptionGenerator()

    result = generator.generate_captions(
        IMAGE_PATH
    )

    print("\nPrediction:")
    print(result["prediction"])

    print("\nGenerated Captions:\n")

    for caption in result["captions"]:
        print(caption)