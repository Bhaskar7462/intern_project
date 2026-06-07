---
title: Multi Tool AI Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.30.0
app_file: streamlit_app.py
pinned: false
---

# 🤖 Multi Tool AI Assistant

An intelligent AI Assistant built using **LangChain** and **Groq API** that can perform multiple tasks using integrated tools such as calculations, web search, Wikipedia lookup, and conversation memory.

## 🚀 Features

- 💬 Conversational AI powered by Groq LLM
- 🧠 Memory support for maintaining conversation context
- 🧮 Calculator Tool for mathematical operations
- 🌐 Web Search Tool for online information retrieval
- 📚 Wikipedia Tool for knowledge lookup
- 🔗 LangChain Tool Integration
- ⚡ Fast inference using Groq API
- 🛠 Modular and extensible architecture

---

## 🏗 Project Structure

```text
Multi Tool AI Assistant/
│
├── agent/
│   └── assistant_agent.py
│
├── memory/
│   └── memory_manager.py
│
├── tools/
│   ├── calculator_tool.py
│   ├── web_search_tool.py
│   └── wikipedia_tool.py
│
├── test/
│   └── test_groq.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

- Python
- LangChain
- Groq API
- Wikipedia API
- Requests
- Environment Variables (.env)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Bhaskar7462/intern_project.git
cd intern_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com

---

## ▶️ Run the Application

```bash
python app.py
```

---

## 🧪 Run Tests

```bash
python test/test_groq.py
```

---

## Example Queries

```text
What is the capital of Japan?

Search Python programming language.

Who is Alan Turing?

Calculate 245 * 78.
```

---

## Future Improvements

- Voice Input and Output
- Weather Tool
- File Management Tool
- App Launcher Tool
- Multi-Agent Architecture
- Streamlit Web Interface
- Long-Term Memory Support

---

## Author

Bhaskar Mishra

B.Tech Student | AI & Software Development Enthusiast

GitHub: https://github.com/Bhaskar7462

---

## License

This project is developed for learning, internship, and educational purposes.
