import re

def refine_news(b_news, n_news):
    b_list = re.split(r'[.!?]\s*', b_news.strip())
    n_list = re.split(r'[.!?]\s*', n_news.strip())
    b_fst = b_list[0]
    n_fst = n_list[0]
    return(b_fst, n_fst)