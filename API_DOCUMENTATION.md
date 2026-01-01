# Mini Assessment Engine API - Let's Get Started! 🚀

## Base URL
```
http://localhost:8000
```

## What This API Does

So basically, this is a complete assessment platform API that handles everything - from user authentication to taking exams and getting automatic grading. Think of it as your backend for any online test or CBT system.

### Where Everything Lives
```
/api/v1/auth/          - All authentication stuff (login, register, logout)
/api/v1/assessments/   - Exam and submission endpoints
/api/docs/             - Swagger UI (test your APIs here, very handy!)
/api/redoc/            - ReDoc Documentation (cleaner version)
```

---

## 🔐 How Authentication Works

This API uses Token Authentication. It's simple - when you register or login, you get a token. Just add that token to your request headers and you're good to go!

### How to Send Your Token
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Important:** Don't put those angle brackets like `<your_token_here>` - just write `Token` followed by a space and your actual token value.

---

## 📋 All the Endpoints Explained

### 1. **Creating a New Account (Registration)**

**Endpoint:** `POST /api/v1/auth/register/`

**Do I need to be logged in?** No, anyone can register.

**What to send:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**What you'll get back if it works (201 Created):**
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

Copy that token! You'll need it for almost every other request.

**If something goes wrong (400 Bad Request):**
```json
{
  "password": ["Password fields didn't match."]
}
```

This happens when your `password` and `password2` don't match. Make sure they're exactly the same!

---

### 2. **Logging Into Your Account**

**Endpoint:** `POST /api/v1/auth/login/`

**Do I need to be logged in?** No (you're trying to login obviously 😅)

**What to send:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**What you'll get back (200 OK):**
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

Again, save that token somewhere safe (not on paper sha, in your app's storage or environment variables).

**If the credentials are wrong (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

Check your username and password again - make sure there's no typo.

---

### 3. **Checking Your Profile**

**Endpoint:** `GET /api/v1/auth/profile/`

**Do I need to be logged in?** Yes! Include your token in the header.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**What you'll get back (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

This is useful when you want to display the current user's info on your frontend.

---

### 4. **Logging Out**

**Endpoint:** `POST /api/v1/auth/logout/`

**Do I need to be logged in?** Yes, you need the token to logout.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**What you'll get back (200 OK):**
```json
{
  "message": "Logout successful"
}
```

After this, the token becomes invalid. Make sure you clear it from your app's storage too.

---

### 5. **Seeing All Available Exams**

**Endpoint:** `GET /api/v1/assessments/exams/`

**Do I need to be logged in?** Nope! This endpoint is open to everyone. Good for showing exams on your landing page.

**You can add these optional parameters:**
- `page` - Which page you want to see (starts from 1)
- `page_size` - How many exams per page (default is 10)

Example: `GET /api/v1/assessments/exams/?page=2&page_size=5`

**What you'll get back (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/assessments/exams/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "course": "Computer Science 101",
      "duration": 60,
      "total_marks": 100.00,
      "description": "Basic Python programming concepts",
      "question_count": 10,
      "created_at": "2026-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Data Structures Midterm",
      "course": "Computer Science 201",
      "duration": 90,
      "total_marks": 100.00,
      "description": "Arrays, Linked Lists, Trees",
      "question_count": 10,
      "created_at": "2026-01-01T11:00:00Z"
    }
  ]
}
```

**Pro tip:** The `question_count` tells you how many questions the exam has, and `duration` is in minutes. Use this info to show students what they're getting into before they start!

---

### 6. **Getting Full Details of a Specific Exam**

**Endpoint:** `GET /api/v1/assessments/exams/{exam_id}/`

**Do I need to be logged in?** No - but you'll need to login to submit answers later.

**Example:** `GET /api/v1/assessments/exams/1/`

**What you'll get back (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "course": "Computer Science 101",
  "duration": 60,
  "description": "Basic Python programming concepts",
  "total_marks": 100.00,
  "passing_marks": 40.00,
  "questions": [
    {
      "id": 1,
      "question_text": "What is a variable in Python?",
      "question_type": "SHORT",
      "marks": 10.00,
      "order": 1,
      "option_a": "",
      "option_b": "",
      "option_c": "",
      "option_d": ""
    },
    {
      "id": 2,
      "question_text": "Which of the following is a valid Python data type?",
      "question_type": "MCQ",
      "marks": 5.00,
      "order": 2,
      "option_a": "Integer",
      "option_b": "Float",
      "option_c": "String",
      "option_d": "All of the above"
    }
  ],
  "created_at": "2026-01-01T10:00:00Z"
}
```

