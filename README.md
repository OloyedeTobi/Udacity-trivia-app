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
