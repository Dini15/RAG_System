# **RoboMaid Assist**  

This repository contains the code and dependencies required to build a **Retrieval-Augmented Generation (RAG) System** that assists users in understanding the **manual book** of a **robotic floor cleaner (Robot Pembersih Lantai)**. It also includes the code used to generate the **synthetic dataset**.  

## **Project Overview**  

The step-by-step process for building this project is as follows:  

### 1. Generate Synthetic PDF  
A **50-page synthetic manual** in **Bahasa Indonesia** was created. The document contains a mix of **text, graphs, charts, and images** to simulate a real-world manual.  

### 2. Generate Synthetic Dataset: Database/SQL  
A **synthetic SQL database** was generated with:  
- **10 columns** (features)  
- **1,000 rows** (in CSV format)  
- A portion of this dataset is included in the synthetic PDF.  

### 3. Build the RAG System  
The system uses the following components:  
- **Embedding model**: Text is embedded using **Ollama**.  
- **Vector database**: Embeddings are stored in **FAISS** for efficient retrieval.  
- **LLM for response generation**: Uses **LLaMa via Groq API**.  
- The system was tested using **10 benchmark questions** (see `questions.txt`).  

### 4. Format the Synthetic PDF Data for Fine-Tuning  
After creating the synthetic PDF and testing the chatbot, the data was reformatted to ensure compatibility with **fine-tuning AI models**.  
