# Workflow Engine

A minimal yet powerful **workflow/graph engine** inspired by LangGraph, built using **FastAPI**. Define nodes, connect them via edges, maintain shared state, and execute end-to-end workflows through REST APIs.

---

## 📌 Features

- 🧠 **Node Types** — Function, Conditional, Loop  
- 🔄 **Shared State Engine** with history tracking  
- 🔀 **Conditional & Dynamic Routing**  
- 🔧 **Tool Registry System** for pluggable custom tools  
- 📡 **REST APIs** for graph creation, execution & inspection  
- 📝 **Execution Logs** with timestamps and state snapshots  
- 🛑 **Infinite Loop Prevention** (max 100 steps)

Includes an **Example Code Review Agent** that:
- Extracts functions  
- Calculates complexity score  
- Detects issues  
- Suggests improvements  
- Computes overall quality score  

---

## 📂 Project Structure

<img width="485" height="235" alt="image" src="https://github.com/user-attachments/assets/bdb32a42-39d7-4df1-aae5-d9e1b92f83a5" />


---

## 🏃 How to Run the Project
1. **Clone the repository**
```bash
git clone <your-repo-url>
cd workflow-engine
```
2. **Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate


# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the FastAPI server**
```bash
uvicorn app.main:app --reload
```

5. **Access the API in your browser**
- 🌐 Base URL: http://localhost:8000

- 📘 Swagger UI: http://localhost:8000/docs

- 📕 ReDoc: http://localhost:8000/redoc


