from fastapi import FastAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from models import Tweet

app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

@app.get("/")
def root():
    return {"message": "Backend is running!"}

@app.post("/analyze")
def analyze_sentiment(tweet: Tweet):
    scores = analyzer.polarity_scores(tweet.text)
    # Example: {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.8}

    sentiment = "neutral"
    if scores["compound"] >= 0.05:
        sentiment = "positive"
    elif scores["compound"] <= -0.05:
        sentiment = "negative"

    return {
        "text": tweet.text,
        "sentiment": sentiment,
        "scores": scores
    }
