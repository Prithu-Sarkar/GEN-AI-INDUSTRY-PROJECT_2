from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from flipkart.data_converter import DataConverter
from flipkart.config import Config


class DataIngestor:
    """
    Embeds Flipkart product reviews into a local FAISS vector store.
    No external vector DB API required — runs fully on Colab.
    """

    def __init__(self):
        print("  🔄 Loading embedding model: BAAI/bge-base-en-v1.5 ...")
        self.embedding = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5"
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
        )
        self.vectorstore = None
        self.retriever   = None
        print("  ✅ Embedding model loaded")

    def ingest(self, csv_path: str = "data/flipkart_product_review.csv"):
        """
        Load CSV → convert to Documents → embed → build FAISS index.
        Run once; the index lives in memory for the session.
        """
        docs   = DataConverter(csv_path).convert()
        chunks = self.splitter.split_documents(docs)
        print(f"  ✂️  {len(docs)} rows → {len(chunks)} chunks")

        print(f"  🔍 Building FAISS index over {len(chunks)} chunks ...")
        self.vectorstore = FAISS.from_documents(chunks, self.embedding)
        self.retriever   = self.vectorstore.as_retriever(
            search_kwargs={"k": 4}
        )
        print("  ✅ FAISS index ready")
        return self.retriever
