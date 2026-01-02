# Mini Assessment Engine - API Documentation

## Overview

This documentation covers the REST API endpoints for the Mini Assessment Engine. The API handles student authentication, exam management, and automated grading of submissions.

**Base URL:** `http://localhost:8000`

**API Version:** v1

**Interactive Documentation:** `http://localhost:8000/api/docs/`

---

## Authentication

The API uses Token Authentication. After registering or logging in, you'll receive a token that must be included in the Authorization header for protected endpoints.

**Header Format:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Testing with Swagger UI

I've set up Swagger UI to make testing easier. You can access it at `http://localhost:8000/api/docs/` where you'll find an interactive interface for all endpoints.

### Getting Started with Swagger

1. Navigate to `http://localhost:8000/api/docs/`
2. Look for the green "Authorize" button at the top right
3. After logging in or registering (see endpoints below), copy your token
4. Click "Authorize" and enter: `Token your_token_here`
5. Now you can test all protected endpoints

---

## API Endpoints

### Authentication Endpoints

#### 1. User Registration

Creates a new user account and returns an authentication token.

**Endpoint:** `POST /api/v1/auth/register/`

**Authentication Required:** No

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Field Requirements:**
- `username`: Required, unique, alphanumeric with underscores
- `password`: Required, minimum 8 characters
- `password2`: Must match password exactly
- `email`: Required, valid email format
- `first_name`: Required
- `last_name`: Required

**Success Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "password": ["Password fields didn't match."]
}
```

**Testing in Swagger:**
1. Expand the `POST /api/v1/auth/register/` endpoint
2. Click "Try it out"
3. Fill in the request body with your details
4. Click "Execute"
5. Copy the token from the response

---

#### 2. User Login

Authenticates an existing user and returns their token.

**Endpoint:** `POST /api/v1/auth/login/`

**Authentication Required:** No

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Success Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

#### 3. Get User Profile

Returns the authenticated user's profile information.

**Endpoint:** `GET /api/v1/auth/profile/`

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

#### 4. Logout

Invalidates the user's authentication token.

**Endpoint:** `POST /api/v1/auth/logout/`

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### Exam Endpoints

#### 5. List All Exams

Retrieves a paginated list of all active exams. This endpoint is public and doesn't require authentication.

**Endpoint:** `GET /api/v1/assessments/exams/`

**Authentication Required:** No

**Query Parameters:**
- `page` (optional): Page number, default is 1
- `page_size` (optional): Items per page, default is 10

**Example Request:**
```
GET /api/v1/assessments/exams/?page=1&page_size=10
```

**Success Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python Basics Assessment",
      "course": "CS101 - Introduction to Programming",
      "duration": 60,
      "total_marks": 100.00,
      "description": "Test your understanding of Python fundamentals",
      "question_count": 7,
      "created_at": "2026-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Web Development Fundamentals",
      "course": "CS201 - Web Technologies",
      "duration": 90,
      "total_marks": 100.00,
      "description": "Assessment covering HTML, CSS, and JavaScript",
      "question_count": 5,
      "created_at": "2026-01-01T11:00:00Z"
    }
  ]
}
```

**Notes:**
- `duration` is in minutes
- `question_count` shows total questions in the exam
- Results are ordered by creation date (newest first)

**Testing in Swagger:**
1. Find `GET /api/v1/assessments/exams/`
2. Click "Try it out"
3. Optionally adjust page and page_size parameters
4. Click "Execute"

---

#### 6. Get Exam Details

Retrieves complete details of a specific exam including all questions.

**Endpoint:** `GET /api/v1/assessments/exams/{id}/`

**Authentication Required:** No

**Path Parameters:**
- `id`: The exam's unique identifier

**Example Request:**
```
GET /api/v1/assessments/exams/1/
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Python Basics Assessment",
  "course": "CS101 - Introduction to Programming",
  "duration": 60,
  "description": "Test your understanding of Python fundamentals",
  "total_marks": 100.00,
  "passing_marks": 40.00,
  "questions": [
    {
      "id": 1,
      "question_text": "What is the correct way to create a list in Python?",
      "question_type": "MCQ",
      "marks": 10.00,
      "order": 1,
      "option_a": "list = (1, 2, 3)",
      "option_b": "list = [1, 2, 3]",
      "option_c": "list = {1, 2, 3}",
      "option_d": "list = <1, 2, 3>"
    },
    {
      "id": 5,
      "question_text": "Explain what a Python dictionary is and provide one use case.",
      "question_type": "SHORT",
      "marks": 20.00,
      "order": 5,
      "option_a": "",
      "option_b": "",
      "option_c": "",
      "option_d": ""
    }
  ],
  "created_at": "2026-01-01T10:00:00Z"
}
```

