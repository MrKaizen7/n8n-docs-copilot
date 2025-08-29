![Banner image](https://user-images.githubusercontent.com/10284570/173569848-c624317f-42b1-45a6-ab09-f0ea3c247648.png)

# n8n Docs

This repository hosts the documentation for [n8n](https://n8n.io/), an extendable workflow automation tool which enables you to connect anything to everything. The documentation is live at [docs.n8n.io](https://docs.n8n.io/).


## Previewing and building the documentation locally

### Prerequisites

* Python 3.8 or above
* Pip
* n8n recommends using a virtual environment when working with Python, such as [venv](https://docs.python.org/3/tutorial/venv.html).
* Follow the [recommended configuration and auto-complete](https://squidfunk.github.io/mkdocs-material/creating-your-site/#minimal-configuration) guidance for the theme. This will help when working with the `mkdocs.yml` file.
* The repo includes a `.editorconfig` file. Make sure your local editor settings **do not override** these settings. In particular:
	- Don't allow your editor to replace tabs with spaces. This can affect our code samples (which must retain tabs for people building nodes).
	- One tab must be equivalent to four spaces.

### Steps

#### For members of the n8n GitHub organization:

1. Set up an SSH token and add it to your GitHub account. Refer to [GitHub | About SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh) for guidance.
2. Then run these commands:

```bash
git clone --recurse-submodules git@github.com:n8n-io/n8n-docs.git
cd n8n-docs
# Set up virtual environment if using one (steps depend on your system)
# Install dependencies
pip install -r requirements.txt
pip install _submodules/insiders
```

#### For external contributors:

Rely on the preview builds on pull requests, or use the free version of Material for MkDocs (most things are the same, some formatting may be missing)

Fork the repository, then:

```bash
git clone https://github.com/<your-username>/n8n-docs.git
cd n8n-docs
pip install -r requirements.txt
pip install mkdocs-material
```

#### To serve a local preview:

```bash
mkdocs serve --strict
```

## Contributing

Please read the [CONTRIBUTING](CONTRIBUTING.md) guide.

You can find [style guidance](https://github.com/n8n-io/n8n-docs/wiki/Styles) in the wiki.


## Support

If you have problems or questions, head to n8n's forum: https://community.n8n.io


## License

n8n-docs is [fair-code](https://faircode.io/) licensed under the [**Sustainable Use License**](https://github.com/n8n-io/n8n/blob/master/LICENSE.md).

More information about the license is available in the [License documentation](https://docs.n8n.io/reference/license/).

---

## n8n Integration Copilot Prototype

This section documents a proof-of-concept for an "n8n Integration Copilot," an interactive AI assistant that answers questions about n8n development. It uses the official n8n documentation as its knowledge base, ensuring that its answers are grounded in factual, up-to-date information.

The system is built on a Retrieval-Augmented Generation (RAG) architecture. It leverages the `google-generativeai` library for embedding and text generation and `ChromaDB` for efficient vector storage and retrieval.

### How it Works

The process is broken down into three main stages:

1.  **Processing:** A script scans the n8n documentation files (`.md`), cleans the text, and chunks it into smaller, semantically-related pieces based on headings.
2.  **Embedding & Storage:** Each text chunk is converted into a numerical vector (an embedding) using the Google AI API. These embeddings, along with the original text and metadata, are stored locally in a ChromaDB vector database.
3.  **Querying & Generation:** An interactive script takes a user's question, embeds it, and queries the ChromaDB to find the most relevant document chunks. The question and this retrieved context are then passed to a generative AI model (Gemini) to synthesize a final, context-aware answer.

### Setup and Installation

**Prerequisites:**
*   Python 3.8+
*   A Google AI API Key

**Instructions:**

1.  **Install Dependencies:** Ensure you have installed all dependencies, including the ones for this prototype.
```bash
pip install -r requirements.txt
```

### Usage

Follow these steps in order to set up the knowledge base and run the copilot.

#### Step 1: Process the Documentation

First, you need to process the raw markdown files from the `docs/` directory into a structured JSON file. Run the following command:

```bash
python process_docs.py
```

This will create a `processed_docs.json` file in your project directory.

#### Step 2: Create the Knowledge Base

Next, you need to embed the processed documents and store them in the local vector database. Before running the script, you must set your Google AI API key as an environment variable.

**In PowerShell (Windows):**
```powershell
$env:GOOGLE_API_KEY = "YOUR_API_KEY"
```

**In Command Prompt (Windows) or bash (Linux/macOS):**
```bash
set GOOGLE_API_KEY=YOUR_API_KEY  # Windows cmd
export GOOGLE_API_KEY='YOUR_API_KEY' # Linux/macOS
```

Once the key is set for your terminal session, run the script:

```bash
python embed_and_store.py
```

This will create a local `n8n_chroma_db/` directory containing the vector database. This process can take some time.

#### Step 3: Run the Copilot

Finally, you can run the interactive copilot. Make sure your API key is still set in your terminal session (as shown in Step 2).

```bash
python copilot.py
```

The script will prompt you for questions. Type your question and press Enter. To end the session, type `quit` or `exit`.

### Project Structure

```
.
├── docs/                     # Source n8n documentation files
├── n8n_chroma_db/            # Local ChromaDB vector store (created by embed_and_store.py)
├── copilot.py                # The final, interactive Q&A application
├── embed_and_store.py        # Script to create embeddings and store them
├── process_docs.py           # Script to parse and chunk the markdown files
├── processed_docs.json       # Staging file for processed text (created by process_docs.py)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```# n8n-docs-copilot
---
Basic functionality was achieved: Talking to ragged documentation.
Further development, such as:
```
- **🔁 Overall improvements**: Enhanced chunking, embedding and copilot capabilities.
- **🌍 Multilingual Intelligence**: Native support for Spanish and English with automatic language detection and smart translation
- **🧠 Conversational Memory**: Maintains context across interactions for natural, flowing conversations
- **📚 Dynamic Knowledge Base**: Automatically updated from official n8n documentation, community resources, and custom content
- **🔍 Semantic Search**: Advanced vector-based search with ChromaDB for finding relevant information
- **🎯 Context-Aware Responses**: Intelligent system that understands your specific use cases and provides targeted advice
- **🔄 Real-time Updates**: Webhook-based system for keeping knowledge base current with latest n8n developments
```
will be continued on [n8nation](https://www.github.com/MrKaizen7/n8nation). You'll like it there, check it out.
---