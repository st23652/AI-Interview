from django.shortcuts import render
from watson_integration.services import WatsonEmotionService
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import generate_interview_question

class AIQuestionView(APIView):
    def post(self, request, *args, **kwargs):
        question_data = generate_interview_question(request.data)
        return Response(question_data)

api_key = 'eQMBQiD41BXLLWAxJ600v4R1oKukf_yBGZSGTP5f1aCu'
url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/3c90b344-3d52-4531-9cc3-87c8655a8375'

watson_service = WatsonEmotionService(api_key, url)

def handle_interview_answer(request, interview_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        
        # Analyze the emotion in the answer
        emotions = watson_service.analyze_emotion(answer)
        
        # Store or process the emotions as needed
        # For example, add them to the interview feedback
        
        return render(request, 'interview_next_question.html', {'emotions': emotions})
