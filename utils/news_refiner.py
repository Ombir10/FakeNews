import re
from spacy.lang.en.stop_words import STOP_WORDS as english_stopwords

stopwords = set(english_stopwords)
def first_part(f_news1, f_news2):
    i = j = 0
    while i < len(f_news1) and j < len(f_news2):
        if f_news1[i] == f_news2[j]:
            j += 1
        i += 1
    return " ".join(f_news1[i:])

def last_part(lst):
    unwanted_words = {'Subscribe', 'BBC'}
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    sentences = lst.split(". ")
    filtered_text = [sent for sent in sentences if not any(word in sent for word in unwanted_words) and not email_pattern.search(sent)]
    
    return filtered_text

def text_preprocessing(text):
    text = re.sub(r"[!@#$()-,\n\"%^*?:.;~\[\]\d]", " ", text)
    words = text.lower().split()
    words = [word.replace("'", "") for word in words if word not in stopwords and len(word) > 2]
    return " ".join(words)

def refine_news(b_news, p_news):
    news1_sentences = b_news.split(". ")
    news2_lines = [line.strip() for line in p_news.splitlines() if line.strip()]
    
    if not news1_sentences or not news2_lines:
        return b_news
    
    fpt = first_part(news1_sentences[0].split(" "), news2_lines[0].split(" "))
    mid_pt = news1_sentences[1:-5] if len(news1_sentences) > 5 else []
    lst_pt = ". ".join(news1_sentences[-5:-1]) if len(news1_sentences) > 5 else ""
    
    refined_fpt = [fpt] if fpt else []
    refined_lst = last_part(lst_pt) if lst_pt else []
    
    refined_fpt.extend(mid_pt)
    refined_fpt.extend(refined_lst)
    refined_news =  ". ".join(refined_fpt)
    pprocess_news = text_preprocessing(refined_news)
    return pprocess_news

