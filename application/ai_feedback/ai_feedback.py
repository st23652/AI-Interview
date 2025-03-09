import openai
from textblob import TextBlob
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

class AIInterviewScorer:
    def __init__(self, job_role):
        self.job_role = job_role
        self.criteria_weights = {
            "content_quality": 0.4,  
            "fluency": 0.2,  
            "confidence": 0.2,  
            "technical_depth": 0.2  
        }

    def analyze_response(self, candidate_response):
        """ Uses GPT-4 to analyze response relevance and structure """
        prompt = f"Evaluate this interview response for a {self.job_role} role:\n\n{candidate_response}\n\nScore it on:\n1. Content Quality (0-10)\n2. Fluency (0-10)\n3. Technical Depth (0-10)\nProvide a short explanation for each."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response["choices"][0]["message"]["content"]

    def analyze_sentiment(self, text):
        """ Uses TextBlob for sentiment analysis (can be replaced with IBM Watson) """
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity  # -1 (negative) to 1 (positive)
        return max(0, min(10, (sentiment_score + 1) * 5))  # Normalize to 0-10 scale

    def calculate_final_score(self, scores):
        """ Compute weighted average score """
        final_score = sum(scores[criteria] * weight for criteria, weight in self.criteria_weights.items())
        return round(final_score, 2)

    def generate_feedback(self, candidate_response):
        """ Main function to evaluate response, calculate scores, and provide feedback """
        ai_analysis = self.analyze_response(candidate_response)
        
        # Extract scores (simulated parsing, can improve extraction logic)
        scores = {
            "content_quality": int(ai_analysis.split("\n")[0].split(":")[-1].strip()),
            "fluency": int(ai_analysis.split("\n")[1].split(":")[-1].strip()),
            "technical_depth": int(ai_analysis.split("\n")[2].split(":")[-1].strip()),
            "confidence": self.analyze_sentiment(candidate_response)  # Sentiment used as proxy
        }

        final_score = self.calculate_final_score(scores)
        feedback = f"Final Score: {final_score}/10\n\nDetailed Feedback:\n{ai_analysis}"

        return {"score": final_score, "feedback": feedback}
