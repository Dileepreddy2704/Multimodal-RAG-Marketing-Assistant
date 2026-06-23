import torch

from PIL import Image

from transformers import CLIPProcessor
from transformers import CLIPVisionModel


class CLIPImageEncoder:

    def __init__(self):

        print("Loading CLIP Vision model...")

        self.model = CLIPVisionModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        print("CLIP Vision loaded successfully")

    def get_image_embedding(self, image_path):

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model(
                pixel_values=inputs["pixel_values"]
            )

        embedding = outputs.pooler_output.cpu().numpy()[0]

        return embedding


if __name__ == "__main__":

    IMAGE_PATH = "data/sample_images/shoe.jpg"

    encoder = CLIPImageEncoder()

    embedding = encoder.get_image_embedding(
        IMAGE_PATH
    )

    print("\nEmbedding Shape:")
    print(embedding.shape)

    print("\nFirst 10 Values:")
    print(embedding[:10])