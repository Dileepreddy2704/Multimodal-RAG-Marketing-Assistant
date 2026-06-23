import torch

from PIL import Image

from transformers import CLIPProcessor
from transformers import CLIPModel


class ImageClassifier:

    def __init__(self):

        print("Loading CLIP classifier...")

        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.labels = [

            # Fashion
            "running shoes",
            "sneakers",
            "formal shoes",
            "boots",
            "athletic apparel",
            "sportswear",
            "hoodie",
            "jacket",
            "backpack",

            # Electronics
            "smartphone",
            "laptop",
            "tablet",
            "smart watch",
            "wireless earbuds",
            "bluetooth speaker",
            "gaming headset",
            "mechanical keyboard",
            "monitor",

            # Beauty
            "skin care product",
            "face serum",
            "moisturizer",
            "perfume",
            "cosmetics",
            "hair care product",

            # Home
            "furniture",
            "sofa",
            "office chair",
            "dining table",
            "home decor",
            "kitchen appliance",

            # Travel
            "luggage",
            "travel backpack",
            "carry-on luggage",
            "camping equipment",

            # Food
            "coffee product",
            "coffee beans",
            "energy drink",
            "protein shake",
            "tea product",

            # Automotive
            "electric vehicle",
            "luxury car",
            "sports car",
            "SUV",
            "motorcycle",

            # Sports
            "football",
            "football boots",
            "basketball",
            "basketball shoes",
            "cricket bat",
            "cricket equipment",
            "tennis racket",
            "tennis shoes",
            "running gear",
            "mountain bike",
            "swimming gear",
            "gym bag",

            # Fitness
            "gym equipment",
            "treadmill",
            "yoga mat",
            "fitness tracker",
            "dumbbells",
            "resistance bands",

            # Luxury
            "designer watch",
            "premium handbag",
            "diamond jewelry",
            "luxury perfume"
        ]

        print("Classifier ready")

    def classify(self, image_path):

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = self.processor(
            text=self.labels,
            images=image,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():

            outputs = self.model(
                **inputs
            )

        logits = outputs.logits_per_image

        probs = logits.softmax(
            dim=1
        )

        best_idx = probs.argmax().item()

        return {
            "label": self.labels[
                best_idx
            ],
            "confidence": float(
                probs[0][best_idx]
            )
        }


if __name__ == "__main__":

    IMAGE_PATH = (
        "data/sample_images/shoe.jpg"
    )

    classifier = ImageClassifier()

    result = classifier.classify(
        IMAGE_PATH
    )

    print("\nPrediction:")
    print(result)