# API Development and Documentation Final Project

# Brief Description
  The udacity trivia app is a web application to manage team trivia games.

 This application:
- Display questions - both all questions and by category.
- Allows users Delete Questions 
- Allows users to add questions and require that they include question and answer text.
- Allows users Search for questions based on a text query string.
- Allows users Play the quiz game, randomizing either all questions or within a specific category.

# API Endpoints
The available endpoints are:

1. Question
   - GET /questions
   - DELETE /questions
   - POST /questions
2. Question by Category
   - GET /categories/<category_id>/questions
3. Category
   - GET /categories
4. Quiz
   - POST /quizzes

# 1. GET /questions
Fetches a list of paginated questions (each page has 10 questions) with their ids, a list of all categories, the total number of questions, and a success indicator for the request.


REQUEST ARGUMENT: `page`(optional)

REQUEST HEADER: None

EXAMPLE REQUEST (using `curl` command in terminal):

```
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```

RETURNS:

Return a dictionary with:
- categories(List)
- current_category(List)
- questions(List of dictionaries)
  - id(int)
  - answer(string)
  - category(int)
  - difficulty(int)
  - question(string)
- total_questions(int)

EXAMPLE RESPONSE:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    "History"
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {...},
  ], 
  "total_questions": 22
}
```
