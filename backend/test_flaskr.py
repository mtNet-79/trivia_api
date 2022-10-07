import os
from turtle import reset
import unittest
import json
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
# from flaskr import app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client      
        self.app.config.from_object('config.TestingConfig')
        # setup_db(self.app)
        # db.app = self.app
        # db.init_app(app)
        # db.create_all()
        # database_path = 'postgres://{}:{}@{}/{}'.format('postgres', 'AudrinaB12', 'localhost:5432', 'trivia_test')
        
        self.new_question = {
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings?",
            "answer": "Maya Angelou",
            "difficulty": 2,
            "category": 4
        }
        
        
        
        
        
        # binds the app to the current context
        # with self.app.app_context():
        # #     print(current_app.config)
        # #     from flaskr import routes
            
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
       
        pass

    def test_get_categories(self):
        # ctx = self.app.app_context()
        # ctx.push()
        """ Test retrieve categories"""
        res = self.client().get("/categories")        
        data = json.loads(res.data)       

        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['categories']))
        # ctx = self.app.app_context()
        # ctx.pop()
        
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404, msg='{0}'.format(res.data))
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_create_question(self):
        res = self.client().post("/add/questions", json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
    
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/question/9999", json=self.new_question)
        # data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405,  msg='{0}'.format(res.data))
        # self.assertEqual(data["success"], False)
        # self.assertEqaul(data["message"], "method not allowed")
        
    def test_search_for_qeustion_with_term(self):
        res = self.client().post("/questions", json={ 'searchTerm': 'Whose'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200,  msg='{0}'.format(res.data))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        
        
        
        
        
        
   

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()