**Things to note:**
- For MCQ questions, the options are in `option_a`, `option_b`, `option_c`, and `option_d`
- For SHORT and ESSAY questions, those option fields will be empty
- `question_type` can be: **MCQ** (multiple choice), **SHORT** (short answer), or **ESSAY** (long answer)
- Each question has its own marks
- The `order` field tells you which question comes first, second, etc.

This is the endpoint you'll call when a student clicks "Start Exam" to show them all the questions.

---

### 7. **Submitting Your Exam Answers (The Main Event!)**

**Endpoint:** `POST /api/v1/assessments/submissions/`

**Do I need to be logged in?** YES! This is the most important one - make sure your token is in the header.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**What to send:**
```json
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer_text": "A variable is a container for storing data values in Python. It is created when you assign a value to it using the assignment operator (=)."
    },
    {
      "question_id": 2,
      "answer_text": "D"
    },
    {
      "question_id": 3,
      "answer_text": "The print() function is used to display output in Python. You can print strings, numbers, variables, and complex expressions."
    }
  ]
}
```

**VERY IMPORTANT RULES:**
1. ✅ You MUST answer ALL questions in the exam - if you skip even one, the API will reject your submission
2. ✅ For MCQ questions, just put the letter (A, B, C, or D) in `answer_text`
3. ✅ For SHORT and ESSAY questions, write your full answer in `answer_text`
4. ✅ You can only submit each exam ONCE - no retakes! So make sure you're ready before hitting submit
5. ✅ The grading happens automatically and immediately - no waiting around

**What you'll get back when it works (201 Created):**
```json
{
  "id": 1,
  "exam_title": "Introduction to Python",
  "student_name": "john_doe",
  "status": "GRADED",
  "score": 85.50,
  "feedback": "Good understanding of Python concepts. You explained variables well and showed clear knowledge of Python basics. Keep it up!",
  "started_at": "2026-01-01T14:00:00Z",
  "graded_at": "2026-01-01T14:05:00Z",
  "answers": [
    {
      "id": 1,
      "question_text": "What is a variable in Python?",
      "question_marks": 10.00,
      "answer_text": "A variable is a container for storing data values...",
      "score": 9.50,
      "feedback": "Excellent explanation with clear examples. You covered the key concepts well."
    },
    {
      "id": 2,
      "question_text": "Which of the following is a valid Python data type?",
      "question_marks": 5.00,
      "answer_text": "D",
      "score": 5.00,
      "feedback": "Correct answer."
    }
  ]
}
```

Notice how each answer has its own score and feedback? That's the automatic grading at work! The AI checks:
- MCQ answers against the correct option
- SHORT/ESSAY answers for expected keywords and quality

**If you already submitted this exam before (400 Bad Request):**
```json
{
  "error": "You have already submitted this exam"
}
```

Sorry, no second chances! Plan well before submitting.

**If you didn't answer all questions (400 Bad Request):**
```json
{
  "non_field_errors": ["All Questions must be answered"]
}
```

Go back and complete all the questions before trying again.

---

### 8. **Viewing All Your Submissions**

**Endpoint:** `GET /api/v1/assessments/submissions/`

**Do I need to be logged in?** Yes - and you'll only see YOUR OWN submissions (unless you're staff/admin).

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Optional parameters:**
- `page` - Page number (if you have many submissions)
- `status` - Filter by status: PENDING, GRADED, or FAILED

Example: `GET /api/v1/assessments/submissions/?status=GRADED`

