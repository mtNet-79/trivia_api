# import os
# from turtle import reset
import unittest
import json
# from flask import current_app
# from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import db, Question
from sqlalchemy import func



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
        
        question = Question(
                question="In what US state is the oldest living tree located?",
                answer="California",
                category_id=4,
                difficulty=2
            )

        question.insert()
        
        self.del_id =  Question.query.all()[0].id

        self.quiz_category = {
            'type': 'History',
            'id': 4
        }

    def tearDown(self):
        """Executed after reach test"""
        # for table in reversed(meta.sorted_tables):
        # db.session.execute(f"TRUNCATE questions RESTART identity;")
        pass

    def test_get_categories(self):
        """ Test retrieve categories"""
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        """ test get pagination failures """
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

    def test_405_create_question_failure(self):
        """ Test add new question failure"""
        res = self.client().post("/add")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405, msg='{0}'.format(res.data))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    

    def test_delete_question(self):
        """ Test delete question failure"""
        res = self.client().delete("/questions/111")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404, msg='{0}'.format(res))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_for_qeustion_with_term(self):
        """ Test get questions with where search term matches"""
        res = self.client().post("/questions", json={'searchTerm': 'Whose'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_bad_request_search_for_qeustion_with_term(self):
        """ Test get questions with where search term failure"""
        res = self.client().post("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    def test_get_questions_by_category(self):
        """ Test get questions by category"""
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_by_category_not_found(self):
        """ Test get questions by category failure """
        res = self.client().get("/categories/4000/questions")
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
        
    def test_delete_question(self):
        """ Test delete question """
        res = self.client().delete("/questions/"+str(self.del_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, msg='{0}'.format(res))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
