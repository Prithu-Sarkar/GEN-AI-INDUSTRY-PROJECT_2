# src/helper.py
# Compatible with LangChain >= 0.2

from typing import List

# LangChain >= 0.2: document loaders in langchain-community
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

# Core text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# LangChain >= 0.2: HuggingFace embeddings in dedicated sub-package
from langchain_huggingface import HuggingFaceEmbeddings

# Schema
from langchain_core.documents import Document


def load_pdf_file(data: str) -> List[Document]:
    """Load all PDF files from the given directory path."""
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    return loader.load()


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """Strip all metadata except source to avoid ChromaDB serialisation issues."""
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source", "unknown")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src},
            )
        )
    return minimal_docs


def text_split(extracted_data: List[Document]) -> List[Document]:
    """Split documents into 500-char chunks with 20-char overlap."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    return text_splitter.split_documents(extracted_data)


def download_hugging_face_embeddings() -> HuggingFaceEmbeddings:
    """Load sentence-transformers/all-MiniLM-L6-v2 (384 dims, free, no API key)."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )