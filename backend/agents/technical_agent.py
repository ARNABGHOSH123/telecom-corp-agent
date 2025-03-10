from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.openai import OpenAI
from langchain_community.tools import Tool
from config import settings
import faiss

def load_and_index_error_codes(docx_file):
    documents = SimpleDirectoryReader(input_files=[docx_file]).load_data()

    settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=settings.OPENAI_API_KEY)

    faiss_index = faiss.IndexFlatL2(1536)
    vector_store = FaissVectorStore(faiss_index)

    index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

    return index


docx_path = "data/Error Codes.docx"
index = load_and_index_error_codes(docx_path)

def query_error_code(query):
    retriever = index.as_retriever(similarity_top_k=2)
    results = retriever.retrieve(query)

    if not results:
        return "No relevant information found. Please refine your query."

    llm = OpenAI(model="gpt-4", temperature=0)
    response = llm.complete(
        f"You are a technical support AI. Based on the following information, provide a structured response:\n\n"
        f"{results[0].text}\n\n"
        f"User Query: {query}\n\n"
        f"Response:"
    )

    return response

techincal_agent = Tool(
    name="ErrorLookupTool",
    func=query_error_code,
    description="Use this tool to get detailed and structured information about an error code. "
    "It will provide an exact answer, including meaning, cause, and resolution, based strictly on "
    "the retrieved FAISS results. It follows clear rules to ensure responses remain specific and relevant.",
)