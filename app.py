from flask import Flask, render_template, request
import pickle, torch
from utils import web_scraper
from utils.tokenization import tokenize
from transformers import DistilBertForSequenceClassification
import re
from markupsafe import Markup

app = Flask(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("utils/vectors/tfidf_vectorizer.pkl", "rb") as vec_file:
    tfidf_vectorizer = pickle.load(vec_file)

with open("utils/models/langid_model.pkl", "rb") as lang_id:
    model_langid = pickle.load(lang_id)

with open("utils/models/fakenews_detection.pkl", "rb") as news_id:
    model_newsid = pickle.load(news_id)

model_newsid.to(device)
# model_newsid = DistilBertForSequenceClassification.from_pretrained(r"C:\Users\raiom.LAPTOP-59QT21KS\FakeNews\utils\models\fakenews_detection.pkl")


@app.route('/')
def index():
    return render_template('landingpage.html')

# @app.after_request
# def add_header(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response

@app.route('/main', methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        url = request.form.get('url')
        
        # if not url or not re.match(r"^https:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/.*)?$", url):
        #     return render_template('index.html', show_modal=True, modal_message="Invalid URL format. Please enter a valid URL starting with 'https://'.")
        
        try:
            # Fetch article using the scraper
            scraper = web_scraper.NewsScraper(url)
            scraper.fetch_article()
            title = scraper.extract_title_from_url()
            print(title)
            article_data = scraper.get_article()
            article = article_data.get('content', '')
            print("Extracted article content:", article)
            # if article:
            #     # Convert article text into vector
            #     article_vector = tfidf_vectorizer.transform([article])
            #     prediction = model_langid.predict(article_vector)[0]
            #                 # else:
            #     return render_template('index.html', error="Could not extract article content.")
            if article_data.get("status_code") == 403:
                return render_template('index.html', show_modal=True, modal_message="The content from this URL could not be retrieved. It may be restricted, paywalled, or formatted in an unsupported way.")

            if not article.strip():
                return render_template('index.html', show_modal=True, modal_message="The article content could not be extracted. Please try another URL.")
                
            # Convert article text into vector
            article_vector = tfidf_vectorizer.transform([article])
            lang_prediction = model_langid.predict(article_vector)[0]

            if lang_prediction == 0:
                return render_template('index.html', show_modal=True, modal_message="Sorry! This system currently supports only news articles written in English.")
                
            input_ids_texts, attention_masks_texts = tokenize([article], [], [])
            print(input_ids_texts, attention_masks_texts)
            input_tensor = input_ids_texts.clone().detach().to(device)
            attention_tensor = attention_masks_texts.clone().detach().to(device)

            with torch.no_grad():
                outputs = model_newsid(input_tensor, attention_mask = attention_tensor)
                logits = outputs.logits
                news_prediction = torch.argmax(logits, dim=1).item()
            prediction = f"News Title: {title}\n\nPrediction: {'Fake News' if news_prediction == 1 else 'Real News'}"
            print('modalmessage', prediction)
            return render_template('index.html', showmodal = True, modalmessage= Markup(f"News Title: {title}<br><br>Prediction: {'Fake News' if news_prediction == 1 else 'Real News'}"))
            
        except Exception as e:
                
            print("Error in web scraping:", e)
            # return render_template('index.html', error=f"Error processing article: {str(e)}")
            return render_template('index.html', show_modal=True, modal_message=f"Error processing article: {str(e)}")
        
if __name__ == "__main__":
    app.run(debug=True)
