
import json
import os
import chromadb
import google.generativeai as genai
import time

# --- Configuration ---
CHROMA_PATH = "n8n_chroma_db"
COLLECTION_NAME = "n8n_docs"
JSON_FILE = "processed_docs.json"
EMBEDDING_MODEL = "models/text-embedding-004"
API_KEY_ENV_VAR = "GOOGLE_API_KEY"

# --- Helper Functions ---
def get_google_api_key():
    """Gets the Google API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set. Please set it to your Google API key.")
    return api_key

def embed_text_batch(texts, model):
    """Embeds a batch of texts using the Google AI API."""
    try:
        return genai.embed_content(model=model, content=texts, task_type="RETRIEVAL_DOCUMENT")['embedding']
    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        # You might want to add retries or more specific error handling here
        time.sleep(10) # Wait before retrying or moving on
        return [[] for _ in texts] # Return empty embeddings for failed batch

# --- Main Script Logic ---
def main():
    """Main function to read data, create embeddings, and store in ChromaDB."""
    print("Starting the embedding and storage process...")

    # 1. Configure Google AI API
    try:
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        print("Google AI API configured.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # 2. Load the processed documents
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        print(f"Successfully loaded {len(documents)} document chunks from {JSON_FILE}.")
    except FileNotFoundError:
        print(f"Error: The file {JSON_FILE} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE}.")
        return

    # 3. Initialize ChromaDB
    print(f"Initializing ChromaDB client at: {CHROMA_PATH}")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    print(f"ChromaDB collection '{COLLECTION_NAME}' is ready.")

    # 4. Process documents in batches
    batch_size = 100  # Google's API has a limit on texts per request
    total_docs = len(documents)

    for i in range(0, total_docs, batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_texts = [doc['content'] for doc in batch_docs]
        
        print(f"\nProcessing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} (documents {i+1}-{min(i+batch_size, total_docs)})...")

        # Generate embeddings for the batch
        print("Generating embeddings...")
        embeddings = embed_text_batch(batch_texts, EMBEDDING_MODEL)

        # Prepare data for ChromaDB
        ids = [f"doc_{doc['source']}_{j}" for j, doc in enumerate(batch_docs, start=i)]
        metadatas = [{'source': doc['source'], 'heading': doc['heading']} for doc in batch_docs]
        contents = [doc['content'] for doc in batch_docs]

        # Filter out any failed embeddings before adding to the collection
        valid_indices = [idx for idx, emb in enumerate(embeddings) if emb]
        if not valid_indices:
            print("Warning: Embedding failed for the entire batch. Skipping.")
            continue
        
        if len(valid_indices) < len(batch_docs):
            print(f"Warning: Failed to embed {len(batch_docs) - len(valid_indices)} documents in this batch.")

        # 5. Add the batch to ChromaDB
        try:
            collection.add(
                ids=[ids[j] for j in valid_indices],
                embeddings=[embeddings[j] for j in valid_indices],
                metadatas=[metadatas[j] for j in valid_indices],
                documents=[contents[j] for j in valid_indices]
            )
            print(f"Successfully added {len(valid_indices)} documents to ChromaDB.")
        except Exception as e:
            print(f"An error occurred while adding documents to ChromaDB: {e}")

    print(f"\n--- Process Complete ---")
    print(f"Total documents processed: {total_docs}")
    print(f"Data stored in ChromaDB collection: '{COLLECTION_NAME}' at '{CHROMA_PATH}'")

if __name__ == '__main__':
    main()
