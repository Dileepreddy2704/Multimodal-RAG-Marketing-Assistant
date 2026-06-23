from app.vision.image_classifier import ImageClassifier
from app.rag.retriever import MarketingRetriever


class MultiModalRetriever:

    def __init__(self):

        self.classifier = ImageClassifier()

        self.retriever = MarketingRetriever()

    def retrieve_from_image(
        self,
        image_path,
        k=3
    ):

        prediction = self.classifier.classify(
            image_path
        )

        query = prediction["label"]

        docs = self.retriever.retrieve(
            query,
            k=k
        )

        return {
            "prediction": prediction,
            "documents": docs
        }


if __name__ == "__main__":

    IMAGE_PATH = "data/sample_images/shoe.jpg"

    retriever = MultiModalRetriever()

    result = retriever.retrieve_from_image(
        IMAGE_PATH
    )

    print("\nImage Understanding:")
    print(result["prediction"])

    print("\nRetrieved Context:\n")

    for doc in result["documents"]:

        print(doc.page_content)
        print("-" * 50)