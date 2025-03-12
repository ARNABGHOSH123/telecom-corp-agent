from agents.marketing_agent import marketing_agent
from agents.technical_agent import technical_agent
from utils.intent_classifier import classify_intent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langchain_openai.chat_models import ChatOpenAI

checkpointer = MemorySaver()

llm = ChatOpenAI(model="gpt-4", temperature=0)

workflow = StateGraph(dict)


def coordinator_agent(state):
    query = state["query"]
    intent = classify_intent(query)
    return {"query": query, "intent": intent}


def agent_selector(state):
    intent = state["intent"]
    query = state["query"]
    if intent == "marketing":
        return {"query": query, "output": marketing_agent(query), "intent": intent}
    elif intent == "technical":
        return {"query": query, "output": technical_agent(query), "intent": intent}
    else:
        return {"output": fallback(), "intent": intent}


def fallback():
    return "Sorry, I couldn't classify your request."


def nlp_answer_generator(state):
    output = state["output"]
    intent = state["intent"]

    if "query" not in state:
        return {"final_response": output}

    query = state["query"]

    if intent == "technical":
        prompt = f"""
        You are a technical support AI. Based on the following information, choose the best possible content based on the multiple options given.
        Given the following query:\n "{query}", \nchoose the most relevant error code explanation from the documents below.

        {output}

        Choose the most relevant document and prepare a very easy-to-read human readable response after understanding user's query deeply.
        - Dont include the user query text in the final response.
        - Dont mention any document numbers.

        Response:
        """
    else:
        prompt = f"""
        You are a technical support AI and a marketing expert. Based on the following information, provide a structured and most relevant response.
        Format your response in a structured and easy-to-read way for the user.

        User query: {query}\n
        Output: {output}\n
        Response:
        """

    final_response = llm.invoke(prompt)

    return {"final_response": final_response.content}


workflow.add_node("coordinator", coordinator_agent)
workflow.add_node("agent_selector", agent_selector)
workflow.add_node("nlp_answer_generator", nlp_answer_generator)

workflow.set_entry_point("coordinator")
workflow.add_edge("coordinator", "agent_selector")
workflow.add_edge("agent_selector", "nlp_answer_generator")
workflow.add_edge("nlp_answer_generator", END)

app = workflow.compile(checkpointer=checkpointer)


def handle_query(query: str):
    try:
        result = app.invoke({"query": query}, config={"configurable": {"thread_id": 1}})
        user_response = result["final_response"]
    except Exception as e:
        print(f"Error: {str(e)}")
        if "context_length_exceeded" in str(e):
            user_response = "User query / answer is very large. Please ask for more specific and short queries."
        else:
            user_response = fallback()

    return user_response
