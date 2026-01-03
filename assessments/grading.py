from .models import Submission, Answer, Question
from django.utils import timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class GradingService:
    @staticmethod
    def grade_submission(submission_id):
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
                    score, feedback = GradingService._grade_descriptive(answer, question)
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
        correct_answer = question.correct_option.strip().upper()

        if student_answer == correct_answer:
            return float(question.marks), 'Correct answer!'
        else:
            return 0.0, f'Incorrect. Correct answer is {correct_answer}'
        
    @staticmethod
    def _grade_descriptive(answer, question):

        if not question.models_answer or not answer.answer_text:
            return 0.0, 'No answer provided'
        
        student_answer = answer.answer_text.lower().strip()
        model_answer = question.models_answer.lower().strip()


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

    @staticmethod
    def _calculate_keyword_score(text, keywords):

        if not keywords:
            return 0.5
        
        # Convert string to list if needed
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        if not keywords:
            return 0.5
        
        text = text.lower()
        found_keywords = sum(1 for keyword in keywords if keyword.lower() in text)
        return found_keywords / len(keywords) if keywords else 0
        

    @staticmethod
    def _calculate_similarity(text1, text2):
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            return 0.0
            
    @staticmethod
    def _generate_feedback(score, max_score, keyword_score, similarity_score):

        percentage = (score/max_score)*100 if max_score > 0 else 0


        if percentage >= 80:
            quality = "Excellent"

        elif percentage >= 60:
            quality = "Good"
        elif percentage >= 40:
            quality = "Fair"
        else:
            quality = "Needs improvement"

        feedback = f"{quality} answer. "
        feedback += f"Keyword coverage: {keyword_score*100:.0f}%. "
        feedback += f"Content similarity: {similarity_score*100:.0f}%."

        return feedback