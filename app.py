from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# Load documents
loader = TextLoader("data/info.txt")
documents = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector database
vectorstore = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever()

# Groq model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


print("\nRAG Chatbot Ready!")
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    # Retrieve relevant docs
    docs = retriever.get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in docs])

    # Create prompt
    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""

    # Get response
    response = llm.invoke(prompt)

    print("\nBot:", response.content)
    print()