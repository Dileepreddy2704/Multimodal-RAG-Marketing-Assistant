from app.llm.groq_client import GroqClient


class MarketingContentGenerator:

    def __init__(self):

        self.llm = GroqClient()

    def generate_content(
        self,
        caption,
        content_type,
        context=""
    ):

        prompt = f"""
You are a professional marketing copywriter.

Selected Caption:
{caption}

Product Context:
{context}

Content Type:
{content_type}

Write engaging marketing content based on the selected caption.

Requirements:
- Professional
- Persuasive
- Marketing focused
- Match the requested content type
- 80 to 150 words

Return only the content.
"""

        response = self.llm.generate(
            prompt
        )

        return response


if __name__ == "__main__":

    generator = MarketingContentGenerator()

    result = generator.generate_content(
        caption="Elevate Your Sneaker Game",
        content_type="Instagram Post",
        context="""
Premium sneakers designed for comfort,
urban style, and everyday performance.
"""
    )

    print("\nGenerated Content:\n")

    print(result)