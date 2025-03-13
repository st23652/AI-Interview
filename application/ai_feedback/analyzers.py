from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class InternalSentimentAnalyzer:
    def __init__(self, method="vader"):
        """
        Initialize the Sentiment Analyzer.

        :param method: "vader" for VADER (default), "textblob" for TextBlob.
        """
        self.method = method
        self.vader_analyzer = SentimentIntensityAnalyzer() if method == "vader" else None

    def analyze(self, text):
        """
        Analyze sentiment of the given text.

        :param text: Input text (string).
        :return: Dictionary with sentiment score and category.
        """
        if not text or not isinstance(text, str):
            return {"score": 0, "sentiment": "Neutral"}

        if self.method == "vader":
            return self._analyze_vader(text)
        else:
            return self._analyze_textblob(text)

    def _analyze_vader(self, text):
        """
        Use VADER to analyze sentiment.

        :param text: Input text.
        :return: Sentiment analysis result.
        """
        sentiment_score = self.vader_analyzer.polarity_scores(text)["compound"]
        sentiment_category = self._get_sentiment_category(sentiment_score)
        return {"score": sentiment_score, "sentiment": sentiment_category}

    def _analyze_textblob(self, text):
        """
        Use TextBlob to analyze sentiment.

        :param text: Input text.
        :return: Sentiment analysis result.
        """
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity
        sentiment_category = self._get_sentiment_category(sentiment_score)
        return {"score": sentiment_score, "sentiment": sentiment_category}

    def _get_sentiment_category(self, score):
        """
        Convert sentiment score to category.

        :param score: Sentiment score.
        :return: "Positive", "Negative", or "Neutral".
        """
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        return "Neutral"
