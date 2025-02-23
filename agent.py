from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import Graph
from typing import List, Any, Dict
import json
from huggingface_hub import InferenceClient
from retriever import retrieve_top_k
from scraper import get_products_from_web
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Together API client
client = InferenceClient(
    provider="together",
    api_key=os.getenv("TOGETHER_ACCESS_TOKEN")
)


# Define the tools
@tool
def retrieve_from_knowledge_base(query: str) -> str:
    """Retrieve information from the knowledge base using RAG."""
    results = retrieve_top_k(query)
    return "\n".join(results) if results else "No relevant information found in the knowledge base."


@tool
def get_beauty_product_recommendations(query: str) -> str:
    """Get beauty product recommendations by scraping the web."""
    return get_products_from_web(query)


tools = [retrieve_from_knowledge_base, get_beauty_product_recommendations]


# Define the LLM using Together API
class TogetherLLM(Runnable):
    def __init__(self, client):
        self.client = client

    def invoke(self, input: Dict[str, Any], **kwargs: Any) -> str:
        messages = [
            {"role": "user", "content": input["input"]}
        ]
        completion = self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # Replace with your desired model
            messages=messages
        )
        return completion.choices[0].message.content


# Initialize the Together LLM
together_llm = TogetherLLM(client)

# Define beauty/makeup-related keywords
BEAUTY_KEYWORDS = [
    "makeup", "beauty", "skincare", "foundation", "lipstick", "eyeliner",
    "mascara", "blush", "concealer", "moisturizer", "serum", "cleanser",
    "toner", "make-up", "cosmetics", "beauty products"
]

# Define product recommendation keywords
RECOMMENDATION_KEYWORDS = [
    "recommend", "suggest", "best", "top", "good", "product", "buy", "purchase"
]


# Define the agent logic
def agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # Get the user input
    user_input = state.get("input", "").lower()

    # Initialize the result variable
    result = ""

    # Check if the query is related to product recommendations
    if any(keyword in user_input for keyword in RECOMMENDATION_KEYWORDS):
        # Use the product recommendation tool
        tool_output = get_beauty_product_recommendations(user_input)
        # Pass the tool output to the LLM for refinement
        result = together_llm.invoke({
            "input": f"The user asked: '{user_input}'. Here are the product recommendations: {tool_output}. Generate "
                     f"a concise and helpful response in 100 words.Do NOT include any reasoning, thoughts, "
                     f"or step-by-step analysis—only return the final response."
        })
    # Check if the query is related to beauty or makeup
    else:
        # Use the knowledge base tool
        tool_output = retrieve_from_knowledge_base(user_input)
        # Pass the tool output to the LLM for refinement
        result = together_llm.invoke({
            "input": f"The user asked: '{user_input}'. Below is the relevant information from the knowledge base:\n\n"
                     f"{tool_output}\n\n"
                     f"Based on this information, provide a direct, concise, and helpful response within 100 words. "
                     f"Do NOT include any reasoning, thoughts, or step-by-step analysis—only return the final response."
                     f"If the knowledge base lacks relevant information, clearly state that you do not have the "
                     f"necessary details and do not attempt to answer the query."
        })

    # else:
    #     # If the query is out of context, pass it to the LLM for a polite response
    #     result = together_llm.invoke({
    #         "input": f"The user asked: '{user_input}'. This query is out of my context. I can only assist with beauty and makeup-related queries or product recommendations. Generate a polite and concise response in under 200 tokens."
    #     })

    # Update the state with the result
    state["output"] = result
    return state


# Define the graph
workflow = Graph()

# Add nodes to the graph
workflow.add_node("agent", RunnableLambda(agent))

# Set the entry point
workflow.set_entry_point("agent")

# Set the exit point
workflow.set_finish_point("agent")

# Compile the graph
app = workflow.compile()

# Run the agent
# query = "How to cook rice"
# response = app.invoke({"input": query})
# print(response["output"])