**What you'll get back (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "exam_title": "Introduction to Python",
      "student_name": "john_doe",
      "status": "GRADED",
      "score": 85.50,
      "feedback": "Good understanding of concepts",
      "started_at": "2026-01-01T14:00:00Z",
      "graded_at": "2026-01-01T14:05:00Z",
      "answers": []
    },
    {
      "id": 2,
      "exam_title": "Data Structures Midterm",
      "student_name": "john_doe",
      "status": "PENDING",
      "score": null,
      "feedback": "",
      "started_at": "2026-01-01T15:00:00Z",
      "graded_at": null,
      "answers": []
    }
  ]
}
```

**Quick explanation of submission statuses:**
- **GRADED** - Your exam has been marked and you have your score
- **PENDING** - Still being processed (though honestly, grading is instant, so this is rare)
- **FAILED** - Your score was below the passing marks 😔

**Note:** The `answers` array is empty here to keep the response light. If you want to see the full details with all answers and feedback, use the next endpoint.

---

### 9. **Getting Full Details of One Submission**

**Endpoint:** `GET /api/v1/assessments/submissions/{submission_id}/`

**Do I need to be logged in?** Yes!

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Example:** `GET /api/v1/assessments/submissions/1/`

**What you'll get back (200 OK):**
```json
{
  "id": 1,
  "exam_title": "Introduction to Python",
  "student_name": "john_doe",
  "status": "GRADED",
  "score": 85.50,
  "feedback": "Good understanding of Python concepts. You explained variables well and demonstrated solid knowledge of basic concepts. Areas for improvement: Provide more examples in essay questions.",
  "started_at": "2026-01-01T14:00:00Z",
  "graded_at": "2026-01-01T14:05:00Z",
  "answers": [
    {
      "id": 1,
      "question_text": "What is a variable in Python?",
      "question_marks": 10.00,
      "answer_text": "A variable is a container for storing data values in Python. It's created when you assign a value using the = operator.",
      "score": 9.50,
      "feedback": "Excellent explanation with clear examples. You covered the key concepts well."
    },
    {
      "id": 2,
      "question_text": "Which of the following is a valid Python data type?",
      "question_marks": 5.00,
      "answer_text": "D",
      "score": 5.00,
      "feedback": "Correct answer."
    },
    {
      "id": 3,
      "question_text": "Explain what the print() function does in Python.",
      "question_marks": 10.00,
      "answer_text": "The print() function displays output to the console.",
      "score": 7.00,
      "feedback": "Good start, but could be more detailed. Try including examples of different use cases."
    }
  ]
}
```

This is the "results page" endpoint. It shows everything:
- Overall score and feedback
- Each question with what you answered
- How many marks you got per question
- Individual feedback for each answer

Perfect for displaying a detailed results page to students after they finish an exam.

---

## 🎯 Using Swagger UI (The Easy Way to Test)

Swagger UI is like a playground for your API. You can test all the endpoints without writing any code. Here's how to use it:

### Step 1: Open Swagger UI
Just go to: `http://localhost:8000/api/docs/`

You'll see a nice interface with all your endpoints listed.

