# AI Desktop Assistant with Local Database Caching

A Python-based desktop application featuring a GUI built with Tkinter, integrated with Google's Gemini 2.0 Flash API, and backed by a local SQLite database to handle smart text caching and long-term memory retrieval.

## 🧠 System Architecture & Features
- **Local Response Caching (SQLite):** The application checks a local SQLite database before making API calls. If the prompt has been answered before, it pulls instantly from local storage, saving bandwidth and API token costs.
- **Context Persistence (JSON):** Stores lightweight session data (like user preferences and user profile names) inside a local JSON file structure.
- **External LLM Integration:** Leverages the `google-generativeai` SDK to handle complex reasoning queries dynamically when local cache misses occur.
- **User Interface (Tkinter):** Clean and straightforward desktop graphical user interface for seamless message exchanges.

## 🛠️ Tech Stack
- Python
- SQLite3
- Tkinter (GUI)
- Google Gemini AI SDK
- JSON / File I/O




## 💬 Just a few words of Suko
This project aims to create a unique personal assistant with its own local database, built upon existing AI models. The initial idea was to develop an assistant capable of real-time voice conversations, a feature that will be implemented in the future. Since the current focus is to establish a solid, functional base, all APIs used are free, making the code easily accessible to anyone.

It is worth highlighting that this code is being developed with the help of ChatGPT. Since I am still gaining experience in programming, the AI is HELPING me shape the code, acting as a co-pilot rather than writing it entirely on its own.
