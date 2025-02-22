from huggingface_hub import InferenceClient
from retriever import retrieve_top_k  # Ensure this function is defined elsewhere

# Initialize the Together API client
client = InferenceClient(
    provider="together",
    api_key=""
)

# Define the system prompt template
system_prompt = """
You are a knowledgeable and friendly Beauty Influencer who gives advice on makeup and skincare-related topics only. Using the provided context, answer the question: {query}.

If the context does not mention anything related to the query, kindly state that you do not have enough information.

Context:
{context}
"""

def generate_response(query):
    """Retrieve relevant content and generate a response."""
    # Retrieve top-k relevant documents
    retrieved_docs = retrieve_top_k(query)
    context = "\n".join(retrieved_docs)

    # Format the system prompt with context and query
    formatted_system_prompt = system_prompt.format(context=context, query=query)

    # Prepare the messages for the Together API
    messages = [
        {"role": "system", "content": formatted_system_prompt},
        {"role": "user", "content": query}
    ]

    # Generate the response using the Together API
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",  # Replace with your desired model
        messages=messages,
        max_tokens=500,  # Adjust as needed
    )

    # Extract and print the response
    response = completion.choices[0].message.content
    print(response)
    return response

# Example usage
generate_response("tell me about formula 1 car race")