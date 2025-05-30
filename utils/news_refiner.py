import re
from spacy.lang.en.stop_words import STOP_WORDS as english_stopwords
from utils import web_scraper

# Convert the stopwords set into a set for fast lookup
stopwords = set(english_stopwords)


def first_part(f_news1, f_news2):
    """
    Finds the first part of f_news1 that doesn't match the beginning of f_news2.

    f_news1, f_news2: List of words (tokenized text) from two news articles.

    Returns the remaining part of f_news1 after the matching sequence with f_news2.
    """
    i = j = 0
    # Traverse both lists (f_news1 and f_news2) to find the common prefix
    while i < len(f_news1) and j < len(f_news2):
        if f_news1[i] == f_news2[j]:
            j += 1
        i += 1
    # Return the rest of f_news1 after the matching part
    return " ".join(f_news1[i:])


def last_part(lst):
    """
    Removes unwanted words (e.g., 'Subscribe', 'BBC') and emails from the last part of a text.

    lst: A string representing a portion of the text.

    Returns a list of sentences that don't contain unwanted words or email addresses.
    """
    unwanted_words = {"Subscribe", "BBC"}
    # Regex pattern to match email addresses
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    # Split the text into sentences based on ". "
    sentences = lst.split(". ")
    # Filter sentences that do not contain unwanted words or email addresses
    filtered_text = [
        sent
        for sent in sentences
        if not any(word in sent for word in unwanted_words)
        and not email_pattern.search(sent)
    ]
    return filtered_text


def text_preprocessing(text):
    """
    Preprocesses the input text by removing special characters, converting to lowercase,
    removing stopwords, and filtering out short words.

    text: The input text string.

    Returns the cleaned-up text as a string.
    """
    # Remove special characters and digits using regular expressions
    text = re.sub(r"[!@#$()-,\n\"%^*?:.;~\[\]\d]", " ", text)
    # Split the text into words and convert to lowercase
    words = text.lower().split()
    # Remove stopwords and words shorter than 3 characters
    words = [
        word.replace("'", "")
        for word in words
        if word not in stopwords and len(word) > 2
    ]
    # Join the filtered words back into a string
    return " ".join(words)


def refine_news(b_news, p_news):
    """
    Refines and preprocesses two pieces of news text (b_news and p_news).

    b_news: The first piece of news (base news).
    p_news: The second piece of news (potentially matching base news).

    Returns a preprocessed string representing the refined news.
    """
    # Split base news into sentences
    news1_sentences = b_news.split(". ")
    # Split potential news into lines and remove empty lines
    news2_lines = [line.strip() for line in p_news.splitlines() if line.strip()]

    # If either base news or potential news is empty, return base news
    if not news1_sentences or not news2_lines:
        return b_news

    # Process the first part (i.e., the common prefix between news articles)
    fpt = first_part(news1_sentences[0].split(" "), news2_lines[0].split(" "))
    # Extract the middle part (all sentences between the first and last 5 sentences)
    mid_pt = news1_sentences[1:-5] if len(news1_sentences) > 5 else []
    # Extract the last part (last 5 sentences or fewer)
    lst_pt = ". ".join(news1_sentences[-5:-1]) if len(news1_sentences) > 5 else ""

    # Initialize lists for refined first part and last part
    refined_fpt = [fpt] if fpt else []
    refined_lst = last_part(lst_pt) if lst_pt else []

    # Combine the first part, middle part, and last part
    refined_fpt.extend(mid_pt)
    refined_fpt.extend(refined_lst)

    # Join the refined parts into a single string
    refined_news = ". ".join(refined_fpt)

    # Preprocess the refined news and return the result
    pprocess_news = text_preprocessing(refined_news)
    return pprocess_news
