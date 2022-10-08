
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
# from flask import current_app
from models import Question, Category
# from flaskr import app
from flask import Blueprint
import random

main = Blueprint('main', __name__)

# app = current_app
QUESTIONS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


CORS(main, origins=["*"])


@main.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@main.route("/categories")
def get_all_categories():
    cats = Category.query.order_by(Category.id).all()
    formatted_categories = [cat.format() for cat in cats]
    if len(cats) == 0:
        abort(500)
    return jsonify({
        "success": True,
        "categories": formatted_categories
    })


@main.route("/questions")
def get_questions():
    sltcn = Question.query.order_by(Question.id).all()
    current_slctn = paginate_results(request, sltcn)
    cats= Category.query.all()
    
    formatted_cats = [cat.format() for cat in cats]

    if len(current_slctn) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": current_slctn,
            "total_questions": len(Question.query.all()),
            "current_category":'all',
            "categories": formatted_cats
        }
    )


"""
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
"""


@main.route("/questions/<int:question_id>")
def get_question(question_id):

    question = Question.query.get(question_id)

    formatted_question = question.format()

    return jsonify({
        'success': True,
        'question': formatted_question
    })


"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""


@main.route("/question/<int:qid>", methods=['DELETE'])
def delete_question(qid):
    question = Question.query.filter(Question.id == qid).one_or_none()
    if question is None:
        abort(404)

    question.delete()
    slctn = Question.query.order_by(Question.id).all()
    curr_questions = paginate_results(request, slctn)

    return jsonify({
        'success': True,
        'deleted': qid,
        'questions': curr_questions,
        'total_questions': len(slctn)
    })


@main.route("/add/questions", methods=['POST'])
def create_question():
    try:
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        question = Question(
            question=new_question,
            answer=new_answer,
            category=new_category,
            difficulty=new_difficulty
        )

        question.insert()

        slctn = Question.query.order_by(Question.id).all()
        current_slctn = paginate_results(request, slctn)

        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_slctn,
            'total_questions': len(slctn)
        })
    except:
        abort(405)


"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""


@main.route("/questions", methods=['POST'])
def search_question():
    body = request.get_json()

    search_term = body.get('searchTerm', None)

    try:
        questions = Question.query.filter(
            Question.question.like(search_term + "%")).all()

        pagedQueryRes = paginate_results(request, questions)

        return jsonify({
            'success': True,
            'questions': pagedQueryRes,
            'totalQuestions': len(questions)
        })

    except:
        abort(405)


"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""


@main.route('/categories/<int:cat_id>/questions')
def get_questions_by_category(cat_id):

    try:
        cats = Category.query.filter(Category.id == cat_id).one_or_none()

        questions = Question.query.filter(Question.category == cat_id).all()

        curr_questions = paginate_results(request, questions)

        return jsonify({
            'success': True,
            'questions': curr_questions,
            'totalQuestions': len(questions),
            'currentCategory': cats.type
        })
    except:
        abort(404)


@main.route('/quizzes', methods=['POST'])
def play_quiz():
    body = request.get_json()

    previous_questions_ids = body.get('previous_questions', None)
    # print(f"previous Q's {previous_questions_ids}")
    quiz_category = body.get('quiz_category', None)
    # print(f"quiz_category:  {quiz_category['id']}")
    questions = Question.query.all()

    rand_index_num = random.randrange(len(questions))
    # print(f"rand_index_num:  {rand_index_num}")
    if quiz_category:
        questions = Question.query.filter(
            Question.category == quiz_category['id']).all()
    count = 0
    if len(previous_questions_ids) > 0:
        while questions[rand_index_num].id in previous_questions_ids :
            rand_index_num = random.randrange(len(questions))
            count += 1
            if count == len(questions):
                break
        else:
            current_question = questions[rand_index_num]
    else:
        current_question = questions[rand_index_num]
    # print(f"current_question:  {current_question}")
    return jsonify({
        'success': True,
        'currentQuestion': current_question.format(),

    })


@main.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                "message": "resource not found"}),
        404,
    )


@main.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405,
                "message": "method not allowed"}),
        405,
    )


@main.errorhandler(422)
def unproccessable_entity(error):
    return (
        jsonify({"success": False, "error": 422,
                "message": "unproccessable entity"}),
        422,
    )


"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""

"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""

"""
@TODO:
Create error handlers for all expected errors
including 404 and 422.
"""
