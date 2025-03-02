import os
import time
import chromadb
from langchain_openai import OpenAIEmbeddings
from scraper import get_article_links, scrape_article_content
from dotenv import load_dotenv

load_dotenv()


def scrape_articles_content():
    listing_url = (
        "https://www.coto.org/resources/?lang=en&view=grid&term=&resource-audience=&"
        "resource-topic=&resource-type=practice-guidance"
    )
    links = get_article_links(listing_url)
    articles = []

    for link in links:
        try:
            article = scrape_article_content(link)
            articles.append(article)
        except Exception:
            print(f"Failed to scrape article at {link}")
        time.sleep(0.5)
    return articles


articles = scrape_articles_content()

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

embedding_model = OpenAIEmbeddings(
    openai_api_key=openai_api_key,
    model="text-embedding-3-small"
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="articles")

documents = []
metadatas = []
ids = []

for article in articles:
    text_to_embed = f"{article['title']}\n\n{article['content']}"
    documents.append(text_to_embed)
    metadatas.append({"title": article['title'], "url": article['url']})
    ids.append(article['url'])

embeddings = embedding_model.embed_documents(documents)

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)
print("Articles added to ChromaDB.")
