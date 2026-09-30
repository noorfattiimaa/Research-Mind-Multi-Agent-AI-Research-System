# 🧠 Research Mind — Multi-Agent AI Research System

**Research Mind** is an AI-powered research assistant that automates the initial stages of research through a structured multi-agent workflow.

It combines web search, content extraction, LLM-powered analysis, report generation, and critical review into a single research pipeline.

## Features

* 🔎 **Web Research** — Searches for relevant research information and sources.
* 📖 **Content Analysis** — Extracts and processes information from selected web pages.
* ✍️ **AI Report Generation** — Organizes findings into a structured research report.
* 🧐 **Critical Review** — Reviews generated content for weaknesses and missing information.
* ⚡ **Groq LLM Inference** — Uses Groq for fast LLM-powered processing.
* 🌐 **Tavily Search** — Provides web search capabilities for the research pipeline.
* 🖥️ **Streamlit Interface** — Provides a simple interactive interface.

## 🔄 Research Pipeline

```text
Research Topic
      ↓
🔎 Search Agent
      ↓
📖 Reader Agent
      ↓
✍️ Writer Agent
      ↓
🧐 Critic Agent
      ↓
📄 Structured Research Report
```

## 🛠️ Tech Stack

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | Core application                   |
| Streamlit     | User interface                     |
| LangChain     | Agent and LLM orchestration        |
| Groq          | LLM inference                      |
| Tavily        | Web search                         |
| BeautifulSoup | Web content extraction             |
| Pydantic      | Data validation                    |
| FAISS         | Vector-based information retrieval |
| Docker        | Containerization                   |

## 🔐 API Configuration

Research Mind requires API credentials for its external AI and search services.

### Required API Keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/noorfattiimaa/Research-Mind-Multi-Agent-AI-Research-System.git
cd Research-Mind-Multi-Agent-AI-Research-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run Research Mind

```bash
streamlit run app.py
```

Open the application at:

```text
http://localhost:8501
```

## 🐳 Docker

Build the Docker image:

```bash
docker build -t research-mind .
```

Run the application:

```bash
docker run -p 8501:8501 --env-file .env research-mind
```

Then open:

```text
http://localhost:8501
```

## 🎯 Purpose

Research Mind is designed to reduce the time and effort required to explore a research topic.

Rather than relying on a single AI response, the system separates the workflow into specialized stages—**searching, reading, writing, and reviewing**—to produce a more structured research output.

## ⚠️ Disclaimer

Research Mind is an AI-assisted research tool. Its generated content and sources should be independently verified before being used in academic papers, publications, or other important work.

## 👩‍💻 Author

**Noor Fatima**
BS Computer Science — UET Lahore

GitHub: **[@noorfattiimaa](https://github.com/noorfattiimaa)**

---

> **Research Mind — From research questions to structured insights.**
