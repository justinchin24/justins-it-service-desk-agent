# 🤖 Autonomous IT Service Desk Agent

An AI-powered, multi-turn IT service desk assistant built with **FastAPI**, **Gemini (Google GenAI SDK)**, and **Streamlit**. This application demonstrates real-world agentic workflow automation—combining conversational chat, automated tool selection, REST API integration, and enterprise service desk operations.

---

## 🏗️ System Architecture

The application is split into a decoupled three-tier client-server architecture:

1. **FastAPI Backend (`app.py`)**: Acts as the enterprise mock server, exposing REST endpoints for permission checks, system health monitoring, and ticket creation.
2. **Gemini Agent Controller (`agent.py`)**: Manages multi-turn conversation state via the Google GenAI SDK, automatically intercepts user intent, extracts tool arguments, executes corresponding Python wrappers, and synthesizes user-friendly responses.
3. **Streamlit Web Interface (`ui.py`)**: Provides a responsive, chat-based web UI featuring persistent session state, formatted response rendering, and dynamic loading spinners.

---

## ⚙️ Key Features

* **Autonomous Tool Calling**: Gemini dynamically evaluates user queries and invokes the appropriate backend tool (`check_permissions`, `get_system_status`, or `create_ticket`) using strict parameter extraction.
* **Persistent Chat History**: Leverages Streamlit session state to retain conversation context across full-page reruns.
* **Robust Error Handling**: Gracefully catches network or execution exceptions and translates technical payloads into natural language explanations.
* **Low-Latency Python Integration**: Utilizes Python's `requests` library and FastAPI for lightning-fast local communication over standard loopback ports (`127.0.0.1:8000`).

## 🚀 Local Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- A Google Gemini API key ([Get an API Key](https://aistudio.google.com/))

### 2. Repository Setup
Clone the repository and open in VS code:
```bash
git clone https://github.com/justinchin24/justins-it-service-desk-agent.git
cd justins-it-service-desk-agent
code .
```

### 3. Virtual Environment Setup
Create and activate an isolated Python virtual environment:
```bash
py -m venv .venv

# On Windows:
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a .env file in the root directory and add your Google Gemini API key:
```bash
echo GEMINI_API_KEY=your_actual_api_key_here > .env
```

### 6. Running the Application
Start the FastAPI Mock Server
```bash
uvicorn app:app --reload
```
Launch the Streamlit web application:
```bash
streamlit run ui.py
```
---

## 📁 Repository Structure

```text
justins-it-service-desk-agent/
│
├── app.py              # FastAPI mock backend server
├── agent.py            # Defines the tool wrappers and Gemini agent logic
├── ui.py               # Streamlit UI implementation & chat logic
├── requirements.txt    # Project dependencies to install
├── .env                # Environment variables and API keys (ignored in git)
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```