from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.marketing_agent import marketing_agent
from agents.technical_agent import techincal_agent
from utils.intent_classifier import classify_intent

llm = ChatOpenAI(model="gpt-4", temperature=0)

multi_agent = initialize_agent(
    tools=[techincal_agent, marketing_agent],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def handle_query(query):
    """Classify and route the query to the appropriate agent."""
    intent = classify_intent(query)

    if intent == "marketing":
        return multi_agent.invoke({"input": query, "tool": "MarketingTool"})
    elif intent == "technical":
        return multi_agent.invoke({"input": query, "tool": "ErrorLookupTool"})
    else:
        return "Sorry, I couldn't classify your request."
