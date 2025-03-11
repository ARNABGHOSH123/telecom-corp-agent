from utils.rag_seed_error_code import faiss_indexes
from config import settings
from langchain_openai import OpenAI

llm = OpenAI(api_key=settings.OPENAI_API_KEY)


def technical_agent(query):
    faiss_results = faiss_indexes.similarity_search_with_score(query, k=10)

    if not faiss_results or len(faiss_results) == 0:
        return "No relevant information found. Please refine your query."

    context = "\n\n".join(
        [f"Doc {i+1}: {doc.page_content}" for i, (doc, _) in enumerate(faiss_results)]
    )

    prompt = f"""
    You are an AI expert in choosing best possible content based on the multiple options given.
    Given the following query:\n "{query}", \nchoose the most relevant error code explanation from the documents below.

    {context}

    Choose the most relevant document and prepare a very easy-to-read human readable response after understanding user's query deeply.
    - Dont include the user query text in the final response.
    - Dont mention any document numbers.
    """

    response = llm.invoke(prompt)

    return response
