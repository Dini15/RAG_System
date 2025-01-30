# Import libraries
import ollama
from PyPDF2 import PdfReader
import tiktoken
import groq
import faiss
import numpy as np
import gradio as gr
import json
import os
import pickle

# == Buat folder models ==
os.makedirs("models", exist_ok=True)

# == Load API Key dari File (Hindari Hardcoded Key) ==
def load_api_key():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["GROQ_API_KEY"]

GROQ_API_KEY = load_api_key()

# == Ekstraksi Teks dari PDF ==
def extract_text_from_pdf(pdf_file: str) -> str:
    """Ekstrak teks dari PDF dan gabungkan menjadi satu string."""
    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf)
        text = " ".join(page.extract_text() or "" for page in reader.pages)
    return text

# == Chunking Teks ==
def chunk_text(text: str, max_tokens: int = 512) -> list:
    """Membagi teks menjadi chunk berdasarkan token menggunakan tokenizer OpenAI."""
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Gunakan tokenizer OpenAI
    tokens = tokenizer.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

# == Embedding dengan Ollama ==
def get_embedding(text: str):
    """Mendapatkan embedding dari teks menggunakan Ollama."""
    embedding = ollama.embed(model="mxbai-embed-large", input=text)
    return np.array(embedding["embeddings"][0], dtype=np.float32)  # Pastikan mengambil list pertama

# == Simpan Embedding ke FAISS ==
d = 1024  # Dimensi embedding dari model `mxbai-embed-large`
index = faiss.IndexFlatL2(d)  # Inisialisasi FAISS Index
text_chunks = []

def add_to_db(text_chunks_local):
    """Menambahkan embedding ke FAISS."""
    global text_chunks
    text_chunks = text_chunks_local  # Simpan chunk ke global var
    embeddings = np.array([get_embedding(text) for text in text_chunks], dtype=np.float32)
    index.add(embeddings)

def search_db(query, k=5):
    """Melakukan pencarian query dalam FAISS Index."""
    query_embedding = np.array([get_embedding(query)], dtype=np.float32).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    return [text_chunks[i] for i in indices[0]]  # Ambil teks chunk yang relevan

def save_to_faiss(index_path="vector_index.faiss"):
    """Menyimpan FAISS index ke file."""
    faiss.write_index(index, index_path)

def load_faiss(index_path="vector_index.faiss"):
    """Memuat kembali FAISS index dari file."""
    global index
    index = faiss.read_index(index_path)

# == Simpan dan Load Model Embedding ==
def save_embeddings(embeddings_path="models/embeddings.pkl"):
    with open(embeddings_path, "wb") as f:
        pickle.dump(index, f)

def load_embeddings(embeddings_path="models/embeddings.pkl"):
    global index
    with open(embeddings_path, "rb") as f:
        index = pickle.load(f)

# == Integrasi LLaMA via Groq API ==
client = groq.Client(api_key=GROQ_API_KEY)

def query_llama(prompt):
    """Menggunakan LLaMA untuk menjawab pertanyaan dengan konteks yang diberikan."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    return response.choices[0].message.content.strip()

# == Main Workflow ==
if __name__ == '__main__':
    pdf_text = extract_text_from_pdf('dini_anggriyani_synthetic_data.pdf')
    text_chunks = chunk_text(pdf_text, max_tokens=1024)  # Sesuaikan dengan LLaMA

    # Tambahkan ke database FAISS
    add_to_db(text_chunks)
    save_to_faiss()  # Simpan FAISS index
    save_embeddings()  

    # Tes pencarian RAG
    retrieved_chunks = search_db("Apa isi dokumen ini?")
    context = "\n".join(retrieved_chunks)
    
    prompt = f"Gunakan informasi berikut untuk menjawab:\n{context}\n\nPertanyaan: Apa isi dokumen ini?"
    answer = query_llama(prompt)
    print(answer)

# == Buat Chatbot Interface ==
def chatbot_interface(user_query):
    retrieved_chunks = search_db(user_query)  # Sudah berupa teks
    context = "\n".join(retrieved_chunks)
    
    prompt = f"Gunakan informasi berikut untuk menjawab:\n{context}\n\nPertanyaan: {user_query}"
    answer = query_llama(prompt)
    
    return answer

iface = gr.Interface(fn=chatbot_interface, inputs="text", outputs="text", title="RAG Chatbot")
iface.launch()
