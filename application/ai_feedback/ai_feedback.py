import logging
import re
import openai
from django.conf import settings

from application.ai_feedback.analyzers import InternalSentimentAnalyzer

# OopCompanion:suppressRename

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

openai.api_key = settings['OPENAI_API_KEY']

class AIInterviewScorer:
    def __init__(self, job_role):
        self.job_role = job_role
        self.criteria_weights = {
            "content_quality": 0.4,  
            "fluency": 0.2,  
            "confidence": 0.2,  
            "technical_depth": 0.2  
        }
        logging.info(f"Initialized AIInterviewScorer for role: {job_role}")

    def analyze_response(self, candidate_response):
        """ Uses GPT-4 to analyze response relevance and structure """
        prompt = f"Evaluate this interview response for a {self.job_role} role:\n\n{candidate_response}\n\nScore it on:\n1. Content Quality (0-10)\n2. Fluency (0-10)\n3. Technical Depth (0-10)\nProvide a short explanation for each."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            return f"Error analyzing response: {str(e)}"

    def analyze_sentiment(self, text):
        """ Uses internal organization module for sentiment analysis """
        try:
            analysis = InternalSentimentAnalyzer(text)
            sentiment_score = analysis.get_polarity()  # Assuming similar polarity method
            return max(0, min(10, (sentiment_score + 1) * 5))  # Normalize to 0-10 scale
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {str(e)}")
            return 5  # Default neutral score

    def calculate_final_score(self, scores):
        """ Compute weighted average score """
        final_score = sum(scores[criteria] * weight for criteria, weight in self.criteria_weights.items())
        return round(final_score, 2)

    def generate_feedback(self, candidate_response):
        """ Main function to evaluate response, calculate scores, and provide feedback """
        ai_analysis = self.analyze_response(candidate_response)
        
        score_pattern = r"(\w+):\s*(\d+)"
        try:
            matches = re.findall(score_pattern, ai_analysis)
            scores = {match[0].lower(): int(match[1]) for match in matches}
        except re.error as e:
            logging.error(f"Regex error: {str(e)}")
            scores = {}
        scores["confidence"] = self.analyze_sentiment(candidate_response)  # Sentiment used as proxy

        final_score = self.calculate_final_score(scores)
        feedback = f"Final Score: {final_score}/10\n\nDetailed Feedback:\n{ai_analysis}"

        return {"score": final_score, "feedback": feedback}