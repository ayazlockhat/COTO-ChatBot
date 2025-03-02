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

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="articles")

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


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

            context_texts.append(
                f"[Source {i+1}: {metadata['title']} - {article_id}]\n{article_content}")

            relevant_articles.append(Article(
                title=metadata['title'],
                url=article_id,
                content=article_content[:200] + "...",
                relevance=1 - distance
            ))

        context = "\n\n".join(context_texts)

        system_message = (
            "You are a chatbot that must answer questions using only the provided articles. "
            "Do NOT incorporate any external data."
            "Always cite your sources using [Source X] notation, where X matches the sources provided."
            "If there are multiple sources, include multiple citations (e.g., [Source 1, Source 3])."
            "At the END of your response, provide a reference list in this format:"
            "'Source X: [Article Title](URL)'. "
            "If you cannot find direct information, say you can't and provide the top 3 articles that could benefit the user."
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""Here are the available articles:
-----------------
{context}
-----------------

Based on these articles, please answer this question:
{query.question}"""}
        ]

        chat_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0
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
