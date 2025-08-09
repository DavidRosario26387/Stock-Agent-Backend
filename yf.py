import json
import feedparser
import requests
from bs4 import BeautifulSoup

def fetch_yahoo_rss(ticker):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link} for e in feed.entries[:5]]

def scrape_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return "Could not fetch article."
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Yahoo Finance articles
        article_block = soup.find("article")
        if article_block:
            paragraphs = [p.get_text(strip=True) for p in article_block.find_all("p")]
            return "\n".join(paragraphs)
        
        # Fallback for external sites: all <p> tags
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        return "\n".join(paragraphs[:10])  # limit length
    
    except Exception as e:
        return f"Error: {e}"

def fetch_full_news(ticker):
    headlines = fetch_yahoo_rss(ticker)
    news_list = []
    for h in headlines:
        content = scrape_article_content(h["link"])
        news_list.append({
            "title": h["title"],
            "link": h["link"],
            "content": content
        })
    return news_list

# Example usage:
# ticker = "INTC"
# news_items = fetch_full_news(ticker)
# for news in news_items:
#     print(news["title"])
#     # print(news["link"])
#     print(news["content"][:500])  # print first 500 chars
#     print("="*100)



# ticker = "TSLA"
# news_items = fetch_full_news(ticker)

# # Convert list of news dicts to JSON string
# news_json = json.dumps(news_items, indent=4)

# print(news_json)