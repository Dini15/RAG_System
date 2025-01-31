# RoboMaid Assist

This repository containts the code and dependencies required to build a Retrieval-Augmented Generation (RAG) System to assist user understand the manual book of the product (Robot Pembersih Lantai). The system extracts information from a synthetic dataset (PDF), embeds the text using Ollama, stores the embeddings in FAISS, retrieves relevant chunks and generates responses using LLaMa via Groq API. The code used to generate synthetic dataset has also been included in this repository. 
