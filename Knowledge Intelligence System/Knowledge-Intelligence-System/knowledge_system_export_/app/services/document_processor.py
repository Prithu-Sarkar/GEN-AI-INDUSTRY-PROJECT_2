"""Document processing service."""

from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class DocumentProcessor:

    SUPPORTED = {
        ".pdf",
        ".txt",
        ".md"
    }

    def __init__(self, config):

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    " ",
                    ""
                ]
            )
        )


    def _load(self, path: str):

        ext = Path(path).suffix.lower()

        if ext not in self.SUPPORTED:

            raise ValueError(
                f"Unsupported format: {ext}"
            )

        if ext == ".pdf":

            loader = PyPDFLoader(path)

        else:

            loader = TextLoader(
                path,
                encoding="utf-8"
            )

        return loader.load()


    def process(self, path: str):

        docs = self._load(path)

        return self.splitter.split_documents(
            docs
        )