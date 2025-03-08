# serializers.py
import rest_framework
from django.contrib.postgres import serializers

from .models import Profile, Job, Application, Interview, Question, InterviewQuestion
from .models import CustomUser

class CustomUserSerializer(serializers.BaseSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(serializers.BaseSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class JobSerializer(serializers.BaseSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.BaseSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class InterviewSerializer(serializers.BaseSerializer):
    class Meta:
        model = Interview
        fields = '__all__'

class QuestionSerializer(serializers.BaseSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class InterviewQuestionSerializer(serializers.BaseSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'
