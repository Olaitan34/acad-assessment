from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from assessments.models import Exam, Question, Submission, Answer
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample exam data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing data before seeding',
        )

    def create_python_basics_exam(self):
        """Create Python Basics exam with MCQ, SHORT, and ESSAY questions"""
        exam, created = Exam.objects.get_or_create(
            title='Python Basics',
            defaults={
                'course': 'Computer Science 101',
                'duration': 60,
                'description': 'Fundamental Python programming concepts including variables, data types, control structures, and OOP',
                'total_marks': 100.00,
                'passing_marks': 40.00,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam.title}'))

            # MCQ Question 1
            Question.objects.create(
                exam=exam,
                question_text='Which of the following is a valid Python data type?',
                question_type='MCQ',
                marks=5.00,
                order=1,
                option_a='Integer',
                option_b='Float',
                option_c='String',
                option_d='All of the above',
                correct_option='D'
            )

            # MCQ Question 2
            Question.objects.create(
                exam=exam,
                question_text='Which operator is used for exponentiation in Python?',
                question_type='MCQ',
                marks=5.00,
                order=2,
                option_a='^',
                option_b='**',
                option_c='exp()',
                option_d='pow',
                correct_option='B'
            )

            # MCQ Question 3
            Question.objects.create(
                exam=exam,
                question_text='Which loop is used to iterate over a sequence in Python?',
                question_type='MCQ',
                marks=5.00,
                order=3,
                option_a='while loop',
                option_b='for loop',
                option_c='do-while loop',
                option_d='foreach loop',
                correct_option='B'
            )

            # MCQ Question 4
            Question.objects.create(
                exam=exam,
                question_text='What is the correct syntax to create a function in Python?',
                question_type='MCQ',
                marks=5.00,
                order=4,
                option_a='function myFunction():',
                option_b='def myFunction():',
                option_c='create myFunction():',
                option_d='func myFunction():',
                correct_option='B'
            )

            # SHORT Question 1
            Question.objects.create(
                exam=exam,
                question_text='What is a variable in Python?',
                question_type='SHORT',
                marks=10.00,
                order=5,
                expected_keywords='container,storage,value,memory,name,assign,reference',
                models_answer='A variable is a named container for storing data values in memory. In Python, you create a variable by assigning a value to a name using the assignment operator (=). Variables can store different types of data and their values can be changed during program execution.'
            )

            # SHORT Question 2
            Question.objects.create(
                exam=exam,
                question_text='Explain the difference between a list and a tuple in Python.',
                question_type='SHORT',
                marks=15.00,
                order=6,
                expected_keywords='mutable,immutable,modify,change,brackets,parentheses,ordered,collection',
                models_answer='Lists and tuples are both ordered collections in Python. The main difference is that lists are mutable (can be modified after creation) and use square brackets [], while tuples are immutable (cannot be modified) and use parentheses (). Lists are better for collections that need to change, while tuples are better for fixed collections and are more memory efficient.'
            )

            # ESSAY Question
            Question.objects.create(
                exam=exam,
                question_text='Explain Object-Oriented Programming (OOP) in Python. Discuss the four main principles of OOP and provide examples of how they are implemented in Python.',
                question_type='ESSAY',
                marks=25.00,
                order=7,
                expected_keywords='encapsulation,inheritance,polymorphism,abstraction,class,object,method,attribute,instance,self,reusability,modularity',
                models_answer='Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects that contain data and code. The four main principles are: 1) Encapsulation - bundling data and methods within a class and controlling access using public/private attributes. 2) Inheritance - creating new classes from existing ones, allowing code reuse (e.g., class Dog(Animal)). 3) Polymorphism - using a single interface for different data types (method overriding). 4) Abstraction - hiding complex implementation details and showing only essential features. In Python, OOP is implemented using classes (defined with class keyword), objects (instances of classes), and methods (functions within classes). These principles promote code reusability, modularity, and maintainability.'
            )

            # MCQ Question 5
            Question.objects.create(
                exam=exam,
                question_text='Which keyword is used to create a class in Python?',
                question_type='MCQ',
                marks=5.00,
                order=8,
                option_a='class',
                option_b='Class',
                option_c='define',
                option_d='object',
                correct_option='A'
            )

            # SHORT Question 3
            Question.objects.create(
                exam=exam,
                question_text='What is the difference between "==" and "is" in Python?',
                question_type='SHORT',
                marks=10.00,
                order=9,
                expected_keywords='equality,identity,value,object,memory,address,compare,same',
                models_answer='The "==" operator checks if two values are equal (value equality), while "is" checks if two variables point to the same object in memory (identity equality). For example, two lists with the same content will be equal (==) but not identical (is) unless they reference the same object.'
            )

            # SHORT Question 4
            Question.objects.create(
                exam=exam,
                question_text='Explain exception handling in Python using try-except blocks.',
                question_type='SHORT',
                marks=15.00,
                order=10,
                expected_keywords='try,except,error,exception,handle,catch,finally,raise,block',
                models_answer='Exception handling in Python uses try-except blocks to catch and handle errors gracefully. Code that might raise an exception is placed in the try block, and error handling code is placed in the except block. You can catch specific exceptions or use a general except clause. The finally block executes regardless of whether an exception occurred. This prevents program crashes and allows for proper error management.'
            )

            self.stdout.write(self.style.SUCCESS(f'Created {exam.questions.count()} questions for {exam.title}'))
        
        return exam

    def handle(self, *args, **kwargs):
        clear_data = kwargs.get('clear')

        if clear_data:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Answer.objects.all().delete()
            Submission.objects.all().delete()
            Question.objects.all().delete()
            Exam.objects.all().delete()
            User.objects.filter(username__in=['student1', 'student2', 'student3']).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared!'))

        self.stdout.write('Seeding database...')

        # Create three test student users
        students = []
        for i in range(1, 4):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@example.com',
                    'first_name': ['Alice', 'Bob', 'Charlie'][i-1],
                    'last_name': ['Johnson', 'Smith', 'Williams'][i-1]
                }
            )
            if created:
                student.set_password('testpass123')
                student.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {student.username}'))
            students.append(student)

        # Create exams using dedicated methods
        self.create_python_basics_exam()

        # Create Data Structures exam
        exam2, created = Exam.objects.get_or_create(
            title='Data Structures',
            defaults={
                'course': 'Computer Science 201',
                'duration': 90,
                'description': 'Understanding fundamental data structures including arrays, linked lists, stacks, queues, trees, and hash tables',
                'total_marks': 100.00,
                'passing_marks': 60.00,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam2.title}'))

            # Add 10 questions to Data Structures exam
            Question.objects.create(
                exam=exam2,
                question_text='What is the time complexity of searching in a hash table?',
                question_type='MCQ',
                marks=5.00,
                order=1,
                option_a='O(1) average case',
                option_b='O(n)',
                option_c='O(log n)',
                option_d='O(n^2)',
                correct_option='A'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Explain the difference between a stack and a queue.',
                question_type='ESSAY',
                marks=20.00,
                order=2,
                expected_keywords='LIFO,FIFO,Last In First Out,First In First Out,push,pop,enqueue,dequeue,order',
                models_answer='A stack is a Last In First Out (LIFO) data structure where elements are added and removed from the same end (top). Operations are push (add) and pop (remove). A queue is a First In First Out (FIFO) data structure where elements are added at the rear and removed from the front. Operations are enqueue (add) and dequeue (remove).'
            )

            Question.objects.create(
                exam=exam2,
                question_text='What is a binary search tree?',
                question_type='SHORT',
                marks=10.00,
                order=3,
                expected_keywords='tree,node,left,right,smaller,greater,sorted,ordered,property',
                models_answer='A binary search tree is a tree data structure where each node has at most two children. For each node, all values in the left subtree are smaller, and all values in the right subtree are greater. This property makes searching efficient.'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Which sorting algorithm has the best average-case time complexity?',
                question_type='MCQ',
                marks=5.00,
                order=4,
                option_a='Bubble Sort - O(n^2)',
                option_b='Selection Sort - O(n^2)',
                option_c='Merge Sort - O(n log n)',
                option_d='Insertion Sort - O(n^2)',
                correct_option='C'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Describe how a linked list works and its advantages over arrays.',
                question_type='ESSAY',
                marks=20.00,
                order=5,
                expected_keywords='node,pointer,reference,dynamic,insertion,deletion,memory,efficient,size',
                models_answer='A linked list is a data structure consisting of nodes where each node contains data and a reference (pointer) to the next node. Unlike arrays, linked lists use dynamic memory allocation and can grow or shrink easily. Advantages include efficient insertion and deletion at any position, no need to specify size beforehand, and efficient memory usage for sparse data. However, random access is slower than arrays.'
            )

            Question.objects.create(
                exam=exam2,
                question_text='What data structure uses LIFO principle?',
                question_type='MCQ',
                marks=5.00,
                order=6,
                option_a='Queue',
                option_b='Stack',
                option_c='Tree',
                option_d='Graph',
                correct_option='B'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Explain the concept of recursion and provide an example.',
                question_type='SHORT',
                marks=10.00,
                order=7,
                expected_keywords='function,calls,itself,base,case,recursive,termination,stack',
                models_answer='Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller subproblems. Every recursive function must have a base case to terminate recursion. Example: factorial(n) = n * factorial(n-1) with base case factorial(0) = 1.'
            )

            Question.objects.create(
                exam=exam2,
                question_text='What is the worst-case time complexity of Quick Sort?',
                question_type='MCQ',
                marks=5.00,
                order=8,
                option_a='O(n)',
                option_b='O(n log n)',
                option_c='O(n^2)',
                option_d='O(log n)',
                correct_option='C'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Describe the concept of a hash function and collision handling.',
                question_type='SHORT',
                marks=10.00,
                order=9,
                expected_keywords='hash,function,key,index,collision,chaining,probing,bucket,mapping',
                models_answer='A hash function maps keys to array indices to enable fast data retrieval in hash tables. Collisions occur when two keys hash to the same index. Common collision handling methods include chaining (storing multiple values at the same index using linked lists) and open addressing (finding alternative slots through linear or quadratic probing).'
            )

            Question.objects.create(
                exam=exam2,
                question_text='Explain the difference between depth-first search (DFS) and breadth-first search (BFS).',
                question_type='SHORT',
                marks=10.00,
                order=10,
                expected_keywords='graph,tree,traversal,stack,queue,explore,visit,level,depth,order',
                models_answer='DFS explores a graph by going as deep as possible along each branch before backtracking, using a stack (or recursion). BFS explores level by level, visiting all neighbors before moving deeper, using a queue. DFS uses less memory but may not find the shortest path, while BFS guarantees the shortest path in unweighted graphs but uses more memory.'
            )

            self.stdout.write(self.style.SUCCESS(f'Created {exam2.questions.count()} questions for {exam2.title}'))

        exam3, created = Exam.objects.get_or_create(
            title='Web Development',
            defaults={
                'course': 'Web Technologies 101',
                'duration': 75,
                'description': 'HTML, CSS, JavaScript fundamentals and modern web development principles',
                'total_marks': 100.00,
                'passing_marks': 50.00,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam3.title}'))

            # Add 10 questions to Web Development exam
            Question.objects.create(
                exam=exam3,
                question_text='What does HTML stand for?',
                question_type='MCQ',
                marks=5.00,
                order=1,
                option_a='Hyper Text Markup Language',
                option_b='High Tech Modern Language',
                option_c='Home Tool Markup Language',
                option_d='Hyperlinks and Text Markup Language',
                correct_option='A'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Explain the CSS box model.',
                question_type='ESSAY',
                marks=20.00,
                order=2,
                expected_keywords='content,padding,border,margin,width,height,spacing,layout,element',
                models_answer='The CSS box model describes how elements are structured and spaced on a web page. It consists of four parts: content (the actual content), padding (space between content and border), border (surrounds the padding), and margin (space outside the border). The total element size includes all these components.'
            )

            Question.objects.create(
                exam=exam3,
                question_text='What is the purpose of JavaScript in web development?',
                question_type='SHORT',
                marks=10.00,
                order=3,
                expected_keywords='interactive,dynamic,behavior,client-side,programming,manipulation,events',
                models_answer='JavaScript adds interactivity and dynamic behavior to web pages. It runs on the client-side (in the browser) and allows manipulation of HTML/CSS, handling user events, making API calls, and creating interactive features.'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Which CSS property is used to change text color?',
                question_type='MCQ',
                marks=5.00,
                order=4,
                option_a='text-color',
                option_b='color',
                option_c='font-color',
                option_d='text-style',
                correct_option='B'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Explain the difference between inline, internal, and external CSS.',
                question_type='ESSAY',
                marks=20.00,
                order=5,
                expected_keywords='style,attribute,tag,head,file,link,separate,maintenance,reusable',
                models_answer='Inline CSS uses the style attribute directly in HTML elements. Internal CSS is defined in the <style> tag within the <head> section. External CSS is defined in a separate .css file and linked using the <link> tag. External CSS is preferred for larger projects as it promotes reusability and easier maintenance.'
            )

            Question.objects.create(
                exam=exam3,
                question_text='What does DOM stand for in web development?',
                question_type='MCQ',
                marks=5.00,
                order=6,
                option_a='Data Object Model',
                option_b='Document Object Model',
                option_c='Display Object Management',
                option_d='Digital Optimization Method',
                correct_option='B'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Explain what responsive web design is and why it is important.',
                question_type='SHORT',
                marks=10.00,
                order=7,
                expected_keywords='mobile,device,screen,size,flexible,adapt,media,query,layout',
                models_answer='Responsive web design is an approach that makes web pages render well on different devices and screen sizes. It uses flexible layouts, media queries, and fluid grids to adapt content. It is important because users access websites from various devices (phones, tablets, desktops), and responsive design ensures a good user experience across all platforms.'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Which HTML tag is used to create a hyperlink?',
                question_type='MCQ',
                marks=5.00,
                order=8,
                option_a='<link>',
                option_b='<a>',
                option_c='<href>',
                option_d='<url>',
                correct_option='B'
            )

            Question.objects.create(
                exam=exam3,
                question_text='What is the difference between var, let, and const in JavaScript?',
                question_type='SHORT',
                marks=15.00,
                order=9,
                expected_keywords='scope,variable,declaration,block,function,reassign,constant,hoisting',
                models_answer='var has function scope and is hoisted. let has block scope and can be reassigned but not redeclared in the same scope. const also has block scope but cannot be reassigned after initialization (though object properties can be modified). let and const are preferred in modern JavaScript for better scope control.'
            )

            Question.objects.create(
                exam=exam3,
                question_text='Explain the concept of semantic HTML and provide examples.',
                question_type='SHORT',
                marks=10.00,
                order=10,
                expected_keywords='meaning,structure,tag,header,footer,nav,article,section,accessibility,SEO',
                models_answer='Semantic HTML uses tags that clearly describe their meaning and content purpose. Examples include <header>, <nav>, <main>, <article>, <section>, <footer>. Benefits include better accessibility for screen readers, improved SEO, and more maintainable code. Semantic tags make the document structure clear to both developers and machines.'
            )

            self.stdout.write(self.style.SUCCESS(f'Created {exam3.questions.count()} questions for {exam3.title}'))

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Total Exams: {Exam.objects.count()}')
        self.stdout.write(f'Total Questions: {Question.objects.count()}')
        self.stdout.write(f'Total Users: {User.objects.count()}')
        self.stdout.write('\n' + self.style.WARNING('Test Student Credentials:'))
        self.stdout.write('  Username: student1, Password: testpass123')
        self.stdout.write('  Username: student2, Password: testpass123')
        self.stdout.write('  Username: student3, Password: testpass123')
        self.stdout.write('\n' + self.style.WARNING('Usage:'))
        self.stdout.write('  python manage.py seed_data          # Add data without clearing')
        self.stdout.write('  python manage.py seed_data --clear  # Clear existing data first')
