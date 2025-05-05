import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import re

# Set paths
faiss_index_path = "index"
document_path = "/home/rguktrkvalley/streamlit/pages/data"

# Load embedding model
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)

def create_index_file(reports):
    try:
        documents = []

        # Case 1: If reports (text strings) are provided
        if reports:
            print("📥 Adding new reports to index...")

            # Filter invalid or empty report entries
            refining=re.sub(r"[*#-]", "", reports)
            refining=refining.replace("\\n","\n")
            #valid_reports = [text for text in refining if isinstance(text, str) and text.strip()]
            
           

            # Convert to Document objects
            documents = [Document(page_content=text) for text in refining]

            if not documents:
                return "❗ No valid reports to index"

        # Case 2: No reports, scan PDFs in the data folder
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

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_documents = text_splitter.split_documents(documents)

        # Load or create FAISS index
        if reports:
            if os.path.exists(f"{faiss_index_path}.faiss"):
                db = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
            else:
                db = FAISS.from_documents([], embeddings)
            db.add_documents(split_documents)
        else:
            db = FAISS.from_documents(split_documents, embeddings)

        # Save the FAISS index
        db.save_local(faiss_index_path)
        print("✅ Index updated and saved successfully.")
        return db

    except Exception as e:
        print("❌ Error in create_index_file:", e)
        return e
#create_index_file(None)

