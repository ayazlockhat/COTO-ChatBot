import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Step 1: Get all article links from the listing page.
def get_article_links(listing_url):
    response = requests.get(listing_url)
    response.raise_for_status()  # Raise an error for bad status codes
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = []

    # Adjust the selector based on the actual HTML structure.
    # For example, if article links are in <a> tags within a certain container.
    # Here, we're assuming that links are inside <a> tags with class "resource-link"
    for a_tag in soup.find_all("a", class_="resource-link resource-item"):
        href = a_tag.get('href')
        if href:
            # Convert relative URLs to absolute URLs
            full_url = urljoin(listing_url, href)
            article_links.append(full_url)

    return article_links

# Step 2: For each article, scrape the content.
def scrape_article_content(article_url):
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    # For example, assume the title is in an <h1> tag
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Extract the main content
    # For example, assume the content is in a <div> with class "article-content"
    content_tag = soup.find("div", class_="entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained")
    content = content_tag.get_text(strip=True) if content_tag else "No content found"

    return {
        "url": article_url,
        "title": title,
        "content": content
    }

if __name__ == "__main__":
    # The listing page with article links.
    listing_url = "https://www.coto.org/resources/?lang=en&view=grid&term=&resource-audience=&resource-topic=&resource-type=practice-guidance"
    
    print("Fetching article links...")
    article_links = get_article_links(listing_url)
    print(f"Found {len(article_links)} articles.")

    articles = []
    for idx, link in enumerate(article_links):
        print(f"Scraping article {idx + 1}/{len(article_links)}: {link}")
        try:
            article_data = scrape_article_content(link)
            articles.append(article_data)
        except Exception as e:
            print(f"Error scraping {link}: {e}")
        # Be courteous and avoid overwhelming the server
        time.sleep(1)

    # For now, simply print the scraped data.
    for article in articles:
        print("\n-----------------------------------")
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Content snippet: {article['content'][:200]}...")  # Print first 200 characters
