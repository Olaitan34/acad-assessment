# Mini Assessment Engine

A Django-based REST API for managing online assessments with automated grading capabilities.

## Project Overview

This project implements a complete assessment platform that allows students to take exams and receive immediate automated feedback. The system handles three types of questions - multiple choice, short answer, and essay - with a grading algorithm that evaluates student responses without requiring manual intervention.

## Tech Stack

- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - API toolkit
- **SQLite** - Database (easily replaceable with PostgreSQL/MySQL)
- **drf-yasg** - Swagger/OpenAPI documentation
- **scikit-learn** - Text processing and similarity calculations
- **Token Authentication** - API security

## Project Structure
```
acad_ai_backend/
├── acad_ai_backend/          # Project settings and configuration
│   ├── settings.py           # Django settings
│   └── urls.py               # Main URL routing
├── assessments/              # Main application
│   ├── models.py             # Database models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API views
│   ├── grading.py            # Grading logic
│   ├── permissions.py        # Custom permissions
│   ├── urls.py               # App-specific routing
│   └── management/           
│       └── commands/
│           └── seed_data.py  # Test data generation
├── manage.py
└── requirements.txt
```

## Setup Instructions

### 1. Clone and Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Load Test Data
```bash
python manage.py seed_data
```

This creates three sample exams with various question types and three test student accounts (student1, student2, student3 - all with password: testpass123).

### 5. Run Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

## API Documentation

