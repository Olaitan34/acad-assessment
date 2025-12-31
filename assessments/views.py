from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import timezone
from .models import Exam, Question, Submission, Answer
from .serializers import (ExamListSerializer, ExamDetailSerializer,
                          SubmissionCreationSerializer, AnswerDetailSerializer
                          )
from .permissions import IsOwnerOrReadOnly
from .grading import GradingService

