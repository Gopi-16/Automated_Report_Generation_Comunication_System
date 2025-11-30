import os
import re

# 🔄 Updated import: PDF Loader moved to langchain_community
from langchain_community.document_loaders import PyMuPDFLoader

# 🔄 Updated import: Text splitter moved to langchain_text_splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 🔄 Updated import: HuggingFace Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔄 Updated import: FAISS moved to community vectorstores
from langchain_community.vectorstores import FAISS

# 🔄 Updated import: Document model
from langchain_core.documents import Document


# Set paths
faiss_index_path = "index"
document_path = "/home/rguktrkvalley/streamlit/pages/data"

# Load embedding model
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model)


def create_index_file(reports):
    try:
        documents = []

        # -------------------------
        # CASE 1 — REPORTS (TEXT)
        # -------------------------
        if reports:
            print("📥 Adding new reports to index...")

            # Clean formatting junk
            refining = re.sub(r"[*#-]", "", reports)
            refining = refining.replace("\\n", "\n")

            # Convert to Document objects
            documents = [Document(page_content=refining)]

            if not documents:
                return "❗ No valid reports to index"

        # -------------------------
        # CASE 2 — LOAD PDF FILES
        # -------------------------
        else:
            print("📂 Loading PDF documents from data folder...")

            for root, _, files in os.walk(document_path):
                for file in files:
                    if file.endswith(".pdf"):
                        pdf_path = os.path.join(root, file)
                        loader = PyMuPDFLoader(pdf_path)
                        documents.extend(loader.load())

            if not documents:
                return "❗ No Documents Found"

        # -------------------------
        # SPLIT INTO CHUNKS
        # -------------------------
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        split_documents = text_splitter.split_documents(documents)

        # -------------------------
        # LOAD OR CREATE INDEX
        # -------------------------
        if reports:
            # If existing FAISS index exists → load and append
            if os.path.exists(f"{faiss_index_path}.faiss"):
                db = FAISS.load_local(
                    folder_path=faiss_index_path,
                    embeddings=embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                db = FAISS.from_documents([], embeddings)

            db.add_documents(split_documents)

        else:
            # Build a fresh FAISS index from pdfs
            db = FAISS.from_documents(split_documents, embeddings)

        # -------------------------
        # SAVE INDEX
        # -------------------------
        db.save_local(faiss_index_path)

        print("✅ Index updated and saved successfully.")
        return db

    except Exception as e:
        print("❌ Error in create_index_file:", e)
        return e

