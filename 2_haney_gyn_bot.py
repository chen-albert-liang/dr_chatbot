"""
Use chromaDB for now to store data from multiple sources
"""
# %%
from langchain.llms import OpenAI
from langchain.document_loaders import JSONLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

import streamlit as st
from streamlit_chat import message

from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
# from langchain.indexes import VectorstoreIndexCreator
# %% Load FAQ data
faq_loader = JSONLoader(
    file_path="./haney_knowledge_base/faqs.json",
    jq_schema=".content",
    text_content=False,
)
faq_json_data = faq_loader.load()

# Load Blog from Haney Gyn website
blog_json_loader = JSONLoader(
    file_path="./haney_knowledge_base/haneygyn_blog.json",
    jq_schema=".content",
    text_content=False,
)
blog_data = blog_json_loader.load()

# Load PDF of menopause glossary
glossary_pdf_loader = PyPDFLoader("./haney_knowledge_base/menopause_glossary.pdf")
glossary_data = glossary_pdf_loader.load()
# glossary_data1 = glossary_pdf_loader.load_and_split()

# %%
loaders = [faq_loader, blog_json_loader, glossary_pdf_loader]
docs = []
for loader in loaders:
    docs.extend(loader.load())

# %%
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

# %%
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# %% Create vector index
# index = VectorstoreIndexCreator().from_loaders([faq_loader])

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# %%
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    retriever=vectorstore.as_retriever(),
    condense_question_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
    return_source_documents=True
    # memory=memory,
)


# %%
def conversational_chat(query):
    result = qa_chain({"question": query, "chat_history": st.session_state["history"]})
    st.session_state["history"].append((query, result["answer"]))

    return result["answer"]


# %%
if "history" not in st.session_state:
    st.session_state["history"] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hello ! Ask HaneyGYN anything 🤗"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hey ! 👋"]

# container for the chat history
response_container = st.container()
# container for the user's text input
container = st.container()

# %%
with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_input(
            "Query:", placeholder="Talk about your female problems (:", key="input"
        )
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        output = conversational_chat(user_input)

        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

# %%
if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(
                st.session_state["past"][i],
                is_user=True,
                key=str(i) + "_user",
                avatar_style="big-smile",
            )
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
# %%
# chat_history = []
# query = "What is menopause?"
# result = qa({"question": query, "chat_history": chat_history})
# print(result["answer"])

# chat_history = [(query, result["answer"])]
# query = "Did it mention what symptoms menopause causes?"
# result = qa({"question": query, "chat_history": chat_history})

# print(result["answer"])

# result["source_documents"][0]
# %%