**Question Types:**
- `MCQ`: Multiple choice question with four options (A, B, C, D)
- `SHORT`: Short answer question (paragraph response expected)
- `ESSAY`: Essay question (detailed response expected)

**Important Notes:**
- MCQ questions will have `option_a` through `option_d` populated
- SHORT and ESSAY questions will have empty option fields
- The correct answers are not exposed through this endpoint
- Questions are ordered by the `order` field

**Testing in Swagger:**
1. Find `GET /api/v1/assessments/exams/{id}/`
2. Click "Try it out"
3. Enter an exam ID (e.g., 1)
4. Click "Execute"

---

### Submission Endpoints

#### 7. Submit Exam Answers

Submits answers for an exam and triggers automatic grading. This is the main endpoint students will use to complete their exams.

**Endpoint:** `POST /api/v1/assessments/submissions/`

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body:**
```json
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer_text": "B"
    },
    {
      "question_id": 2,
      "answer_text": "C"
    },
    {
      "question_id": 5,
      "answer_text": "A Python dictionary is a mutable, unordered collection of key-value pairs. Each key must be unique and immutable. Dictionaries are commonly used for storing related data, such as user profiles where keys represent field names like 'name' and 'email', and values contain the actual data."
    }
  ]
}
```

**Request Rules:**
1. You must answer ALL questions in the exam
2. For MCQ questions, `answer_text` should be a single letter: A, B, C, or D
3. For SHORT and ESSAY questions, `answer_text` should be your complete written answer
4. Each student can only submit an exam once - no retakes allowed
5. The `question_id` must correspond to actual questions in the specified exam

**Success Response (201 Created):**
```json
{
  "id": 1,
  "exam_title": "Python Basics Assessment",
  "student_name": "john_doe",
  "status": "GRADED",
  "score": 85.50,
  "feedback": "Good understanding of Python fundamentals. Strong performance on multiple choice questions. Essay answers demonstrate clear comprehension of key concepts.",
  "started_at": "2026-01-02T10:00:00Z",
  "submitted_at": "2026-01-02T10:45:00Z",
  "graded_at": "2026-01-02T10:45:05Z",
  "answers": [
    {
      "id": 1,
      "question_text": "What is the correct way to create a list in Python?",
      "question_marks": 10.00,
      "answer_text": "B",
      "score": 10.00,
      "feedback": "Correct answer!"
    },
    {
      "id": 5,
      "question_text": "Explain what a Python dictionary is and provide one use case.",
      "question_marks": 20.00,
      "answer_text": "A Python dictionary is a mutable, unordered collection...",
      "score": 18.50,
      "feedback": "Excellent explanation. Keyword coverage: 83%. Content similarity: 92%."
    }
  ]
}
```

**Error Responses:**

Already submitted (400 Bad Request):
```json
{
  "error": "You have already submitted this exam"
}
```

Missing questions (400 Bad Request):
```json
{
  "non_field_errors": ["All questions must be answered"]
}
```

Invalid exam (400 Bad Request):
```json
{
  "exam_id": ["Exam not found or inactive"]
}
```

**About the Grading Process:**
- Grading happens immediately when you submit
- MCQ questions are graded by comparing with the stored correct answer
- SHORT and ESSAY questions use a weighted grading algorithm:
  - 40% based on keyword matching
  - 60% based on semantic similarity to the model answer
- Each answer receives individual feedback
- Overall feedback summarizes your performance

**Testing in Swagger:**
1. Make sure you're authorized (see Authentication section)
2. First, get exam details to see all question IDs
3. Find `POST /api/v1/assessments/submissions/`
4. Click "Try it out"
5. Fill in the request body with answers for ALL questions
6. Click "Execute"
7. Review your graded results

---

#### 8. List Your Submissions

Retrieves a paginated list of all submissions made by the authenticated user.

**Endpoint:** `GET /api/v1/assessments/submissions/`

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Query Parameters:**
- `page` (optional): Page number, default is 1
- `page_size` (optional): Items per page, default is 10
- `status` (optional): Filter by status (PENDING, GRADED, FAILED)

**Example Requests:**
```
GET /api/v1/assessments/submissions/
GET /api/v1/assessments/submissions/?status=GRADED
GET /api/v1/assessments/submissions/?page=2
```

