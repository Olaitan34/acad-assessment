from .models import Submission, Answer, Question
from django.utils import timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class GradingService:
    @staticmethod
    def grade_sumbission(submission_id):
        try:
            submission = Submission.objects.select_related('exam').prefetch_related(
                'answers__question'
            ).get(id=submission_id)

            total_score = 0
            feedback_parts = []

            for answer in submission.answers.all():
                question = answer.question

                if question.question_type == 'MCQ':
                    score, feedback = GradingService._grade_mcq(answer, question)
                elif question.question_type in ['SHORT', 'ESSAY']:
                    score, feedback = GradingService._grade_descrptive(answer, question)
                else:
                    score, feedback = 0, 'Unknown question type.'

                answer.score = score
                answer.feedback = feedback
                answer.save()

                total_score += score
                feedback_parts.append(f"Q{question.order}: {feedback}")

            submission.score = total_score
            submission.status = 'GRADED'
            submission.graded_at = timezone.now()
            submission.feedback = "\n".join(feedback_parts)
            submission.save()
            return submission
        except Exception as e:
            submission.status = 'FAILED'
            submission.feedback = f'Grading failed: {str(e)}'
            submission.save()
            raise


    @staticmethod
    def _grade_mcq(answer, question):

        student_answer = answer.answer_text.strip().upper()
        correct_answer = question.correct_answer.strip().upper()

        if student_answer == correct_answer:
            return float(question.marks), 'correct answer!'
        else:
            return 0.0, f'Incorrect. Correct answer is {correct_answer}'
        
    @staticmethod
    def _grade_descrptive(answer, question):

        if not question.model_answer or not answer.answer_text:
            return 0.0, 'No answer provided'
        
        student_answer = answer.answer_text.lower().strip()
        model_answer = question.model_answer.lower().strip()


        keyword_score = GradingService._calculate_keyword_score(
            student_answer, question.expected_keywords
        )
        
        # 2. Cosine Similarity (60% weight)
        similarity_score = GradingService._calculate_similarity(
            student_answer, model_answer
        )
        
        # Combined score
        final_score = (0.4 * keyword_score + 0.6 * similarity_score) * float(question.marks)
        
        # Generate feedback
        feedback = GradingService._generate_feedback(
            final_score, float(question.marks), keyword_score, similarity_score
        )
        
        return round(final_score, 2), feedback