import os

if os.name != "nt":
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
from PIL import Image

# Load env
load_dotenv()

# Load users
if not os.path.exists("users.json"):

    with open("users.json", "w") as file:

        json.dump({}, file)

with open("users.json", "r") as file:

    users = json.load(file)



# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Load Logo Icon
icon = Image.open("assets/VR.png")

# Page config
st.set_page_config(
    page_title="Vidyarishi AI Chatbot",
    page_icon=icon,
    layout="wide"
)

# Session Defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Auto Login After Refresh
if st.query_params.get("login") == "true":

    st.session_state.logged_in = True

    st.session_state.user_email = st.query_params.get("user")



# Login Page
if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.2,1])

    with col2:

        st.title("Vidyarishi AI")

        st.write("Login or create your account")

        tab1, tab2 = st.tabs(["Login", "Create Account"])

        # LOGIN TAB
        with tab1:

            login_email = st.text_input(
                "Email",
                key="login_email"
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            login_btn = st.button(
                "Login",
                use_container_width=True
            )

            if login_btn:
                if login_email in users and users[login_email] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = login_email
                    st.query_params["login"] = "true"
                    st.query_params["user"] = login_email
                    st.success("Login Successful")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")

        # CREATE ACCOUNT TAB
        with tab2:

            new_email = st.text_input(
                "New Email",
                key="new_email"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )
            
            confirm_password = st.text_input(
    "Confirm Password",
    type="password",
    key="confirm_password"
)

            create_btn = st.button(
                "Create Account",
                use_container_width=True
            )

            if create_btn:

                if new_email in users:

                    st.error("Account already exists")

                else:

                    if new_password != confirm_password:

                        st.error("Passwords do not match")

                    else:

                        users[new_email] = new_password

                    with open("users.json", "w") as file:

                        json.dump(users, file)

                    st.success("Account Created Successfully")

    st.stop()

# Custom CSS
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

/* Main Container */
.main {
    color: white;
}

/* Chat Input Box */
.stChatInput input {
    background: linear-gradient(135deg, #1e293b, #0f172a) !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
    padding: 14px !important;
    font-size: 16px !important;
    box-shadow: 0 0 15px rgba(59,130,246,0.15);
    transition: 0.3s ease;
}

/* Input Hover */
.stChatInput input:hover {
    border: 1px solid #60a5fa !important;
}

/* Input Focus */
.stChatInput input:focus {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59,130,246,0.35) !important;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: rgba(30,41,59,0.65);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 14px;
    border: 1px solid #1e293b;
    backdrop-filter: blur(10px);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0f172a);
    border-right: 1px solid #1e293b;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Main Heading */
h1 {
    color: #38bdf8;
    font-size: 42px !important;
    font-weight: 700 !important;
}

/* Paragraph Text */
p {
    color: #cbd5e1;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
    transition: 0.3s ease;
}

/* Button Hover */
.stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 18px rgba(124,58,237,0.4);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #475569;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.image("assets/vr logo.png", width=250)

    st.title("India's No.1 EdTech Platform")

    st.write("AI Powered Chatbot")

    st.markdown("---")

    st.write("### Features")

    st.write("✅ Question Answering")
    st.write("✅ AI Chat")
    st.write("✅ Fast Responses")
    st.write("✅ Groq + LangChain")

    st.markdown("---")

    logout_btn = st.button(
    "Logout",
    use_container_width=True
)

if logout_btn:

    st.session_state.logged_in = False

    st.session_state.user_email = ""

    st.query_params.clear()

    st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="
        text-align:center;
        color:gray;
        font-size:13px;
        padding-top:10px;
    ">

    Developed by <br>
    <b style="color:white;">
    Shashank Sharma
    </b>

    </div>
    """, unsafe_allow_html=True)
        
        

# Main title
st.title(" Vidyarishi  Chatbot")

st.write("Ask questions about Vidyarishi India.")

@st.cache_resource
def load_rag():

    # Load text file
    loader = TextLoader("data/info.txt")

    documents = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = text_splitter.split_documents(documents)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    if os.path.exists("./chroma_db"):
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
    else:
        vectorstore = Chroma.from_documents(
            docs,
            embeddings,
            persist_directory="./chroma_db"
        )

    retriever = vectorstore.as_retriever()

    return retriever

retriever = load_rag()

# LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chats
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Ask something about Vidyarishi India...")

if query:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve docs
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are Vidyarishi India's official AI assistant.

Answer professionally and clearly.

Always answer questions related to:
- Vidyarishi India
- Online Degrees
- Admissions
- Placements
- Universities
- Career Guidance
- Student Support

Even if the user does not mention Vidyarishi India directly,
understand the question is about Vidyarishi India.

If context is missing,
still try to answer helpfully.

Context:
{context}

Question:
{query}
"""

    # AI response
    response = llm.invoke(prompt)

    bot_response = response.content

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_response)