from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.web_scraper import article_1, article_2
from utils.news_refiner import refine_news
from utils.ai_models import language_id, news_pred
from markupsafe import Markup


app = FastAPI()

# Mount templates and static directories
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landingpage.html", {"request": request})


@app.get("/predict", response_class=HTMLResponse, name="predict")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse, name="predict")
async def post_form(request: Request, url: str = Form(...)):
    try:
        article_data, article1 = article_1(url)
        article2, newstitle = article_2(url)
        refined_article = refine_news(article1, article2)

        print("Extracted article1 content:", article1)
        print("Extracted article2 content:", article2)
        print("Refined article content:", refined_article)

        if article_data.get("status_code") == 403:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "show_modal": True,
                    "modal_message": "The content from this URL could not be retrieved. It may be restricted, paywalled, or formatted in an unsupported way.",
                },
            )

        if not article1.strip():
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "show_modal": True,
                    "modal_message": "The article content could not be extracted. Please try another URL.",
                },
            )

        lang_prediction = language_id(refined_article)
        print("Language identification:", lang_prediction)

        if lang_prediction == 0:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "show_modal": True,
                    "modal_message": "Sorry! This system currently supports only news articles written in English.",
                },
            )

        news_prediction = news_pred(refined_article)
        result = "Fake News" if news_prediction == 1 else "Real News"
        print(f"Prediction: {result}")

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "show_modal": True,
                "modal_message": Markup(
                    f"News Title: {newstitle}<br><br>Prediction: {result}"
                ),
            },
        )

    except Exception as e:
        print("Error in web scraping:", e)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "show_modal": True,
                "modal_message": f"Error processing article: {str(e)}",
            },
        )
