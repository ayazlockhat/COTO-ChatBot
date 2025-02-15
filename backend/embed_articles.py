import os
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Use the updated import for OpenAIEmbeddings per deprecation warning.
from langchain_community.embeddings import OpenAIEmbeddings

import chromadb
# Import the scraping functions from scraper.py
from scraper import get_article_links, scrape_article_content

def scrape_articles_content():
    """
    Retrieve all article links from the listing page and then scrape each article.
    Returns a list of articles, where each article is a dict with keys: "title", "url", and "content".
    """
    listing_url = (
        "https://www.coto.org/resources/?lang=en&view=grid&term=&resource-audience=&"
        "resource-topic=&resource-type=practice-guidance"
    )
    links = get_article_links(listing_url)
    articles = []
    print(f"Found {len(links)} article links.")
    
    for idx, link in enumerate(links):
        print(f"Scraping article {idx + 1}/{len(links)}: {link}")
        try:
            article = scrape_article_content(link)
            articles.append(article)
        except Exception as e:
            print(f"Error scraping {link}: {e}")
        # Pause briefly to avoid overloading the server
        time.sleep(1)
    return articles

# Get articles using the wrapper function
articles = scrape_articles_content()

# Ensure your OpenAI API key is set in your environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

# Initialize the OpenAI embeddings model using the cheapest model
embedding_model = OpenAIEmbeddings(
    openai_api_key=openai_api_key,
    model="text-embedding-3-small"
)

# Set up the ChromaDB client using the new instantiation (in-memory for testing)
client = chromadb.Client()

# Create or get an existing collection to store the articles
collection = client.get_or_create_collection(name="articles")

# Prepare lists for batch processing
documents = []   # Combined title + content for each article
metadatas = []   # Metadata for each article
ids = []         # Using the URL as a unique identifier

for article in articles:
    text_to_embed = f"{article['title']}\n\n{article['content']}"
    documents.append(text_to_embed)
    metadatas.append({"title": article['title'], "url": article['url']})
    ids.append(article['url'])

# Generate embeddings for all documents in one batch call
embeddings = embedding_model.embed_documents(documents)

# Add all documents to ChromaDB in one batch
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids  # using the URL as a unique identifier
)

print("Embeddings generated in batch and stored in ChromaDB!")
