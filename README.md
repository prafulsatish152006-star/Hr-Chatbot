# HR AI Assistant — RAG-Based Employee & HR Policy Intelligence System

An AI-powered Human Resources assistant built using **Retrieval-Augmented Generation (RAG)** to provide accurate, context-grounded answers to employee-related and HR policy questions.

The system combines **ChromaDB**, **Sentence Transformers**, **Groq LLMs**, structured employee data, and HR policy documents to create an intelligent HR knowledge system capable of retrieving relevant information and generating natural-language responses based on the available organizational data.

Unlike a basic LLM chatbot that relies entirely on its pretrained knowledge, this system retrieves relevant information from a dedicated HR knowledge base before generating an answer. This helps reduce hallucinations and ensures that responses are grounded in the organization's available employee records and HR policies.

---

##  Project Overview

Human Resources departments work with large amounts of employee information and policy documentation. Finding specific information manually can be time-consuming, especially when users need answers about employee attributes, departments, job roles, job levels, overtime, attrition, or company policies.

This project addresses that problem by creating an **AI-powered HR assistant** that allows users to ask questions in natural language.

For example:

* "What department does employee 441 work in?"
* "What is employee 441's job role?"
* "How many years has employee 441 been with the company?"
* "What are the consequences of violating an HR policy?"
* "What does the HR policy say about disciplinary action?"
* "What is the relationship between overtime and attrition?"
* "How many employees work in Research & Development?"

The system retrieves the appropriate information from the HR knowledge base and uses an LLM to generate a concise, human-readable response.

---

##  Architecture

The project follows a **Retrieval-Augmented Generation architecture**:

```text
                 ┌──────────────────────┐
                 │      User Query      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Query Processing   │
                 └──────────┬───────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
   Employee-specific query          General / Policy query
             │                             │
             ▼                             ▼
      Exact Employee ID             Semantic Retrieval
          Lookup                         │
             │                           ▼
             │                     Sentence Transformer
             │                           │
             │                           ▼
             │                       ChromaDB
             │                           │
             └──────────────┬────────────┘
                            │
                            ▼
                  Retrieved HR Context
                            │
                            ▼
                    Groq LLM Generation
                            │
                            ▼
                    Grounded HR Answer
```

The system combines **exact lookup** and **semantic retrieval** rather than relying entirely on vector similarity.

This is particularly important for employee-specific questions because an employee number is an exact identifier and should not be treated purely as a semantic search query.

---

## Retrieval-Augmented Generation

The core of the project is the RAG pipeline.

The process is:

```text
User Question
      ↓
Question Processing
      ↓
Relevant HR Information Retrieval
      ↓
Context Construction
      ↓
LLM Prompt
      ↓
Groq LLM
      ↓
Grounded Answer
```

The retrieved information is provided to the language model as context.

The LLM is instructed to use the retrieved information as the source of truth instead of inventing information.

This makes the system significantly more reliable for organization-specific questions.

---

## Employee Knowledge Base

The employee dataset contains **1,470 employee records** with multiple attributes related to employee demographics, job information, compensation, satisfaction, performance, overtime, and attrition.

The employee records are converted into structured documents before being indexed into ChromaDB.

The knowledge base contains information such as:

* Employee Number
* Age
* Department
* Job Role
* Job Level
* Monthly Income
* Business Travel
* Job Satisfaction
* Environment Satisfaction
* Relationship Satisfaction
* Work-Life Balance
* Years at Company
* Years in Current Role
* Years Since Last Promotion
* Overtime
* Attrition
* Education
* Marital Status
* and other employee attributes

Each employee record can therefore be retrieved and supplied as context to the language model.

---

##  HR Policy Knowledge Base

In addition to employee data, the system also incorporates an HR policy document.

The policy document is processed into smaller chunks so that relevant sections can be retrieved efficiently.

The policy processing pipeline includes:

```text
HR Policy PDF
      ↓
Text Extraction
      ↓
Document Cleaning
      ↓
Chunking
      ↓
Embedding Generation
      ↓
ChromaDB
```

The processed policy document resulted in **22 policy chunks**, which are stored alongside the employee information in the HR knowledge base.

This allows the assistant to answer questions related to HR policies using the actual policy content rather than relying on general knowledge from the LLM.

---

##  ChromaDB Vector Database

The project uses **ChromaDB** as the vector database.

The final HR knowledge collection contains:

```text
Employee documents : 1470
HR policy chunks    : 22
--------------------------------
Total documents     : 1492
```

The collection is named:

```text
hr_knowledge
```

ChromaDB is used to perform semantic similarity search for queries where vector retrieval is appropriate.

---

##  Sentence Transformers

The project uses the Sentence Transformers model:

```text
all-MiniLM-L6-v2
```

The model converts text into numerical vector representations called embeddings.

These embeddings allow the system to compare the semantic similarity between:

```text
User Question
        ↓
Question Embedding
        ↓
Compare with stored embeddings
        ↓
Retrieve relevant documents
```

