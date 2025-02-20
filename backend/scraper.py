import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import io
from PyPDF2 import PdfReader

def get_article_links(listing_url):
    response = requests.get(listing_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = []
    for a_tag in soup.find_all("a", class_=["resource-link resource-item", "resource-link resource-item has-external"]):
        href = a_tag.get('href')
        if href:
            full_url = urljoin(listing_url, href)
            article_links.append(full_url)
    return article_links

def scrape_article_content(article_url):
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    content_tag = soup.find("div", class_="entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained")
    content = content_tag.get_text(strip=True) if content_tag else "No content found"

    return {
        "url": article_url,
        "title": title,
        "content": content
    }

def scrape_pdf_content(article_url):
    response = requests.get(article_url)
    response.raise_for_status()
    pdf_data = response.content
    pdf_file = io.BytesIO(pdf_data)
    
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

if __name__ == "__main__":
    listing_url = "https://www.coto.org/resources/?lang=en&view=grid&term=&resource-audience=&resource-topic=&resource-type=practice-guidance"
    
    print("Fetching article links...")
    article_links = get_article_links(listing_url)
    print(f"Found {len(article_links)} articles.")

    articles = []
    for idx, link in enumerate(article_links):
        print(f"Scraping article {idx + 1}/{len(article_links)}: {link}")
        try:
            # Check if the link is a PDF
            if link.lower().endswith(".pdf"):
                pdf_text = scrape_pdf_content(link)
                article_data = {
                    "url": link,
                    "title": "PDF Document",
                    "content": pdf_text if pdf_text else "No content found"
                }
            else:
                article_data = scrape_article_content(link)
            articles.append(article_data)
        except Exception as e:
            print(f"Error scraping {link}: {e}")
        time.sleep(1)

    for article in articles:
        print("\n-----------------------------------")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Content snippet: {article['content'][:200]}...")
