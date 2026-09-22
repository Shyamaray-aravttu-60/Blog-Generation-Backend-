# Blog Generation Backend

An AI-powered backend service built with **FastAPI**, **LangGraph**, and **LangChain (Groq)** for generating structured blog posts through multi-stage prompt chaining, coupled with **PostgreSQL** user persistence via **SQLAlchemy**.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Workflow](#architecture--workflow)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [License](#license)

---

## 🎯 Overview

The **Blog Generation Backend** provides a streamlined API to automate long-form blog creation. Rather than generating a full article in a single prompt—which often leads to hallucinated structure or poor formatting—this service uses **LangGraph** to execute a two-step stateful workflow:
1. **Outline Generation**: Creates a structured, multi-section outline based on a topic.
2. **Blog Synthesis**: Synthesizes the outline and topic into a polished, complete blog article.

Additionally, the application includes user registration and retrieval capabilities backed by PostgreSQL.

---

## ✨ Key Features

- **Stateful AI Orchestration**: Uses LangGraph `StateGraph` to manage graph state across multiple AI execution steps.
- **Structured Outputs**: Employs Pydantic schema parsers (`PydanticOutputParser`) to ensure structured AI responses.
- **Fast & Scalable REST API**: Built on FastAPI with automated OpenAPI/Swagger documentation generation.
- **Groq LLM Acceleration**: Integrates with Groq API for rapid execution of LLM prompts.
- **User Management**: Simple signup and user retrieval endpoints with database persistence via SQLAlchemy.
- **Cross-Origin Resource Sharing (CORS)**: Configured out of the box for easy integration with web frontends.

---

## 🔄 Architecture & Workflow

### LangGraph Workflow

```text
       ┌─────────────┐
       │   [START]   │
       └──────┬──────┘
              │
              ▼
    ┌──────────────────┐
    │ llm_outline_gen  │  ──► Generates detailed outline using Pydantic output parser
    └─────────┬────────┘
              │
              ▼
    ┌──────────────────┐
    │  llm_blog_gen    │  ──► Combines topic & outline to produce complete blog post
    └─────────┬────────┘
              │
              ▼
       ┌─────────────┐
       │    [END]    │
       └─────────────┘
```

---

## 📂 Project Structure

```text
Blog-Generation-Backend/
├── .env                  # Environment variables (API keys, DB connection strings)
├── .gitignore            # Git ignore rules
├── blogGen_workflow.py   # LangGraph workflow definition & LLM nodes
├── database.py           # SQLAlchemy database setup and session creation
├── main.py               # FastAPI application, route handlers, middleware
├── models.py             # SQLAlchemy ORM models (User model)
├── requirements.txt      # Python package dependencies
└── valSchems.py          # Pydantic validation schemas for API & LLM parsing
```

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI / Agentic Workflow**: [LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)
- **LLM Provider**: [Groq](https://groq.com/)
- **ORM / Database**: [SQLAlchemy](https://www.sqlalchemy.org/) & [PostgreSQL](https://www.postgresql.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)

---

## ⚡ Prerequisites

Make sure you have the following installed on your machine:
- **Python 3.10+**
- **PostgreSQL** database server running locally or hosted (e.g., Supabase, Neon, Render)
- **Groq API Key** (obtainable from [Groq Console](https://console.groq.com/))

---

## 🔑 Environment Variables

Create a `.env` file in the root directory of the project and populate it with your credentials:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# PostgreSQL Database Connection URL
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Blog-Generation-Backend.git
   cd Blog-Generation-Backend
   ```

2. **Create and activate a virtual environment**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Application

1. **Ensure PostgreSQL is running** and your database URL is correctly configured in `.env`.

2. **Start the FastAPI development server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Verify running application**:
   - The server runs by default at `http://127.0.0.1:8000`
   - Open your browser to `http://127.0.0.1:8000/docs` to view the interactive **Swagger UI** documentation.
   - Alternatively, view **ReDoc** documentation at `http://127.0.0.1:8000/redoc`.

---

## 📖 API Documentation

### 1. General & Chat Endpoints

#### `GET /`
- **Description**: Root health/demo check.
- **Response**:
  ```json
  {
    "message": "This is demo app built by sham"
  }
  ```

#### `POST /chat`
- **Description**: Send a direct text prompt to the Groq LLM.
- **Request Body**:
  ```json
  {
    "prompt": "Summarize the history of space exploration in 3 bullet points."
  }
  ```
- **Response**:
  ```json
  {
    "response": "1. Early Milestones...\n2. Moon Landing...\n3. Modern Commercial Space Era..."
  }
  ```

---

### 2. AI Blog Generation Endpoint

#### `POST /get_blog`
- **Description**: Triggers the LangGraph multi-stage workflow (Outline $\rightarrow$ Blog Generation).
- **Query Parameter**: `topic` (string)
- **Example URL**: `/get_blog?topic=The%20Future%20of%20Quantum%20Computing`
- **Response Body**:
  ```json
  {
    "topic": "The Future of Quantum Computing",
    "outline": "Introduction into Quantum Mechanics...\nKey Applications...",
    "blog": "# The Future of Quantum Computing\n\nQuantum computing is poised to transform..."
  }
  ```

---

### 3. User Management Endpoints

#### `POST /user/signup`
- **Description**: Registers a new user in the PostgreSQL database.
- **Request Body**:
  ```json
  {
    "name": "Alex Smith",
    "age": 29,
    "email": "alex.smith@example.com",
    "gender": "Male",
    "password": "strongpassword123"
  }
  ```
- **Response**:
  ```json
  {
    "name": "Alex Smith",
    "age": 29,
    "gender": "Male"
  }
  ```

#### `GET /all_users`
- **Description**: Retrieves all registered users from the database.
- **Response**:
  ```json
  [
    {
      "name": "Alex Smith",
      "age": 29,
      "gender": "Male"
    }
  ]
  ```

---

## 🗄 Database Schema

The application automatically creates the `users` table on startup via SQLAlchemy ORM.

### `users` Table

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Auto-increment | Unique identifier |
| `name` | `String` | Non-nullable | Full user name |
| `age` | `Integer` | Non-nullable | Age of the user |
| `gender` | `String` | Non-nullable | User gender |
| `email` | `String` | Unique, Non-nullable, Indexed | User email address |
| `password` | `String` | Non-nullable | Encrypted or raw password |

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).