**Success Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "exam_title": "Python Basics Assessment",
      "student_name": "john_doe",
      "status": "GRADED",
      "score": 85.50,
      "feedback": "Good understanding of Python fundamentals",
      "started_at": "2026-01-02T10:00:00Z",
      "submitted_at": "2026-01-02T10:45:00Z",
      "graded_at": "2026-01-02T10:45:05Z",
      "answers": []
    }
  ]
}
```

**Status Values:**
- `PENDING`: Submission is being processed (rare, as grading is nearly instant)
- `GRADED`: Submission has been graded successfully
- `FAILED`: An error occurred during grading

**Note:** The `answers` array is empty in list view for performance. Use the detail endpoint to see individual answers.

**Testing in Swagger:**
1. Ensure you're authorized
2. Find `GET /api/v1/assessments/submissions/`
3. Click "Try it out"
4. Optionally add filters
5. Click "Execute"

---

#### 9. Get Submission Details

Retrieves complete details of a specific submission including all answers and individual feedback.

**Endpoint:** `GET /api/v1/assessments/submissions/{id}/`

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Path Parameters:**
- `id`: The submission's unique identifier

**Example Request:**
```
GET /api/v1/assessments/submissions/1/
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "exam_title": "Python Basics Assessment",
  "student_name": "john_doe",
  "status": "GRADED",
  "score": 85.50,
  "feedback": "Good understanding of Python fundamentals. Strong performance on multiple choice questions. Essay answers demonstrate clear comprehension of key concepts.",
  "started_at": "2026-01-02T10:00:00Z",
  "submitted_at": "2026-01-02T10:45:00Z",
  "graded_at": "2026-01-02T10:45:05Z",
  "answers": [
    {
      "id": 1,
      "question_text": "What is the correct way to create a list in Python?",
      "question_marks": 10.00,
      "answer_text": "B",
      "score": 10.00,
      "feedback": "Correct answer!"
    },
    {
      "id": 2,
      "question_text": "Which keyword is used to define a function in Python?",
      "question_marks": 10.00,
      "answer_text": "C",
      "score": 10.00,
      "feedback": "Correct answer!"
    },
    {
      "id": 5,
      "question_text": "Explain what a Python dictionary is and provide one use case.",
      "question_marks": 20.00,
      "answer_text": "A Python dictionary is a mutable, unordered collection of key-value pairs. Each key must be unique and immutable. Dictionaries are commonly used for storing related data, such as user profiles.",
      "score": 18.50,
      "feedback": "Excellent explanation. Keyword coverage: 83%. Content similarity: 92%."
    }
  ]
}
```

**Security Note:** Students can only view their own submissions. Attempting to access another student's submission will return a 403 Forbidden error.

**Testing in Swagger:**
1. Ensure you're authorized
2. Find `GET /api/v1/assessments/submissions/{id}/`
3. Click "Try it out"
4. Enter your submission ID
5. Click "Execute"

---

## Common Errors

### 400 Bad Request
Indicates invalid data in your request. The response will specify which field has an issue.

Example:
```json
{
  "password": ["This field is required."]
}
```

### 401 Unauthorized
Your authentication token is missing or invalid. Make sure the Authorization header is properly formatted.

### 403 Forbidden
You're authenticated but don't have permission to access this resource. Common when trying to view another student's submission.

### 404 Not Found
The requested resource doesn't exist. Check that the ID in your URL is correct.

---

## Testing the Complete Flow

Here's a typical workflow to test the entire system:

1. **Register a new user** (`POST /api/v1/auth/register/`)
2. Copy the token and authorize in Swagger
3. **Browse available exams** (`GET /api/v1/assessments/exams/`)
4. **Get exam details** (`GET /api/v1/assessments/exams/1/`)
5. Note all question IDs and prepare your answers
6. **Submit your answers** (`POST /api/v1/assessments/submissions/`)
7. **View your submission** (`GET /api/v1/assessments/submissions/1/`)
8. **Logout** when finished (`POST /api/v1/auth/logout/`)

---

## Performance Notes

The API implements several optimizations:

- Database queries use `select_related()` and `prefetch_related()` to minimize database hits
- List endpoints are paginated to prevent overwhelming responses
- Indexes are placed on frequently queried fields
- Grading happens synchronously but completes in under a second for typical submissions

---

## Security Features

- Token-based authentication ensures secure access
- Students can only view and modify their own data
- Correct answers for MCQ questions are never exposed through the API
- All inputs are validated before processing
- Django's built-in protections guard against common vulnerabilities (SQL injection, XSS, CSRF)

---

**Documentation Last Updated:** January 2, 2026