from rest_framework import serializers # Correct import for ModelSerializer

# Correctly import the models that actually exist.
from .models import (
    CustomUser, 
    Profile, 
    Job, 
    JobApplication, # Correct name
    Interview, 
    InterviewQuestion, 
    AssessmentQuestion # Correct name
)


class CustomUserSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = Profile
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = Job
        fields = '__all__'

# Corrected serializer for JobApplication
class JobApplicationSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = JobApplication # Use correct model
        fields = '__all__'

class InterviewSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = Interview
        fields = '__all__'

# This serializer can now be used for InterviewQuestion
class InterviewQuestionSerializer(serializers.ModelSerializer): # Use ModelSerializer
    class Meta:
        model = InterviewQuestion
        fields = '__all__'