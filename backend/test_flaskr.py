import os
from tabnanny import check
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:postgres@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    #  TESTS FOR QUESTIONS

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_404_invalid_page_numbers(self):
        test = self.client().get('/questions?page=111111')
        data = json.loads(test.data)
        
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        #post question to be deleted
        question = {
            'question': 'The sun rises from?',
            'answer': 'The east',
            'category': '4',
            'difficulty': 4
        }

        test = self.client().post('/questions', json=question)
        data = json.loads(test.data)
        question_id = data[0]['question_id']

        test = self.client().delete(f'/questions/{question_id}')
        data = json.loads(test.data)
        self.assertTrue(data[0]['success'])
        self.assertEqual(test.status_code, 200)
        


    def test_error_404_delete_question(self):
        test = self.client().delete(f'/questions/{4567}')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Requested resource can not be found')

#GENERAL TESTS
    def test_get_questions_by_category(self):
        test = self.client().get('/categories/6/questions')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 200)
        self.assertTrue(len(data[0]['questions']) > 0)
        self.assertTrue(data[0]['total_questions'] > 0)

    def test_error_400_get_questions_by_category(self):
        test = self.client().get('/categories/134/questions')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_create_question(self):
        question = {
            'question': 'The sun rises from??',
            'answer': 'The east',
            'category': '4',
            'difficulty': 4
        }

        test = self.client().post('/questions', json=question)
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertTrue(data[0]['success'])

    

    def test_search_question(self):
        test = self.client().get('/questions', json={"searchTerm": "how"})
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)


    def test_search_question_error(self):
        test = self.client().post('/questions')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')



    #TEST FOR CATEGORIES
    def test_get_categories(self):
        test = self.client().get('/categories')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_error_405_get_all_categories(self):
       #wrong method(patch)
        test = self.client().patch('/categories')
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not allowed for requested url")
        self.assertEqual(data['success'], False)

    

   
    #TEST FOR QUIZES  
    def test_play_quiz(self):
        quiz = {
            'previous_questions':[1,2,3],
            'quiz_category': {
                'id': 4,
                'type': 'History'
            }
        }

        test = self.client().post('/quizzes', json=quiz)
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 3)

        self.assertEqual(data['question']['category'], 4)

    def test_error_400_play_quiz(self):      
        test = self.client().post('/quizzes')
        data = json.loads(test.data)

        self.assertEqual(test.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()