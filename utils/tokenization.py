import torch
from transformers import DistilBertTokenizer

# Initialize the tokenizer for DistilBERT from a specific path
tokenizer = DistilBertTokenizer.from_pretrained(r'C:\Users\raiom.LAPTOP-59QT21KS\FakeNews\utils\models\tokenizer')
    
def sliding_window_tokenization(text, tokenizer, max_length=512, stride=128):
    # Tokenizes the text into chunks with sliding window mechanism to handle long texts
    encoded_chunks = tokenizer(
        text,
        max_length=max_length,             # Set max token length for each chunk
        truncation=True,                    # Truncate text if it exceeds max_length
        stride=stride,                      # Define stride (how much overlap there is between chunks)
        return_overflowing_tokens=True,     # Return additional tokens that overflow max_length
        return_tensors="pt",                # Return as PyTorch tensors
        return_attention_mask=True,         # Return attention mask for model input
        padding='max_length'                # Pad each chunk to max_length
    )
    
    return encoded_chunks


def tokenize(texts, input_ids_texts, attention_masks_texts):
    """
    Tokenizes a list of texts and appends their input_ids and attention_masks to the respective lists.
    
    texts: list of input texts to be tokenized
    input_ids_texts: list to append input_ids tensors to
    attention_masks_texts: list to append attention masks tensors to
    """
    
    # Iterate through each text in the input list
    for i, text in enumerate(texts):
        # Tokenize the current text using the sliding window method
        encoded_chunks = sliding_window_tokenization(text, tokenizer)
        
        # Calculate number of chunks for this text (useful for debugging or analysis)
        num_chunks = len(encoded_chunks['input_ids'])
        
        # Append the input_ids and attention_masks from the tokenized chunks
        input_ids_texts.append(encoded_chunks['input_ids'])
        attention_masks_texts.append(encoded_chunks['attention_mask'])
     
    # Concatenate the input_ids and attention_masks along the batch dimension (dim=0)
    input_ids_texts = torch.cat(input_ids_texts, dim=0)
    attention_masks_texts = torch.cat(attention_masks_texts, dim=0)
    
    # Return the concatenated input_ids and attention_masks tensors
    return input_ids_texts, attention_masks_texts
