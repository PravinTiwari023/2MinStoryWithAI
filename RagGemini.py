import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_core.prompts import ChatPromptTemplate
import cassio
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# Get Google API key
google_api_key = os.getenv('GOOGLE_API_KEY')
# Get Cassandra/AstraDB credentials
astra_db_token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
astra_db_id = os.getenv('ASTRA_DB_ID')

# Initialize Cassandra/AstraDB connection
cassio.init(token=astra_db_token, database_id=astra_db_id)

# Load the PDF document
pdf_loader = PyPDFLoader('DeathMystery.pdf')
text_document = pdf_loader.load()

# Split the document into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
document_chunks = text_splitter.split_documents(text_document)

# Initialize the OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Set up the Cassandra vector store
astra_vector_store = Cassandra(
    embedding=embeddings,
    table_name="mystery_with_ai",
    session=None,
    keyspace=None
)

# Add document chunks to the Cassandra vector store
astra_vector_store.add_documents(document_chunks)

# Create a VectorStoreIndexWrapper for the Cassandra vector store
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

# Configure Google Generative AI with the API key
genai.configure(api_key=google_api_key)

# Initialize the ChatGoogleGenerativeAI with the specified model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are playing an important character in this act named Mr. Detective. You have all the information about the mystery but you cannot directly reveal who the culprit is. You need to help others if someone asks about anything but don't directly tell who the culprit is. Mr. Detective always talks neutrally so that it becomes difficult to guess who the culprit is.

<context>
{context}
</context>
Question: {input}
""")

# Set up the retriever for the vector store
retriever = astra_vector_store.as_retriever()

# Create a document chain to process the documents with the LLM and the prompt template
document_chain = create_stuff_documents_chain(llm, prompt_template)

# Create a retrieval chain that integrates the retriever and the document chain
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Function to generate content based on a query
def generate_content(query):
    return retrieval_chain.invoke({"input": query})['answer']

# Test the function
print(generate_content("tell me everything about Mark"))