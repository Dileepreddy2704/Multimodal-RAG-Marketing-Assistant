import os
import pandas as pd

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from sentence_transformers import SentenceTransformer


DATA_PATH = "app/rag/knowledge_base.csv"
INDEX_PATH = "app/rag/faiss_index"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class SentenceTransformerEmbeddings:

    def __init__(self):
        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True
        ).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()


def load_knowledge_base():

    df = pd.read_csv(DATA_PATH)

    documents = []

    for _, row in df.iterrows():

        text = f"""
Category: {row['category']}
Title: {row['title']}
Content: {row['content']}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "category": row["category"],
                    "title": row["title"]
                }
            )
        )

    return documents


def build_faiss_index():

    print("Loading knowledge base...")

    documents = load_knowledge_base()

    print(f"Loaded {len(documents)} documents")

    embeddings = SentenceTransformerEmbeddings()

    print("Creating FAISS index...")

    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )

    os.makedirs(
        INDEX_PATH,
        exist_ok=True
    )

    vectorstore.save_local(
        INDEX_PATH
    )

    print("Index created successfully")


if __name__ == "__main__":
    build_faiss_index()