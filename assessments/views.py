from urllib import request
from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# from django.db import timezone
from .models import Exam, Question, Submission, Answer
from .serializers import (ExamListSerializer, ExamDetailSerializer,
                          SubmissionCreateSerializer, SubmissionDetailSerializer,
                          AnswerDetailSerializer
                          )
from .permissions import IsOwnerOrReadOnly
from .grading import GradingService



class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Exam.objects.filter(is_active=True).prefetch_related('questions')


    def get_serializer_class(self):
        if self.action == 'list':
            return ExamListSerializer
        return ExamDetailSerializer


class SubmissionViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = SubmissionDetailSerializer

    def get_queryset(self):
        # Handle swagger schema generation with anonymous user
        if getattr(self, 'swagger_fake_view', False):
            return Submission.objects.none()
        
        if self.request.user.is_staff:
            return Submission.objects.all().select_related('exam', 'student').prefetch_related('answers__question')
        return Submission.objects.filter(student=self.request.user).select_related('exam').prefetch_related('answers__question')
    
    

        
        
    def create(self, request):

        serializer = SubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        exam_id = serializer.validated_data['exam_id']
        answers_data = serializer.validated_data['answers']

        if Submission.objects.filter(student=request.user, exam_id=exam_id).exists():
            return Response(
                {"error": "You have already submitted this exam"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            submission = Submission.objects.create(
                student=request.user,
                exam_id=exam_id,
                submitted_at=timezone.now(),
                status='PENDING'
            )

            answer_objects = [
                Answer(
                    submission=submission,
                    question_id=ans['question_id'],
                    answer_text=ans['answer_text']
                )
                for ans in answers_data
            ]
            Answer.objects.bulk_create(answer_objects)

        try:
            GradingService.grade_submission(submission.id)
        except Exception as e:
            submission.status = 'FAILED'
            submission.feedback = f"Grading error: {str(e)}"
            submission.save()

        submission.refresh_from_db()
        result_serializer = SubmissionDetailSerializer(submission)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)