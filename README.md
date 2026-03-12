# Agentic RAG Application

An intelligent retrieval-augmented generation (RAG) application powered by LangGraph and OpenAI. This application builds a conversational agent that can answer questions by retrieving relevant information from documents and generating accurate, context-aware responses.

## 🎯 Features

- **Agentic Workflow**: Uses LangGraph to orchestrate complex multi-step reasoning
- **Retrieval-Augmented Generation**: Combines document retrieval with LLM capabilities for accurate answers
- **Vector Search**: Leverages Chroma for efficient semantic document searching
- **OpenAI Integration**: Uses GPT-4o-mini for intelligent response generation
- **Tool Integration**: Integrates custom retriever tools for document-based Q&A
- **Message History**: Maintains conversation context through message states

## 🏗️ Project Structure

```
.
├── User.py                    # Main entry point for the application
├── agent/
│   ├── __init__.py
│   └── RAGAgent.py           # Agent workflow definition
├── RAG/
│   ├── __init__.py
│   ├── embedding.py          # Vector store and embedding configuration
│   └── text_splitter.py      # Document loading and splitting
├── tools/
│   └── retrieverTool.py      # Retriever tool definition
├── db/
│   └── chroma_db/            # Vector database storage
├── .env                       # Environment variables (API keys)
└── .venv/                     # Virtual environment

```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- OpenAI API Key
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd "AI /Agentic RAG Application"
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install langchain-core langchain-community langchain-openai langchain-chroma langgraph python-dotenv
   ```

4. **Configure environment variables**

   Create or update the `.env` file with your OpenAI API key:

   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### Usage

Run the application:

```bash
python User.py
```

Example output:

```
What is the capital of France?
The capital of France is Paris.
```

## 📝 How It Works

1. **User Query**: User provides a question through `User.py`
2. **Agent Processing**: The agent (in `agent/RAGAgent.py`) receives the query
3. **Document Retrieval**: If needed, the retriever tool searches the vector database for relevant documents
4. **LLM Response**: OpenAI's GPT-4o-mini generates an answer based on retrieved context
5. **Output**: The final response is returned to the user

## 🔧 Configuration

### Vector Store

- **Database**: Chroma
- **Embeddings**: OpenAI's `text-embedding-3-small`
- **Collection**: `my_collection`
- **Storage**: `db/chroma_db`

### Language Model

- **Model**: `gpt-4o-mini`
- **Temperature**: 0.9 (for more creative responses)

### Document Processing

- **Chunk Size**: 1000 tokens
- **Chunk Overlap**: 200 tokens
- **Source**: Web articles (configurable in `RAG/text_splitter.py`)

## 📦 Key Dependencies

- **langgraph**: Agent orchestration and workflow management
- **langchain**: LLM framework and utilities
- **langchain-openai**: OpenAI integration
- **langchain-chroma**: Vector store implementation
- **python-dotenv**: Environment variable management

## 🔐 Security

⚠️ **Important**: Never commit your `.env` file with API keys to version control. Keep your OpenAI API key secure.

## 📚 Document Sources

Currently configured to load documents from web articles. Modify `RAG/text_splitter.py` to:

- Load from local files
- Load from PDFs
- Load from other sources

## 🛠️ Troubleshooting

### ModuleNotFoundError

Ensure you've activated the virtual environment and installed all dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### API Key Issues

Verify that:

- `.env` file exists in the project root
- `OPENAI_API_KEY` is set correctly
- Your OpenAI account has sufficient credits

### Vector Database Issues

If you encounter database errors, reset the Chroma database:

```bash
rm -rf db/chroma_db
```

The database will be recreated on the next run.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements.

## 📄 License

This project is open source. See LICENSE file for details.

## 💡 Future Enhancements

- [ ] Multi-source document loading
- [ ] Advanced agent reasoning capabilities
- [ ] Streaming responses
- [ ] Conversation persistence
- [ ] Performance optimization
- [ ] Unit and integration tests
- [ ] Docker deployment
- [ ] API endpoint exposure

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with LangChain + LangGraph + OpenAI**