Interactive API documentation is available at:
- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`

See `API_DOCUMENTATION.md` for detailed endpoint descriptions and usage examples.

## Database Schema

### Core Models

**Exam**
- Stores exam metadata (title, course, duration, marks)
- Links to multiple questions
- Tracks active/inactive status

**Question**
- Belongs to an exam
- Supports three types: MCQ, SHORT, ESSAY
- Stores correct answers and grading criteria
- Maintains question order

**Submission**
- Links student to exam
- Tracks submission status and timestamps
- Stores final score and feedback
- Enforces one submission per student per exam

**Answer**
- Individual answer for each question
- Stores student's response
- Contains score and feedback per question

### Key Design Decisions

I used `unique_together` constraints to prevent duplicate submissions and answers. Database indexes were added on frequently queried fields like student ID and exam ID to improve performance when retrieving results.

The relationship between models follows Django best practices - foreign keys with appropriate `on_delete` behaviors and meaningful `related_name` attributes for reverse lookups.

## Grading System

### Why I Chose a Mock Grading Service

After reviewing the assessment requirements, I decided to implement a custom grading algorithm rather than integrate an external LLM. Here's my reasoning:

**1. Bonus Points Consideration**
The assignment explicitly mentions bonus points for building a mock grading service from scratch. This suggested that demonstrating algorithmic thinking was valued over simply making API calls to existing services.

**2. Cost and Reliability**
Using external LLM APIs would introduce costs and dependency on third-party services. A mock grader runs entirely locally, makes the system more reliable, and keeps it free to operate.

**3. Learning and Demonstration**
Building the grading logic myself allowed me to demonstrate understanding of natural language processing concepts, text similarity algorithms, and automated evaluation techniques.

**4. Performance**
The mock grader processes submissions instantly without network latency. Responses typically complete in under a second even for exams with multiple essay questions.

### How the Grading Algorithm Works

The grading system uses different approaches based on question type:

#### Multiple Choice Questions (MCQ)
These are straightforward - the system compares the student's answer against the stored correct option. If they match, full marks are awarded. If not, zero marks.

#### Short Answer and Essay Questions
These use a more sophisticated approach combining two techniques:

**Keyword Matching (40% weight)**
The system checks how many expected keywords appear in the student's answer. For example, if a question about Python dictionaries expects keywords like "key-value", "mutable", "mapping", and "unordered", it counts how many the student mentioned.

The keyword score is calculated as:
```
keyword_score = (found_keywords / total_expected_keywords)
```

**Semantic Similarity (60% weight)**
This is where it gets interesting. I used TF-IDF (Term Frequency-Inverse Document Frequency) vectorization combined with cosine similarity to measure how close the student's answer is to the model answer in meaning, not just exact words.

Here's the process:
1. Convert both the student answer and model answer into TF-IDF vectors
2. Calculate cosine similarity between the vectors (ranges from 0 to 1)
3. A score closer to 1 means the answers are semantically similar

**Final Score Calculation**
```
final_score = (0.4 × keyword_score + 0.6 × similarity_score) × question_marks
```

I weighted similarity higher because it's more important that students understand the concept than that they use specific terminology. However, keyword matching ensures they're at least covering the right topics.

### Example Grading Scenario

Question: "Explain what a Python dictionary is"
Model Answer: "A dictionary is a mutable, unordered collection of key-value pairs in Python"
Expected Keywords: ["key-value", "mutable", "collection", "unordered"]

Student Answer A: "A dictionary stores key-value pairs and is mutable"
- Keywords found: 2/4 = 50%
- Similarity: ~75%
- Final: (0.4 × 0.5 + 0.6 × 0.75) = 65% of marks

Student Answer B: "It's a data structure with keys and values that you can change"
- Keywords found: 1/4 = 25% (only "values" detected, "key-value" as phrase not found)
- Similarity: ~60%
- Final: (0.4 × 0.25 + 0.6 × 0.6) = 46% of marks

### Why This Approach Works

The combination of keyword matching and semantic similarity creates a balanced grading system. It rewards students who understand the concepts even if they phrase things differently, while still ensuring they cover the essential points.

The weights (40/60) were chosen after some experimentation. Pure keyword matching was too strict - students could understand a concept but phrase it differently and get penalized. Pure similarity was too lenient - students could write vaguely related content and score well. The current balance seems to work well for typical academic assessments.

### Limitations and Future Improvements

I'm aware this approach has limitations:

1. It doesn't understand context or reasoning chains like an LLM would
2. Keyword matching is somewhat naive - it doesn't handle synonyms automatically
3. The algorithm can't detect factual errors if they're phrased similarly to correct answers

For a production system, I would consider:
- Adding more sophisticated NLP preprocessing (lemmatization, synonym handling)
- Implementing a hybrid approach where complex questions use LLM evaluation
- Creating a feedback mechanism where instructors can adjust grading parameters
- Possibly using sentence transformers for better semantic understanding

## Security Considerations

**Authentication**
The API uses Django REST Framework's token authentication. Tokens are generated on registration/login and must be included in request headers for protected endpoints.

**Authorization**
Students can only view and submit their own exams. The system enforces this through custom permissions that check ownership before allowing access to submission data.

**Data Validation**
All inputs are validated at the serializer level before reaching the database. This includes checking for required fields, correct data types, and business logic constraints (like ensuring all questions are answered).

**No Answer Exposure**
Correct answers for MCQ questions and model answers for descriptive questions are never exposed through the API. Only admin users can see this information through the Django admin interface.

## Performance Optimizations

I paid attention to database efficiency since result retrieval was specifically mentioned in the assessment criteria:

**Query Optimization**
- Used `select_related()` for foreign key relationships (exam, student) to prevent N+1 queries
- Used `prefetch_related()` for reverse relationships (questions, answers)
- Added database indexes on frequently queried fields

**Example from submissions viewset:**
```python
Submission.objects.filter(
    student=self.request.user
).select_related('exam').prefetch_related('answers__question')
```

This retrieves a submission with all its answers and related questions in just 3 queries instead of potentially dozens.

**Pagination**
All list endpoints return paginated results (10 items per page by default) to keep response sizes manageable and response times fast.

## Testing

The `seed_data` management command creates realistic test data:
- 3 complete exams (Python, Web Development, Data Structures)
- Mix of MCQ, SHORT, and ESSAY questions
- Expected keywords and model answers for automated grading
- 3 test student accounts

This makes it easy to test the entire flow without manually creating data.

## API Versioning

The API uses URL-based versioning (`/api/v1/`). This approach was chosen because:
- It's explicit and easy to understand
- Allows running multiple API versions simultaneously
- Makes it clear to clients which version they're using
- Follows REST API best practices

Future versions can be added at `/api/v2/` without breaking existing clients.

## What I Learned

This project helped me understand several important concepts:

**Database Design**
Thinking through relationships between entities and using constraints like `unique_together` to enforce business rules at the database level.

**API Design**
Structuring endpoints logically, handling errors gracefully, and providing clear feedback to API consumers.

**Text Processing**
Working with scikit-learn for text similarity was interesting. I learned about TF-IDF vectorization and how cosine similarity can measure semantic closeness.

**Django Best Practices**
Proper use of serializers, viewsets, permissions, and Django's ORM features like `select_related()` and `prefetch_related()`.

## Potential Enhancements

Given more time, I would add:

1. **Detailed Analytics** - Tracking average scores, question difficulty, time taken per question
2. **Question Bank** - Reusable questions across multiple exams
3. **Randomization** - Different question orders for different students
4. **Time Tracking** - Enforcing exam duration and preventing submissions after time expires
5. **Partial Submissions** - Allowing students to save progress and return later
6. **Rich Text Support** - Enabling formatted text, images, and code snippets in questions/answers
7. **LLM Integration** - Optional high-stakes grading using Claude/GPT for complex essays
8. **Plagiarism Detection** - Comparing submissions to detect copying

## Conclusion

This project demonstrates a complete assessment system with automated grading. The mock grading algorithm uses established NLP techniques to evaluate student responses without external dependencies. The API is documented, secured, and optimized for performance.

I focused on building something that works well, is easy to test, and demonstrates understanding of backend development principles rather than just connecting to external services.

---

**Author:** [Your Name]  
**Date:** January 2026  
**For:** Acad AI Backend Assessment