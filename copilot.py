
import os
import chromadb
import google.generativeai as genai

# --- Configuration ---
CHROMA_PATH = "n8n_chroma_db"
COLLECTION_NAME = "n8n_docs"
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-1.5-flash"
API_KEY_ENV_VAR = "GOOGLE_API_KEY"

# --- Helper Functions ---
def get_google_api_key():
    """Gets the Google API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set. Please set it to your Google API key.")
    return api_key

def format_context(results):
    """Formats the retrieved documents into a string for the prompt."""
    context = "\n--- Retrieved Documentation Context ---"
    for i, doc in enumerate(results['documents'][0]):
        source = results['metadatas'][0][i]['source']
        heading = results['metadatas'][0][i]['heading']
        context += f"\n\nSource {i+1}: {source} (Section: {heading})\n"
        context += f"Content: {doc}\n"
    context += "\n-------------------------------------\n"
    return context

# --- Main Application Logic ---
def main():
    """Main function to run the interactive Copilot."""
    # 1. Configure Google AI API
    try:
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        print("Google AI API configured.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # 2. Initialize ChromaDB Client
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"Connected to ChromaDB collection: '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        print("Please ensure the database was created successfully by running embed_and_store.py")
        return

    # 3. Initialize Generative Model
    model = genai.GenerativeModel(GENERATION_MODEL)
    print(f"n8n Integration Copilot is ready. Ask your questions below.")
    print("Type 'quit' or 'exit' to stop.")

    # 4. Interactive Q&A Loop
    while True:
        try:
            query = input("\nQuestion: ")
            if query.lower() in ['quit', 'exit']:
                break
            if not query.strip():
                continue

            # a. Embed the user's query
            print("\nEmbedding your question...")
            query_embedding = genai.embed_content(model=EMBEDDING_MODEL, content=query, task_type="RETRIEVAL_QUERY")['embedding']

            # b. Query ChromaDB for relevant documents
            print("Searching for relevant documents...")
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=5 # Retrieve the top 5 most relevant chunks
            )

            # c. Format the context and create the prompt
            context = format_context(results)
            prompt = f"Question: {query}\n\n{context}\n\nBased on the provided documentation, please answer the user's question. If the context does not contain the answer, state that you could not find relevant information in the documentation."

            # d. Generate the answer
            print("Generating answer...")
            response = model.generate_content(prompt)
            
            # e. Print the results
            print("\n--- Answer ---")
            print(response.text)
            print(context) # Also print the sources used

        except Exception as e:
            print(f"An error occurred: {e}")

    print("\nCopilot session ended. Goodbye!")

if __name__ == '__main__':
    main()
