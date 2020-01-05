import os
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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    def test_get__all_questions(self):
        """
        verify that the total questions from query equals the ones from the requests
        verify that the result is a list of items from the query
        """
        numberOfQuestions = Question.query.count()
        response = self.client().get("/questions")
        input = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(input["questions"], list))
        self.assertEqual(input["totalQuestions"], numberOfQuestions)

    def test_search_question_impossible_substring(self):
        """
        tries to find a string that does not exist. should not return any questions
        """
        response = self.client().post(
            "/questions/search",
            json={"search_term": "DCcdciwnw&xxs"})



        input= json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(input["message"], 'has not found any item from query')
        self.assertFalse(input["success"])

    def test_search_question_possible_substring(self):
        """
        tries to find a string that does  exist. should not return any questions
        """
        response = self.client().post("/questions/search",json={'search_term': 'What'})

        input= json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(input["success"],True)

    def test_new_quiz(self):
        """
        tries to start a new quiz round
        """
        newQuiz = {'previous_questions': [],
                          'quiz_category': {'type': 'History', 'id': 4}}

        response = self.client().post('/quizzes', json=newQuiz)
        input = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(input['success'], True)

    def test_get_question_impossible_category(self):
        """
        tries to get a question in an impossible category
        should return false and code 404
        """
        response = self.client().get("categories/99/questions")
        input= json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertFalse(input["success"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
