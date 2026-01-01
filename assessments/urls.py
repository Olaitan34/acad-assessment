from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, SubmissionViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'submissions', SubmissionViewSet, basename='submission')

app_name = 'assessments'

urlpatterns = [
    path('', include(router.urls)),
]