### Step 2: Create Your Account
1. Look for the **authentication** section (it's green)
2. Click on `POST /api/v1/auth/register/`
3. Click the **"Try it out"** button on the right
4. Fill in your details in the request body:
```json
{
  "username": "testuser",
  "password": "TestPass123!",
  "password2": "TestPass123!",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```
5. Click **"Execute"**
6. Scroll down to see the response
7. **IMPORTANT:** Copy that token from the response! You'll need it next.

### Step 3: Login With Your Token
1. At the very top of the page, you'll see an **"Authorize"** button with a lock icon (🔒)
2. Click it
3. In the popup, type: `Token` (space) then paste your token
   - Example: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
   - Don't put angle brackets or anything fancy - just Token, space, and the actual token value
4. Click **"Authorize"**
5. Click **"Close"**

Now you're logged in! All your requests will include your token automatically.

### Step 4: Browse Available Exams
1. Scroll down to the **assessments** section (it's blue)
2. Click on `GET /api/v1/assessments/exams/`
3. Click **"Try it out"**
4. Click **"Execute"**
5. Check out the response - you'll see all available exams

If you're testing with fresh data, you might not see any exams. Run the seed command first:
```bash
python manage.py seed_data
```

### Step 5: Get Full Exam Details
1. Click on `GET /api/v1/assessments/exams/{id}/`
2. Click **"Try it out"**
3. Put an exam ID in the `id` field (like `1`)
4. Click **"Execute"**
5. You'll see all the questions for that exam

Take note of the question IDs - you'll need them when submitting answers!

### Step 6: Submit Your Answers
1. Click on `POST /api/v1/assessments/submissions/`
2. Click **"Try it out"**
3. Fill in your answers in the request body. Make sure you answer ALL questions!

Example (adjust the question_ids and exam_id to match yours):
```json
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer_text": "A variable is a named location in memory that stores a value. In Python, you create variables by simply assigning values to them."
    },
    {
      "question_id": 2,
      "answer_text": "D"
    },
    {
      "question_id": 3,
      "answer_text": "The print() function outputs data to the console. It can print strings, numbers, variables, and expressions."
    }
  ]
}
```
4. Click **"Execute"**
5. Boom! 💥 You'll see your graded results immediately

### Step 7: Check Your Submissions
1. Click on `GET /api/v1/assessments/submissions/`
2. Click **"Try it out"**
3. Click **"Execute"**
4. You'll see a list of all your submissions

Want the full details with feedback? Use the detail endpoint:
1. Click on `GET /api/v1/assessments/submissions/{id}/`
2. Put your submission ID
3. Execute
4. See your complete results with feedback for each answer

---

## 📮 Using Postman (For the API Testing Pros)

If you prefer Postman (and honestly, who doesn't for serious API testing?), here's how to set it up properly.

### Step 1: Create Your Collection

Open Postman and create a new collection called "Mini Assessment Engine" (or whatever name you like).

### Step 2: Setup Environment Variables

This is important - it'll save you from typing the same things over and over:

1. Create a new environment (let's call it "Local Development")
2. Add these variables:
   - `base_url` = `http://localhost:8000`
   - `token` = (leave this empty for now, we'll set it automatically)

### Step 3: Register a New User

Create a new request in your collection:

**Method:** POST  
**URL:** `{{base_url}}/api/v1/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (select raw → JSON):**
```json
{
  "username": "testuser",
  "password": "TestPass123!",
  "password2": "TestPass123!",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```

**Pro Tip:** Add this to the Tests tab to automatically save your token:
```javascript
if (pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.token);
    console.log("Token saved:", jsonData.token);
}
```

Click Send, and boom! Your token is automatically saved to the environment.

### Step 4: Login (Alternative to Registration)

If you already have an account, you can just login:

**Method:** POST  
**URL:** `{{base_url}}/api/v1/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

**Tests Script (same as before):**
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.token);
    console.log("Token saved:", jsonData.token);
}
```

### Step 5: Get Your Profile

Let's test that the token is working:

**Method:** GET  
**URL:** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Token {{token}}
```

If this works and shows your user info, you're golden! ✨

### Step 6: Browse All Exams

**Method:** GET  
**URL:** `{{base_url}}/api/v1/assessments/exams/`

**Headers (optional for this one):**
```
Authorization: Token {{token}}
```

You'll see all available exams. Note the IDs - you'll need them!

### Step 7: Get Specific Exam Details

**Method:** GET  
**URL:** `{{base_url}}/api/v1/assessments/exams/1/`

(Change the `1` to whatever exam ID you want to check)

**Headers:**
```
Authorization: Token {{token}}
```

This shows you all the questions. Copy the question IDs because you'll need them for submission.

### Step 8: Submit Your Answers

This is the big one! Make sure you have answers for ALL questions.

**Method:** POST  
**URL:** `{{base_url}}/api/v1/assessments/submissions/`

**Headers:**
```
Authorization: Token {{token}}
Content-Type: application/json
```

**Body:**
```json
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer_text": "A variable is a named storage location in memory that holds a value. In Python, variables are created when you assign a value to them using the assignment operator (=). For example: name = 'John' creates a variable called name that stores the string 'John'."
    },
    {
      "question_id": 2,
      "answer_text": "D"
    },
    {
      "question_id": 3,
      "answer_text": "The print() function in Python is used to output or display information to the console. It can handle various data types including strings, numbers, lists, and more."
    }
  ]
}
```

**Remember:**
- For MCQ questions, just put the letter (A, B, C, or D)
- For SHORT and ESSAY questions, write proper answers
- Answer ALL questions or it won't go through!

Hit Send and watch the magic happen - you'll get your graded results immediately! 🎉

### Step 9: View All Your Submissions

**Method:** GET  
**URL:** `{{base_url}}/api/v1/assessments/submissions/`

**Headers:**
```
Authorization: Token {{token}}
```

You can also filter by status:  
`{{base_url}}/api/v1/assessments/submissions/?status=GRADED`

### Step 10: Get Detailed Results for One Submission

**Method:** GET  
**URL:** `{{base_url}}/api/v1/assessments/submissions/1/`

(Replace `1` with your actual submission ID)

**Headers:**
```
Authorization: Token {{token}}
```

This shows you everything - your full answers, individual question scores, and feedback for each answer.

### Step 11: Logout

When you're done testing:

**Method:** POST  
**URL:** `{{base_url}}/api/v1/auth/logout/`

**Headers:**
```
Authorization: Token {{token}}
```

After this, your token becomes invalid. You can add a test script to clear it:
```javascript
pm.environment.unset("token");
console.log("Token cleared from environment");
```

---

## 🔒 Security Features (Don't Sleep On This!)

### 1. **Token Authentication**
The API uses token-based auth which is pretty secure. Here's how it works:
- When you register or login, you get a unique token
- This token identifies you for all future requests
- Always include it in the `Authorization` header like: `Token your_actual_token_here`
- The token is valid until you logout or it's deleted from the database

### 2. **Permission Controls**
We've got proper access control set up:
- **Students** can only see and submit their own exams - no snooping on other people's work!
- **Staff/Admin users** can see everyone's submissions (for grading purposes)
- Exams are public (anyone can view them), but only admins can create or modify exams
- You can't submit someone else's exam - the API checks that you're the authenticated user

### 3. **Input Validation**
Everything you send gets validated before processing:
- Passwords must match during registration
- Email must be in proper format
- All required fields must be present
- Data types are checked (numbers are numbers, strings are strings, etc.)
- The serializers handle all this automatically - you'll get clear error messages if something's wrong

### 4. **Data Privacy**
Your data is safe:
- Students can ONLY see their own submissions
- The API checks submission ownership before showing any data
- Django's built-in security features protect against SQL injection, XSS, CSRF, etc.
- Passwords are hashed and salted (never stored in plain text)

**Bottom line:** As long as you keep your token secret, your account is secure. Don't share it, don't commit it to GitHub, and definitely don't hardcode it in your frontend! Use environment variables.

---

## ⚠️ Common Errors and What They Mean

### 400 Bad Request
```json
{
  "field_name": ["Error message explaining what went wrong"]
}
```
**What this means:** You sent something wrong in your request - maybe a field is missing, or the data format is incorrect. Check the error message, it usually tells you exactly what's wrong.

**Example:**
```json
{
  "password": ["Password fields didn't match."]
}
```
Fix: Make sure `password` and `password2` are the same!

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**What this means:** You either forgot to include your token, or it's invalid/expired.

**How to fix:**
- Make sure you added the `Authorization` header
- Check that it's formatted correctly: `Token your_token_here`
- If you logged out, you need to login again to get a new token

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```
**What this means:** You're authenticated (logged in), but you don't have permission to do what you're trying to do.

**Common causes:**
- Trying to view another student's submission (not allowed!)
- Trying to create/edit exams without admin privileges
- Accessing a resource that doesn't belong to you

### 404 Not Found
```json
{
  "detail": "Not found."
}
```
**What this means:** The thing you're looking for doesn't exist.

**Common causes:**
- Wrong exam ID (exam might have been deleted or never existed)
- Wrong submission ID
- Typo in the URL

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```
**What this means:** Something broke on the server side (not your fault!).

**What to do:**
- Check the Django server console for the full error
- Make sure the database is running
- Check if all migrations are applied (`python manage.py migrate`)
- If it persists, check the code for bugs

---

## 📊 Database Schema (The Backend Structure)

Here's how everything is organized in the database:

### Exam Model
This stores all the exam information:
- `id` - Unique identifier for each exam
- `title` - Exam name (e.g., "Introduction to Python")
- `course` - Which course it belongs to
- `duration` - How long students have to complete it (in minutes)
- `description` - What the exam is about
- `total_marks` - Maximum possible score
- `passing_marks` - Minimum score to pass
- `is_active` - Whether students can take this exam or not
- `created_at` & `updated_at` - Timestamps

### Question Model
Each exam has multiple questions:
- `id` - Unique question identifier
- `exam` - Which exam this question belongs to (Foreign Key)
- `question_text` - The actual question
- `question_type` - Can be **MCQ** (multiple choice), **SHORT** (short answer), or **ESSAY** (long answer)
- `marks` - How many points this question is worth
- `order` - Question number (1st, 2nd, 3rd, etc.)
- `option_a`, `option_b`, `option_c`, `option_d` - The MCQ options (empty for SHORT/ESSAY)
- `correct_option` - The right answer for MCQ questions (A, B, C, or D)
- `expected_keywords` - Keywords the grader looks for in SHORT/ESSAY answers
- `model_answer` - Reference answer for comparison

### Submission Model
When a student submits an exam:
- `id` - Unique submission identifier
- `student` - Who submitted it (Foreign Key to User)
- `exam` - Which exam was submitted (Foreign Key to Exam)
- `status` - Can be **PENDING**, **GRADED**, or **FAILED**
- `score` - Total marks earned
- `feedback` - Overall feedback on the submission
- `started_at` - When they opened the exam
- `submitted_at` - When they hit submit
- `graded_at` - When the grading finished
- **Important:** One student can only submit each exam once (database constraint)

### Answer Model
Individual answers for each question in a submission:
- `id` - Unique answer identifier
- `submission` - Which submission this belongs to (Foreign Key)
- `question` - Which question this answers (Foreign Key)
- `answer_text` - What the student wrote
- `score` - Points earned for this specific answer
- `feedback` - Feedback specific to this answer
- **Important:** One answer per question per submission (database constraint)

---

## 🚀 Performance Tips

### Why This Matters
When you're building a real application, you don't want slow API calls. Nobody has time to wait! Here's how this API is optimized:

### Database Query Optimization
The API uses Django's `select_related()` and `prefetch_related()` to reduce database hits:

**For listing exams with question counts:**
```python
Exam.objects.filter(is_active=True).prefetch_related('questions')
```
This loads all exams and their questions in just 2 queries instead of N+1 queries!

**For getting submission details:**
```python
Submission.objects.select_related('exam', 'student').prefetch_related('answers__question')
```
Gets everything you need in a few optimized queries instead of dozens of separate ones.

### Pagination
All list endpoints return paginated results (10 items per page by default). This means:
- Faster response times
- Less data transferred
- Better user experience
- Your server doesn't die trying to send 1000 exams at once 😅

You can adjust the page size if needed:
```
GET /api/v1/assessments/exams/?page_size=20
```

### Other Performance Features
- Database indexes on frequently queried fields (like exam IDs, student IDs)
- Efficient serializers that only fetch needed data
- Proper use of Django's ORM to avoid redundant queries

**Bottom line:** The API is already optimized, but if you're building the frontend, implement pagination properly and don't try to load everything at once!

---

## 🧪 Testing the API

### First, Create Some Test Data

Before you start testing, you need some exams in the database. Good news - there's a management command for that!

```bash
python manage.py seed_data
```

This creates:
- 3 test students (student1, student2, student3 - all with password: `testpass123`)
- 3 complete exams:
  - **Python Basics** (10 questions, 100 marks total)
  - **Data Structures** (10 questions, 100 marks total)
  - **Web Development** (10 questions, 100 marks total)

Each exam has a mix of MCQ, SHORT, and ESSAY questions.

**To clear existing data and start fresh:**
```bash
python manage.py seed_data --clear
```

### Now Test the Full Flow

Here's a typical user journey you can test:

1. **Register** a new user account
2. **Login** to get your authentication token
3. **Browse** available exams (see what's out there)
4. **Get details** of a specific exam (view all questions)
5. **Submit answers** for all questions in the exam
6. **Check submission status** (see your score immediately!)
7. **View detailed results** with feedback for each answer
8. **Logout** when done

### Quick Test Using Swagger

The easiest way to test everything:
1. Go to `http://localhost:8000/api/docs/`
2. Follow the Swagger UI steps above (registration → authorization → browse → submit)
3. You'll see results in real-time!

### Test With Postman

If you prefer Postman:
1. Set up your collection as described in the Postman section
2. Run requests one by one
3. Use the Tests scripts to auto-save tokens
4. Check responses at each step

---

## 📝 Important Notes to Remember

### About Grading
- ✅ **Grading is 100% automatic** - no waiting for manual marking
- ✅ Happens **immediately** when you submit
- ✅ MCQ questions are graded by comparing with the correct option
- ✅ SHORT/ESSAY questions are graded based on keyword matching and answer quality
- ✅ Each answer gets individual feedback
- ✅ You also get overall feedback for the whole exam

### About Submissions
- ⚠️ **You MUST answer ALL questions** - can't skip any!
- ⚠️ **One submission per exam per student** - no retakes or do-overs
- ⚠️ Once submitted, you can't change your answers
- ⚠️ Make sure you're ready before hitting that submit button!

### About Authentication
- 🔑 Token is **required** for most endpoints (profile, submit, view submissions)
- 🔑 Tokens are **permanent** until you logout or delete them
- 🔑 Keep your token **secret** - treat it like a password
- 🔑 Public endpoints (list exams, exam details) don't need tokens

### About Pagination
- 📄 List endpoints return **10 items per page** by default
- 📄 Use `page` and `page_size` parameters to control this
- 📄 Check the `next` and `previous` fields in the response for navigation

### About Exam Format
- 📝 Each exam has **10 questions** (with our seed data)
- 📝 Total marks: **100** for each exam
- 📝 Question types: **MCQ**, **SHORT**, or **ESSAY**
- 📝 Each question has its own marks allocation

---

## 🆘 Need Help?

If you run into issues:

1. **Check the error message** - Most times it tells you exactly what's wrong
2. **Look at the Swagger UI docs** - It has examples for every endpoint (`/api/docs/`)
3. **Verify your token format** - Should be `Token your_actual_token` (no angle brackets!)
4. **Make sure all required fields are included** - Check the examples in this doc
5. **Check the Django server logs** - The console usually shows detailed errors
6. **Run migrations** if you're getting database errors:
   ```bash
   python manage.py migrate
   ```
7. **Seed data** if you don't have any exams:
   ```bash
   python manage.py seed_data
   ```

### Common "Gotchas" (Things That Trip People Up)

1. **Forgetting to answer all questions** - The API will reject incomplete submissions
2. **Wrong token format** - It's `Token abc123`, not `Bearer abc123` or `<Token abc123>`
3. **Trying to submit the same exam twice** - You only get one shot!
4. **Not including Content-Type header** - Should be `application/json` for POST requests
5. **Using wrong question/exam IDs** - Always check the IDs from the list/detail endpoints first

---

## 🎓 For Developers Integrating This API

If you're building a frontend for this:

### Recommended Flow
1. Create a login/registration page
2. Store the token securely (localStorage or secure cookies)
3. Create an exams list page (use the list endpoint)
4. Create an exam detail page that shows all questions
5. Build a form that collects answers for ALL questions
6. Submit everything at once (not one by one!)
7. Show the graded results immediately after submission
8. Build a "My Submissions" page to show history

### State Management Tips
- Store the user token and info in global state (Redux, Context, Zustand, etc.)
- Cache the exam list to reduce API calls
- Keep track of which questions have been answered before allowing submission
- Show validation errors clearly to users

### UX Recommendations
- Show a countdown timer based on the exam duration
- Prevent navigation away from the exam page without confirmation
- Disable the submit button until all questions are answered
- Show a loading spinner during submission (even though it's fast)
- Display results in a clear, organized way with color coding (green for correct, red for wrong, etc.)

---

**API Version:** v1  
**Last Updated:** January 1, 2026  
**Built With:** Django 6.0 + Django REST Framework 3.16.1  
**Made with ❤️ for Acad AI**

---

That's everything! You're now ready to build something amazing with this API. Good luck with your assessment engine! 🚀
