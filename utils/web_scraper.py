import requests
from bs4 import BeautifulSoup
from newspaper import Article
class NewsScraper:
    def __init__(self, url):
        self.url = url
        self.content = ""
        self.status_code = None

    def fetch_article(self):
        """Fetches the article content from the given URL."""
        try:
            response = requests.get(self.url)
            self.status_code = response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content_tags = soup.find_all('p')  # Extract paragraphs
            self.content = ' '.join([tag.get_text().strip() for tag in content_tags])
        # except requests.RequestException as e:
        #     self.content = f"Error fetching content: {str(e)}"
            # self.content = 403
        except requests.HTTPError as http_err:
            self.content = "Error fetching content"
            self.status_code = response.status_code  # Capture error status code
        except requests.RequestException as e:
            self.content = "Error fetching content"
            self.status_code = 500  # Set generic server error code if request fails
    def extract_title_from_url(self):
        """Extracts and formats the title from the URL."""
        raw_title = self.url.split('/')[-1]
        return raw_title.replace('-', ' ').replace('.html', '').strip()
    def get_article(self):
        """Returns the scraped article as a dictionary."""
        return {
            'content': self.content if self.content else 'Content not found',
            'status_code': self.status_code
        }

class News:
    def __init__(self, url):
        self.url = url
        self.content = ""
        self.status_code = None
    
    def fetch_news(self):
        try:
            article = Article(self.url)
            article.download()
            article.parse()
            title = article.title
            self.content = article.text
            self.status_code = 200  # Success
            return {
                'title': title,
                'content': self.content if self.content else 'Content not found',
                'status_code': self.status_code
            }
        except Exception as e:
            print(f"Error: {e}")
            self.content = "Error fetching content"
            self.status_code = 430
            return {
                'content': self.content,
                'status_code': self.status_code
            }
