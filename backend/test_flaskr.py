# import os
# from turtle import reset
import unittest
import json
# from flask import current_app
# from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
# from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config.from_object('config.TestingConfig')

        self.new_question = {
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings?",
            "answer": "Maya Angelou",
            "difficulty": 2,
            "category": 4
        }

        self.quiz_category = {
            'type': 'History',
            'id': 4
        }

    def tearDown(self):
        """Executed after reach test"""

        pass

    def test_get_categories(self):
        """ Test retrieve categories"""
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404, msg='{0}'.format(res.data))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_question(self):
        """ Test add new question"""
        res = self.client().post("/add", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    #  USE APPROPRIATE ID IN res = self.client().delete("/questions/<id>") AND UNCOMMENT

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/40")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200, msg='{0}'.format(res))
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["deleted"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertTrue(data["total_questions"])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().delete("/add", json=self.new_question)
        # data = json.loads(res.data)

        self.assertEqual(res.status_code, 405,  msg='{0}'.format(res.data))
        # self.assertEqual(data["success"], False)
        # self.assertEqual(data["message"], "method not allowed")

    def test_search_for_qeustion_with_term(self):
        """ Test get questions with where search term matches"""
        res = self.client().post("/questions", json={'searchTerm': 'Whose'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_by_category_not_found(self):
        res = self.client().get("/categories/400/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_play_question(self):
        res = self.client().post("/quizzes",
                                 json={
                                     'previous_questions': [13, 26],
                                     'quiz_category': self.quiz_category
                                 }
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["currentQuestion"])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
