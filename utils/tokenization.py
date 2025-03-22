import torch
from transformers import DistilBertTokenizer

tokenizer = DistilBertTokenizer.from_pretrained(r'C:\Users\raiom.LAPTOP-59QT21KS\FakeNews\utils\models\tokenizer')

# def text_processing():
    
def sliding_window_tokenization(text, tokenizer, max_length=512, stride=128):
    encoded_chunks = tokenizer(
        text,
        max_length=max_length,
        truncation=True,
        stride=stride,
        return_overflowing_tokens=True,
        return_tensors="pt",
        return_attention_mask = True,
        padding='max_length'
    )
    
    return encoded_chunks


def tokenize(texts, input_ids_texts, attention_masks_texts):
    for i, text in enumerate(texts):
        encoded_chunks = sliding_window_tokenization(text, tokenizer)
        
        num_chunks = len(encoded_chunks['input_ids'])
        
        input_ids_texts.append(encoded_chunks['input_ids'])
        attention_masks_texts.append(encoded_chunks['attention_mask'])
        
        # replicated_titles.extend([input_ids_titles[i]] * num_chunks)
        # replicated_masks.extend([attention_masks_titles[i]] * num_chunks)
     
    input_ids_texts = torch.cat(input_ids_texts, dim=0)
    attention_masks_texts = torch.cat(attention_masks_texts, dim=0)
    return input_ids_texts, attention_masks_texts
