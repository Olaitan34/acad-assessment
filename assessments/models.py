from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Exam(models.Model):
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    duration =models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    passing_marks = models.DecimalField(max_digits=5, decimal_places=2, default=40)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', 'is_active']),
        ]

        def __str__(self):
            return f"{self.title} - {self.course}"


class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('SHORT', 'Short Answer'),
        ('ESSAY', 'Essay')
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    order = models.IntegerField(default=0)

    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_option = models.CharField(max_length=1, blank=True)


    expected_keywords = models.TextField(default=list, blank=True)
    models_answer = models.TextField(blank=True)

    class Meta:
        ordering = ['exam', 'order']
        indexes = [
            models.Index(fields=['exam', 'order']),
        ]
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.order}"
    

class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Grading'),
        ('GRADED', 'Graded'),
        ('FAILED', 'Grading Failed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True )
    feedback = models.TextField(blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'exam'], name='unique_student_exam')
        ]
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['exam', 'status']),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"
    

class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
     

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['submission', 'question'], name='unique_submission_question')
        ]
        indexes = [
            models.Index(fields=['submission', 'question'])
        ]

    def __str__(self):
        return f'{self.submission} - Q{self.question.order}'
