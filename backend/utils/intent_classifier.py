import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

def classify_intent(query):
    """Determine if a query is marketing-related or technical."""

    prompt = f"""Classify this query into one of the following categories:
    - "marketing" (for sales, promotions, or product inquiries)
    - "technical" (for error troubleshooting and diagnostics)
    - "other" (for any other enquiry)
    
    Query: {query}
    
    Respond with only the category name.
    """

    response = openai.chat.completions.create(
        model="gpt-4-turbo", messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()
