from rest_framework import serializers
from .models import Exam, Question, Submission,Answer
from django.contrib.auth.models import User



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'marks', 'order',
                  'option_a', 'option_b', 'option_c', 'option_d']
        

class ExamListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'duration', 'total_marks',
                  'description', 'question_count', 'created_at']
    def get_question_count(self, obj):
        return obj.questions.count()
    
class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'duration', 'description',
                  'total_marks', 'passing_marks', 'questions', 'created_at']
    

class AnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField()

class SubmissionCreateSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    answers = AnswerSubmissionSerializer(many=True)

    def validate_exam_id(self, value):
        try:
            exam = Exam.objects.get(id=value, is_active=True)
        except Exam.DoesNotExist:
            raise serializers.ValidationError('Exam not found or inactive')
        return value
    
    def validate(self, data):
        exam_id = data['exam_id']
        answers = data['answers']

        exam_questions = Question.objects.filter(exam_id=exam_id).values_list('id', flat=True)
        answered_questions = [ans['question_id'] for ans in answers]

        if set(exam_questions) != set(answered_questions):
            raise serializers.ValidationError('All Questions must be answered')
        
        return data


class AnswerDetailSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question_marks = serializers.DecimalField(source='question.marks', max_digits=5,
                                              decimal_places=2, read_only=True)
    
    class Meta:
        model = Answer
        fields = ['id', 'question_text', 'question_marks', 'answer_text', 'score', 'feedback']


        class Meta:
            model = Submission
            fields = ['id', 'exam_title', 'student_name', 'status', 'score',
                      'feedback', 'started_at', 'graded_at', 'answers']