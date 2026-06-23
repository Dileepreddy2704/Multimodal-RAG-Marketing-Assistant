import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model_name = os.getenv(
            "MODEL_NAME",
            "llama3-70b-8192"
        )

    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content


if __name__ == "__main__":

    groq_client = GroqClient()

    response = groq_client.generate(
        "Write three short marketing slogans for premium sneakers."
    )

    print("\nResponse:\n")
    print(response)