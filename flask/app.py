# Importing required libraries and modules
from flask import Flask, render_template, request
from markupsafe import Markup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.web_scraper import article_1, article_2
from utils.news_refiner import refine_news
from utils.ai_models import language_id, news_pred
from utils.visualization import highlight_attention

template_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "templates")
)

static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

# Initializing the Flask app
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


# Route for the landing page
@app.route("/")
def index():
    return render_template("landingpage.html")


# Route to handle the main prediction logic
@app.route("/main", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        url = request.form.get("url")  # Get the URL input from the user

        try:
            article_data, article1 = article_1(url)
            article2, newstitle, stat = article_2(url)
            # Refine and merge the scraped articles for better prediction
            refined_article = refine_news(article1, article2)
            print("Extracted article3 content:", refined_article)

            # Handle restricted or failed article access
            if article_data.get("status_code") == 403 and stat == 403:
                return render_template(
                    "index.html",
                    show_modal=True,
                    modal_message="The content from this URL could not be retrieved. "
                    "It may be restricted, paywalled, or formatted in an unsupported way.",
                )

            if not article1.strip():  # Check if the article is empty
                return render_template(
                    "index.html",
                    show_modal=True,
                    modal_message="The article content could not be extracted. Please try another URL.",
                )

            lang_prediction = language_id(refined_article)

            # If the article is not in English, reject with a modal message
            if lang_prediction == 0:
                return render_template(
                    "index.html",
                    show_modal=True,
                    modal_message="Sorry! This system currently supports only news articles written in English.",
                )

            news_prediction, tokens, attention_scores = news_pred(refined_article)
            print("top tokens:", tokens)
            highlighted_html = highlight_attention(tokens, attention_scores)
            # Save the output to an HTML filec
            filename = "attention_visualization.html"
            output_path = os.path.join(os.getcwd(), filename)
            print(f"Saving to: {output_path}")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"<html><body>{highlighted_html}</body></html>")

            # Prepare the prediction message
            prediction = f"News Title: {newstitle}\n\nPrediction: {'Fake News' if news_prediction == 1 else 'Real News'}"
            print(prediction)

            # Display the prediction in a modal popup
            return render_template(
                "index.html",
                showmodal=True,
                modalmessage=Markup(
                    f"News Title: {newstitle}<br><br>Prediction: {'Fake News' if news_prediction == 1 else 'Real News'}<br><br>Based on attention to:{', '.join(tokens)}"
                ),
            )

        # Catch and display any error during scraping or prediction
        except Exception as e:
            print("Error in web scraping:", e)
            return render_template(
                "index.html",
                show_modal=True,
                modal_message=f"Error processing article: {str(e)}",
            )


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
