import pickle, torch
from utils.tokenization import tokenize
from transformers import DistilBertTokenizer

# Initialize the tokenizer for DistilBERT from a specific path
tokenizer = DistilBertTokenizer.from_pretrained(
    r"C:\Users\raiom.LAPTOP-59QT21KS\FakeNews\utils\models\tokenizer"
)


# Load trained language identification model
def language_id(refined_article):
    with open("utils/vectors/tfidf_vectorizer.pkl", "rb") as vec_file:
        tfidf_vectorizer = pickle.load(vec_file)
        # Vectorize the article using the TF-IDF vectorizer for language prediction
        article_vector = tfidf_vectorizer.transform([refined_article])

    with open("utils/models/langid_model.pkl", "rb") as lang_id:
        model_langid = pickle.load(lang_id)
        lang_prediction = model_langid.predict(article_vector)[0]
    return lang_prediction


# Load trained fake news detection model
def news_pred(refined_article):
    # Check for available device: use GPU if available, else CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    with open("utils/models/fakenews_detection.pkl", "rb") as news_id:
        model_newsid = pickle.load(news_id)
        # Ensure config is set to return attentions and use eager implementation
        model_newsid.config.output_attentions = True
        model_newsid.config.attn_implementation = "eager"
        # Move model to the appropriate device (CPU/GPU)
        model_newsid.to(device)
        model_newsid.eval()
        # Tokenize the article for DistilBERT
        input_ids_texts, attention_masks_texts = tokenize([refined_article], [], [])
        input_tensor = input_ids_texts.clone().detach().to(device)
        attention_tensor = attention_masks_texts.clone().detach().to(device)

        # Make prediction using the fake news detection model
        with torch.no_grad():
            outputs = model_newsid(input_tensor, attention_mask=attention_tensor)
            logits = outputs.logits
            attentions = outputs.attentions
            news_prediction = torch.argmax(logits, dim=1).item()
    # Average attention: last layer, all heads, from [CLS]
    last_layer_attention = attentions[-1][0]  # shape: (heads, seq_len, seq_len)
    cls_attention = last_layer_attention[:, 0, :]  # (heads, seq_len)
    mean_cls_attention = cls_attention.mean(dim=0).cpu().numpy()  # (seq_len,)

    tokens = tokenizer.convert_ids_to_tokens(input_ids_texts[0])
    # Filter out special and subword tokens, but keep original index
    filtered_token_info = [
        (i, token)
        for i, token in enumerate(tokens)
        if token not in ["[PAD]", "[CLS]", "[SEP]"] and not token.startswith("##")
    ]
    top_n = 10
    # Get (index, token) pairs sorted by attention
    token_attention_pairs = list(enumerate(filtered_token_info))
    top_indices = sorted(
        filtered_token_info, key=lambda x: mean_cls_attention[x[0]], reverse=True
    )[:top_n]
    # Extract top tokens only
    top_tokens = [tokens[i] for i, _ in top_indices]

    return news_prediction, top_tokens, mean_cls_attention
