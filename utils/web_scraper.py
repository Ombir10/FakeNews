# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from newspaper import Article


# Class for scraping news content using requests and BeautifulSoup
class NewsScraper:
    def __init__(self, url):
        self.url = url  # News article URL
        self.content = ""  # Placeholder for the scraped content
        self.status_code = None  # To store the HTTP status code

    def fetch_article(self):
        try:
            # Send GET request to the URL
            response = requests.get(self.url)
            self.status_code = response.raise_for_status()  # Will be None if successful
            response.raise_for_status()  # Raise error if status is not 200

            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract all paragraph tags and combine their text
            content_tags = soup.find_all("p")
            self.content = " ".join([tag.get_text().strip() for tag in content_tags])

        except requests.HTTPError as http_err:
            # Handle HTTP-specific errors (e.g. 404, 403)
            self.content = "Error fetching content"
            self.status_code = response.status_code
        except requests.RequestException as e:
            # Handle general request exceptions
            self.content = "Error fetching content"
            self.status_code = 500  # Custom internal error code

    def get_article(self):
        # Return article content and status as a dictionary
        return {
            "content": self.content if self.content else "Content not found",
            "status_code": self.status_code,
        }


# Alternative class for scraping using newspaper3k library
class News:
    def __init__(self, url):
        self.url = url  # News article URL
        self.content = ""  # Placeholder for article text
        self.status_code = None  # HTTP status code placeholder
        self.title = ""

    def extract_title_from_url(self):
        # Extracts a readable title from the URL
        article = Article(self.url)
        article.download()
        article.parse()
        title = article.title
        return title

    def fetch_news(self):
        try:
            # Create and download the article using newspaper3k
            article = Article(self.url)
            article.download()
            article.parse()

            # Extract title and content
            self.title = article.title
            self.content = article.text
            self.status_code = 200  # Success

            return {
                "title": self.title if self.title else "Content not found",
                "content": self.content if self.content else "Content not found",
                "status_code": self.status_code,
            }
        except Exception as e:
            # Handle errors during downloading or parsing
            print(f"Error: {e}")
            self.content = "Error fetching content"
            self.status_code = 403  # Custom error code for parse failure

            return {"content": self.content, "status_code": self.status_code}


def article_1(url):
    # Scrape article content from the given URL using two different strategies
    newscraper1 = NewsScraper(url)
    newscraper1.fetch_article()
    article_data = newscraper1.get_article()
    article1 = article_data.get("content")
    return article_data, article1


def article_2(url):
    newscraper2 = News(url)
    article2 = newscraper2.fetch_news().get("content")
    newstitle = newscraper2.fetch_news().get("title")
    status = newscraper2.fetch_news().get("status_code")
    return article2, newstitle, status