This allows the assistant to understand queries based on meaning rather than requiring an exact keyword match.

---

##  Exact Employee Retrieval

One important improvement implemented in the project is **exact employee-number retrieval**.

A pure semantic search approach can sometimes retrieve unrelated employee records when the user asks about a specific employee number.

For example:

```text
"What department does employee 441 work in?"
```

Instead of relying entirely on semantic similarity, the system detects the employee number and performs an exact lookup.

The retrieval process becomes:

```text
Employee 441 detected
        ↓
Exact employee_number lookup
        ↓
Employee 441 record
        ↓
Relevant context
        ↓
LLM
        ↓
Answer
```

This prevents the system from accidentally answering the question using information from another employee.

This hybrid retrieval approach improves reliability for employee-specific questions.

---

##  Groq LLM Integration

After retrieving the relevant HR context, the project uses a **Groq-hosted large language model** to generate the final response.

The LLM receives:

```text
HR Context
+
User Question
+
System Instructions
```

and generates an answer based on the retrieved information.

The system prompt emphasizes:

* Context-grounded responses
* No hallucination
* Accurate employee identification
* Correct field mapping
* Numerical accuracy
* Evidence-based answers
* Proper policy interpretation
* Handling missing information
* Avoiding unsupported assumptions
* Not mixing information between employees

The model is also instructed not to expose internal RAG implementation details to the end user.

---

##  Hallucination Reduction

A major goal of the project is to reduce LLM hallucination.

The assistant is instructed to follow a **context-first approach**.

If the required information is not available in the retrieved context, the system should not invent an answer.

Instead, it should indicate that the information is not available in the provided HR knowledge base.

This is especially important for HR systems because employee information and company policies should be handled carefully and accurately.

---

##  HR Analytics

The project also includes an HR analytics notebook containing data visualizations created from the employee dataset.

The analysis includes several professional HR-focused visualizations.

### 1. Employees by Department

Shows the distribution of employees across different departments.

This provides an overview of the organizational workforce structure.

### 2. Employees by Job Role

Shows how employees are distributed across different job roles.

This can help identify which roles have the largest representation.

### 3. Attrition Rate by Department

Analyzes employee attrition across departments.

This can help identify departments where employee turnover may be relatively higher.

### 4. Overtime vs Attrition

Compares overtime status with employee attrition.

This provides an analytical view of whether employees working overtime show different attrition patterns.

### 5. Average Monthly Income by Job Level

Analyzes average employee income across different job levels.

This provides insight into the relationship between organizational level and compensation.

### 6. Job Satisfaction Distribution

Shows the distribution of employee job satisfaction scores.

This provides an overview of employee satisfaction levels within the dataset.

### 7. Age Distribution

Visualizes the age distribution of employees.

This helps understand the demographic structure of the workforce.

### 8. Correlation Heatmap

A correlation heatmap is used to examine relationships between numerical HR attributes.

This can help identify relationships between variables such as:

* Age
* Monthly Income
* Job Level
* Years at Company
* Years in Current Role
* Years Since Last Promotion
* Job Satisfaction
* Environment Satisfaction
* and other numerical attributes

The analytics notebook is located in:

```text
analysis/analysis.ipynb
```

---

##  Accuracy Testing

The project also includes an accuracy-testing workflow for evaluating the HR assistant.

Testing focuses on different categories of questions, including:

* Exact employee queries
* Employee attribute queries
* HR policy questions
* Semantic retrieval questions
* Numerical questions
* Missing-information questions
* Comparison questions
* Aggregation questions
* Employee identification
* Policy interpretation

The purpose of testing is not only to determine whether the LLM generates a reasonable sentence, but also whether:

1. The correct information was retrieved.
2. The correct employee was identified.
3. The answer is supported by the retrieved context.
4. The answer correctly maps to the requested HR field.
5. The LLM avoids unsupported claims.

The project therefore treats **retrieval accuracy and answer groundedness** as important components of overall system accuracy.

---

##  Technologies Used

### Programming Language

* Python

### AI / Machine Learning

* Sentence Transformers
* Natural Language Processing
* Retrieval-Augmented Generation
* Large Language Models

### Vector Database

* ChromaDB

### LLM

* Groq

### Data Processing

* Pandas
* JSON
* Python data-processing libraries

### Document Processing

* PDF text extraction
* Python document processing
* Text chunking

### Data Visualization

* Matplotlib
* Seaborn
* Jupyter Notebook

### Environment

* Python virtual environment
* VS Code
* Jupyter Notebook

---

##  Project Structure

```text
Hr-Chatbot/
│
├── analysis/
│   └── analysis.ipynb
│
├── archive/
│   ├── HR_Employee_Data.csv
│   └── new_HR_Employee_data.csv
│
├── documents/
│   ├── employee_documents.json
│   ├── hr policies.docx
│   └── hr_policy_chunks.json
│
├── scripts/
│   ├── clean_data.py
│   ├── create_employee_documents.py
│   ├── create_vector_db.py
│   ├── process_hr_policy.py
│   ├── rag.py
│   ├── test_retrieval.py
│   └── test_retrivials.py
│
├── accuracy_hr_measure.docx
├── hr policies.pdf
└── .gitignore
```

