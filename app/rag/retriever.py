from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


INDEX_PATH = "app/rag/faiss_index"


class MarketingRetriever:

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query, k=3):

        docs = self.vectorstore.similarity_search(
            query,
            k=k
        )

        return docs


if __name__ == "__main__":

    retriever = MarketingRetriever()

    results = retriever.retrieve(
        "lightweight running shoes"
    )

    print("\nRetrieved Documents:\n")

    for doc in results:

        print(doc.page_content)
        print("-" * 50)