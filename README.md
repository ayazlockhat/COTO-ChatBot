## **ChatOTP - COTO Resource Chatbot**

### **Overview**
This project is a chatbot that answers user questions based on articles from the [COTO Resources](https://www.coto.org/resources/) page. The chatbot uses an LLM (OpenAI) with document embeddings stored in a vector database for fast and accurate responses.

---

### **Tech Stack**
- **Frontend:** React + Vite + TailwindCSS  
- **Backend:** FastAPI + LangChain  
- **Scraping:** BeautifulSoup + Requests  
- **Storage:** ChromaDB (Vector Database)  
- **LLM:** OpenAI API - GPT-4o mini and text-embedding-ada-002
- **Deployment:** Docker + Cloudflare Tunnel

---

### **Local Deployment Instructions** with Docker

#### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-repo/COTO-ChatBot.git
cd COTO-ChatBot
```

#### **2️⃣ Set Up Environment Variables**

Create the **backend `.env` file**:

```bash
echo "OPENAI_API_KEY=your-openai-api-key" > backend/.env
```

Create the **frontend `.env` file**:

```bash
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

#### **3️⃣ Build with Docker**

```bash
docker build -t chatotp .
```

#### **4️⃣ Run the Application**

```bash
docker run -d -p 8000:8000 -p 8501:8501 \
  -v ~/docker/chatotp/COTO-ChatBot/backend/chroma_db:/app/backend/chroma_db \
  --restart unless-stopped \
  --name chatotp chatotp
```

#### **5️⃣ Access the Application**

- **Frontend:** Open http://localhost:8501
- **Backend API:** Open http://localhost:8000/docs for FastAPI Swagger UI

---

### **Images**
| ![Image 1](https://github.com/user-attachments/assets/d8e6f3fd-db79-4075-9967-bbb1be9908fc) | ![Image 2](https://github.com/user-attachments/assets/1bb8b2f1-5044-420e-93f7-45d66b6203dd) |
|:--:|:--:|
| **Main Page** | **Chat Response** |

| ![image](https://github.com/user-attachments/assets/de0abba5-2251-40eb-abc5-c0118b31abcf) | ![image](https://github.com/user-attachments/assets/a035a30f-da52-404d-a60d-34bdac59c271) |
|:--:|:--:|
| **Additional Features** | **Swagger FastAPI** |



---