---

##  Complete Data Pipeline

The employee data pipeline follows:

```text
Raw HR Dataset
      ↓
Data Cleaning
      ↓
Clean Employee Dataset
      ↓
Employee Document Generation
      ↓
Sentence Transformer Embeddings
      ↓
ChromaDB
```

The policy pipeline follows:

```text
HR Policy Document
      ↓
Text Extraction
      ↓
Cleaning
      ↓
Chunking
      ↓
Sentence Transformer Embeddings
      ↓
ChromaDB
```

Both knowledge sources are then available to the HR assistant.

---

##  Example Queries

### Employee Questions

```text
What department does employee 441 work in?
```

```text
What is employee 441's job role?
```

```text
How many years has employee 441 been with the company?
```

### HR Policy Questions

```text
What are the consequences of violating an HR policy?
```

```text
What does the HR policy say about disciplinary action?
```

### Analytical Questions

```text
How many employees are in each department?
```

```text
Which department has the highest attrition?
```

```text
What is the relationship between overtime and attrition?
```

---

##  Security & Configuration

API credentials are stored using environment variables rather than hard-coded directly into the source code.

The `.env` file is excluded from version control through `.gitignore`.

Sensitive runtime files such as:

```text
.env
venv/
.venv/
chroma_db/
```

are excluded from the Git repository.

---

##  Future Improvements

The current project focuses on the RAG backend and HR analytics.

Planned improvements include:

* React-based HR assistant frontend
* FastAPI backend API
* Interactive HR analytics dashboard
* Employee search interface
* Source references showing the originating dataset row and column
* Better structured-data querying
* SQL/Pandas-based aggregation routing
* Improved evaluation framework
* Retrieval precision and recall measurement
* Conversation history
* Role-based access control
* More comprehensive HR policy coverage
* Production deployment

A particularly important future improvement is **query routing**.

Not every question should be answered through vector search.

For example:

```text
Employee-specific question
        ↓
Exact employee lookup

Policy question
        ↓
Semantic policy retrieval

Company-wide statistics
        ↓
Structured dataset query

Ranking question
        ↓
Full dataset analysis
```

This hybrid architecture can provide significantly better accuracy than using semantic retrieval for every type of question.

---

##  Project Goals

The main goals of this project are:

* Build a practical RAG application
* Apply semantic search to real-world organizational data
* Combine structured employee data with unstructured HR policies
* Reduce hallucinations in LLM-generated responses
* Implement exact entity retrieval for employee-specific queries
* Generate grounded natural-language answers
* Analyze HR data using visualization techniques
* Evaluate retrieval and answer accuracy
* Build an architecture that can eventually be extended into a production HR AI assistant

---

##  Key Highlights

**RAG-based HR assistant**

Uses retrieval before LLM generation to ground responses in HR knowledge.

**Hybrid retrieval**

Uses exact employee identification for employee-specific questions and semantic retrieval for general/policy questions.

**1,492 knowledge documents**

Combines 1,470 employee records with 22 HR policy chunks.

**Vector search**

Uses ChromaDB and Sentence Transformers for semantic retrieval.

**LLM-powered answers**

Uses Groq for natural-language response generation.

**HR analytics**

Includes multiple workforce, attrition, satisfaction, compensation, and correlation visualizations.

**Accuracy evaluation**

Includes dedicated testing of retrieval and generated answers.

**Hallucination-aware design**

The assistant is designed to answer using available context rather than inventing unsupported information.

---

## 📈 Project Status

### Completed

* [x] HR dataset cleaning
* [x] Employee document generation
* [x] HR policy processing
* [x] Policy chunking
* [x] Sentence Transformer embeddings
* [x] ChromaDB vector database
* [x] Employee retrieval
* [x] Exact employee-number retrieval
* [x] HR policy retrieval
* [x] Groq LLM integration
* [x] Grounded HR responses
* [x] HR analytics
* [x] Accuracy testing

### Planned

* [ ] React frontend
* [ ] FastAPI integration
* [ ] Interactive analytics dashboard
* [ ] Source/row/column tracing
* [ ] Structured query routing
* [ ] Production deployment

---

##  Conclusion

This project demonstrates the development of a practical **AI-powered HR knowledge system** using Retrieval-Augmented Generation.

Rather than treating an LLM as the sole source of information, the system combines a vector database, semantic embeddings, structured employee records, HR policy documents, exact employee lookup, and LLM-based generation.

The project also demonstrates an important principle in real-world AI applications: **retrieval strategy must match the type of question being asked**.

Semantic search is useful for finding relevant policy information and general knowledge, while exact lookups and structured data analysis are better suited for employee identifiers, statistics, rankings, and aggregations.

The resulting architecture provides a strong foundation for developing a production-ready HR AI assistant with a web frontend, API layer, analytics dashboard, improved evaluation, and enterprise-level access controls.
