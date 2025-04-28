from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import emoji
import re

# Load model and tokenizer
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']

def preprocess(text):
    text = emoji.demojize(text)
    print(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    return text

def analyze_sentiment(text):
    text = preprocess(text)
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    scores = torch.nn.functional.softmax(logits, dim=1)[0]
    sentiment = labels[scores.argmax().item()]
    return sentiment
