from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from retriever import retrieve_top_k

# Initialize the Ollama LLM
llm = OllamaLLM(model="phi3", temperature=0.5)

# Define the prompt template
prompt = """
You are a knowledgeable and friendly Beauty Influencer who gives advice on makeup and skincare-related topics only. Using the provided context, answer the question: {query}.

If the context does not mention anything related to {query}, kindly state that you do not have enough information and suggest general beauty tips instead.

Context:
{context}
"""

prompt_template = PromptTemplate(
    input_variables=["context", "query"],  # Fixed input variables
    template=prompt
)

def generate_response(query):
    """Retrieve relevant content and generate a response."""
    # Retrieve top-k relevant documents
    retrieved_docs = retrieve_top_k(query)
    context = "\n".join(retrieved_docs)

    # Format the final prompt
    final_prompt = prompt_template.format(context=context, query=query)

    # Generate the response using the LLM
    response = llm.invoke(final_prompt)  # Use `invoke` instead of `predict`

    # Print and return the response
    print(response)
    return response

# Example usage
generate_response("how to apply foundation")