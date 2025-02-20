from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="articles")

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define request/response models
class Query(BaseModel):
    question: str
    top_k: Optional[int] = 3

class Article(BaseModel):
    title: str
    url: str
    content: str
    relevance: float

class ChatResponse(BaseModel):
    answer: str
    relevant_articles: List[Article]

@app.post("/api/chat", response_model=ChatResponse)
async def chat(query: Query):
    try:
        # Generate embedding for the question
        embedding_response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=query.question
        )
        question_embedding = embedding_response.data[0].embedding
        
        # Query ChromaDB for relevant articles
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=query.top_k
        )
        
        # Prepare context from relevant articles
        context_texts = []
        relevant_articles = []
        
        for i in range(len(results['ids'][0])):
            article_id = results['ids'][0][i]
            article_content = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            
            # Add to context with source marker
            context_texts.append(f"[Source {i+1}: {metadata['title']}]\n{article_content}")
            
            # Add to relevant articles list
            relevant_articles.append(Article(
                title=metadata['title'],
                url=article_id,
                content=article_content[:200] + "...",
                relevance=1 - distance
            ))
        
        # Combine context
        context = "\n\n".join(context_texts)
        
        # Updated system message to encourage more helpful responses
        system_message = """You are a helpful assistant that provides information based on the available articles. 
When answering:
1. If you find directly relevant information, provide it with source references
2. If you find partially relevant information, explain how it relates to the question
3. If you find related guidelines or information that might be helpful, share those
4. Always cite your sources using [Source X] notation and add the sources link to the [Source X] text
5. Be clear about what information comes from which source
6. If you make connections between multiple sources, explain your reasoning
7. At the end, link each source to the top 3 relevant articles

If no relevant information is found, suggest related topics from the articles that might be helpful."""

        # Create message for ChatGPT
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""Here are the available articles:
-----------------
{context}
-----------------

Based on these articles, please answer this question:
{query.question}

Remember to cite sources and explain any connections you make between different pieces of information."""}
        ]
        
        chat_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2
        )
        
        answer = chat_response.choices[0].message.content
        
        return ChatResponse(
            answer=answer,
            relevant_articles=relevant_articles
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)