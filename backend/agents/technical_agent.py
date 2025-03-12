from utils.rag_seed_error_code import faiss_indexes


def technical_agent(query):
    faiss_results = faiss_indexes.similarity_search_with_score(query, k=10)

    if not faiss_results or len(faiss_results) == 0:
        return "No relevant information found. Please refine your query."

    context = "\n\n".join(
        [f"Doc {i+1}: {doc.page_content}" for i, (doc, _) in enumerate(faiss_results)]
    )

    return context
